# AI-First CRM — HCP Module (LogInteractionScreen)

An AI-powered CRM system for pharmaceutical field representatives to log and manage interactions with Healthcare Professionals (HCPs). Built with **LangGraph**, **Groq LLM (gemma2-9b-it)**, **FastAPI**, and **React + Redux**.

---

## 🏗️ Architecture

```
┌──────────────────┐         ┌──────────────────────────────────────┐
│   React + Redux  │◄──────► │           FastAPI Backend            │
│   Frontend       │  REST   │                                      │
│                  │         │  ┌──────────────────────────────┐    │
│  ┌────────────┐  │         │  │   LangGraph Agent (ReAct)    │    │
│  │ Form Mode  │  │         │  │                              │    │
│  └────────────┘  │         │  │  ┌── log_interaction ───┐    │    │
│  ┌────────────┐  │         │  │  ├── edit_interaction ──┤    │    │
│  │ Chat Mode  │──┼─────────┼──┤  ├── search_hcp ───────┤    │    │
│  └────────────┘  │         │  │  ├── get_history ───────┤    │    │
│                  │         │  │  ├── suggest_followup ──┤    │    │
│  Redux Store:    │         │  │  └── get_product_info ──┘    │    │
│  - hcpSlice      │         │  │         │                    │    │
│  - interactionS. │         │  │    Groq LLM (gemma2-9b-it)  │    │
│  - chatSlice     │         │  └──────────────────────────────┘    │
│                  │         │           │                          │
└──────────────────┘         │  ┌────────▼─────────┐               │
                             │  │  SQLite / Postgres │               │
                             │  └──────────────────┘               │
                             └──────────────────────────────────────┘
```

---

## ✨ Features

### LogInteractionScreen (Dual Mode)
- **📋 Structured Form**: Traditional form with dropdowns for interaction type, product chips, sentiment selector, and text areas for notes and follow-ups.
- **💬 AI Chat Assistant**: Conversational interface powered by LangGraph + Groq. Describe your meeting in natural language — the AI extracts structured data and logs it automatically.

### LangGraph AI Agent — 6 Tools
| # | Tool | Description |
|---|------|-------------|
| 1 | **`log_interaction`** | Logs a new interaction. Captures structured data from natural language. LLM generates summaries and extracts entities. |
| 2 | **`edit_interaction`** | Modifies previously logged interactions. Only specified fields are updated. |
| 3 | **`search_hcp`** | Finds HCPs by name, specialty, or institution. |
| 4 | **`get_interaction_history`** | Retrieves recent interaction history for an HCP. |
| 5 | **`suggest_follow_up`** | AI-powered follow-up recommendations based on history and sentiment trends. |
| 6 | **`get_product_info`** | Looks up pharmaceutical products in the portfolio. |

### Tech Stack
| Layer | Technology |
|-------|-----------|
| Frontend | React.js + Redux Toolkit + Vite |
| Backend | Python + FastAPI |
| AI Agent | LangGraph (StateGraph, ReAct pattern) |
| LLM | Groq — `gemma2-9b-it` |
| Database | SQLite (dev) / PostgreSQL (prod-ready) |
| Font | Google Inter |

---

## 📁 Project Structure

```
crm-hcp-module/
├── backend/
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # SQLAlchemy DB config
│   ├── models.py               # ORM models (HCP, Product, Interaction)
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── crud.py                 # CRUD operations
│   ├── seed.py                 # Sample data seeder
│   ├── agent/
│   │   ├── __init__.py
│   │   ├── state.py            # LangGraph AgentState definition
│   │   ├── tools.py            # 6 LangGraph tools
│   │   └── graph.py            # LangGraph StateGraph + Groq LLM
│   ├── routers/
│   │   ├── hcps.py             # /api/hcps endpoints
│   │   ├── interactions.py     # /api/interactions endpoints
│   │   └── agent_chat.py       # /api/agent/chat endpoint
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── src/
│   │   ├── main.jsx            # React + Redux entry
│   │   ├── App.jsx             # App root
│   │   ├── index.css           # Design system (Inter font)
│   │   ├── store/
│   │   │   ├── store.js        # Redux store
│   │   │   ├── hcpSlice.js     # HCP state
│   │   │   ├── interactionSlice.js
│   │   │   └── chatSlice.js    # AI chat state
│   │   ├── components/
│   │   │   ├── HCPSelector.jsx
│   │   │   ├── StructuredForm.jsx
│   │   │   ├── ChatInterface.jsx
│   │   │   └── InteractionHistory.jsx
│   │   ├── pages/
│   │   │   └── LogInteractionScreen.jsx
│   │   └── services/
│   │       └── api.js          # Axios API client
│   └── index.html
└── README.md
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- A Groq API key ([Get one free](https://console.groq.com/keys))

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure API key
# Edit .env and set your GROQ_API_KEY

# Run the server
uvicorn main:app --reload --port 8000
```

The API starts at **http://localhost:8000**
- Swagger docs: **http://localhost:8000/docs**
- Health check: **http://localhost:8000/api/health**

### 2. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The frontend starts at **http://localhost:5173**

---

## 🔑 Environment Variables

Create `backend/.env`:
```
GROQ_API_KEY=gsk_your_key_here
GROQ_MODEL=gemma2-9b-it
DATABASE_URL=sqlite:///./crm_hcp.db
FRONTEND_URL=http://localhost:5173
```

---

## 📚 API Endpoints

### HCPs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/hcps/` | List all HCPs (with search) |
| GET | `/api/hcps/{id}` | Get HCP by ID |
| POST | `/api/hcps/` | Create HCP |

### Interactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/interactions/` | List interactions (filter by hcp_id) |
| POST | `/api/interactions/` | Log new interaction |
| PUT | `/api/interactions/{id}` | Edit interaction |
| DELETE | `/api/interactions/{id}` | Delete interaction |

### AI Agent
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/agent/chat` | Conversational AI interface |

### Products
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/products` | List pharmaceutical products |

---

## 🗄️ Database Schema

### HCP (Healthcare Professional)
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| first_name | String | First name |
| last_name | String | Last name |
| specialty | String | Medical specialty |
| institution | String | Hospital/clinic |
| tier | String | Priority tier (A/B/C) |
| city, state | String | Location |

### Interaction
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| hcp_id | FK → HCP | Associated doctor |
| interaction_type | String | Detail Aid, Virtual Meeting, etc. |
| products_discussed | String | Comma-separated product names |
| key_topics | Text | Discussion topics |
| hcp_feedback | Text | Doctor's feedback |
| sentiment | String | Positive / Neutral / Negative |
| follow_up_actions | Text | Next steps |
| ai_summary | Text | LLM-generated summary |

### Product
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Product name |
| therapeutic_area | String | e.g., Cardiovascular |

---

## 🤖 LangGraph Agent Details

The agent uses a **ReAct (Reason + Act)** pattern implemented with LangGraph's `StateGraph`:

1. **User sends message** → `/api/agent/chat`
2. **LLM (gemma2-9b-it)** analyzes the message and decides which tool(s) to call
3. **ToolNode** executes the selected tool(s) against the database
4. **LLM generates final response** with confirmation and structured data
5. **Response returned** to the frontend chat interface

The `tools_condition` in LangGraph handles the decision loop — if the LLM response contains tool calls, they are executed; otherwise, the final response is returned to the user.

---

## 📄 License

MIT
