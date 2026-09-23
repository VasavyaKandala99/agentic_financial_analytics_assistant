from langgraph.types import Command

from src.langgraph_workflows.financial_assistant_graph import (
    financial_assistant_graph,
)


def main():
    config = {
        "configurable": {
            "thread_id": "financial-review-1"
        }
    }

    question = input("\nAsk the Financial Analytics Assistant: ")

    result = financial_assistant_graph.invoke(
        {
            "question": question,
            "route": "data",
            "answer": "",
            "requires_approval": False,
            "decision": "",
        },
        config=config,
    )

    print("\n--- WORKFLOW RESULT ---")
    print(result)

    if "__interrupt__" in result:
        print("\n--- HUMAN APPROVAL REQUIRED ---")

        decision = input("Approve or reject? ").strip().lower()

        while decision not in {"approved", "rejected"}:
            decision = input(
                "Please type 'approved' or 'rejected': "
            ).strip().lower()

        final_result = financial_assistant_graph.invoke(
            Command(resume=decision),
            config=config,
        )

        print("\n--- RESUMED WORKFLOW ---")
        print(final_result)

if __name__ == "__main__":
    main()