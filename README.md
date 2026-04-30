<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>MedAgent CRM Pro – README</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #050810;
    --surface: #0b1120;
    --border: #1a2540;
    --accent: #00d4ff;
    --accent2: #7c3aed;
    --accent3: #10b981;
    --text: #e8edf8;
    --muted: #5a6a8a;
    --red: #ef4444;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: var(--bg); color: var(--text); font-family: 'Syne', sans-serif; min-height: 100vh; overflow-x: hidden; }
  body::before { content: ''; position: fixed; inset: 0; background-image: linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px); background-size: 40px 40px; pointer-events: none; z-index: 0; }
  .container { max-width: 900px; margin: 0 auto; padding: 60px 24px; position: relative; z-index: 1; }
  .hero { text-align: center; padding-bottom: 64px; border-bottom: 1px solid var(--border); margin-bottom: 64px; position: relative; }
  .hero::after { content: ''; position: absolute; bottom: -1px; left: 50%; transform: translateX(-50%); width: 200px; height: 1px; background: linear-gradient(90deg, transparent, var(--accent), transparent); }
  .badge { display: inline-flex; align-items: center; gap: 8px; background: rgba(0,212,255,0.08); border: 1px solid rgba(0,212,255,0.25); border-radius: 100px; padding: 6px 16px; font-size: 12px; color: var(--accent); letter-spacing: 0.12em; text-transform: uppercase; font-weight: 600; margin-bottom: 28px; font-family: 'JetBrains Mono', monospace; }
  .badge::before { content: ''; width: 6px; height: 6px; border-radius: 50%; background: var(--accent); animation: pulse 2s infinite; }
  @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.5; transform: scale(0.8); } }
  .hero h1 { font-size: clamp(36px, 6vw, 64px); font-weight: 800; line-height: 1.05; letter-spacing: -0.03em; margin-bottom: 8px; }
  .hero h1 span.grad { background: linear-gradient(135deg, #00d4ff 0%, #7c3aed 60%, #10b981 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; }
  .subtitle-tag { font-family: 'Instrument Serif', serif; font-style: italic; font-size: 20px; color: var(--muted); margin-bottom: 32px; }
  .author-line { font-size: 13px; color: var(--muted); font-family: 'JetBrains Mono', monospace; margin-bottom: 32px; }
  .author-line strong { color: var(--accent); }
  .stack-pills { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-bottom: 36px; }
  .pill { background: var(--surface); border: 1px solid var(--border); border-radius: 6px; padding: 5px 12px; font-size: 12px; color: var(--muted); font-family: 'JetBrains Mono', monospace; transition: all 0.2s; }
  .pill:hover { border-color: var(--accent); color: var(--accent); }
  .cta-row { display: flex; gap: 12px; justify-content: center; flex-wrap: wrap; }
  .btn { display: inline-flex; align-items: center; gap: 8px; padding: 11px 24px; border-radius: 8px; font-size: 14px; font-weight: 600; text-decoration: none; transition: all 0.2s; cursor: pointer; font-family: 'Syne', sans-serif; }
  .btn-primary { background: var(--accent); color: #050810; }
  .btn-primary:hover { background: #33ddff; transform: translateY(-1px); box-shadow: 0 8px 24px rgba(0,212,255,0.3); }
  .btn-ghost { background: transparent; border: 1px solid var(--border); color: var(--text); }
  .btn-ghost:hover { border-color: var(--accent); color: var(--accent); }
  .section { margin-bottom: 56px; }
  .section-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
  .section-icon { width: 36px; height: 36px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; flex-shrink: 0; }
  .icon-blue { background: rgba(0,212,255,0.12); border: 1px solid rgba(0,212,255,0.2); }
  .icon-purple { background: rgba(124,58,237,0.12); border: 1px solid rgba(124,58,237,0.3); }
  .icon-green { background: rgba(16,185,129,0.12); border: 1px solid rgba(16,185,129,0.3); }
  .section-title { font-size: 22px; font-weight: 700; letter-spacing: -0.02em; }
  .overview-card { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 28px; position: relative; overflow: hidden; }
  .overview-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px; background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent3)); }
  .overview-card p { font-size: 15px; line-height: 1.7; color: #9aaac4; margin-bottom: 20px; }
  .mode-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .mode-card { background: rgba(255,255,255,0.03); border: 1px solid var(--border); border-radius: 8px; padding: 16px; transition: border-color 0.2s; }
  .mode-card:hover { border-color: rgba(0,212,255,0.4); }
  .mode-label { font-size: 12px; color: var(--accent); font-family: 'JetBrains Mono', monospace; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
  .mode-desc { font-size: 13px; color: var(--muted); line-height: 1.5; }
  .tools-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
  .tool-card { background: var(--surface); border: 1px solid var(--border); border-radius: 10px; padding: 20px; transition: all 0.25s; position: relative; overflow: hidden; }
  .tool-card:hover { border-color: var(--accent2); transform: translateY(-2px); box-shadow: 0 12px 32px rgba(124,58,237,0.12); }
  .tool-number { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
  .tool-name { font-family: 'JetBrains Mono', monospace; font-size: 14px; color: var(--accent); font-weight: 500; margin-bottom: 8px; }
  .tool-desc { font-size: 13px; color: var(--muted); line-height: 1.6; }
  .arch-block { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
  .arch-pre { padding: 24px; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 1.8; color: #6b8cba; overflow-x: auto; background: transparent; }
  .arch-pre .hl { color: var(--accent); } .arch-pre .hl2 { color: var(--accent2); } .arch-pre .hl3 { color: var(--accent3); }
  .tech-table { width: 100%; border-collapse: collapse; font-size: 14px; }
  .tech-table th { text-align: left; padding: 10px 16px; font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em; color: var(--muted); border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; }
  .tech-table td { padding: 13px 16px; border-bottom: 1px solid rgba(26,37,64,0.6); color: #9aaac4; line-height: 1.5; }
  .tech-table tr:hover td { background: rgba(0,212,255,0.03); }
  .tech-table td:first-child { color: var(--accent3); font-weight: 600; white-space: nowrap; width: 110px; }
  .steps { display: flex; flex-direction: column; gap: 0; }
  .step { display: flex; gap: 20px; position: relative; }
  .step-left { display: flex; flex-direction: column; align-items: center; }
  .step-num { width: 32px; height: 32px; border-radius: 50%; border: 2px solid var(--accent); display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: 700; color: var(--accent); flex-shrink: 0; background: var(--bg); position: relative; z-index: 1; }
  .step-line { width: 2px; flex: 1; background: var(--border); min-height: 24px; margin: 4px 0; }
  .step:last-child .step-line { display: none; }
  .step-content { padding-bottom: 24px; flex: 1; }
  .step-title { font-size: 14px; font-weight: 700; margin-bottom: 8px; color: var(--text); }
  .code-block { background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #7ec8e3; line-height: 1.8; overflow-x: auto; white-space: pre; }
  .code-block .comment { color: var(--muted); }
  .api-table { width: 100%; border-collapse: collapse; font-size: 13px; }
  .api-table th { padding: 10px 14px; text-align: left; font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); border-bottom: 1px solid var(--border); font-family: 'JetBrains Mono', monospace; }
  .api-table td { padding: 12px 14px; border-bottom: 1px solid rgba(26,37,64,0.5); color: #9aaac4; }
  .method { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600; padding: 3px 8px; border-radius: 4px; display: inline-block; }
  .method-get { background: rgba(16,185,129,0.15); color: var(--accent3); }
  .method-post { background: rgba(0,212,255,0.15); color: var(--accent); }
  .method-put { background: rgba(245,158,11,0.15); color: #f59e0b; }
  .method-delete { background: rgba(239,68,68,0.15); color: var(--red); }
  .endpoint { font-family: 'JetBrains Mono', monospace; font-size: 12px; color: #c4d0e8; }
  .schema-block { background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-left: 3px solid var(--accent2); border-radius: 8px; padding: 20px; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 2; overflow-x: auto; color: #7ec8e3; white-space: pre; }
  .schema-block .kw { color: #c084fc; } .schema-block .field { color: var(--accent3); } .schema-block .type { color: #f59e0b; }
  .file-tree { background: rgba(0,0,0,0.4); border: 1px solid var(--border); border-radius: 8px; padding: 20px; font-family: 'JetBrains Mono', monospace; font-size: 12px; line-height: 2; color: var(--muted); white-space: pre; }
  .file-tree .dir { color: var(--accent); } .file-tree .file { color: #c4d0e8; } .file-tree .comment { color: #3d5080; }
  .notes-list { display: flex; flex-direction: column; gap: 10px; }
  .note-item { display: flex; align-items: flex-start; gap: 12px; background: var(--surface); border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; font-size: 13px; color: #9aaac4; line-height: 1.6; }
  .note-dot { width: 6px; height: 6px; border-radius: 50%; background: var(--accent); margin-top: 7px; flex-shrink: 0; }
  .demo-list { background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 24px; }
  .demo-item { display: flex; align-items: center; gap: 14px; padding: 10px 0; border-bottom: 1px solid rgba(26,37,64,0.6); font-size: 14px; color: #9aaac4; }
  .demo-item:last-child { border-bottom: none; }
  .demo-num { width: 24px; height: 24px; border-radius: 50%; background: rgba(124,58,237,0.2); border: 1px solid rgba(124,58,237,0.4); display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; color: #c084fc; flex-shrink: 0; font-family: 'JetBrains Mono', monospace; }
  .footer { margin-top: 64px; padding-top: 32px; border-top: 1px solid var(--border); text-align: center; }
  .footer p { font-size: 12px; color: var(--muted); font-family: 'JetBrains Mono', monospace; }
  @media (max-width: 600px) { .tools-grid, .mode-grid { grid-template-columns: 1fr; } }
</style>
</head>
<body>
<div class="container">
  <div class="hero">
    <div class="badge">AI-First CRM · Life Sciences</div>
    <h1>🏥 <span class="grad">MedAgent</span><br>CRM-Pro</h1>
    <p class="subtitle-tag">AI-Powered HCP Interaction Module</p>
    <p class="author-line">Built by <strong>Aditya Kumar</strong></p>
    <div class="stack-pills">
      <span class="pill">React + Redux</span>
      <span class="pill">FastAPI</span>
      <span class="pill">LangGraph</span>
      <span class="pill">Groq LLM</span>
      <span class="pill">SQLite / PostgreSQL</span>
    </div>
    <div class="cta-row">
      <a href="https://med-agent-crm-pro.vercel.app/" class="btn btn-primary">🚀 Live Demo</a>
      <a href="https://medagent-crm-pro-production.up.railway.app/docs" class="btn btn-ghost">📄 API Docs</a>
      <a href="https://github.com/adityakr09/MedAgent-CRM-Pro/blob/main/Demo.gif" class="btn btn-ghost">▶ Watch Demo</a>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-blue">📸</div><h2 class="section-title">Overview</h2></div>
    <div class="overview-card">
      <p>An AI-first CRM system for Life Sciences field representatives to <strong style="color:#e8edf8">log, manage, and analyze interactions</strong> with Healthcare Professionals (HCPs). Built to replace manual data entry with intelligent, conversational workflows.</p>
      <div class="mode-grid">
        <div class="mode-card"><div class="mode-label">📋 Structured Form</div><div class="mode-desc">Traditional form-based logging with AI-powered follow-up suggestions built in</div></div>
        <div class="mode-card"><div class="mode-label">🤖 AI Chat Interface</div><div class="mode-desc">Conversational logging powered by LangGraph + Groq LLM — just talk naturally</div></div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-purple">🧠</div><h2 class="section-title">Architecture</h2></div>
    <div class="arch-block">
      <pre class="arch-pre"><span class="hl">┌─────────────────────────────────────────────┐
│              React Frontend                 │
│  Redux Store ──► InteractionForm / Chat     │
│        └──► axios ──► FastAPI Backend       │
└────────────────────┬────────────────────────┘</span>
                     │ HTTP
<span class="hl2">┌────────────────────▼────────────────────────┐
│            FastAPI (Python)                 │
│  /api/interactions  ──►  SQLAlchemy ORM     │
│  /api/chat          ──►  LangGraph Agent    │
│                              │              │
│         ┌────────────────────▼──────────┐   │
│         │       LangGraph Agent         │   │
│         │  5 Tools via Groq LLM         │   │
│         │  log · edit · history         │   │
│         │  suggest · sentiment          │   │
│         └───────────────────────────────┘   │
└────────────────────┬────────────────────────┘</span>
                     │
<span class="hl3">┌────────────────────▼────────────────────────┐
│      SQLite (dev) / PostgreSQL (prod)       │
└─────────────────────────────────────────────┘</span></pre>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-blue">🤖</div><h2 class="section-title">LangGraph Agent & Tools</h2></div>
    <div class="tools-grid">
      <div class="tool-card"><div class="tool-number">Tool 01</div><div class="tool-name">log_interaction</div><div class="tool-desc">Captures interaction data from natural language. Extracts key points, infers HCP sentiment, generates AI summary, persists to DB.</div></div>
      <div class="tool-card"><div class="tool-number">Tool 02</div><div class="tool-name">edit_interaction</div><div class="tool-desc">Modifies any previously logged interaction by ID. Accepts partial updates — re-generates AI summary if content is updated.</div></div>
      <div class="tool-card"><div class="tool-number">Tool 03</div><div class="tool-name">get_hcp_history</div><div class="tool-desc">Retrieves interaction history for any HCP (fuzzy name match). Returns last N interactions sorted by most recent.</div></div>
      <div class="tool-card"><div class="tool-number">Tool 04</div><div class="tool-name">suggest_follow_up</div><div class="tool-desc">Generates 3 specific, actionable follow-up steps based on interaction context using llama-3.3-70b-versatile.</div></div>
      <div class="tool-card" style="grid-column: span 2;"><div class="tool-number">Tool 05</div><div class="tool-name">analyze_sentiment</div><div class="tool-desc">Analyzes free-text interaction notes to infer HCP sentiment with a confidence score and rationale. Helps reps understand the emotional tone of their last meeting.</div></div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-green">🗄️</div><h2 class="section-title">Database Schema</h2></div>
    <div class="schema-block"><span class="kw">CREATE TABLE</span> interactions (
    <span class="field">id</span>                <span class="type">INTEGER</span>  PRIMARY KEY AUTOINCREMENT,
    <span class="field">hcp_name</span>          <span class="type">VARCHAR(255)</span> NOT NULL,
    <span class="field">interaction_type</span>  <span class="type">VARCHAR(100)</span> NOT NULL,
    <span class="field">date</span>              <span class="type">VARCHAR(50)</span>  NOT NULL,
    <span class="field">time</span>              <span class="type">VARCHAR(50)</span>,
    <span class="field">attendees</span>         <span class="type">TEXT</span>,
    <span class="field">topics_discussed</span>  <span class="type">TEXT</span>,
    <span class="field">materials_shared</span>  <span class="type">TEXT</span>,
    <span class="field">samples_distributed</span> <span class="type">TEXT</span>,
    <span class="field">sentiment</span>         <span class="type">VARCHAR(50)</span>  DEFAULT 'Neutral',
    <span class="field">outcomes</span>          <span class="type">TEXT</span>,
    <span class="field">follow_up_actions</span> <span class="type">TEXT</span>,
    <span class="field">ai_summary</span>        <span class="type">TEXT</span>,
    <span class="field">created_at</span>        <span class="type">DATETIME</span>,
    <span class="field">updated_at</span>        <span class="type">DATETIME</span>
);</div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-blue">🛠️</div><h2 class="section-title">Tech Stack</h2></div>
    <div class="arch-block">
      <table class="tech-table">
        <thead><tr><th>Layer</th><th>Technology</th></tr></thead>
        <tbody>
          <tr><td>Frontend</td><td>React 18, Redux Toolkit, Axios</td></tr>
          <tr><td>Styling</td><td>Custom CSS with Google Inter font</td></tr>
          <tr><td>Backend</td><td>Python 3.12, FastAPI, Uvicorn</td></tr>
          <tr><td>AI Agent</td><td>LangGraph 1.1+, LangChain</td></tr>
          <tr><td>LLMs</td><td>Groq llama-3.3-70b-versatile (active)</td></tr>
          <tr><td>Database</td><td>SQLite (dev) / PostgreSQL (prod) via SQLAlchemy</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-green">🚀</div><h2 class="section-title">Getting Started</h2></div>
    <div class="steps">
      <div class="step">
        <div class="step-left"><div class="step-num">1</div><div class="step-line"></div></div>
        <div class="step-content">
          <div class="step-title">Clone the repo</div>
          <div class="code-block">git clone https://github.com/adityakr09/aivoa-crm.git
cd aivoa-crm</div>
        </div>
      </div>
      <div class="step">
        <div class="step-left"><div class="step-num">2</div><div class="step-line"></div></div>
        <div class="step-content">
          <div class="step-title">Backend Setup</div>
          <div class="code-block">cd backend
cp .env.example .env
# Edit .env — add your GROQ_API_KEY
pip install -r requirements.txt
uvicorn main:app --reload --port 8000</div>
        </div>
      </div>
      <div class="step">
        <div class="step-left"><div class="step-num">3</div><div class="step-line"></div></div>
        <div class="step-content">
          <div class="step-title">Frontend Setup</div>
          <div class="code-block">cd frontend
npm install
npm start
# Runs at http://localhost:3000</div>
        </div>
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-purple">📁</div><h2 class="section-title">Project Structure</h2></div>
    <div class="file-tree"><span class="dir">aivoa-crm/</span>
├── <span class="dir">backend/</span>
│   ├── <span class="file">main.py</span>          <span class="comment"># FastAPI app, REST + /api/chat endpoints</span>
│   ├── <span class="file">agent.py</span>         <span class="comment"># LangGraph agent with 5 tools</span>
│   ├── <span class="file">database.py</span>      <span class="comment"># SQLAlchemy models + async DB setup</span>
│   ├── <span class="file">requirements.txt</span>
│   └── <span class="file">.env.example</span>
│
└── <span class="dir">frontend/src/</span>
    ├── <span class="file">App.js</span>
    ├── <span class="dir">store/</span>
    │   ├── <span class="file">store.js</span>              <span class="comment"># Redux store</span>
    │   ├── <span class="file">interactionsSlice.js</span>  <span class="comment"># CRUD state management</span>
    │   └── <span class="file">chatSlice.js</span>          <span class="comment"># Chat state management</span>
    └── <span class="dir">components/</span>
        ├── <span class="file">LogInteractionScreen.jsx</span>
        ├── <span class="file">InteractionForm.jsx</span>
        ├── <span class="file">ChatInterface.jsx</span>
        └── <span class="file">InteractionsList.jsx</span></div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-purple">🎥</div><h2 class="section-title">Demo Walkthrough</h2></div>
    <div class="demo-list">
      <div class="demo-item"><div class="demo-num">1</div>Logging interaction via structured form</div>
      <div class="demo-item"><div class="demo-num">2</div>AI Chat logging via natural language</div>
      <div class="demo-item"><div class="demo-num">3</div>All 5 LangGraph tools in action</div>
      <div class="demo-item"><div class="demo-num">4</div>Edit and delete interactions</div>
      <div class="demo-item"><div class="demo-num">5</div>AI-powered follow-up suggestions</div>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-green">🌐</div><h2 class="section-title">API Endpoints</h2></div>
    <div class="arch-block">
      <table class="api-table">
        <thead><tr><th>Method</th><th>Endpoint</th><th>Description</th></tr></thead>
        <tbody>
          <tr><td><span class="method method-get">GET</span></td><td class="endpoint">/api/interactions</td><td>List all interactions</td></tr>
          <tr><td><span class="method method-post">POST</span></td><td class="endpoint">/api/interactions</td><td>Create new interaction</td></tr>
          <tr><td><span class="method method-put">PUT</span></td><td class="endpoint">/api/interactions/{id}</td><td>Update existing interaction</td></tr>
          <tr><td><span class="method method-delete">DELETE</span></td><td class="endpoint">/api/interactions/{id}</td><td>Delete interaction</td></tr>
          <tr><td><span class="method method-post">POST</span></td><td class="endpoint">/api/chat</td><td>Chat with AI agent</td></tr>
          <tr><td><span class="method method-get">GET</span></td><td class="endpoint">/api/hcps</td><td>List unique HCP names</td></tr>
        </tbody>
      </table>
    </div>
  </div>

  <div class="section">
    <div class="section-header"><div class="section-icon icon-blue">📝</div><h2 class="section-title">Notes</h2></div>
    <div class="notes-list">
      <div class="note-item"><div class="note-dot"></div>Database defaults to SQLite for development. Set <code style="background:rgba(0,212,255,0.1);padding:2px 6px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#00d4ff">DATABASE_URL=postgresql+asyncpg://...</code> in .env for production.</div>
      <div class="note-item"><div class="note-dot"></div>All AI features require a valid <code style="background:rgba(0,212,255,0.1);padding:2px 6px;border-radius:4px;font-family:'JetBrains Mono',monospace;font-size:12px;color:#00d4ff">GROQ_API_KEY</code> in .env.</div>
      <div class="note-item"><div class="note-dot"></div>CORS is open (*) for development — restrict in production.</div>
    </div>
  </div>

  <div class="footer">
    <p>MedAgent-CRM-Pro · Built by Aditya Kumar · React · FastAPI · LangGraph · Groq</p>
  </div>
</div>
</body>
</html>
