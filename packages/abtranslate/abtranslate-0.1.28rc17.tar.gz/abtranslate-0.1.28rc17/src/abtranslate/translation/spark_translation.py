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
    package_path = SparkFiles.get("model.zip")

    if not os.path.exists(package_path):
        raise FileNotFoundError(f"Model path {package_path} doesn't exist")

    # Load package ONCE outside UDF
    import abtranslate.config.constants
    abtranslate.config.constants.PACKAGE_DIR = package_dir  # still not ideal
    package = load_argostranslate_model(package_path)

    # Build translator once
    if translator_config:
        translator = package.load_translator(translator_config, optimized_config=optimized_config)
    else:
        translator = package.load_translator(optimized_config=optimized_config)

    @pandas_udf(StringType())
    def translate_udf(column: pd.Series) -> pd.Series:
        if translation_config:
            return pd.Series(translator.translate_batch(column, translation_config))
        else:
            return pd.Series(translator.translate_batch(column))

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
    
    from abtranslate.config.constants import PACKAGE_DIR
    PACKAGE_DIR = Path(f"/tmp/abtranslate/packages_{task_id}")  # override as needed
    
    # Ensure working dir exists
    PACKAGE_DIR.mkdir(parents=True, exist_ok=True)
    dst_model_path = PACKAGE_DIR / "model.zip"

    # Copy to executor-local dir if not already
    if not dst_model_path.exists():
        shutil.copy(model_path, dst_model_path)

    # Add to Spark distributed files (no need to check listFiles)
    spark.sparkContext.addFile(str(dst_model_path))

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
