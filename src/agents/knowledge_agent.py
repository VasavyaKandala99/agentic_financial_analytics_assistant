"""Business knowledge specialist agent."""

from agents import Agent

from src.rag.knowledge_search import build_file_search_tool


knowledge_agent = Agent(
    name="Business Knowledge Specialist",
    instructions=(
        "You are a business knowledge specialist for financial analytics. "
        "Use the file-search tool to answer questions about business definitions, "
        "analytical concepts, and supporting financial knowledge. "
        "Ground answers in the retrieved knowledge base. "
        "Do not invent definitions or unsupported facts. "
        "If the knowledge base does not contain enough information, say so clearly."
    ),
    tools=[
        build_file_search_tool(),
    ],
)