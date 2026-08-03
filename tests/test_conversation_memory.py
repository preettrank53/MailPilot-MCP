import asyncio

from ai_service import run_iterative_gmail_agent


async def run_test() -> None:
    first_request = (
        "Find my newest unread email from Medium. "
        "Include enough identifying information so I can "
        "refer to it in my next message."
    )

    first_result = await run_iterative_gmail_agent(
        first_request
    )

    print("First answer:")
    print(first_result["answer"])

    conversation_history = [
        {
            "role": "user",
            "content": first_request,
        },
        {
            "role": "assistant",
            "content": first_result["answer"],
        },
    ]

    second_request = "Now read and summarize it."

    second_result = await run_iterative_gmail_agent(
        user_request=second_request,
        conversation_history=conversation_history,
    )

    print("\nSecond answer:")
    print(second_result["answer"])

    print("\nSecond request tool history:")
    for tool_call in second_result["tool_history"]:
        print(
            f"- {tool_call['tool_name']}: "
            f"{tool_call['arguments']}"
        )


def main() -> None:
    import sys
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        pass
    asyncio.run(run_test())


if __name__ == "__main__":
    main()
