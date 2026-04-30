<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00d4ff,100:7c3aed&height=200&section=header&text=MedAgent%20CRM%20Pro&fontSize=48&fontColor=ffffff&fontAlignY=35&desc=AI-First%20HCP%20Interaction%20Module&descAlignY=55&descSize=20" width="100%"/>

<br/>

[![Live Demo](https://img.shields.io/badge/🚀_Live_Demo-med--agent--crm--pro.vercel.app-00d4ff?style=for-the-badge&logoColor=white)](https://med-agent-crm-pro.vercel.app/)
[![API Docs](https://img.shields.io/badge/📄_API_Docs-Swagger_UI-7c3aed?style=for-the-badge)](https://medagent-crm-pro-production.up.railway.app/docs)
[![Demo GIF](https://img.shields.io/badge/▶_Watch-Demo-10b981?style=for-the-badge)](https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Demo.gif)

<br/>

![React](https://img.shields.io/badge/React_18-20232A?style=flat-square&logo=react&logoColor=61DAFB)
![Redux](https://img.shields.io/badge/Redux_Toolkit-764ABC?style=flat-square&logo=redux&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat-square&logo=fastapi)
![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat-square&logo=langchain&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat-square&logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=flat-square&logo=sqlite&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Railway](https://img.shields.io/badge/Railway-0B0D0E?style=flat-square&logo=railway&logoColor=white)

<br/>

> **Built by — Aditya Kumar**

</div>

---

## 📸 Screenshots

<table>
  <tr>
    <th align="center">📋 Log Interaction Form</th>
    <th align="center">📜 Interaction History</th>
    <th align="center">🤖 AI Follow-up Suggestions</th>
  </tr>
  <tr>
    <td><img src="https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183225.png" width="280"/></td>
    <td><img src="https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183331.png" width="280"/></td>
    <td><img src="https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183446.png" width="280"/></td>
  </tr>
</table>

---

## 🧬 What is MedAgent CRM Pro?

An **AI-first Customer Relationship Management (CRM)** system built for Life Sciences field representatives — to **log, manage, and analyze** interactions with Healthcare Professionals (HCPs).

The **Log Interaction Screen** supports two powerful modes:

| Mode | Description |
|------|-------------|
| 📋 **Structured Form** | Traditional form-based logging with AI-powered follow-up suggestions |
| 🤖 **AI Chat Interface** | Conversational logging via natural language — powered by LangGraph + Groq LLM |

---

## 🧠 Architecture

```
┌─────────────────────────────────────────────────────┐
│                  React Frontend                     │
│   Redux Store ─► InteractionForm / ChatInterface    │
│         └─► axios ─► FastAPI Backend                │
└────────────────────────┬────────────────────────────┘
                         │ HTTP
┌────────────────────────▼────────────────────────────┐
│              FastAPI (Python)                       │
│   /api/interactions  ─►  SQLAlchemy ORM             │
│   /api/chat          ─►  LangGraph Agent            │
│                               │                     │
│              ┌────────────────▼──────────────────┐  │
│              │         LangGraph Agent            │  │
│              │   ┌──────────────────────────┐    │  │
│              │   │    5 Tools via Groq LLM  │    │  │
│              │   │  1. log_interaction      │    │  │
│              │   │  2. edit_interaction     │    │  │
│              │   │  3. get_hcp_history      │    │  │
│              │   │  4. suggest_follow_up    │    │  │
│              │   │  5. analyze_sentiment    │    │  │
│              │   └──────────────────────────┘    │  │
│              └───────────────────────────────────┘  │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│           SQLite (dev) / PostgreSQL (prod)          │
└─────────────────────────────────────────────────────┘
```

---

## 🤖 LangGraph Agent & Tools

The LangGraph agent is an **intelligent orchestrator** that interprets natural language from field reps and routes to the right tool automatically.

<details>
<summary><b>🔧 Tool 1 — <code>log_interaction</code></b></summary>
<br/>

Captures interaction data from natural language or structured input. Uses **Groq `llama-3.3-70b-versatile`** to:
- Extract and summarize key discussion points
- Infer HCP sentiment (Positive / Neutral / Negative)
- Generate a concise AI summary
- Persist all fields to the database

</details>

<details>
<summary><b>✏️ Tool 2 — <code>edit_interaction</code></b></summary>
<br/>

Allows modification of any previously logged interaction by ID. Accepts **partial updates** — only provided fields are changed. Re-generates AI summary if content is updated.

</details>

<details>
<summary><b>📜 Tool 3 — <code>get_hcp_history</code></b></summary>
<br/>

Retrieves the interaction history for any HCP using **fuzzy name matching**. Returns the last N interactions sorted by most recent, giving reps full context before a visit.

</details>

<details>
<summary><b>💡 Tool 4 — <code>suggest_follow_up</code></b></summary>
<br/>

Uses **`llama-3.3-70b-versatile`** to generate **3 specific, actionable follow-up steps** for the field rep based on interaction context. Suggestions can be directly added to the form.

</details>

<details>
<summary><b>🧪 Tool 5 — <code>analyze_sentiment</code></b></summary>
<br/>

Analyzes free-text interaction notes to infer **HCP sentiment** with a confidence score and rationale. Helps reps understand the emotional tone of their last meeting.

</details>

---

## 🗄️ Database Schema

```sql
CREATE TABLE interactions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    hcp_name            VARCHAR(255) NOT NULL,
    interaction_type    VARCHAR(100) NOT NULL,
    date                VARCHAR(50)  NOT NULL,
    time                VARCHAR(50),
    attendees           TEXT,
    topics_discussed    TEXT,
    materials_shared    TEXT,
    samples_distributed TEXT,
    sentiment           VARCHAR(50)  DEFAULT 'Neutral',
    outcomes            TEXT,
    follow_up_actions   TEXT,
    ai_summary          TEXT,
    created_at          DATETIME,
    updated_at          DATETIME
);
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | React 18, Redux Toolkit, Axios |
| **Styling** | Custom CSS, Google Fonts |
| **Backend** | Python 3.12, FastAPI, Uvicorn |
| **AI Agent** | LangGraph 1.1+, LangChain |
| **LLM** | Groq `llama-3.3-70b-versatile` |
| **Database** | SQLite (dev) / PostgreSQL (prod) via SQLAlchemy |
| **Hosting** | Vercel (Frontend) · Railway (Backend) |

---

## 🚀 Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Groq API key → [Get one free here](https://console.groq.com)

### 1️⃣ Clone the repo

```bash
git clone https://github.com/adityakr09/aivoa-crm.git
cd aivoa-crm
```

### 2️⃣ Backend Setup

```bash
cd backend
cp .env.example .env
# Add your GROQ_API_KEY to .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

> Backend runs at `http://localhost:8000` · API Docs at `http://localhost:8000/docs`

### 3️⃣ Frontend Setup

```bash
cd frontend
npm install
npm start
```

> Frontend runs at `http://localhost:3000`

---

## 📁 Project Structure

```
aivoa-crm/
├── backend/
│   ├── main.py              # FastAPI app — REST + /api/chat endpoints
│   ├── agent.py             # LangGraph agent with 5 tools
│   ├── database.py          # SQLAlchemy models + async DB setup
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/
    └── src/
        ├── App.js
        ├── store/
        │   ├── store.js                 # Redux store
        │   ├── interactionsSlice.js     # CRUD state management
        │   └── chatSlice.js             # Chat state management
        └── components/
            ├── LogInteractionScreen.jsx # Main screen with sidebar
            ├── InteractionForm.jsx      # Structured form
            ├── ChatInterface.jsx        # AI chat interface
            └── InteractionsList.jsx     # Interactions panel with edit/delete
```

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/interactions` | List all interactions |
| `POST` | `/api/interactions` | Create new interaction |
| `PUT` | `/api/interactions/{id}` | Update existing interaction |
| `DELETE` | `/api/interactions/{id}` | Delete interaction |
| `POST` | `/api/chat` | Chat with AI agent |
| `GET` | `/api/hcps` | List unique HCP names |

---

## 🎥 Demo Walkthrough

> The video walkthrough covers:
> 1. Logging an interaction via structured form
> 2. AI Chat logging via natural language
> 3. All 5 LangGraph tools in action
> 4. Edit and delete interactions
> 5. AI-powered follow-up suggestions

---

## 📝 Notes

> [!NOTE]
> Database defaults to **SQLite** for development. Set `DATABASE_URL=postgresql+asyncpg://...` in `.env` for production.

> [!IMPORTANT]
> All AI features require a valid **`GROQ_API_KEY`** in `.env`.

> [!WARNING]
> CORS is open (`*`) for development — **restrict in production**.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,100:00d4ff&height=120&section=footer" width="100%"/>

**Made with ❤️ by Aditya Kumar**

</div>
