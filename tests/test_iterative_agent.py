import asyncio
import json

from ai_service import run_iterative_gmail_agent


async def run_test() -> None:
    user_request = "Reply to Jia from Unstop and confirm I am interested."

    result = await run_iterative_gmail_agent(
        user_request
    )

    print(f"User request: {user_request}")
    print(f"Total tool calls: {result['total_tool_calls']}")
    print("Tool history:")
    for i, step in enumerate(result["tool_history"], 1):
        print(
            f"  Step {i}: {step['tool_name']} with arguments: {step['arguments']}"
        )

    print("\nPending Action:")
    print("-" * 50)
    print(json.dumps(result.get("pending_action"), indent=2))
    print("-" * 50)

    print("\nFinal answer:")
    print("-" * 50)
    print(result.get("answer"))
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
