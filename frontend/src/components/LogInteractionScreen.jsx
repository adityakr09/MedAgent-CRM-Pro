import React, { useState, useRef, useEffect } from "react";

const API = process.env.REACT_APP_API_URL || "https://medagent-crm-pro-production.up.railway.app";

const emptyForm = {
  hcp_name: "",
  interaction_type: "Meeting",
  date: new Date().toISOString().split("T")[0],
  time: new Date().toTimeString().slice(0, 5),
  attendees: "",
  topics_discussed: "",
  materials_shared: "",
  samples_distributed: "",
  sentiment: "Neutral",
  outcomes: "",
  follow_up_actions: "",
};

// Tools that update the left form
const FORM_UPDATE_TOOLS = ["log_interaction", "edit_last_interaction"];

export default function LogInteractionScreen() {
  const [form, setForm] = useState(emptyForm);
  const [chatInput, setChatInput] = useState("");
  const [messages, setMessages] = useState([
    {
      role: "ai",
      text: 'Log interaction details here (e.g., "Met Dr. Smith, discussed Product X efficacy, positive sentiment, shared brochure") or ask for help.',
    },
  ]);
  const [loading, setLoading] = useState(false);
  const [logStatus, setLogStatus] = useState("");
  const [aiFollowUps, setAiFollowUps] = useState([]);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const updateForm = (fields) => {
    setForm((prev) => {
      const updated = { ...prev };
      for (const [key, val] of Object.entries(fields)) {
        if (val !== null && val !== undefined && String(val).trim() !== "" &&
            String(val) !== "None" && String(val) !== "null") {
          if (key === "sentiment") {
            const s = String(val).toLowerCase();
            if (s.includes("positive")) updated.sentiment = "Positive";
            else if (s.includes("negative")) updated.sentiment = "Negative";
            else updated.sentiment = "Neutral";
          } else {
            updated[key] = val;
          }
        }
      }
      return updated;
    });
  };

  const sendChat = async () => {
    const msg = chatInput.trim();
    if (!msg || loading) return;
    setChatInput("");
    setMessages((prev) => [...prev, { role: "user", text: msg }]);
    setLoading(true);

    try {
      const res = await fetch(`${API}/api/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: msg,
          history: messages.slice(-6).map((m) => ({
            role: m.role === "user" ? "user" : "assistant",
            content: m.text,
          })),
          current_form: form,
        }),
      });
      const data = await res.json();

      const toolUsed = data.tool || "";
      const replyText = data.response || "Done!";
      const formUpdate = data.form_update || {};
      const suggestions = data.suggestions || [];

      // ── Tool 4: suggest_follow_up ──
      if (toolUsed === "suggest_follow_up" && suggestions.length > 0) {
        setAiFollowUps(suggestions);
        setMessages((prev) => [...prev, { role: "ai", text: replyText }]);
      }
      // ── Tools 1 & 2: log_interaction / edit_last_interaction ──
      else if (FORM_UPDATE_TOOLS.includes(toolUsed) && Object.keys(formUpdate).length > 0) {
        updateForm(formUpdate);
        setMessages((prev) => [
          ...prev,
          { role: "ai", text: replyText },
        ]);
      }
      // ── Tools 3 & 5: get_hcp_history / analyze_sentiment (display only) ──
      else {
        setMessages((prev) => [...prev, { role: "ai", text: replyText }]);
      }
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ Error: " + err.message },
      ]);
    }
    setLoading(false);
  };

  const handleLog = async () => {
    if (!form.hcp_name) {
      setLogStatus("❌ HCP Name is required");
      return;
    }
    setLogStatus("Saving...");
    try {
      const res = await fetch(`${API}/api/interactions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (res.ok) {
        setLogStatus("✅ Interaction logged!");
        setMessages((prev) => [
          ...prev,
          { role: "ai", text: "✅ Interaction saved to database successfully!" },
        ]);
        setTimeout(() => {
          setForm(emptyForm);
          setAiFollowUps([]);
          setLogStatus("");
        }, 2000);
      } else {
        setLogStatus("❌ Failed to log");
      }
    } catch (e) {
      setLogStatus("❌ Error: " + e.message);
    }
  };

  const handleClear = () => {
    setForm(emptyForm);
    setAiFollowUps([]);
    setMessages([
      { role: "ai", text: "Form cleared. Tell me about your interaction with an HCP." },
    ]);
  };

  return (
    <div style={styles.page}>
      <h2 style={styles.title}>Log HCP Interaction</h2>
      <div style={styles.container}>

        {/* ── LEFT PANEL — FORM ── */}
        <div style={styles.leftPanel}>
          <div style={styles.sectionHeader}>INTERACTION DETAILS</div>

          <div style={styles.row}>
            <label style={styles.label}>HCP Name</label>
            <input
              style={styles.input}
              placeholder="Search or select HCP..."
              value={form.hcp_name}
              onChange={(e) => setForm({ ...form, hcp_name: e.target.value })}
            />
          </div>

          <div style={styles.twoCol}>
            <div>
              <label style={styles.label}>Interaction Type</label>
              <select
                style={styles.input}
                value={form.interaction_type}
                onChange={(e) => setForm({ ...form, interaction_type: e.target.value })}
              >
                {["Meeting", "Call", "Email", "Conference", "Other"].map((t) => (
                  <option key={t}>{t}</option>
                ))}
              </select>
            </div>
            <div>
              <label style={styles.label}>Date</label>
              <input
                type="date"
                style={styles.input}
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
              />
            </div>
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Attendees</label>
            <input
              style={styles.input}
              placeholder="Enter names or search..."
              value={form.attendees}
              onChange={(e) => setForm({ ...form, attendees: e.target.value })}
            />
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Topics Discussed</label>
            <textarea
              style={styles.textarea}
              placeholder="Enter key discussion points..."
              value={form.topics_discussed}
              onChange={(e) => setForm({ ...form, topics_discussed: e.target.value })}
            />
          </div>

          <div style={styles.sectionHeader}>MATERIALS SHARED / SAMPLES DISTRIBUTED</div>

          <div style={styles.row}>
            <label style={styles.label}>Materials Shared</label>
            <input
              style={styles.input}
              placeholder="No materials added"
              value={form.materials_shared}
              onChange={(e) => setForm({ ...form, materials_shared: e.target.value })}
            />
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Samples Distributed</label>
            <input
              style={styles.input}
              placeholder="No samples added"
              value={form.samples_distributed}
              onChange={(e) => setForm({ ...form, samples_distributed: e.target.value })}
            />
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Observed/Inferred HCP Sentiment</label>
            <div style={styles.sentimentRow}>
              {["Positive", "Neutral", "Negative"].map((s) => (
                <label key={s} style={styles.sentimentLabel}>
                  <input
                    type="radio"
                    name="sentiment"
                    value={s}
                    checked={form.sentiment === s}
                    onChange={() => setForm({ ...form, sentiment: s })}
                  />
                  {" "}{s === "Positive" ? "😊" : s === "Neutral" ? "😐" : "😟"} {s}
                </label>
              ))}
            </div>
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Outcomes</label>
            <textarea
              style={styles.textarea}
              placeholder="Key outcomes or agreements..."
              value={form.outcomes}
              onChange={(e) => setForm({ ...form, outcomes: e.target.value })}
            />
          </div>

          <div style={styles.row}>
            <label style={styles.label}>Follow-up Actions</label>
            <textarea
              style={styles.textarea}
              placeholder="Enter next steps or tasks..."
              value={form.follow_up_actions}
              onChange={(e) => setForm({ ...form, follow_up_actions: e.target.value })}
            />
          </div>

          {/* AI Suggested Follow-ups panel */}
          {aiFollowUps.length > 0 && (
            <div style={styles.aiFollowUpBox}>
              <div style={styles.aiFollowUpHeader}>✨ AI Suggested Follow-ups</div>
              {aiFollowUps.map((suggestion, i) => (
                <div key={i} style={styles.aiFollowUpItem}>
                  <span style={styles.aiFollowUpBullet}>→</span>
                  <span style={{ flex: 1 }}>{suggestion}</span>
                  <button
                    style={styles.aiFollowUpBtn}
                    onClick={() =>
                      setForm((f) => ({
                        ...f,
                        follow_up_actions: f.follow_up_actions
                          ? f.follow_up_actions + "\n• " + suggestion
                          : "• " + suggestion,
                      }))
                    }
                  >
                    Use
                  </button>
                </div>
              ))}
            </div>
          )}

          <div style={styles.btnRow}>
            <button style={styles.clearBtn} onClick={handleClear}>
              Clear
            </button>
            <button style={styles.logBtn} onClick={handleLog}>
              🗃 Log Interaction
            </button>
          </div>
          {logStatus && (
            <div
              style={{
                marginTop: 8,
                color: logStatus.startsWith("✅") ? "green" : "red",
                fontSize: 13,
              }}
            >
              {logStatus}
            </div>
          )}
        </div>

        {/* ── RIGHT PANEL — AI CHAT ── */}
        <div style={styles.rightPanel}>
          <div style={styles.chatHeader}>
            <span style={{ fontSize: 20 }}>🤖</span>
            <div>
              <div style={styles.chatTitle}>AI Assistant</div>
              <div style={styles.chatSub}>Log interaction via chat</div>
            </div>
          </div>

          <div style={styles.chatMessages}>
            {messages.map((m, i) => (
              <div key={i} style={m.role === "user" ? styles.userMsg : styles.aiMsg}>
                {/* Render line breaks in AI messages */}
                {m.text.split("\n").map((line, j) =>
                  line ? <div key={j}>{line}</div> : <br key={j} />
                )}
              </div>
            ))}
            {loading && (
              <div style={styles.aiMsg}>⏳ Processing...</div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div style={styles.chatInputRow}>
            <textarea
              style={styles.chatInput}
              placeholder="Describe Interaction..."
              value={chatInput}
              onChange={(e) => setChatInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  sendChat();
                }
              }}
            />
            <button style={styles.sendBtn} onClick={sendChat} disabled={loading}>
              🗃<br />Log
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    fontFamily: "'Inter', sans-serif",
    padding: "20px",
    background: "#f5f7fa",
    minHeight: "100vh",
  },
  title: { fontSize: 24, fontWeight: 700, marginBottom: 16, color: "#1a1a2e" },
  container: { display: "flex", gap: 20, alignItems: "flex-start" },
  leftPanel: {
    flex: 1.2,
    background: "#fff",
    borderRadius: 12,
    padding: 24,
    boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
  },
  rightPanel: {
    flex: 0.8,
    background: "#fff",
    borderRadius: 12,
    padding: 20,
    boxShadow: "0 2px 12px rgba(0,0,0,0.08)",
    display: "flex",
    flexDirection: "column",
    height: "85vh",
    position: "sticky",
    top: 20,
  },
  sectionHeader: {
    fontWeight: 700,
    fontSize: 12,
    color: "#888",
    letterSpacing: 1,
    marginBottom: 12,
    marginTop: 8,
  },
  row: { marginBottom: 14 },
  twoCol: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
    marginBottom: 14,
  },
  label: {
    display: "block",
    fontSize: 13,
    fontWeight: 600,
    color: "#444",
    marginBottom: 4,
  },
  input: {
    width: "100%",
    padding: "8px 10px",
    border: "1px solid #ddd",
    borderRadius: 8,
    fontSize: 13,
    boxSizing: "border-box",
    outline: "none",
    fontFamily: "'Inter', sans-serif",
  },
  textarea: {
    width: "100%",
    padding: "8px 10px",
    border: "1px solid #ddd",
    borderRadius: 8,
    fontSize: 13,
    boxSizing: "border-box",
    minHeight: 72,
    resize: "vertical",
    outline: "none",
    fontFamily: "'Inter', sans-serif",
  },
  sentimentRow: { display: "flex", gap: 20, marginTop: 6 },
  sentimentLabel: {
    fontSize: 13,
    cursor: "pointer",
    display: "flex",
    alignItems: "center",
    gap: 4,
  },
  btnRow: { display: "flex", gap: 10, marginTop: 16 },
  clearBtn: {
    padding: "10px 20px",
    border: "1px solid #ddd",
    borderRadius: 8,
    background: "#fff",
    cursor: "pointer",
    fontSize: 13,
    fontWeight: 600,
    fontFamily: "'Inter', sans-serif",
  },
  logBtn: {
    padding: "10px 24px",
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    borderRadius: 8,
    cursor: "pointer",
    fontSize: 13,
    fontWeight: 700,
    fontFamily: "'Inter', sans-serif",
  },
  chatHeader: {
    display: "flex",
    gap: 10,
    alignItems: "center",
    marginBottom: 12,
    paddingBottom: 12,
    borderBottom: "1px solid #eee",
  },
  chatTitle: { fontWeight: 700, fontSize: 15 },
  chatSub: { fontSize: 11, color: "#999" },
  chatMessages: {
    flex: 1,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 10,
    marginBottom: 12,
  },
  userMsg: {
    background: "#4f46e5",
    color: "#fff",
    padding: "10px 14px",
    borderRadius: "12px 12px 4px 12px",
    fontSize: 13,
    alignSelf: "flex-end",
    maxWidth: "85%",
    lineHeight: 1.5,
  },
  aiMsg: {
    background: "#f0f4ff",
    color: "#333",
    padding: "10px 14px",
    borderRadius: "12px 12px 12px 4px",
    fontSize: 13,
    alignSelf: "flex-start",
    maxWidth: "90%",
    lineHeight: 1.6,
    whiteSpace: "pre-wrap",
  },
  chatInputRow: { display: "flex", gap: 8, alignItems: "flex-end" },
  chatInput: {
    flex: 1,
    padding: "10px 12px",
    border: "1px solid #ddd",
    borderRadius: 10,
    fontSize: 13,
    resize: "none",
    minHeight: 60,
    outline: "none",
    fontFamily: "'Inter', sans-serif",
  },
  sendBtn: {
    padding: "10px 16px",
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    borderRadius: 10,
    cursor: "pointer",
    fontWeight: 700,
    fontSize: 12,
    minWidth: 56,
    fontFamily: "'Inter', sans-serif",
  },
  aiFollowUpBox: {
    background: "#f0f4ff",
    border: "1px solid #c7d2fe",
    borderRadius: 10,
    padding: "12px 14px",
    marginBottom: 14,
  },
  aiFollowUpHeader: {
    fontWeight: 700,
    fontSize: 12,
    color: "#4f46e5",
    marginBottom: 8,
    letterSpacing: 0.5,
  },
  aiFollowUpItem: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    marginBottom: 6,
    fontSize: 13,
    color: "#333",
  },
  aiFollowUpBullet: { color: "#4f46e5", fontWeight: 700, fontSize: 14 },
  aiFollowUpBtn: {
    padding: "3px 10px",
    background: "#4f46e5",
    color: "#fff",
    border: "none",
    borderRadius: 6,
    cursor: "pointer",
    fontSize: 11,
    fontWeight: 600,
    whiteSpace: "nowrap",
    fontFamily: "'Inter', sans-serif",
  },
};
