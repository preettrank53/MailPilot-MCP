import streamlit as st

from gmail_service import get_email, search_emails


st.set_page_config(
    page_title="MailPilot MCP",
    page_icon="📧",
    layout="centered",
)

if "selected_email" not in st.session_state:
    st.session_state.selected_email = None

if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "search_completed" not in st.session_state:
    st.session_state.search_completed = False


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

            st.session_state.search_results = emails
            st.session_state.selected_email = None
            st.session_state.search_completed = True

        except ValueError as error:
            st.warning(str(error))

        except RuntimeError as error:
            st.error(str(error))

        except Exception:
            st.error(
                "An unexpected error occurred while searching Gmail."
            )


emails = st.session_state.search_results

if emails:
    st.success(
        f"Found {len(emails)} matching emails."
    )

    for index, email in enumerate(emails, start=1):
        title = f"{index}. {email['subject']}"

        with st.expander(title):
            st.write(f"**From:** {email['sender']}")
            st.write(f"**Date:** {email['date']}")
            st.caption(f"Message ID: {email['id']}")

            if st.button(
                "Read email",
                key=f"read_{email['id']}",
            ):
                try:
                    with st.spinner("Loading email..."):
                        st.session_state.selected_email = get_email(
                            email["id"]
                        )

                except ValueError as error:
                    st.warning(str(error))

                except RuntimeError as error:
                    st.error(str(error))

                except Exception:
                    st.error(
                        "An unexpected error occurred while loading the email."
                    )

elif st.session_state.search_completed:
    st.info("No matching emails were found.")


selected_email = st.session_state.selected_email

if selected_email:
    st.divider()
    st.subheader(selected_email["subject"])

    st.write(f"**From:** {selected_email['sender']}")
    st.write(f"**To:** {selected_email['recipient']}")
    st.write(f"**Date:** {selected_email['date']}")

    st.markdown("### Email body")
    st.text(selected_email["body"])

    if st.button("Close email"):
        st.session_state.selected_email = None
        st.rerun()
