import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class AnalyticsState(TypedDict):
    question: str
    route: str
    answer: str


def router(state: AnalyticsState):
    response = client.responses.create(
        model="gpt-5-mini",
        input=f"""
Classify this financial analytics question.

Return ONLY one word:

data = questions requiring numerical analysis, KPIs, transactions,
revenue, trends, comparisons, aggregations, or calculations.

knowledge = questions asking for definitions, explanations,
business concepts, or documentation.

Question:
{state["question"]}
"""
    )

    route = response.output_text.strip().lower()

    if route not in {"data", "knowledge"}:
        route = "knowledge"

    return {"route": route}


def data_node(state: AnalyticsState):
    return {
        "answer": f"DATA route selected for: {state['question']}"
    }


def knowledge_node(state: AnalyticsState):
    return {
        "answer": f"KNOWLEDGE route selected for: {state['question']}"
    }


def choose_route(state: AnalyticsState):
    return state["route"]


builder = StateGraph(AnalyticsState)

builder.add_node("router", router)
builder.add_node("data", data_node)
builder.add_node("knowledge", knowledge_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "data": "data",
        "knowledge": "knowledge",
    },
)

builder.add_edge("data", END)
builder.add_edge("knowledge", END)

graph = builder.compile()


if __name__ == "__main__":
    result = graph.invoke(
        {
            "question": "Compare monthly revenue across countries",
            "route": "",
            "answer": "",
        }
    )

    print(result)