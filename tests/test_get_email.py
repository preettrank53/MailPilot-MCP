from gmail_service import get_email, search_emails


def main() -> None:
    search_results = search_emails(
        query="newer_than:7d",
        max_results=1,
    )

    if not search_results:
        print("No recent email was found.")
        return

    message_id = search_results[0]["id"]
    email = get_email(message_id)

    print("Email retrieved successfully.\n")
    print(f"From: {email['sender']}")
    print(f"To: {email['recipient']}")
    print(f"Subject: {email['subject']}")
    print(f"Date: {email['date']}")
    print("\nBody preview:")
    print("-" * 50)
    print(email["body"][:500])
    print("-" * 50)


if __name__ == "__main__":
    main()
