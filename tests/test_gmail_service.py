from gmail_service import list_recent_emails


def main() -> None:
    emails = list_recent_emails(max_results=5)

    if not emails:
        print("No inbox emails were found.")
        return

    print(f"Found {len(emails)} recent inbox emails.\n")

    for index, email in enumerate(emails, start=1):
        print(f"Email {index}")
        print(f"From: {email['sender']}")
        print(f"Subject: {email['subject']}")
        print(f"Date: {email['date']}")
        print("-" * 50)


if __name__ == "__main__":
    main()
