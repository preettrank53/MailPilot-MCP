from gmail_service import get_inbox_summary


def main() -> None:
    # Test validation: empty query
    try:
        get_inbox_summary(query="   ")
        print("FAIL: Expected ValueError for empty query")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    # Test validation: max_results out of range
    try:
        get_inbox_summary(max_results=0)
        print("FAIL: Expected ValueError for max_results < 1")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    try:
        get_inbox_summary(max_results=51)
        print("FAIL: Expected ValueError for max_results > 50")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    # Fetch real inbox summary
    print("\nFetching inbox summary (newer_than:7d)...")
    summary = get_inbox_summary(
        query="newer_than:7d",
        max_results=10,
    )

    print("PASS: Successfully retrieved inbox summary.")
    assert "total_emails" in summary, "Summary missing 'total_emails'"
    assert "unread" in summary, "Summary missing 'unread'"
    assert "senders" in summary, "Summary missing 'senders'"
    assert "emails" in summary, "Summary missing 'emails'"

    print(f"\nTotal Emails: {summary['total_emails']}")
    print(f"Unread Count: {summary['unread']}")

    # Verify sender ranking sorting
    print("\nSender Ranking:")
    senders = summary["senders"]
    assert len(senders) <= 5, "Senders list exceeded 5 entries."
    
    last_count = 999999
    for entry in senders:
        print(f"  - {entry['sender']}: {entry['count']} email(s)")
        assert entry["count"] <= last_count, "Senders list is not sorted descending by count."
        last_count = entry["count"]
    print("PASS: Senders are correctly sorted descending.")

    # Verify lightweight email list structure
    print("\nRecent Emails:")
    emails = summary["emails"]
    for index, email in enumerate(emails, start=1):
        print(f"  Email {index}:")
        print(f"    Subject: {email['subject']}")
        print(f"    Sender: {email['sender']}")
        print(f"    Date: {email['date']}")
        
        # Verify no body is retrieved
        assert "body" not in email, "Email metadata contains 'body' field when it should be lightweight."
        assert "id" not in email, "Email metadata contains 'id' field when it should be lightweight."
        
    print("PASS: Emails are lightweight (no body, no ID).")


if __name__ == "__main__":
    main()
