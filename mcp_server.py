from typing import Any

from mcp.server.fastmcp import FastMCP

from gmail_service import get_email, search_emails


mcp = FastMCP("MailPilot Gmail MCP")


@mcp.tool()
def search_gmail(
    query: str,
    max_results: int = 5,
) -> list[dict[str, Any]]:
    """
    Search the authenticated user's Gmail account.

    Use Gmail search syntax such as:
    - is:unread
    - from:github.com
    - subject:interview
    - newer_than:7d

    Args:
        query: Gmail search query.
        max_results: Maximum number of matching emails to return.

    Returns:
        Matching email metadata containing message ID, sender,
        subject and date.
    """

    return search_emails(
        query=query,
        max_results=max_results,
    )


@mcp.tool()
def get_gmail_email(
    message_id: str,
) -> dict[str, Any]:
    """
    Retrieve one Gmail message using its message ID.

    Use this tool after search_gmail returns a message ID.

    Args:
        message_id: Gmail message ID returned by search_gmail.

    Returns:
        Email details containing the message ID, thread ID, sender,
        recipient, subject, date and plain-text body.
    """

    return get_email(message_id)


if __name__ == "__main__":
    mcp.run(transport="stdio")
