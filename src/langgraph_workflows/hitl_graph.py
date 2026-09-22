from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt, Command


class ApprovalState(TypedDict):
    recommendation: str
    decision: str


def request_approval(state: ApprovalState):
    decision = interrupt(
        {
            "message": "Analyst approval required",
            "recommendation": state["recommendation"],
        }
    )

    return {
        "decision": decision
    }


def finalize(state: ApprovalState):
    return {
        "recommendation": (
            f"{state['recommendation']} | "
            f"Human decision: {state['decision']}"
        )
    }

def reject(state: ApprovalState):
    return {
        "recommendation": (
            f"{state['recommendation']} | "
            "Recommendation rejected by analyst."
        )
    }

def route_decision(state: ApprovalState):
    if state["decision"].lower() == "approved":
        return "approved"

    return "rejected"


builder = StateGraph(ApprovalState)

builder.add_node("request_approval", request_approval)
builder.add_node("finalize", finalize)
builder.add_node("reject", reject)

builder.add_edge(START, "request_approval")

builder.add_conditional_edges(
    "request_approval",
    route_decision,
    {
        "approved": "finalize",
        "rejected": "reject",
    },
)

builder.add_edge("finalize", END)
builder.add_edge("reject", END)

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":
    config = {
        "configurable": {
            "thread_id": "approval-1"
        }
    }

    # First invocation: workflow pauses at interrupt()
    first_result = graph.invoke(
        {
            "recommendation": "Investigate the unusual increase in transaction volume.",
            "decision": "",
        },
        config=config,
    )

    print("\n--- PAUSED ---")
    print(first_result)

    print("\n--- HUMAN REJECTS ---")

final_result = graph.invoke(
    Command(resume="rejected"),
    config=config,
)

print("\n--- RESUMED AND COMPLETED ---")
print(final_result)