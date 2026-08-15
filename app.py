import asyncio
import os
from typing import Any

import streamlit as st

from ai_service import run_iterative_gmail_agent
from mcp_client import call_mcp_tool


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

    if "pending_action" not in st.session_state:
        st.session_state.pending_action = None


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


def display_pending_draft(
    pending_action: dict[str, Any],
) -> None:
    """Display a pending Gmail draft for user approval."""

    if (
        not pending_action
        or pending_action.get("tool_name")
        != "create_gmail_draft"
    ):
        return

    arguments = pending_action.get(
        "arguments",
        {},
    )

    to = arguments.get("to", "")
    subject = arguments.get("subject", "")
    body = arguments.get("body", "")

    st.divider()
    st.subheader("Draft preview")

    st.write(f"**To:** {to}")
    st.write(f"**Subject:** {subject}")

    st.text_area(
        "Body",
        value=body,
        height=220,
        disabled=True,
        key="pending_draft_body_preview",
    )

    confirm_column, cancel_column = st.columns(2)

    with confirm_column:
        create_clicked = st.button(
            "Create Draft",
            type="primary",
            use_container_width=True,
        )

    with cancel_column:
        cancel_clicked = st.button(
            "Cancel",
            use_container_width=True,
        )

    if create_clicked:
        try:
            access_token = st.user.tokens.get(
                "access"
            )

            if not access_token:
                st.error(
                    "Your Gmail session has expired. "
                    "Reconnect Gmail and try again."
                )
                return

            with st.spinner(
                "Creating Gmail draft..."
            ):
                result = asyncio.run(
                    call_mcp_tool(
                        tool_name="create_gmail_draft",
                        arguments={
                            "to": to,
                            "subject": subject,
                            "body": body,
                        },
                        access_token=access_token,
                    )
                )

            st.session_state.pending_action = None

            st.success(
                "Draft created successfully in Gmail."
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": (
                        "Draft created successfully in Gmail. "
                        "It has not been sent."
                    ),
                }
            )

            st.rerun()

        except RuntimeError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "An unexpected error occurred while "
                "creating the Gmail draft."
            )

    if cancel_clicked:
        st.session_state.pending_action = None

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "Draft creation cancelled. "
                    "No Gmail draft was created."
                ),
            }
        )

        st.rerun()


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
        st.session_state.pending_action = None
        st.rerun()

with col3:
    if st.button("Disconnect", use_container_width=True):
        st.session_state.messages = []
        st.session_state.last_tool_history = []
        st.session_state.pending_action = None
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
            with st.status("MailPilot is checking your Gmail...", expanded=True) as status:
                def update_status(message: str) -> None:
                    st.write(f"✓ {message}")

                result = asyncio.run(
                    run_iterative_gmail_agent(
                        user_request=prompt,
                        conversation_history=conversation_history,
                        access_token=st.user.tokens.get("access"),
                        on_step_callback=update_status,
                    )
                )
                status.update(label="MailPilot finished checking Gmail.", state="complete", expanded=False)

            answer = result["answer"]
            tool_history = result["tool_history"]
            pending_action = result.get("pending_action")

            st.session_state.pending_action = pending_action

            if pending_action:
                st.info(
                    "I prepared a Gmail draft. Review it below before creating it."
                )
            elif answer:
                st.markdown(answer)

            display_tool_history(tool_history)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": (
                    "I prepared a Gmail draft. Review it below before creating it."
                    if pending_action
                    else answer
                ),
                "tool_history": tool_history,
            }
        )

        st.session_state.last_tool_history = (
            tool_history
        )
        st.rerun()

    except ValueError as error:
        with st.chat_message("assistant"):
            st.warning(str(error))

    except RuntimeError as error:
        with st.chat_message("assistant"):
            st.error(str(error))

    except Exception as error:
        with st.chat_message("assistant"):
            st.error(
                f"An unexpected error occurred while processing your request: {str(error)}"
            )
            import traceback
            st.code(traceback.format_exc(), language="python")


if st.session_state.pending_action:
    display_pending_draft(
        st.session_state.pending_action
    )
