"""Handoff-based agent routing."""

from agents import Agent

from src.agents.data_agent import data_agent
from src.agents.knowledge_agent import knowledge_agent


data_handoff_agent = Agent(
    name="Data Analysis Specialist",
    instructions=(
        "Handle quantitative financial analytics questions using the available "
        "transaction-data tools. Base numerical claims only on tool results."
    ),
    tools=data_agent.tools,
)


knowledge_handoff_agent = Agent(
    name="Business Knowledge Specialist",
    instructions=(
        "Handle business definitions, financial analytics concepts, and "
        "knowledge-base questions using file search. Ground answers in retrieved content."
    ),
    tools=knowledge_agent.tools,
)


triage_agent = Agent(
    name="Financial Analytics Triage Agent",
    instructions=(
        "Route quantitative transaction and KPI questions to the Data Analysis Specialist. "
        "Route business definitions and conceptual questions to the Business Knowledge Specialist. "
        "Choose the specialist best suited to answer the user's request."
    ),
    handoffs=[
        data_handoff_agent,
        knowledge_handoff_agent,
    ],
)