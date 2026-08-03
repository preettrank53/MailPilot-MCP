import asyncio
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_DIR = Path(__file__).resolve().parent.parent
SERVER_FILE = PROJECT_DIR / "mcp_server.py"


async def run_client() -> None:
    """Connect to the Gmail MCP server and test its search tool."""

    server_parameters = StdioServerParameters(
        command=sys.executable,
        args=[str(SERVER_FILE)],
        cwd=str(PROJECT_DIR),
    )

    async with stdio_client(server_parameters) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream,
        ) as session:
            await session.initialize()

            tools_response = await session.list_tools()

            print("Connected to MCP server.")
            print(f"Discovered {len(tools_response.tools)} tool(s).\n")

            for tool in tools_response.tools:
                print(f"Tool name: {tool.name}")
                print(f"Description: {tool.description}")
                print(f"Input schema: {tool.inputSchema}")
                print("-" * 50)

            result = await session.call_tool(
                "search_gmail",
                arguments={
                    "query": "newer_than:7d",
                    "max_results": 2,
                },
            )

            print("\nTool call completed.")
            print(f"Is error: {result.isError}")

            for content in result.content:
                if content.type == "text":
                    print(content.text)


def main() -> None:
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
