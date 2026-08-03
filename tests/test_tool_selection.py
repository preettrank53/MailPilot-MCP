import asyncio
import json

from ai_service import select_gmail_tool


async def run_test() -> None:
    user_request = "Show my five unread emails."

    decision = await select_gmail_tool(
        user_request
    )

    print(f"User request: {user_request}")
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


def main() -> None:
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
