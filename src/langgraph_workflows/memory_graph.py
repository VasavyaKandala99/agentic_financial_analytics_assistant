from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver


class MemoryState(TypedDict):
    message: str
    previous_message: str


def remember(state: MemoryState):
    previous = state.get("previous_message", "")

    print(f"Previous message: {previous}")
    print(f"Current message: {state['message']}")

    return {
        "previous_message": state["message"]
    }


builder = StateGraph(MemoryState)

builder.add_node("remember", remember)

builder.add_edge(START, "remember")
builder.add_edge("remember", END)


# Checkpointer stores graph state
checkpointer = InMemorySaver()

graph = builder.compile(checkpointer=checkpointer)


if __name__ == "__main__":

    config = {
        "configurable": {
            "thread_id": "user-1"
        }
    }

    print("\n--- TURN 1 ---")

    graph.invoke(
        {
            "message": "What were the monthly KPIs?",
            "previous_message": "",
        },
        config=config,
    )

    config_2 = {
        "configurable": {
            "thread_id": "user-2"
        }
    }

    print("\n--- TURN 2 ---")

    result = graph.invoke(
        {
            "message": "For March",
        },
        config=config_2,
    )

    print(result)