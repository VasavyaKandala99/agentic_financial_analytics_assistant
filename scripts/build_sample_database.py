"""Build a local SQLite database from the public sample transaction data."""

import sqlite3
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "sample"
    / "sample_transactions.csv"
)

DB_PATH = PROJECT_ROOT / "analytics.db"


def build_database():
    df = pd.read_csv(CSV_PATH)

    with sqlite3.connect(DB_PATH) as conn:
        df.to_sql(
            "transactions",
            conn,
            if_exists="replace",
            index=False,
        )

    print(f"Database created: {DB_PATH}")
    print(f"Rows loaded: {len(df):,}")


if __name__ == "__main__":
    build_database()