"""Basic smoke tests for the financial analytics assistant."""

from src.agents.data_agent import data_agent
from src.agents.knowledge_agent import knowledge_agent
from src.agents.manager_agent import manager_agent
from src.agents.guarded_manager_agent import guarded_manager_agent
from src.rag.knowledge_search import build_file_search_tool


def test_agent_names():
    assert data_agent.name == "Data Analysis Specialist"
    assert knowledge_agent.name == "Business Knowledge Specialist"
    assert manager_agent.name == "Financial Analytics Manager"
    assert guarded_manager_agent.name == "Guarded Financial Analytics Manager"


def test_file_search_tool_builds():
    tool = build_file_search_tool()
    assert tool.__class__.__name__ == "FileSearchTool"