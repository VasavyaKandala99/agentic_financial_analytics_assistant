from langgraph.checkpoint.memory import InMemorySaver

from typing import TypedDict, Literal
from pydantic import BaseModel
from openai import OpenAI

from dotenv import load_dotenv

load_dotenv(override=True)

from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from agents import Runner

from src.agents.data_agent import data_agent
from src.agents.knowledge_agent import knowledge_agent

class FinancialAssistantState(TypedDict):
    question: str
    route: Literal["data", "knowledge"]
    answer: str
    requires_approval: bool
    decision: str

class RouteDecision(BaseModel):
    route: Literal["data", "knowledge"]

class ApprovalDecision(BaseModel):
    requires_approval: bool

def router_node(state: FinancialAssistantState):
    client = OpenAI()
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Route the user's financial analytics question. "
                    "Choose 'data' when the question requires numerical analysis, "
                    "KPIs, transactions, calculations, comparisons, trends, or database data. "
                    "Choose 'knowledge' when the question asks for definitions, "
                    "business concepts, policies, or documentation."
                ),
            },
            {
                "role": "user",
                "content": state["question"],
            },
        ],
        text_format=RouteDecision,
    )

    return {"route": response.output_parsed.route}

def data_node(state: FinancialAssistantState):
    result = Runner.run_sync(
        data_agent,
        state["question"],
    )

    return {"answer": result.final_output}

def knowledge_node(state: FinancialAssistantState):
    result = Runner.run_sync(
        knowledge_agent,
        state["question"],
    )

    return {"answer": result.final_output}

def approval_check_node(state: FinancialAssistantState):
    client = OpenAI()
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": (
                    "Determine whether the assistant's answer proposes or recommends "
                    "an action that should require human analyst approval before proceeding. "
                    "Routine factual answers, KPI results, definitions, and explanations "
                    "do not require approval. Recommendations to investigate, escalate, "
                    "execute, change, or take operational action require approval."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question: {state['question']}\n"
                    f"Answer: {state['answer']}"
                ),
            },
        ],
        text_format=ApprovalDecision,
    )

    return {
        "requires_approval": response.output_parsed.requires_approval
    }

def human_approval_node(state: FinancialAssistantState):
    decision = interrupt(
        {
            "message": "Analyst approval required",
            "question": state["question"],
            "answer": state["answer"],
        }
    )

    return {"decision": decision}

def choose_approval_path(state: FinancialAssistantState):
    if state["requires_approval"]:
        return "human_approval"

    return "end"

def choose_route(state: FinancialAssistantState):
    return state["route"]

builder = StateGraph(FinancialAssistantState)

builder.add_node("router", router_node)
builder.add_node("data", data_node)
builder.add_node("knowledge", knowledge_node)
builder.add_node("approval_check", approval_check_node)
builder.add_node("human_approval", human_approval_node)

builder.add_edge(START, "router")

builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "data": "data",
        "knowledge": "knowledge",
    },
)

# Both specialist paths go through the approval check
builder.add_edge("data", "approval_check")
builder.add_edge("knowledge", "approval_check")

builder.add_conditional_edges(
    "approval_check",
    choose_approval_path,
    {
        "human_approval": "human_approval",
        "end": END,
    },
)

builder.add_edge("human_approval", END)

checkpointer = InMemorySaver()

financial_assistant_graph = builder.compile(
    checkpointer=checkpointer
)

