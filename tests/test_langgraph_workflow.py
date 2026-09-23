import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from types import SimpleNamespace
from unittest.mock import patch

import src.langgraph_workflows.financial_assistant_graph as graph_module

financial_assistant_graph = graph_module.financial_assistant_graph

def mock_parse(*args, **kwargs):
    text_format = kwargs.get("text_format")
    input_data = kwargs.get("input", [])
    input_text = str(input_data)

    if text_format.__name__ == "RouteDecision":
        route = "data" if "transaction volume" in input_text.lower() else "knowledge"

        return SimpleNamespace(
            output_parsed=SimpleNamespace(route=route)
        )

    if text_format.__name__ == "ApprovalDecision":
        requires_approval = "Recommend whether" in input_text

        return SimpleNamespace(
            output_parsed=SimpleNamespace(
                requires_approval=requires_approval
            )
        )

@patch.object(
    graph_module.OpenAI,
    "responses",
    create=True,
)

def test_normal_request_completes_without_approval(mock_openai):
    mock_openai.parse.side_effect = mock_parse
    config = {
        "configurable": {
            "thread_id": "test-normal-request"
        }
    }

    result = financial_assistant_graph.invoke(
        {
            "question": "What does settlement mean?",
            "route": "knowledge",
            "answer": "",
            "requires_approval": False,
            "decision": "",
        },
        config=config,
    )

    assert result["route"] == "knowledge"
    assert result["requires_approval"] is False
    assert result["decision"] == ""
    assert "__interrupt__" not in result

@patch.object(
    graph_module.OpenAI,
    "responses",
    create=True,
)

def test_recommendation_pauses_for_human_approval(mock_openai):
    mock_openai.parse.side_effect = mock_parse
    config = {
        "configurable": {
            "thread_id": "test-hitl-interrupt"
        }
    }

    result = financial_assistant_graph.invoke(
        {
            "question": "Recommend whether we should investigate an unusual increase in transaction volume.",
            "route": "data",
            "answer": "",
            "requires_approval": True,
            "decision": "",
        },
        config=config,
    )

    assert result["requires_approval"] is True
    assert result["decision"] == ""
    assert "__interrupt__" in result

@patch.object(
    graph_module.OpenAI,
    "responses",
    create=True,
)
    
def test_hitl_approval_resumes_graph(mock_openai):
    mock_openai.parse.side_effect = mock_parse
    from langgraph.types import Command

    config = {"configurable": {"thread_id": "pytest-hitl-approval"}}

    initial = financial_assistant_graph.invoke(
        {
            "question": "Recommend whether we should investigate an unusual increase in transaction volume."
        },
        config=config,
    )

    assert "__interrupt__" in initial

    resumed = financial_assistant_graph.invoke(
        Command(resume="approved"),
        config=config,
    )

    assert resumed["decision"] == "approved"