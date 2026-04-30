
```markdown
# <img src="[https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Medical%20Symbol.png](https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Objects/Medical%20Symbol.png)" alt="Medical Symbol" width="40" height="40" vertical-align="middle" /> MedAgent-CRM-Pro

### *AI-First HCP Interaction Module for Life Sciences*

[![Build Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](https://med-agent-crm-pro.vercel.app/)
[![React](https://img.shields.io/badge/Frontend-React%2018-blue?style=for-the-badge&logo=react)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/AI-Groq%20Llama%203.3-orange?style=for-the-badge)](https://groq.com/)

---

## 👨‍💻 Built By
**Aditya Kumar**  
*AI Application Developer & Full-Stack Engineer*

---

## 🚀 Quick Links

| 🌐 Live Demo | 📖 API Docs | 🎥 Video Demo |
| :--- | :--- | :--- |
| [med-agent-crm-pro.vercel.app](https://med-agent-crm-pro.vercel.app/) | [Swagger UI Documentation](https://medagent-crm-pro-production.up.railway.app/docs) | [Watch Implementation](https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Demo.gif) |

---

## 📸 Interface Preview

<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr style="border: none;">
      <td align="center" style="border: none;">
        <img src="[https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183225.png](https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183225.png)" width="280" style="border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/><br/>
        <b>Log Interaction Form</b>
      </td>
      <td align="center" style="border: none;">
        <img src="[https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183331.png](https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183331.png)" width="280" style="border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/><br/>
        <b>Interaction History</b>
      </td>
      <td align="center" style="border: none;">
        <img src="[https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183446.png](https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Screenshot%202026-04-28%20183446.png)" width="280" style="border-radius:10px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);"/><br/>
        <b>AI Suggestions</b>
      </td>
    </tr>
  </table>
</div>

---

## 🧠 Smart Features

MedAgent-CRM-Pro isn't just a database; it's an intelligent assistant.

*   **Hybrid Logging:** Choose between a **Structured Form** or a **Conversational AI Chat**.
*   **Sentiment Analysis:** Automatically detects HCP mood (Positive/Neutral/Negative).
*   **Smart Summaries:** LLM-generated concise summaries for quick review.
*   **Predictive Follow-ups:** AI suggests next steps based on meeting context.

---

## 🛠️ Tech Stack & Architecture

### **Core Technologies**
- **Frontend:** `React 18`, `Redux Toolkit`, `Axios`
- **Backend:** `Python 3.12`, `FastAPI`, `SQLAlchemy`
- **AI Orchestration:** `LangGraph`, `LangChain`
- **Inference:** `Groq llama-3.3-70b-versatile`

### **System Workflow**
```mermaid
graph TD
    A[User Interface] -->|Action| B(Redux Store)
    B -->|HTTP Request| C[FastAPI Backend]
    C -->|Natural Language| D{LangGraph Agent}
    D -->|Tool Call| E[PostgreSQL/SQLite]
    D -->|LLM Reasoning| F[Groq AI]
    F -->|Analysis/Summary| C
    C -->|Response| A
🤖 Agentic Tools (LangGraph)The system utilizes 5 specialized tools to handle complex CRM tasks:log_interaction: Extracts data from natural chat to save structured logs.edit_interaction: Intelligent partial updates to existing records.get_hcp_history: Fuzzy-match search for previous HCP touchpoints.suggest_follow_up: Generates 3 actionable steps for the representative.analyze_sentiment: Evaluates the emotional tone of the discussion.⚙️ Installation & SetupBashgit clone https://github.com/adityakr09/aivoa-crm.git
cd aivoa-crm
Bashcd backend
cp .env.example .env
# Add your GROQ_API_KEY to .env
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
Bashcd frontend
npm install
npm start
📋 API ReferenceMethodEndpointFunctionGET/api/interactionsFetch all recordsPOST/api/chatInteract with LangGraph AgentPUT/api/interactions/{id}Update recordDELETE/api/interactions/{id}Remove record
