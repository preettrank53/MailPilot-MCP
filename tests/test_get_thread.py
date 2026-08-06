from gmail_service import build_thread, get_thread, search_threads


def main() -> None:
    # Test validation: empty thread_id
    try:
        get_thread(thread_id="   ")
        print("FAIL: Expected ValueError for empty thread_id")
    except ValueError as e:
        print(f"PASS: Got expected error: {e}")

    # Fetch a valid thread to test retrieval and building
    threads = search_threads(
        query="newer_than:30d",
        max_results=1,
    )

    if not threads:
        print("SKIP: No threads found in the last 30 days to test get_thread.")
        return

    target_thread_id = threads[0]["thread_id"]
    print(f"\nRetrieving thread with ID: {target_thread_id}...")

    # Test get_thread (raw response)
    raw_thread = get_thread(thread_id=target_thread_id)
    print("PASS: Successfully retrieved raw thread.")
    assert "messages" in raw_thread, "Raw thread missing 'messages' field."
    assert "id" in raw_thread, "Raw thread missing 'id' field."

    # Test build_thread (structured response)
    built = build_thread(raw_thread)
    print("PASS: Successfully built structured thread.")

    print(f"\nThread details:")
    print(f"Thread ID: {built['thread_id']}")
    print(f"Subject: {built['subject']}")
    print(f"Message Count: {built['message_count']}")
    
    # Confirm chronological order sorting by checking internalDates
    raw_messages = raw_thread.get("messages", [])
    timestamps = [int(m.get("internalDate", 0)) for m in raw_messages]
    sorted_timestamps = sorted(timestamps)
    
    # Check if the messages in 'built' are in sorted chronological order
    built_message_ids = [m["message_id"] for m in built["messages"]]
    raw_msg_map = {m["id"]: int(m.get("internalDate", 0)) for m in raw_messages}
    built_timestamps = [raw_msg_map[mid] for mid in built_message_ids if mid in raw_msg_map]
    
    assert built_timestamps == sorted(built_timestamps), "Messages are not sorted chronologically."
    print("PASS: Messages successfully verified in chronological order.")

    for index, message in enumerate(
        built["messages"],
        start=1,
    ):
        print(f"\n  Message {index}:")
        print(f"    From: {message['sender']}")
        print(f"    To: {message['recipient']}")
        print(f"    Date: {message['date']}")
        print(f"    Body preview: {message['body'][:150]}...")


if __name__ == "__main__":
    main()
