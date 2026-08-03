from mcp_server import search_gmail


def main() -> None:
    results = search_gmail(
        query="newer_than:7d",
        max_results=2,
    )

    print(f"Tool returned {len(results)} emails.")

    for email in results:
        print(f"Subject: {email['subject']}")
        print(f"From: {email['sender']}")
        print("-" * 40)


if __name__ == "__main__":
    main()
