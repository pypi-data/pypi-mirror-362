import os
import shutil
from pathlib import Path

import pandas as pd 
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import pandas_udf
from pyspark import SparkFiles
from pyspark.sql.types import StringType
from pyspark.sql import functions as F


from abtranslate.translator.package import load_argostranslate_model
from abtranslate.utils.logger import logger


PACKAGES_PATH = "/tmp/abtranslate/packages/"
MODELS_PATH = "/tmp/abtranslate/model/"

def translate_column(translator_config=None, 
                     translation_config=None, 
                     optimized_config=True):
    task_id = os.getenv('SPARK_TASK_ATTEMPT_ID', str(os.getpid()))
    package_dir = Path(f"/tmp/abtranslate/packages_{task_id}")
    
    # Ensure package directory exists
    package_dir.mkdir(parents=True, exist_ok=True)
    
    package_path = SparkFiles.get("model.zip")

    if not os.path.exists(package_path):
        raise FileNotFoundError(f"Model path {package_path} doesn't exist")

    # Update the global PACKAGE_DIR constant BEFORE loading the package
    import abtranslate.config.constants
    abtranslate.config.constants.PACKAGE_DIR = package_dir
    
    # Load package ONCE outside UDF
    package = load_argostranslate_model(package_path)

    # Build translator once
    if translator_config:
        translator = package.load_translator(translator_config, optimized_config=optimized_config)
    else:
        translator = package.load_translator(optimized_config=optimized_config)

    @pandas_udf(StringType())
    def translate_udf(column: pd.Series) -> pd.Series:
        # Handle empty or null values
        if column.empty:
            return pd.Series([], dtype=str)
        
        # Filter out None/null values and convert to list
        clean_column = column.dropna().astype(str)
        if clean_column.empty:
            return pd.Series([''] * len(column), dtype=str)
        
        try:
            if translation_config:
                results = translator.translate_batch(clean_column.tolist(), translation_config)
            else:
                results = translator.translate_batch(clean_column.tolist())
            
            # Handle the case where we had null values - map back to original indices
            result_series = pd.Series([''] * len(column), dtype=str)
            result_series[clean_column.index] = results
            return result_series
            
        except Exception as e:
            logger.error(f"Translation failed: {e}")
            # Return empty strings on failure
            return pd.Series([''] * len(column), dtype=str)

    return translate_udf

def translate_with_udf(
    model_path: str,
    spark_df: DataFrame,
    input_column_name: str,
    output_column_name: str,
    translator_config=None,
    translation_config=None,
    optimized_config=True,
) -> DataFrame:
    
    spark = SparkSession.builder.getOrCreate()
    task_id = os.getenv('SPARK_TASK_ATTEMPT_ID', str(os.getpid()))
    
    # Create task-specific package directory
    package_dir = Path(f"/tmp/abtranslate/packages_{task_id}")
    package_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy model to a standardized name in the package directory
    dst_model_path = package_dir / "model.zip"
    
    # Copy to executor-local dir if not already there
    if not dst_model_path.exists():
        shutil.copy(model_path, dst_model_path)
        logger.info(f"Copied model from {model_path} to {dst_model_path}")

    # Add to Spark distributed files
    spark.sparkContext.addFile(str(dst_model_path))
    logger.info(f"Added {dst_model_path} to Spark distributed files")

    # Apply the translation UDF
    translate_udf = translate_column(
        translator_config=translator_config,
        translation_config=translation_config,
        optimized_config=optimized_config
    )

    df_translated = spark_df.withColumn(
        output_column_name,
        translate_udf(F.col(input_column_name))
    )

    return df_translated