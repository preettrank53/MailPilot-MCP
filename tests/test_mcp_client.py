import asyncio

from mcp_client import call_mcp_tool, list_mcp_tools


async def run_test() -> None:
    tools = await list_mcp_tools()

    print(f"Discovered {len(tools)} MCP tools.\n")

    for tool in tools:
        print(f"Tool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print(f"Schema: {tool['input_schema']}")
        print("-" * 50)

    emails = await call_mcp_tool(
        "search_gmail",
        {
            "query": "newer_than:7d",
            "max_results": 2,
        },
    )

    print(f"\nSearch returned {len(emails)} email(s).")

    if not emails:
        print("No recent emails were found.")
        return

    first_email = emails[0]

    print(f"Selected subject: {first_email['subject']}")

    full_email = await call_mcp_tool(
        "get_gmail_email",
        {
            "message_id": first_email["id"],
        },
    )

    print("\nEmail retrieved through reusable MCP client.")
    print(f"From: {full_email['sender']}")
    print(f"Subject: {full_email['subject']}")

    print("\nBody preview:")
    print("-" * 50)
    print(full_email["body"][:500])
    print("-" * 50)




def main() -> None:
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
