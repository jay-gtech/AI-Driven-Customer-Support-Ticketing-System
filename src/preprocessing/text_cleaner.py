import re
import pandas as pd


def clean_text(text: str) -> str:
    """
    Clean and normalize text for NLP tasks.
    """
    if not isinstance(text, str):
        return ""

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)

    # Remove extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply text preprocessing to ticket dataset.
    """
    df = df.copy()

    # Combine subject and description
    df["combined_text"] = (
        df["subject"].fillna("") + " " + df["description"].fillna("")
    )

    # Clean text
    df["clean_text"] = df["combined_text"].apply(clean_text)

    return df
