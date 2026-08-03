import asyncio
from typing import Any

import streamlit as st

from ai_service import run_iterative_gmail_agent


st.set_page_config(
    page_title="MailPilot MCP",
    page_icon="📧",
    layout="centered",
)


def initialize_session_state() -> None:
    """Initialize values that must survive Streamlit reruns."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_tool_history" not in st.session_state:
        st.session_state.last_tool_history = []


def display_tool_history(
    tool_history: list[dict[str, Any]],
) -> None:
    """Display MCP tool activity in a compact expander."""

    if not tool_history:
        return

    with st.expander(
        f"Tool activity ({len(tool_history)} call(s))"
    ):
        for index, tool_call in enumerate(
            tool_history,
            start=1,
        ):
            st.markdown(
                f"**{index}. `{tool_call['tool_name']}`**"
            )

            st.json(
                tool_call["arguments"]
            )


initialize_session_state()

st.title("MailPilot MCP")
st.caption(
    "AI-powered Gmail assistant using Groq and MCP"
)

with st.sidebar:
    st.subheader("Example prompts")

    st.code(
        "Show my five unread emails.",
        language=None,
    )

    st.code(
        "Summarize my newest unread email.",
        language=None,
    )

    st.code(
        "Find my latest email from Medium.",
        language=None,
    )

    st.warning(
        "Email data returned by Gmail tools is sent to the "
        "configured AI provider for generating the answer."
    )

    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.last_tool_history = []
        st.rerun()


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if message.get("tool_history"):
            display_tool_history(
                message["tool_history"]
            )


prompt = st.chat_input(
    "Ask something about your Gmail inbox"
)

if prompt:
    conversation_history = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in st.session_state.messages
        if message.get("role") in {"user", "assistant"}
        and message.get("content")
    ]

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            with st.spinner(
                "MailPilot is checking your Gmail..."
            ):
                result = asyncio.run(
                    run_iterative_gmail_agent(
                        user_request=prompt,
                        conversation_history=conversation_history,
                    )
                )

            answer = result["answer"]
            tool_history = result["tool_history"]

            st.markdown(answer)
            display_tool_history(tool_history)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "tool_history": tool_history,
            }
        )

        st.session_state.last_tool_history = (
            tool_history
        )

    except ValueError as error:
        with st.chat_message("assistant"):
            st.warning(str(error))

    except RuntimeError as error:
        with st.chat_message("assistant"):
            st.error(str(error))

    except Exception:
        with st.chat_message("assistant"):
            st.error(
                "An unexpected error occurred while processing "
                "your request."
            )
