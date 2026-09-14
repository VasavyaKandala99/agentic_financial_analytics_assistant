"""Knowledge retrieval utilities for the financial analytics assistant."""

import os

from dotenv import load_dotenv
from openai import OpenAI
from agents import FileSearchTool


load_dotenv()


def get_vector_store_id() -> str:
    """Return the configured OpenAI vector store ID."""

    vector_store_id = os.getenv("OPENAI_VECTOR_STORE_ID")

    if not vector_store_id:
        raise RuntimeError(
            "OPENAI_VECTOR_STORE_ID is not configured. "
            "Add it to your environment or local .env file."
        )

    return vector_store_id


def build_file_search_tool(
    max_num_results: int = 3,
) -> FileSearchTool:
    """
    Build the hosted file-search tool used by the knowledge agent.

    Args:
        max_num_results: Maximum number of retrieved chunks.

    Returns:
        Configured OpenAI Agents SDK FileSearchTool.
    """

    return FileSearchTool(
        vector_store_ids=[get_vector_store_id()],
        max_num_results=max_num_results,
    )


def search_knowledge_base(
    query: str,
    max_num_results: int = 3,
):
    """
    Search the vector store directly.

    This helper is useful for testing retrieval independently
    from the LLM agent.

    Args:
        query: Natural-language retrieval query.
        max_num_results: Maximum number of search results.

    Returns:
        OpenAI vector-store search response.
    """

    client = OpenAI()

    return client.vector_stores.search(
        vector_store_id=get_vector_store_id(),
        query=query,
        max_num_results=max_num_results,
    )