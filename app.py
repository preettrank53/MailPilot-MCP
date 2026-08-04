import asyncio
import os
from typing import Any

import streamlit as st

from ai_service import run_iterative_gmail_agent


st.set_page_config(
    page_title="MailPilot MCP",
    page_icon="📧",
    layout="centered",
)


def load_hosted_secrets() -> None:
    """Expose hosted Streamlit secrets as process environment values."""

    secret_names = (
        "GROQ_API_KEY",
        "GROQ_MODEL",
    )

    for secret_name in secret_names:
        if secret_name in st.secrets:
            os.environ[secret_name] = str(
                st.secrets[secret_name]
            )


load_hosted_secrets()


def require_gmail_connection() -> None:
    """Stop the app until the user connects a Google account."""

    if not st.runtime.exists():
        return

    try:
        if st.user.is_logged_in:
            return
    except (AttributeError, KeyError):
        return

    st.title("MailPilot MCP")
    st.caption("AI-powered Gmail assistant")

    st.write(
        "Connect your Gmail account to search and summarize "
        "your emails."
    )

    if st.button(
        "Connect Gmail",
        type="primary",
        use_container_width=False,
    ):
        st.login()

    st.stop()


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


require_gmail_connection()

if st.runtime.exists():
    access_token = st.user.tokens.get("access")
    if not access_token:
        st.error(
            "Google did not return a Gmail access token. "
            "Disconnect Gmail and authorize again."
        )
        st.stop()

initialize_session_state()

st.title("MailPilot MCP")
st.caption(
    "AI-powered Gmail assistant using Groq and MCP"
)

# Minimal horizontal control bar instead of a sidebar
col1, col2, col3 = st.columns([2, 1, 1])
user_email = getattr(st.user, "email", "")

with col1:
    if user_email:
        st.caption(f"Connected: **{user_email}**")

with col2:
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_tool_history = []
        st.rerun()

with col3:
    if st.button("Disconnect", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_tool_history = []
        st.logout()

st.divider()


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
                        access_token=st.user.tokens.get("access"),
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
