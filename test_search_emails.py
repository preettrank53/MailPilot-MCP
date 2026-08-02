from gmail_service import search_emails


def main() -> None:
    query = "is:unread"
    emails = search_emails(
        query=query,
        max_results=5,
    )

    print(f'Search query: "{query}"')
    print(f"Found {len(emails)} matching emails.\n")

    if not emails:
        print("No matching emails were found.")
        return

    for index, email in enumerate(emails, start=1):
        print(f"Email {index}")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
