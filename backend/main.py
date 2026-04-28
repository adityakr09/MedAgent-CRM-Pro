from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import sqlite3, os, json, re
from datetime import datetime
from agent import run_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB Setup ───────────────────────────────────────────────────────────────────
def get_db():
    conn = sqlite3.connect("crm.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hcp_name TEXT, interaction_type TEXT DEFAULT 'Meeting',
        date TEXT, time TEXT, attendees TEXT, topics_discussed TEXT,
        materials_shared TEXT, samples_distributed TEXT,
        sentiment TEXT DEFAULT 'Neutral', outcomes TEXT,
        follow_up_actions TEXT, ai_summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()
    conn.close()

init_db()

# ── Models ─────────────────────────────────────────────────────────────────────
class ChatReq(BaseModel):
    message: str
    history: Optional[List[dict]] = []
    current_form: Optional[dict] = None

class Interaction(BaseModel):
    hcp_name: Optional[str] = ""
    interaction_type: Optional[str] = "Meeting"
    date: Optional[str] = ""
    time: Optional[str] = ""
    attendees: Optional[str] = ""
    topics_discussed: Optional[str] = ""
    materials_shared: Optional[str] = ""
    samples_distributed: Optional[str] = ""
    sentiment: Optional[str] = "Neutral"
    outcomes: Optional[str] = ""
    follow_up_actions: Optional[str] = ""

# ── Chat Endpoint (LangGraph powered) ─────────────────────────────────────────
@app.post("/api/chat")
async def chat(req: ChatReq):
    try:
        # All logic is handled by LangGraph agent in agent.py
        result = await run_agent(
            user_message=req.message,
            history=req.history,
            current_form=req.current_form
        )

        response_text = result.get("response", "Done!")
        form_update = result.get("form_update", {})
        tool_used = result.get("tool", "")

        # Clean up form_update — remove null/empty values
        if form_update:
            form_update = {
                k: v for k, v in form_update.items()
                if v and str(v).strip() not in ["", "null", "None", "N/A"]
            }

            # Normalize sentiment
            if "sentiment" in form_update:
                s = form_update["sentiment"].lower()
                if "positive" in s:
                    form_update["sentiment"] = "Positive"
                elif "negative" in s:
                    form_update["sentiment"] = "Negative"
                else:
                    form_update["sentiment"] = "Neutral"

            # Safety: hcp_name must be short (name only)
            if "hcp_name" in form_update:
                words = form_update["hcp_name"].split()
                if len(words) > 4:
                    form_update["hcp_name"] = " ".join(words[:3])

        # Extract AI suggested follow-ups from response for the form panel
        ai_follow_ups = []
        if tool_used in ["suggest_followup", "log_interaction"] or "follow" in req.message.lower():
            # Try to extract bullet points from response as follow-up suggestions
            lines = response_text.split("\n")
            for line in lines:
                line = line.strip()
                if line.startswith(("•", "-", "*", "1.", "2.", "3.")):
                    clean = re.sub(r'^[•\-\*\d\.]\s*', '', line).strip()
                    if clean and len(clean) > 10:
                        ai_follow_ups.append(clean)
            ai_follow_ups = ai_follow_ups[:3]  # max 3

        return {
            "response": response_text,
            "form_update": form_update,
            "tool": tool_used,
            "ai_follow_ups": ai_follow_ups
        }

    except Exception as e:
        return {
            "response": f"⚠️ Agent error: {str(e)}",
            "form_update": {},
            "tool": "",
            "ai_follow_ups": []
        }

# ── Interactions CRUD ──────────────────────────────────────────────────────────
@app.get("/api/interactions")
async def get_interactions():
    conn = get_db()
    rows = conn.execute("SELECT * FROM interactions ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/interactions")
async def save_interaction(data: Interaction):
    conn = get_db()
    conn.execute("""INSERT INTO interactions 
        (hcp_name,interaction_type,date,time,attendees,topics_discussed,
         materials_shared,samples_distributed,sentiment,outcomes,follow_up_actions)
        VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (data.hcp_name, data.interaction_type, data.date, data.time,
         data.attendees, data.topics_discussed, data.materials_shared,
         data.samples_distributed, data.sentiment, data.outcomes,
         data.follow_up_actions))
    conn.commit()
    conn.close()
    return {"status": "saved"}

@app.put("/api/interactions/{interaction_id}")
async def update_interaction(interaction_id: int, data: Interaction):
    conn = get_db()
    conn.execute("""UPDATE interactions SET
        hcp_name=?, interaction_type=?, date=?, topics_discussed=?,
        materials_shared=?, samples_distributed=?, sentiment=?,
        outcomes=?, follow_up_actions=?
        WHERE id=?""",
        (data.hcp_name, data.interaction_type, data.date,
         data.topics_discussed, data.materials_shared,
         data.samples_distributed, data.sentiment,
         data.outcomes, data.follow_up_actions, interaction_id))
    conn.commit()
    conn.close()
    return {"status": "updated"}

@app.delete("/api/interactions/{interaction_id}")
async def delete_interaction(interaction_id: int):
    conn = get_db()
    conn.execute("DELETE FROM interactions WHERE id=?", (interaction_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}

@app.get("/")
async def root():
    return {"status": "ok", "message": "AIVOA CRM Backend — LangGraph Powered ✅"}
