from gmail_service import search_threads


def main() -> None:
    # Test validation: empty query
    try:
        search_threads(
            query="   ",
            max_results=3,
        )
        print("FAIL: Expected ValueError for empty query")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    # Test validation: max_results > 20
    try:
        search_threads(
            query="is:unread",
            max_results=21,
        )
        print("FAIL: Expected ValueError for max_results > 20")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    # Test valid query execution
    threads = search_threads(
        query="newer_than:30d",
        max_results=3,
    )

    print(
        f"\nFound {len(threads)} Gmail thread(s) for valid query.\n"
    )

    for index, thread in enumerate(
        threads,
        start=1,
    ):
        print(f"Thread {index}")
        print(
            f"Subject: {thread['subject']}"
        )
        print(
            f"Messages: {thread['message_count']}"
        )
        print(
            f"Participants: "
            f"{', '.join(thread['participants'])}"
        )
        print(
            f"Latest date: "
            f"{thread['latest_date']}"
        )
        print(
            f"Snippet: {thread['snippet'][:150]}"
        )
        print("-" * 50)


if __name__ == "__main__":
    main()
