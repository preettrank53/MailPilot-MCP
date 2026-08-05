# MailPilot MCP

AI-Powered Gmail Assistant - Built with Model Context Protocol (MCP), Streamlit & Groq

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mailpilot-mcp.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.60-red) ![MCP](https://img.shields.io/badge/MCP-Standard-orange) ![Deployed](https://img.shields.io/badge/Deployed-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-yellow)

## [Live Demo : mailpilot-mcp.streamlit.app](https://mailpilot-mcp.streamlit.app)

MailPilot is an intelligent, multi-user AI-powered email assistant designed to streamline your Gmail inbox management. Leveraging advanced large language models via Groq and the Model Context Protocol (MCP), it automates search, conversation tracking, and email summarization using natural language. MailPilot features a secure, multitenant architecture that dynamically routes and isolates user credentials, ensuring absolute data privacy and zero API leakage during processing.

## Key Features
* **Natural Language Chat Interface**: Retrieve, filter, and summarize emails by chatting naturally (e.g. *"Summarize my newest unread email"*).
* **Multi-Turn Conversational Memory**: Seamlessly understand follow-up contexts (e.g. *"Now read it and write a summary"*).
* **Conversational Thread Search**: Group and search complete email threads (`search_gmail_threads`) to inspect participants, message count, and snippets without fetching heavy body contents prematurely.
* **Lazy Email Payload Retrieval**: Search results return lightweight metadata; full email bodies (`get_gmail_email`) are fetched only when the reasoning agent explicitly decides to read them.
* **Decoupled Token Security**: Propagates Google OAuth access tokens privately to the MCP subprocess environment (`MAILPILOT_GMAIL_ACCESS_TOKEN`), keeping credentials hidden from LLM schemas, prompt histories, and tool traces.
* **Autonomous ReAct Reasoning Loop**: Coordinates successive tool planning and execution dynamically, capped at 5 tool calls to prevent infinite loops.
* **Visual Tool Activity Traces**: Collapsible UI expanders show exact tool calls, arguments, and responses behind the LLM's answers.

## Architecture

MailPilot leverages a decoupled model-client-server architecture. The Streamlit front-end authenticates the user, obtains a short-lived access token, and launches a reasoning loop. When the LLM decides to call a tool, the MCP Client spawns the MCP Server as an isolated child process, passing the access token privately through the process environment variables to run queries directly against the Gmail API.

```
Connected Streamlit User (OAuth) → st.user.tokens
                                        ↓
                            ┌──────────────────────┐
                            │    Agent ReAct Loop  │
                            │                      │
                            │  Groq (Llama 3.3)    │
                            └──────────────────────┘
                                        ↓
                            ┌──────────────────────┐
                            │    MCP Stdio Client  │ (Injects Token to Subprocess Env)
                            └──────────────────────┘
                                        ↓ (Subprocess stdio)
                            ┌──────────────────────┐
                            │    MCP Stdio Server  │ (Extracts Token from Env)
                            └──────────────────────┘
                                        ↓
                            ┌──────────────────────┐
                            │  Gmail Service Layer │ (Dynamic Credential Builder)
                            └──────────────────────┘
                                        ↓
                                    Gmail API
```

## Tech Stack

| Category | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| Agent Framework | Model Context Protocol (MCP) | 1.29.0 | Decoupled tool discovery and stdio-based execution |
| LLM Provider | Groq SDK | 1.6.0 | Fast, high-quality reasoning using Llama 3.3-70b-versatile |
| Web Interface | Streamlit | 1.60.0 | Chat dashboard interface and horizontal session control bar |
| Authentication | Streamlit Auth (Authlib) | 1.7.2 | Dynamic OIDC Google Login and Gmail read-only token acquisition |
| API Integration | Google API Python Client | 2.198.0 | Workspace Gmail REST API endpoints interaction |

## Getting Started

### Prerequisites
* Python 3.11+
* [Groq API Key](https://console.groq.com/keys)
* [Google Cloud Console Project](https://console.cloud.google.com/) with Gmail API enabled and OAuth client IDs generated.

### Local Installation
1. Clone the repository
2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\activate
   ```
3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and fill in:
   ```env
   GROQ_API_KEY=your-groq-key-here
   GROQ_MODEL=llama-3.3-70b-versatile
   ```
5. To test locally with Desktop OAuth credentials, place your downloaded client secrets file in the project root as `credentials.json` and start Streamlit:
   ```powershell
   streamlit run app.py
   ```

### Environment Variables

| Variable | Required | Source |
| :--- | :--- | :--- |
| `GROQ_API_KEY` | Yes | [Groq Console](https://console.groq.com/keys) |
| `GROQ_MODEL` | Yes | `llama-3.3-70b-versatile` |

---

## How to Use MailPilot

1. **Step 1 — Connect your Gmail Account**: Click **Connect Gmail** on the launch screen to authenticate and authorize read-only access.
2. **Step 2 — Search and Query**: Type commands into the chat input, such as *"Show me my latest unread emails from GitHub"* or *"Summarize the conversation with Medium"*.
3. **Step 3 — Inspect Tool Activity**: Expand the **Tool activity** block beneath the assistant's answer to view the sequence of tool calls executed by the agent.
4. **Step 4 — Disconnect**: Cleanly terminate your session and revoke active browser tokens by clicking **Disconnect** in the top control bar.

---

## Project Structure

```
MailPilot-MCP/
├── .streamlit/
│   └── secrets.toml        # Streamlit Web OAuth credentials configuration (ignored)
├── ai_service.py           # Groq API LLM orchestrator and ReAct loop logic
├── app.py                  # Streamlit frontend, control headers, and authentication gates
├── auth.py                 # Gmail Desktop OAuth 2.0 flow helper
├── gmail_service.py        # Gmail API wrappers, thread parsing, and payload decoder
├── mcp_client.py           # Reusable Stdio-based MCP Client and subprocess launcher
├── mcp_server.py           # FastMCP Server exposing Gmail search, retrieval, and threads tools
├── requirements.txt        # Production Python dependencies
├── README.md               # Project documentation
├── .gitignore              # Files/folders ignored by Git
├── credentials.json        # Google Desktop OAuth client secret file (ignored)
├── token.json              # Cached Desktop OAuth access/refresh token (ignored)
└── tests/                  # Automated verification and protocol test suite
    ├── __init__.py
    ├── test_search_threads.py   # Test suite for thread searching and parameter validations
    ├── test_tool_selection.py  # Verifies model tool selection and routing decisions
    ├── test_gmail_agent.py     # Verifies the complete single-tool agent loop
    ├── test_iterative_agent.py # Verifies the multi-step reasoning agent loop
    ├── test_conversation_memory.py # Verifies conversation memory and follow-up contexts
    ├── test_web_access_token.py # Verifies web user access token integration
    └── test_token_propagation.py # Verifies private token propagation to MCP subprocesses
```

---

## Deployment

### Streamlit Community Cloud
1. Push your repository to GitHub.
2. Log in to [Streamlit Share](https://share.streamlit.io/) and deploy your repository from the `main` branch.
3. Configure the following variables under **App settings > Secrets**:

```toml
GROQ_API_KEY = "your-groq-api-key"
GROQ_MODEL = "llama-3.3-70b-versatile"

[auth]
redirect_uri = "https://mailpilot-mcp.streamlit.app/oauth2callback"
cookie_secret = "your-cookie-secret-urlsafe-token"
client_id = "your-google-web-client-id"
client_secret = "your-google-web-client-secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
expose_tokens = ["access"]

[auth.client_kwargs]
scope = "openid profile email https://www.googleapis.com/auth/gmail.readonly"
prompt = "select_account consent"
```

*Ensure that `https://mailpilot-mcp.streamlit.app/oauth2callback` is added to your **Authorized redirect URIs** under your OAuth client ID credentials in the Google Cloud Console.*

---

## Testing

All tests are designed to execute independently using module imports. Run the test suite using:

```powershell
# Test thread searching and metadata parsing
.venv\Scripts\python -m tests.test_search_threads

# Test AI tool-routing and selection
.venv\Scripts\python -m tests.test_tool_selection

# Test ReAct iterative reasoning loop
.venv\Scripts\python -m tests.test_iterative_agent

# Test token propagation to MCP subprocess
.venv\Scripts\python -m tests.test_token_propagation
```

---

## Known Limitations
* Free-tier Groq API keys might experience brief rate limiting when performing rapid multi-step reasoning cycles (resolved by utilizing higher-tiered models like Llama 3.3).
* Streamlit Community Cloud filesystem is ephemeral; local desktop cached files (if any) are not preserved across app restarts.
* The Gmail API scope is configured for read-only access. Email editing, drafting, or sending are not supported out of the box.

## License
MIT License - feel free to use this project as a reference or starting point

⭐ If you found this project useful, please consider starring the repository