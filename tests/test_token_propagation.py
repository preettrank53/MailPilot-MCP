import asyncio
from unittest.mock import AsyncMock, patch

from mcp_client import call_mcp_tool


async def run_test() -> None:
    fake_token = "fake-web-access-token"

    with patch(
        "mcp_client.run_with_mcp_session",
        new_callable=AsyncMock,
    ) as mocked_runner:
        mocked_runner.return_value = []

        result = await call_mcp_tool(
            tool_name="search_gmail",
            arguments={
                "query": "is:unread",
                "max_results": 1,
            },
            access_token=fake_token,
        )

        assert result == []

        _, keyword_arguments = (
            mocked_runner.await_args
        )

        assert (
            keyword_arguments["access_token"]
            == fake_token
        )

    print(
        "Access token was forwarded privately "
        "to the MCP session runner."
    )


def main() -> None:
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
