"""Conversation session helpers."""

from agents import SQLiteSession


def create_session(
    session_id: str = "financial_analytics_session",
    db_path: str = "analytics_conversations.db",
) -> SQLiteSession:
    """Create a persistent SQLite-backed conversation session."""
    return SQLiteSession(session_id, db_path)