# MailPilot MCP

MailPilot MCP is an AI-powered Gmail assistant built using Python, Streamlit, Gmail API, OAuth 2.0, and Model Context Protocol.

## Current status

- Project structure created
- Streamlit interface running
- Gmail OAuth 2.0 authentication flow completed
- Connected to Gmail API and successfully listing recent email subjects
- Gmail search functionality added supporting advanced query syntax (e.g. `is:unread`, `from:sender`, `newer_than:7d`)
- Email body extraction functionality implemented with recursive MIME traversal and Base64URL decoding
- Integrated Gmail search with Streamlit frontend displaying structured results with collapsible detail expanders
- Added detailed email viewing within the Streamlit UI, persisting state using Streamlit Session State across script reruns
- Created a basic Model Context Protocol (MCP) server exposing the Gmail search functionality as an MCP tool