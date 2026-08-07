from gmail_service import build_email_message


def main() -> None:
    encoded = build_email_message(
        to="example@example.com",
        subject="Test Draft",
        body="Hello from MailPilot.",
    )

    assert isinstance(encoded, str)
    assert encoded

    print("Email message encoding passed.")


if __name__ == "__main__":
    main()
