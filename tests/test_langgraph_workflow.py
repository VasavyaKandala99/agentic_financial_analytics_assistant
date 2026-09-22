import os

os.environ.setdefault("OPENAI_API_KEY", "test-key")

from src.langgraph_workflows.financial_assistant_graph import financial_assistant_graph

def test_normal_request_completes_without_approval():
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

def test_recommendation_pauses_for_human_approval():
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

def test_hitl_approval_resumes_graph():
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