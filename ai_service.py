import json
import os
from typing import Any

from dotenv import load_dotenv
from groq import Groq

from mcp_client import list_mcp_tools


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


def convert_mcp_tools_to_groq(
    mcp_tools: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Convert MCP tool definitions into Groq function tools."""

    groq_tools: list[dict[str, Any]] = []

    for tool in mcp_tools:
        groq_tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"],
                },
            }
        )

    return groq_tools


async def select_gmail_tool(
    user_request: str,
) -> dict[str, Any]:
    """Ask Groq to select an appropriate Gmail MCP tool."""

    cleaned_request = user_request.strip()

    if not cleaned_request:
        raise ValueError("user_request cannot be empty.")

    mcp_tools = await list_mcp_tools()
    groq_tools = convert_mcp_tools_to_groq(mcp_tools)

    client = get_groq_client()
    model_name = get_model_name()

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an email assistant. "
                    "Use the available Gmail tools when the user asks "
                    "to search, find, list, or read Gmail messages. "
                    "Do not invent message IDs."
                ),
            },
            {
                "role": "user",
                "content": cleaned_request,
            },
        ],
        tools=groq_tools,
        tool_choice="auto",
        temperature=0,
    )

    message = response.choices[0].message

    if not message.tool_calls:
        return {
            "type": "text",
            "content": message.content or "",
        }

    tool_call = message.tool_calls[0]

    try:
        arguments = json.loads(
            tool_call.function.arguments
        )
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "Groq returned invalid tool arguments."
        ) from error

    return {
        "type": "tool_call",
        "tool_call_id": tool_call.id,
        "tool_name": tool_call.function.name,
        "arguments": arguments,
    }
