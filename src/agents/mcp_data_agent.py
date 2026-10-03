"""Data analysis specialist agent using MCP tools."""

from agents import Agent
from agents.mcp import MCPServerStdio 

analytics_mcp_server = MCPServerStdio(
    name="Financial Analytics MCP Server",
    params={
        "command": "python",
        "args": ["-m", "src.mcp.server"],
    },
    cache_tools_list=True,
)

mcp_data_agent = Agent(
    name="MCP Data Analysis Specialist",
    instructions=(
        "You are a financial data analysis specialist. "
        "Use the available MCP-provided SQL-backed tools to answer quantitative questions "
        "about transaction performance. "
        "Use monthly_kpis for monthly KPI questions and country_breakdown "
        "for country-level analysis. "
        "When a user provides a month in natural language, convert it to YYYY-MM format "
        "before calling an MCP analytics tool. For example, August 2026 becomes 2026-08. "
        "Base numerical claims only on tool results. "
        "Do not invent unavailable metrics, data, or causal explanations. "
        "Clearly state when the available data cannot answer a question."
    ),
    mcp_servers=[analytics_mcp_server],
)