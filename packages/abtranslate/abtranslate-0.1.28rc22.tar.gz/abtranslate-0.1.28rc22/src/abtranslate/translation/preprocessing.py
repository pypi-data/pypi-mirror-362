import pandas as pd
import regex as re
from pyspark.sql.functions import pandas_udf
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
BOUNDARY  = '▁'
UNK_TOKEN = '***.'

# Use Unicode property (needs `regex` module)
PATTERN   = re.compile(r'([^\p{IsHan}]+)', flags=re.UNICODE)

@pandas_udf("struct<masked_text:string, extracted_tokens:string>")
def extract_and_mask_udf(col: pd.Series) -> pd.DataFrame:
    """
    Return a struct with:
      • masked_text      – original text with each non‑Chinese span → <unk>
      • extracted_tokens – those spans joined by BOUNDARY
    Null and non‑string inputs become ''.
    """
    s = col.astype("string").fillna("")          # null‑safe → pandas StringDtype

    extracted = s.apply(lambda t: BOUNDARY.join(PATTERN.findall(t)))
    masked    = s.apply(lambda t: PATTERN.sub(UNK_TOKEN, t))

    return pd.DataFrame(
        {"masked_text": masked.astype(str),
         "extracted_tokens": extracted.astype(str)}
    )

# -------------------------------------------------------------------
@pandas_udf("string")
def restore_tokens_udf(masked: pd.Series,
                       extracted: pd.Series) -> pd.Series:
    m = masked.astype("string").fillna("")
    e = extracted.astype("string").fillna("")

    def rebuild(pair):
        masked_txt, extracted_txt = pair
        parts  = masked_txt.split(UNK_TOKEN)
        tokens = extracted_txt.split(BOUNDARY) if extracted_txt else []
        return "".join(
            part + (tokens[i] if i < len(tokens) else "")
            for i, part in enumerate(parts)
        )

    return pd.Series(map(rebuild, zip(m, e)))
