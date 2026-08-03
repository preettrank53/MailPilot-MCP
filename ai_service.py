import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def get_groq_client() -> Groq:
    """Create a Groq client using the configured API key."""

    api_key = os.getenv("GROQ_API_KEY", "").strip()

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    return Groq(api_key=api_key)


def get_model_name() -> str:
    """Return the configured Groq model name."""

    model_name = os.getenv("GROQ_MODEL", "").strip()

    if not model_name:
        raise RuntimeError(
            "GROQ_MODEL is not configured."
        )

    return model_name


def generate_text(prompt: str) -> str:
    """Generate a text response using Groq."""

    cleaned_prompt = prompt.strip()

    if not cleaned_prompt:
        raise ValueError("prompt cannot be empty.")

    client = get_groq_client()
    model_name = get_model_name()

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": cleaned_prompt,
            }
        ],
        model=model_name,
    )

    response_text = chat_completion.choices[0].message.content

    if not response_text:
        raise RuntimeError(
            "Groq returned no text response."
        )

    return response_text.strip()
