import pandas as pd

REQUIRED_COLUMNS = [
    "ticket_id",
    "subject",
    "description",
    "channel",
    "category",
    "priority",
    "created_at",
    "customer_plan",
    "sla_breached",
    "escalated"
]


def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    print(" Dataset loaded")
    return df


def validate_schema(df: pd.DataFrame):
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing_cols:
        raise ValueError(f" Missing columns: {missing_cols}")
    print(" Schema validated")


def ingest_data(file_path: str) -> pd.DataFrame:
    df = load_data(file_path)
    validate_schema(df)
    return df
