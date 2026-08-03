import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


PROJECT_DIR = Path(__file__).resolve().parent.parent
SERVER_FILE = PROJECT_DIR / "mcp_server.py"


def get_text_content(result: object) -> str:
    """Return the first text block from an MCP tool result."""

    for content in result.content:
        if content.type == "text":
            return content.text

    raise RuntimeError("The MCP tool returned no text content.")


async def run_client() -> None:
    """Connect to the Gmail MCP server and test its search and retrieval tools."""

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

            # 1. Search for recent emails
            search_result = await session.call_tool(
                "search_gmail",
                arguments={
                    "query": "newer_than:7d",
                    "max_results": 2,
                },
            )

            if search_result.isError:
                raise RuntimeError(
                    get_text_content(search_result)
                )

            # Robust parsing of search_gmail results (handles both JSON lists and multiple text content blocks)
            emails = []
            for content in search_result.content:
                if content.type == "text":
                    try:
                        emails.append(json.loads(content.text))
                    except json.JSONDecodeError:
                        pass

            print(f"\nSearch returned {len(emails)} email(s).")

            if not emails:
                print("No recent emails were found.")
                return

            first_email = emails[0]
            message_id = first_email["id"]

            print(f"Selected subject: {first_email['subject']}")
            print(f"Selected message ID: {message_id}")

            # 2. Get full details for the first email
            email_result = await session.call_tool(
                "get_gmail_email",
                arguments={
                    "message_id": message_id,
                },
            )

            if email_result.isError:
                raise RuntimeError(
                    get_text_content(email_result)
                )

            email_text = get_text_content(email_result)
            email = json.loads(email_text)

            print("\nFull email retrieved through MCP.")
            print(f"From: {email['sender']}")
            print(f"To: {email['recipient']}")
            print(f"Subject: {email['subject']}")
            print(f"Date: {email['date']}")

            print("\nBody preview:")
            print("-" * 50)
            print(email["body"][:500])
            print("-" * 50)

            # 3. Test empty message ID through MCP
            print("\nTesting invalid empty message ID through MCP...")
            try:
                invalid_result = await session.call_tool(
                    "get_gmail_email",
                    arguments={
                        "message_id": "   ",
                    },
                )
                print(f"Invalid ID is error: {invalid_result.isError}")
                for content in invalid_result.content:
                    if content.type == "text":
                        print(content.text)
            except Exception as error:
                print(f"Empty message ID call failed as expected: {error}")

            # 4. Test nonexistent message ID through MCP
            print("\nTesting nonexistent message ID through MCP...")
            try:
                nonexistent_result = await session.call_tool(
                    "get_gmail_email",
                    arguments={
                        "message_id": "not-a-real-gmail-message-id",
                    },
                )
                print(f"Nonexistent ID is error: {nonexistent_result.isError}")
                for content in nonexistent_result.content:
                    if content.type == "text":
                        print(content.text)
            except Exception as error:
                print(f"Nonexistent message ID call failed as expected: {error}")


def main() -> None:
    asyncio.run(run_client())


if __name__ == "__main__":
    main()
