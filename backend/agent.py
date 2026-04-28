import os, json
from typing import Annotated, TypedDict
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DATABASE_URL = "sqlite+aiosqlite:///./crm.db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=GROQ_API_KEY, temperature=0.1)

# ── TOOLS ──────────────────────────────────────────────────────────────────────

@tool
async def log_interaction(
    hcp_name: str, interaction_type: str, date: str,
    topics_discussed: str, attendees: str = "", materials_shared: str = "",
    samples_distributed: str = "", outcomes: str = "",
    follow_up_actions: str = "", time: str = "", sentiment: str = "Neutral"
) -> str:
    """
    Tool 1: Log a new HCP interaction to the database.
    Use when the user describes meeting/visiting/calling an HCP.
    """
    try:
        async with AsyncSessionLocal() as db:
            await db.execute(text("""
                INSERT INTO interactions
                (hcp_name, interaction_type, date, time, attendees, topics_discussed,
                 materials_shared, samples_distributed, sentiment, outcomes,
                 follow_up_actions, ai_summary, created_at)
                VALUES (:hcp_name, :interaction_type, :date, :time, :attendees,
                        :topics_discussed, :materials_shared, :samples_distributed,
                        :sentiment, :outcomes, :follow_up_actions, :ai_summary, :created_at)
            """), {
                "hcp_name": hcp_name, "interaction_type": interaction_type,
                "date": date, "time": time, "attendees": attendees,
                "topics_discussed": topics_discussed, "materials_shared": materials_shared,
                "samples_distributed": samples_distributed, "sentiment": sentiment,
                "outcomes": outcomes, "follow_up_actions": follow_up_actions,
                "ai_summary": "", "created_at": datetime.utcnow()
            })
            await db.commit()
        return json.dumps({
            "status": "success",
            "message": f"Interaction with {hcp_name} logged successfully!",
            "form_fields": {
                "hcp_name": hcp_name, "interaction_type": interaction_type,
                "date": date, "topics_discussed": topics_discussed,
                "materials_shared": materials_shared, "samples_distributed": samples_distributed,
                "sentiment": sentiment, "outcomes": outcomes,
                "follow_up_actions": follow_up_actions, "attendees": attendees
            }
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
async def edit_last_interaction(
    hcp_name: str = None, topics_discussed: str = None,
    outcomes: str = None, follow_up_actions: str = None,
    sentiment: str = None, materials_shared: str = None,
    samples_distributed: str = None, interaction_type: str = None
) -> str:
    """
    Tool 2: Edit/update specific fields of the most recently logged interaction.
    Use when user says: change, update, edit, sorry, fix, correct, wrong.
    Only updates the fields explicitly provided.
    """
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(text(
                "SELECT id FROM interactions ORDER BY created_at DESC LIMIT 1"
            ))
            row = result.fetchone()
            if not row:
                return json.dumps({"status": "error", "message": "No interactions found to edit."})

            interaction_id = row[0]
            updates = {k: v for k, v in {
                "hcp_name": hcp_name, "topics_discussed": topics_discussed,
                "outcomes": outcomes, "follow_up_actions": follow_up_actions,
                "sentiment": sentiment, "materials_shared": materials_shared,
                "samples_distributed": samples_distributed,
                "interaction_type": interaction_type
            }.items() if v is not None}

            if not updates:
                return json.dumps({"status": "error", "message": "No fields to update."})

            set_clause = ", ".join([f"{k}=:{k}" for k in updates.keys()])
            updates["id"] = interaction_id
            await db.execute(
                text(f"UPDATE interactions SET {set_clause} WHERE id=:id"), updates
            )
            await db.commit()

        # Return the updated fields so the frontend can update the form
        updated_fields = {k: v for k, v in updates.items() if k != "id"}
        return json.dumps({
            "status": "success",
            "message": f"Interaction #{interaction_id} updated!",
            "form_fields": updated_fields
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
async def get_hcp_history(hcp_name: str) -> str:
    """
    Tool 3: Get past interaction history for a specific HCP.
    Use when user asks: show history, past interactions, previous meetings, what did I discuss with X.
    Returns a formatted list of past interactions — does NOT update the form.
    """
    try:
        async with AsyncSessionLocal() as db:
            result = await db.execute(text("""
                SELECT id, interaction_type, date, topics_discussed, sentiment, outcomes, follow_up_actions
                FROM interactions
                WHERE hcp_name LIKE :name
                ORDER BY created_at DESC
                LIMIT 5
            """), {"name": f"%{hcp_name}%"})
            rows = result.fetchall()

        if not rows:
            return json.dumps({
                "status": "no_data",
                "message": f"No past interactions found for {hcp_name}.",
                "display_only": True
            })

        interactions = []
        for r in rows:
            interactions.append({
                "id": r[0], "type": r[1], "date": r[2],
                "topics": r[3], "sentiment": r[4],
                "outcomes": r[5], "follow_up": r[6]
            })

        return json.dumps({
            "status": "success",
            "hcp": hcp_name,
            "count": len(interactions),
            "interactions": interactions,
            "display_only": True   # <-- tells frontend: show in chat, don't update form
        })
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})


@tool
async def suggest_follow_up(hcp_name: str, last_interaction_summary: str) -> str:
    """
    Tool 4: Suggest intelligent follow-up actions after an HCP interaction.
    Use when user asks: suggest follow-ups, what should I do next, recommend actions.
    Returns suggestions to show in chat — does NOT update the form automatically.
    """
    try:
        resp = llm.invoke([HumanMessage(content=f"""You are a pharma CRM assistant. Suggest 3 specific, actionable follow-up actions for a field medical rep.

HCP Name: {hcp_name}
Last Interaction Summary: {last_interaction_summary}

Reply ONLY with valid JSON (no extra text):
{{"suggestions": ["specific action 1", "specific action 2", "specific action 3"]}}

Make suggestions specific to the interaction context.""")])

        raw = resp.content.strip()
        s = raw.find("{")
        e = raw.rfind("}") + 1
        data = json.loads(raw[s:e]) if s >= 0 else {"suggestions": [raw]}

        return json.dumps({
            "status": "success",
            "hcp": hcp_name,
            "suggestions": data.get("suggestions", []),
            "display_only": True   # <-- show in chat, optionally fill form
        })
    except Exception as ex:
        return json.dumps({"status": "error", "message": str(ex)})


@tool
async def analyze_sentiment(interaction_note: str) -> str:
    """
    Tool 5: Analyze the sentiment of an HCP interaction note or description.
    Use when user says: analyze, what is the sentiment, how did it go, assess tone.
    Returns analysis to show in chat — does NOT update the form.
    """
    try:
        resp = llm.invoke([HumanMessage(content=f"""Analyze the sentiment of this HCP interaction note from a pharma field rep perspective:

"{interaction_note}"

Reply ONLY with valid JSON:
{{"sentiment": "Positive", "confidence": "High", "rationale": "one sentence reason", "recommendation": "one actionable next step"}}

sentiment must be exactly: Positive, Neutral, or Negative""")])

        raw = resp.content.strip()
        s = raw.find("{")
        e = raw.rfind("}") + 1
        data = json.loads(raw[s:e]) if s >= 0 else {
            "sentiment": "Neutral", "confidence": "Low",
            "rationale": raw, "recommendation": "Follow up with HCP"
        }

        return json.dumps({
            "status": "success",
            "display_only": True,   # <-- show in chat only, don't touch form
            **data
        })
    except Exception as ex:
        return json.dumps({"status": "error", "message": str(ex)})


# ── LANGGRAPH AGENT ────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tools = [log_interaction, edit_last_interaction, get_hcp_history, suggest_follow_up, analyze_sentiment]
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

TODAY = datetime.now().strftime("%d-%m-%Y")
SYSTEM = f"""You are an AI assistant for a Life Sciences pharma CRM. You control a form on the LEFT panel via tools.

TODAY'S DATE: {TODAY}

TOOL SELECTION RULES (follow strictly):
1. log_interaction → user describes a NEW meeting/visit/call with an HCP
2. edit_last_interaction → user says: change, update, edit, sorry, fix, correct, wrong, mistake
3. get_hcp_history → user asks about past/previous interactions, history, what did I discuss
4. suggest_follow_up → user asks for follow-up suggestions, next steps, what to do after
5. analyze_sentiment → user asks to analyze/assess sentiment, how it went, tone of interaction

RESPONSE RULES:
- For log_interaction: after tool call, say "✅ Interaction logged successfully!! The details (HCP Name, Date, Sentiment, and Materials) have been automatically populated based on your summary. Would you like me to suggest a specific follow-up action, such as scheduling a meeting?"
- For edit_last_interaction: after tool call, say "✅ Updated! I've corrected the specified fields while keeping everything else the same."
- For get_hcp_history: format the history results as a readable list in your response. Say "📋 Here's the interaction history:"
- For suggest_follow_up: present suggestions as a numbered list. Say "💡 Here are suggested follow-up actions:"
- For analyze_sentiment: give a clear sentiment analysis. Say "🔍 Sentiment Analysis:"
- Keep responses concise and professional."""


def should_continue(state):
    last = state["messages"][-1]
    if hasattr(last, "tool_calls") and last.tool_calls:
        return "tools"
    return END


def call_model(state):
    return {"messages": [llm_with_tools.invoke([SystemMessage(content=SYSTEM)] + state["messages"])]}

g = StateGraph(AgentState)
g.add_node("agent", call_model)
g.add_node("tools", tool_node)
g.set_entry_point("agent")
g.add_conditional_edges("agent", should_continue)
g.add_edge("tools", "agent")
agent_graph = g.compile()


# ── TOOL DETECTION HELPERS ─────────────────────────────────────────────────────

# Tools that should update the form
FORM_UPDATE_TOOLS = {"log_interaction", "edit_last_interaction"}
# Tools that should only display in chat
DISPLAY_ONLY_TOOLS = {"get_hcp_history", "suggest_follow_up", "analyze_sentiment"}


def detect_tool_used(messages: list) -> str:
    """Detect which tool was called by scanning tool_calls in messages."""
    for msg in reversed(messages):
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            tc = msg.tool_calls[0]
            return tc["name"] if isinstance(tc, dict) else tc.get("name", "") if hasattr(tc, "get") else getattr(tc, "name", "")
    return ""


def extract_tool_result(messages: list) -> dict:
    """Extract the parsed JSON result from the last tool message."""
    from langchain_core.messages import ToolMessage
    for msg in reversed(messages):
        if isinstance(msg, ToolMessage):
            try:
                return json.loads(msg.content)
            except Exception:
                pass
    return {}


async def run_agent(user_message: str, history: list = None, current_form: dict = None) -> dict:
    """
    Main agent entry point. Returns:
    - response: text to show in chat
    - form_update: dict of fields to update (empty if display-only tool)
    - tool: name of tool used
    - suggestions: list of follow-up suggestions (for suggest_follow_up tool)
    """
    messages = []
    if history:
        for m in history[-6:]:  # keep last 6 messages for context
            if m["role"] == "user":
                messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                messages.append(AIMessage(content=m["content"]))

    messages.append(HumanMessage(content=user_message))

    # Run LangGraph
    result = await agent_graph.ainvoke({"messages": messages})
    all_messages = result["messages"]
    response_text = all_messages[-1].content

    # Detect which tool was used
    tool_used = detect_tool_used(all_messages)
    tool_result = extract_tool_result(all_messages)

    form_update = {}
    suggestions = []

    if tool_used in FORM_UPDATE_TOOLS:
        # ── Log or Edit: update the form ──
        raw_fields = tool_result.get("form_fields", {})
        # Normalize and clean
        for k, v in raw_fields.items():
            if v and str(v).strip() not in ["", "null", "None", "N/A"]:
                if k == "sentiment":
                    s = str(v).lower()
                    if "positive" in s:
                        form_update["sentiment"] = "Positive"
                    elif "negative" in s:
                        form_update["sentiment"] = "Negative"
                    else:
                        form_update["sentiment"] = "Neutral"
                elif k == "hcp_name":
                    # Safety: trim to reasonable name length
                    words = str(v).split()
                    form_update["hcp_name"] = " ".join(words[:4])
                else:
                    form_update[k] = v

    elif tool_used == "suggest_follow_up":
        # ── Suggest follow-ups: show in chat, return suggestions list ──
        suggestions = tool_result.get("suggestions", [])
        # Format response nicely if the LLM didn't
        if suggestions and "💡" not in response_text:
            formatted = "💡 **Suggested Follow-up Actions for {}:**\n\n".format(
                tool_result.get("hcp", "the HCP")
            )
            for i, s in enumerate(suggestions, 1):
                formatted += f"{i}. {s}\n"
            response_text = formatted

    elif tool_used == "analyze_sentiment":
        # ── Analyze sentiment: show in chat only ──
        if tool_result.get("status") == "success" and "🔍" not in response_text:
            sentiment = tool_result.get("sentiment", "Neutral")
            confidence = tool_result.get("confidence", "")
            rationale = tool_result.get("rationale", "")
            recommendation = tool_result.get("recommendation", "")
            response_text = (
                f"🔍 **Sentiment Analysis:**\n\n"
                f"**Sentiment:** {sentiment} (Confidence: {confidence})\n"
                f"**Reason:** {rationale}\n"
                f"**Recommendation:** {recommendation}"
            )

    elif tool_used == "get_hcp_history":
        # ── HCP History: format and show in chat only ──
        if tool_result.get("status") == "success":
            hcp = tool_result.get("hcp", "HCP")
            interactions = tool_result.get("interactions", [])
            if interactions:
                formatted = f"📋 **Interaction History for {hcp}** ({len(interactions)} records):\n\n"
                for item in interactions:
                    formatted += (
                        f"**#{item['id']}** — {item['type']} on {item['date']}\n"
                        f"• Topics: {item['topics'] or 'N/A'}\n"
                        f"• Sentiment: {item['sentiment'] or 'N/A'}\n"
                        f"• Outcomes: {item['outcomes'] or 'N/A'}\n\n"
                    )
                response_text = formatted
            else:
                response_text = f"📋 No past interactions found for {hcp}."
        elif tool_result.get("status") == "no_data":
            response_text = tool_result.get("message", "No history found.")

    return {
        "response": response_text,
        "form_update": form_update,   # empty dict for display-only tools
        "tool": tool_used,
        "suggestions": suggestions
    }
