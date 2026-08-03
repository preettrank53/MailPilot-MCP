# MailPilot MCP

MailPilot MCP is an AI-powered Gmail assistant built using Python, Streamlit, Gmail API, OAuth 2.0, and Model Context Protocol.

## Project Structure

```text
MailPilot-MCP/
├── ai_service.py           # Groq API LLM assistant integration
├── app.py                  # Streamlit interface
├── auth.py                 # Gmail OAuth 2.0 flow helper
├── gmail_service.py        # Gmail API service and search layer
├── mcp_client.py           # Reusable Model Context Protocol (MCP) client module
├── mcp_server.py           # Model Context Protocol (MCP) server
├── requirements.txt        # Pinned dependencies
├── README.md               # Project documentation
├── .gitignore              # Files/folders ignored by Git
├── credentials.json        # Google OAuth credentials (ignored)
├── token.json              # Cached OAuth tokens (ignored)
└── tests/                  # Verification and test suite
    ├── __init__.py
    ├── test_ai_service.py
    ├── test_auth.py
    ├── test_gmail_service.py
    ├── test_search_emails.py
    ├── test_get_email.py
    ├── test_mcp_tool.py
    ├── test_mcp_client.py
    ├── test_tool_selection.py  # Verifies model tool selection and routing decisions
    ├── test_gmail_agent.py     # Verifies the complete single-tool agent loop
    ├── test_iterative_agent.py # Verifies the multi-step reasoning agent loop
    ├── test_app_import.py      # Verifies Streamlit app imports
    └── test_conversation_memory.py # Verifies conversation memory and follow-up contexts
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

# Test the Groq text generation AI service
.venv\Scripts\python -m tests.test_ai_service

# Test the model's tool selection and arguments generation
.venv\Scripts\python -m tests.test_tool_selection

# Test the complete single-tool Gmail agent workflow
.venv\Scripts\python -m tests.test_gmail_agent

# Test the multi-step iterative AI agent reasoning loop
.venv\Scripts\python -m tests.test_iterative_agent

# Run syntax/import test on the Streamlit app
.venv\Scripts\python -m tests.test_app_import

# Test conversation memory and follow-up context resolution
.venv\Scripts\python -m tests.test_conversation_memory
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
- Added the `get_gmail_email` tool to retrieve full email body details by message ID, establishing a clean separation between search and retrieval (lazy loading)
- Extracted and encapsulated the low-level MCP transport and connection details into a reusable `mcp_client.py` module
- Integrated Groq API for text generation using the official SDK, loading credentials and model config from `.env` (fully git-ignored)
- Upgraded Groq model to `openai/gpt-oss-20b` and implemented dynamic model-side tool selection and routing without execution
- Built the complete single-tool agent loop executing Groq-selected tools dynamically through the MCP client and generating grounded answers
- Built a multi-step iterative AI agent Reasoning Loop (`run_iterative_gmail_agent`) allowing complex, sequential tool execution (e.g. `search_gmail` -> `get_gmail_email` -> grounded final answer) while enforcing a loop execution limit of 5 calls to prevent infinite loops.
- Connected the multi-step iterative Gmail agent to a Streamlit Chat interface, replacing the manual search panels with a conversational workspace, exposing tool traces, and preserving conversation logs across runs.
- Implemented short-term conversational memory within the iterative Gmail agent, allowing the model to resolve contextual follow-ups (such as "it" or "the previous email") using a validated, token-optimized message window.