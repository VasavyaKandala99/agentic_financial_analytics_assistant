import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


server_params = StdioServerParameters(
    command="python",
    args=["-m", "src.mcp.server"],
)


async def main():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"Discovered MCP tool: {tool.name}")

            result = await session.call_tool(
                "monthly_kpis",
                arguments={"month": "2026-08"},
            )

            print("\nMCP monthly_kpis result:")
            print(result)

            country_result = await session.call_tool(
                "country_breakdown",
                arguments={"month": "2026-08"},
            )

            print("\nMCP country_breakdown result:")
            print(country_result)

if __name__ == "__main__":
    asyncio.run(main())