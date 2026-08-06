import asyncio
import json

from ai_service import select_gmail_tool


async def test_request(user_request: str) -> None:
    decision = await select_gmail_tool(user_request)

    print(f"\nUser request: {user_request}")
    print(f"Decision type: {decision['type']}")

    if decision["type"] == "tool_call":
        print(f"Tool selected: {decision['tool_name']}")
        print("Arguments:")
        print(
            json.dumps(
                decision["arguments"],
                indent=2,
            )
        )
    else:
        print(f"Model response: {decision['content']}")
    print("-" * 50)


async def run_test() -> None:
    # Existing test case
    await test_request("Show my five unread emails.")

    # New thread search test case
    await test_request("Summarize my conversation with Medium.")


def main() -> None:
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
