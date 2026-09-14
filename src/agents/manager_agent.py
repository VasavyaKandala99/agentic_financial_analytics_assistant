"""Manager agent that coordinates specialist agents."""

from agents import Agent

from src.agents.data_agent import data_agent
from src.agents.knowledge_agent import knowledge_agent


manager_agent = Agent(
    name="Financial Analytics Manager",
    instructions=(
        "You are the manager for a financial analytics assistant. "
        "Delegate quantitative transaction and KPI questions to the data analysis specialist. "
        "Delegate business definitions, analytical concepts, and supporting knowledge questions "
        "to the business knowledge specialist. "
        "For questions that require both numerical analysis and business context, use both tools "
        "and combine their outputs into one clear answer. "
        "Do not invent unsupported numbers, definitions, or causal explanations."
    ),
    tools=[
        data_agent.as_tool(
            tool_name="data_analysis_specialist",
            tool_description=(
                "Use for quantitative analysis of transaction data, monthly KPIs, "
                "and country-level performance."
            ),
        ),
        knowledge_agent.as_tool(
            tool_name="business_knowledge_specialist",
            tool_description=(
                "Use for business definitions, financial analytics concepts, "
                "and knowledge-base questions."
            ),
        ),
    ],
)