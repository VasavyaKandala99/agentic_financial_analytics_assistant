"""Test the Data Analysis Agent using MCP-provided tools."""

import asyncio

from dotenv import load_dotenv
from agents import Runner

from src.agents.mcp_data_agent import (
    analytics_mcp_server,
    mcp_data_agent,
)

load_dotenv()


async def main():
    async with analytics_mcp_server:
        result = await Runner.run(
            mcp_data_agent,
            "Give me the country-level transaction breakdown for August 2026.",
        )

        print("\nMCP Agent response:")
        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())