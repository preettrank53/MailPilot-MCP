import streamlit as st


st.set_page_config(
    page_title="MailPilot MCP",
    page_icon="📧",
    layout="centered",
)

st.title("MailPilot MCP")
st.subheader("AI-powered Gmail assistant")

st.info("Project setup completed successfully.")

user_input = st.text_input(
    "Ask something about your Gmail inbox",
    placeholder="Example: Show my latest unread emails",
)

if st.button("Submit"):
    if user_input.strip():
        st.success(f"You entered: {user_input}")
    else:
        st.warning("Please enter a message.")
