import streamlit as st

from gmail_service import search_emails


st.set_page_config(
    page_title="MailPilot MCP",
    page_icon="📧",
    layout="centered",
)

st.title("MailPilot MCP")
st.subheader("Search your Gmail inbox")

st.write(
    "Enter a Gmail search query to find matching emails."
)

query = st.text_input(
    "Gmail search query",
    placeholder="Example: is:unread newer_than:7d",
)

max_results = st.number_input(
    "Maximum results",
    min_value=1,
    max_value=20,
    value=5,
    step=1,
)

search_button = st.button(
    "Search emails",
    type="primary",
)

if search_button:
    if not query.strip():
        st.warning("Enter a Gmail search query.")

    else:
        try:
            with st.spinner("Searching Gmail..."):
                emails = search_emails(
                    query=query,
                    max_results=int(max_results),
                )

            if not emails:
                st.info("No matching emails were found.")

            else:
                st.success(
                    f"Found {len(emails)} matching emails."
                )

                for index, email in enumerate(emails, start=1):
                    title = (
                        f"{index}. "
                        f"{email['subject']}"
                    )

                    with st.expander(title):
                        st.write(
                            f"**From:** {email['sender']}"
                        )
                        st.write(
                            f"**Date:** {email['date']}"
                        )
                        st.caption(
                            f"Message ID: {email['id']}"
                        )

        except ValueError as error:
            st.warning(str(error))

        except RuntimeError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "An unexpected error occurred while searching Gmail."
            )
