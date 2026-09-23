from langgraph.types import Command

import src.langgraph_workflows.financial_assistant_graph as graph_module


financial_assistant_graph = graph_module.financial_assistant_graph


def fake_router_node(state):
    question = state["question"].lower()

    if "transaction volume" in question:
        return {"route": "data"}

    return {"route": "knowledge"}


def fake_data_node(state):
    return {
        "answer": (
            "Transaction volume increased compared with the prior period."
        )
    }


def fake_knowledge_node(state):
    return {
        "answer": (
            "Settlement is the process of completing a financial transaction."
        )
    }


def fake_approval_check_node(state):
    requires_approval = "recommend whether" in state["question"].lower()

    return {"requires_approval": requires_approval}


def build_test_graph():
    return graph_module.build_financial_assistant_graph(
        router=fake_router_node,
        data=fake_data_node,
        knowledge=fake_knowledge_node,
        approval_check=fake_approval_check_node,
    )


def test_normal_request_completes_without_approval():
    graph = build_test_graph()

    config = {
        "configurable": {
            "thread_id": "test-normal-request"
        }
    }

    result = graph.invoke(
        {
            "question": "What does settlement mean?",
            "route": "",
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
    graph = build_test_graph()

    config = {
        "configurable": {
            "thread_id": "test-hitl-interrupt"
        }
    }

    result = graph.invoke(
        {
            "question": (
                "Recommend whether we should investigate an unusual "
                "increase in transaction volume."
            ),
            "route": "",
            "answer": "",
            "requires_approval": False,
            "decision": "",
        },
        config=config,
    )

    assert result["requires_approval"] is True
    assert result["decision"] == ""
    assert "__interrupt__" in result


def test_hitl_approval_resumes_graph():
    graph = build_test_graph()

    config = {
        "configurable": {
            "thread_id": "pytest-hitl-approval"
        }
    }

    initial = graph.invoke(
        {
            "question": (
                "Recommend whether we should investigate an unusual "
                "increase in transaction volume."
            ),
            "route": "",
            "answer": "",
            "requires_approval": False,
            "decision": "",
        },
        config=config,
    )

    assert "__interrupt__" in initial

    resumed = graph.invoke(
        Command(resume="approved"),
        config=config,
    )

    assert resumed["decision"] == "approved"