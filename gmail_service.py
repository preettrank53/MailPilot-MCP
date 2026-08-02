from typing import Any

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import authenticate_gmail


def build_gmail_service() -> Any:
    """Create and return an authenticated Gmail API service."""

    credentials = authenticate_gmail()

    return build(
        "gmail",
        "v1",
        credentials=credentials,
        cache_discovery=False,
    )


def get_header(headers: list[dict[str, str]], name: str) -> str:
    """Return a specific email header value."""

    for header in headers:
        if header.get("name", "").lower() == name.lower():
            return header.get("value", "")

    return ""


def list_recent_emails(max_results: int = 5) -> list[dict[str, str]]:
    """Return basic details for recent inbox emails."""

    if max_results < 1:
        raise ValueError("max_results must be at least 1.")

    service = build_gmail_service()

    try:
        response = (
            service.users()
            .messages()
            .list(
                userId="me",
                labelIds=["INBOX"],
                maxResults=max_results,
            )
            .execute()
        )

        messages = response.get("messages", [])
        results: list[dict[str, str]] = []

        for message in messages:
            message_id = message["id"]

            message_data = (
                service.users()
                .messages()
                .get(
                    userId="me",
                    id=message_id,
                    format="metadata",
                    metadataHeaders=["From", "Subject", "Date"],
                )
                .execute()
            )

            headers = message_data.get("payload", {}).get("headers", [])

            results.append(
                {
                    "id": message_id,
                    "sender": get_header(headers, "From"),
                    "subject": get_header(headers, "Subject") or "(No subject)",
                    "date": get_header(headers, "Date"),
                }
            )

        return results

    except HttpError as error:
        raise RuntimeError(
            f"Gmail API request failed: {error}"
        ) from error
