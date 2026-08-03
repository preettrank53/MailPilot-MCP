# MailPilot MCP

MailPilot MCP is an AI-powered Gmail assistant built using Python, Streamlit, Gmail API, OAuth 2.0, and Model Context Protocol.

## Project Structure

```text
MailPilot-MCP/
├── app.py                  # Streamlit interface
├── auth.py                 # Gmail OAuth 2.0 flow helper
├── gmail_service.py        # Gmail API service and search layer
├── mcp_server.py           # Model Context Protocol (MCP) server
├── requirements.txt        # Pinned dependencies
├── README.md               # Project documentation
├── .gitignore              # Files/folders ignored by Git
├── credentials.json        # Google OAuth credentials (ignored)
├── token.json              # Cached OAuth tokens (ignored)
└── tests/                  # Verification and test suite
    ├── __init__.py
    ├── test_auth.py
    ├── test_gmail_service.py
    ├── test_search_emails.py
    ├── test_get_email.py
    ├── test_mcp_tool.py
    └── test_mcp_client.py
```

## Running Tests

All verification and protocol tests have been consolidated in the `tests/` directory. You can run them as modules from the project root:

```powershell
# Test authentication flow
.venv\Scripts\python -m tests.test_auth

# Test basic Gmail service and email listing
.venv\Scripts\python -m tests.test_gmail_service

# Test search query functionality
.venv\Scripts\python -m tests.test_search_emails

# Test email body fetching and parsing
.venv\Scripts\python -m tests.test_get_email

# Test the MCP tool directly in Python
.venv\Scripts\python -m tests.test_mcp_tool

# Test the MCP server and tool over stdio transport using the MCP client
.venv\Scripts\python -m tests.test_mcp_client
```

## Current status

- Project structure created and organized cleanly
- Streamlit interface running
- Gmail OAuth 2.0 authentication flow completed
- Connected to Gmail API and successfully listing recent email subjects
- Gmail search functionality added supporting advanced query syntax (e.g. `is:unread`, `from:sender`, `newer_than:7d`)
- Email body extraction functionality implemented with recursive MIME traversal and Base64URL decoding
- Integrated Gmail search with Streamlit frontend displaying structured results with collapsible detail expanders
- Added detailed email viewing within the Streamlit UI, persisting state using Streamlit Session State across script reruns
- Created a basic Model Context Protocol (MCP) server exposing the Gmail search functionality as an MCP tool
- Implemented an MCP client that starts the server as a subprocess and tests tool discovery and execution over the stdio transport