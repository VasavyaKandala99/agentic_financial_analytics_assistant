import os
from openai import OpenAI
from typing import TypedDict
from dotenv import load_dotenv

load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

from agents import Runner
from langgraph.graph import StateGraph, START, END

from src.agents.data_agent import data_agent
from src.agents.knowledge_agent import knowledge_agent


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
business concepts, policies, or documentation.

Question:
{state["question"]}
"""
    )

    route = response.output_text.strip().lower()

    if route not in {"data", "knowledge"}:
        route = "knowledge"

    return {"route": route}


def choose_route(state: AnalyticsState):
    return state["route"]


def data_node(state: AnalyticsState):
    result = Runner.run_sync(
        data_agent,
        state["question"],
    )

    return {
        "answer": result.final_output
    }

def knowledge_node(state: AnalyticsState):
    result = Runner.run_sync(
        knowledge_agent,
        state["question"],
    )

    return {
        "answer": result.final_output
    }


builder = StateGraph(AnalyticsState)

builder.add_node("router", router)
builder.add_node("data_agent", data_node)
builder.add_node("knowledge_agent", knowledge_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "data": "data_agent",
        "knowledge": "knowledge_agent",
    },
)

builder.add_edge("data_agent", END)
builder.add_edge("knowledge_agent", END)

analytics_graph = builder.compile()


if __name__ == "__main__":
    result = analytics_graph.invoke(
        {
            "question": "What were the monthly KPIs for 2024-03?",
            "route": "",
            "answer": "",
        }
    )

    print(result)