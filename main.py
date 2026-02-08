from src.ingestion.load_data import ingest_data

if __name__ == "__main__":
    df = ingest_data("data/raw/tickets.csv")
    print(df.head())
