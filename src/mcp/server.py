"""MCP server exposing financial analytics capabilities."""

from mcp.server import MCPServer

from src.tools.analytics_tools import (
    get_monthly_kpis,
    get_country_breakdown,
)

mcp = MCPServer("Financial Analytics")

@mcp.tool()
def monthly_kpis(month: str) -> dict:
    """Return aggregate transaction KPIs for a specified month."""
    return get_monthly_kpis(month)

@mcp.tool()
def country_breakdown(month: str) -> list | dict:
    """Return transaction KPIs grouped by country for a specified month."""
    return get_country_breakdown(month)

if __name__ == "__main__":
    mcp.run()