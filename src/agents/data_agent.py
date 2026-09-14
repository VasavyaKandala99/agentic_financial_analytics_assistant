"""Data analysis specialist agent."""

from agents import Agent

from src.tools.analytics_tools import monthly_kpis, country_breakdown


data_agent = Agent(
    name="Data Analysis Specialist",
    instructions=(
        "You are a financial data analysis specialist. "
        "Use the available SQL-backed tools to answer quantitative questions "
        "about transaction performance. "
        "Use monthly_kpis for monthly KPI questions and country_breakdown "
        "for country-level analysis. "
        "Base numerical claims only on tool results. "
        "Do not invent unavailable metrics, data, or causal explanations. "
        "Clearly state when the available data cannot answer a question."
    ),
    tools=[
        monthly_kpis,
        country_breakdown,
    ],
)