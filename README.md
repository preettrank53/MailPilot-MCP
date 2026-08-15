# MailPilot MCP

AI-Powered Gmail Assistant - Built with Model Context Protocol (MCP), Streamlit & Groq

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mailpilot-mcp.streamlit.app)

![Python](https://img.shields.io/badge/Python-3.11+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.60-red) ![MCP](https://img.shields.io/badge/MCP-Standard-orange) ![Deployed](https://img.shields.io/badge/Deployed-Live-brightgreen) ![License](https://img.shields.io/badge/License-MIT-yellow)

## [Live Demo : mailpilot-mcp.streamlit.app](https://mailpilot-mcp.streamlit.app)

MailPilot is an intelligent, multi-user AI-powered email assistant designed to streamline your Gmail inbox management. Leveraging advanced large language models via Groq and the Model Context Protocol (MCP), it automates search, conversation tracking, and email summarization using natural language. MailPilot features a secure, multitenant architecture that dynamically routes and isolates user credentials, ensuring absolute data privacy and zero API leakage during processing.

> [!IMPORTANT]  
> **OAuth Demo Access:** The application currently runs under Google OAuth testing mode. Gmail accounts must be added as authorized test users in the Google Cloud Console before connecting because the project requests sensitive Gmail API permissions. 

---

## Key Features
* **Natural Language Chat Interface**: Retrieve, filter, and summarize emails by chatting naturally (e.g. *"Summarize my newest unread emails"*).
* **Multi-Turn Conversational Memory**: Seamlessly understand follow-up contexts (e.g. *"Now read it and write a summary"*).
* **Safe Human-in-the-Loop Write Actions**: Write operations (like reply drafting) are blocked at the agent level and returned as a `pending_action`. Streamlit renders a Draft Preview allowing the user to review the exact recipient, subject, and body before confirming or cancelling the action.
* **Gmail Draft Generation (`create_gmail_draft`)**: Automatically constructs RFC-compliant `EmailMessage` payloads and securely saves them in the user's Gmail drafts folder via base64url encoding.
* **Conversational Thread Search**: Group and search complete email threads (`search_gmail_threads`) to inspect participants, message count, and snippets without fetching heavy body contents prematurely.
* **Lazy Email Payload Retrieval**: Search results return lightweight metadata; full email bodies (`get_gmail_email`) are fetched only when the reasoning agent explicitly decides to read them.
* **Decoupled Token Security**: Propagates Google OAuth access tokens privately to the MCP subprocess environment (`MAILPILOT_GMAIL_ACCESS_TOKEN`), keeping credentials hidden from LLM schemas, prompt histories, and tool traces.
* **Autonomous ReAct Reasoning Loop**: Coordinates successive tool planning and execution dynamically, capped at 5 tool calls to prevent infinite loops.
* **Resilient Rate-Limit Handling**: Automatically intercepts Groq API rate limit errors (HTTP 429) and performs exponential backoff retries, ensuring smooth agent execution on free-tier keys.
* **Visual Tool Activity Traces**: Collapsible UI expanders show exact tool calls, arguments, and responses behind the LLM's answers.

---

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

---

## Tech Stack

| Category | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| Agent Framework | Model Context Protocol (MCP) | 1.29.0 | Decoupled tool discovery and stdio-based execution |
| LLM Provider | Groq SDK | 1.6.0 | Fast, high-quality reasoning using GPT OSS 120B |
| Web Interface | Streamlit | 1.60.0 | Chat dashboard interface and horizontal session control bar |
| Authentication | Streamlit Auth (Authlib) | 1.7.2 | Dynamic OIDC Google Login and Gmail access/refresh token acquisition |
| API Integration | Google API Python Client | 2.198.0 | Workspace Gmail REST API endpoints interaction |

---

## License
MIT License - feel free to use this project as a reference or starting point

⭐ If you found this project useful, please consider starring the repository