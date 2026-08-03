import asyncio
import json

from ai_service import run_gmail_agent


async def run_test() -> None:
    user_request = "Show my three unread emails."

    result = await run_gmail_agent(
        user_request
    )

    print(f"User request: {user_request}")
    print(f"Tool used: {result['tool_used']}")

    if result["tool_arguments"] is not None:
        print("Tool arguments:")
        print(
            json.dumps(
                result["tool_arguments"],
                indent=2,
            )
        )

    print("\nFinal answer:")
    print("-" * 50)
    print(result["answer"])
    print("-" * 50)


def main() -> None:
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
