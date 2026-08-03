from ai_service import generate_text


def main() -> None:
    prompt = (
        "Explain the Model Context Protocol in exactly two "
        "simple sentences."
    )

    response = generate_text(prompt)

    print("Groq response:")
    print("-" * 50)
    print(response)
    print("-" * 50)




if __name__ == "__main__":
    main()
