"""Test the manager agent with the MCP-backed data specialist."""

import asyncio

from dotenv import load_dotenv
from agents import Runner

from src.agents.manager_agent import manager_agent
from src.agents.mcp_data_agent import analytics_mcp_server


load_dotenv(override=True)


async def main():
    async with analytics_mcp_server:
        result = await Runner.run(
            manager_agent,
            "Give me the country-level transaction breakdown for August 2026.",
        )

        print("\nManager MCP response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())