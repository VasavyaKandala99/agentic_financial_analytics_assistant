"""SQL analytics tools used by the financial analytics agents."""

import json
import sqlite3
from pathlib import Path

import pandas as pd
from agents.decorators import tool


# Repository root:
# agentic-financial-analytics-assistant/
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Local generated database. This file is ignored by Git.
DB_PATH = PROJECT_ROOT / "analytics.db"


def get_monthly_kpis(month: str) -> dict:
    """
    Retrieve aggregate transaction KPIs for a specified month.

    Args:
        month: Month in YYYY-MM format, for example 2026-08.

    Returns:
        Dictionary containing transaction count, transaction volume,
        average transaction value, and failed transaction rate.
    """

    query = """
    SELECT
        SUBSTR(transaction_date, 1, 7) AS month,
        COUNT(*) AS transaction_count,
        ROUND(SUM(transaction_amount), 2) AS transaction_volume,
        ROUND(AVG(transaction_amount), 2) AS avg_transaction_value,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN transaction_status = 'failed'
                    THEN 1
                    ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS failed_transaction_rate
    FROM transactions
    WHERE SUBSTR(transaction_date, 1, 7) = ?
    GROUP BY SUBSTR(transaction_date, 1, 7);
    """

    with sqlite3.connect(DB_PATH) as local_conn:
        result = pd.read_sql_query(
            query,
            local_conn,
            params=[month],
        )

    if result.empty:
        return {
            "error": f"No data available for {month}"
        }

    # Convert NumPy/Pandas values into normal Python values.
    return json.loads(
        result.iloc[0].to_json()
    )


def get_country_breakdown(month: str) -> list | dict:
    """
    Retrieve transaction KPIs grouped by country for a specified month.

    Args:
        month: Month in YYYY-MM format, for example 2026-08.

    Returns:
        List of country-level KPI dictionaries, or an error dictionary
        when no data is available.
    """

    query = """
    SELECT
        country,
        COUNT(*) AS transaction_count,
        ROUND(SUM(transaction_amount), 2) AS transaction_volume,
        ROUND(AVG(transaction_amount), 2) AS avg_transaction_value,
        ROUND(
            100.0 * SUM(
                CASE
                    WHEN transaction_status = 'failed'
                    THEN 1
                    ELSE 0
                END
            ) / COUNT(*),
            2
        ) AS failed_transaction_rate
    FROM transactions
    WHERE SUBSTR(transaction_date, 1, 7) = ?
    GROUP BY country
    ORDER BY failed_transaction_rate DESC;
    """

    with sqlite3.connect(DB_PATH) as local_conn:
        result = pd.read_sql_query(
            query,
            local_conn,
            params=[month],
        )

    if result.empty:
        return {
            "error": f"No data available for {month}"
        }

    return json.loads(
        result.to_json(orient="records")
    )


@tool
def monthly_kpis(month: str) -> str:
    """
    Retrieve transaction KPIs for a specified month.

    Args:
        month: Month in YYYY-MM format, for example 2026-08.
    """

    result = get_monthly_kpis(month)

    return json.dumps(result)


@tool
def country_breakdown(month: str) -> str:
    """
    Retrieve transaction KPIs grouped by country for a specified month.

    Args:
        month: Month in YYYY-MM format, for example 2026-08.
    """

    result = get_country_breakdown(month)

    return json.dumps(result)