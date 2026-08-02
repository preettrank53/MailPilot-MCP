from auth import authenticate_gmail


def main() -> None:
    credentials = authenticate_gmail()

    if credentials.valid:
        print("Gmail authentication completed successfully.")
    else:
        print("Gmail authentication failed.")


if __name__ == "__main__":
    main()
