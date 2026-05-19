# PrimeConSemLayer: System Architecture & Implementation Plan

## Project Overview
AI-driven semantic layer bridging SAP ECC/S4HANA with a modern React/Tailwind frontend. Translates natural language into SAP data operations, process mining visualizations, and automated Root Cause Analysis.

## Tech Stack
- **Frontend**: React (Vite), Tailwind CSS, React Flow (@xyflow/react), Recharts
- **Backend**: Python FastAPI, LangGraph (Multi-Agent), Anthropic Claude 3.5 / OpenAI GPT-4o
- **Data**: pandas, pm4py, pyrfc (ECC), SAP OData (S/4HANA)
- **Infrastructure**: Docker Compose, PostgreSQL, Redis

## Architecture Decisions
- PostgreSQL for KPI history and RCA audit logs
- Both pyrfc (ECC) and OData (S/4HANA) connectors, read-only with table allowlists
- Anthropic Claude 3.5 as default LLM, configurable via env var
- Strict JSON contracts via Pydantic schemas between backend agents and frontend
- Decoupled frontend: process-mining (React Flow) and dashboards (Recharts) share zero imports

---

## File Manifest

### Root
- `docker-compose.yml` — 4 services: backend, frontend, postgres, redis
- `.env.example` — all environment variable templates

### Backend (FastAPI + LangGraph)
- `backend/Dockerfile` — Python 3.11 slim, installs requirements from requirements.txt
- `backend/requirements.txt` — fastapi, uvicorn, langgraph, langchain-anthropic, langchain-openai, pandas, pm4py, pyrfc, httpx, asyncpg, sqlalchemy, redis, networkx
- `backend/app/__init__.py`
- `backend/app/main.py` — FastAPI entrypoint, CORS, router registration
- `backend/app/config.py` — Pydantic settings for LLM, SAP ECC, SAP S/4HANA, DB, Redis
- `backend/app/api/__init__.py`
- `backend/app/api/routes/__init__.py`
- `backend/app/api/routes/query.py` — POST /api/query/ — NL to SAP insights
- `backend/app/api/routes/process_mining.py` — POST /api/process-mining/discover, /conformance
- `backend/app/api/routes/dashboards.py` — GET /api/dashboards/list, /{kpi_id}, /{kpi_id}/trend
- `backend/app/api/routes/rca.py` — POST /api/rca/analyze, /api/rca/diagnose/{kpi_id}
- `backend/app/api/schemas/__init__.py`
- `backend/app/api/schemas/query.py` — QueryRequest, QueryResponse, ChartConfig
- `backend/app/api/schemas/process_mining.py` — ProcessMiningRequest, ProcessMiningResponse, ReactFlowNode, ReactFlowEdge, ProcessType enum
- `backend/app/api/schemas/dashboard.py` — DashboardResponse, KPIListResponse, RCAStep, RCAResponse
- `backend/app/agents/__init__.py`
- `backend/app/agents/orchestrator.py` — LangGraph state machine: classify → route → execute → format
- `backend/app/agents/sap_data_agent.py` — LLM translates NL → SAP table spec → fetches via RFC/OData
- `backend/app/agents/process_mining_agent.py` — Orchestrates event log extraction, DFG discovery, React Flow conversion
- `backend/app/agents/rca_agent.py` — Anomaly detection + LLM-driven root cause reasoning
- `backend/app/agents/ui_agent.py` — LLM generates chart configurations for frontend
- `backend/app/connectors/__init__.py`
- `backend/app/connectors/sap_rfc.py` — pyrfc wrapper, RFC_READ_TABLE, table allowlist (VBAK, VBAP, EKKO, EKPO, etc.)
- `backend/app/connectors/sap_odata.py` — httpx async client for S/4HANA OData entity sets
- `backend/app/process_mining/__init__.py`
- `backend/app/process_mining/event_log.py` — SAP table → event log DataFrame, sample data generator
- `backend/app/process_mining/discovery.py` — pm4py DFG discovery, inductive miner, conformance checking
- `backend/app/process_mining/react_flow_converter.py` — DFG → React Flow nodes/edges JSON
- `backend/app/rca/__init__.py`
- `backend/app/rca/engine.py` — Deterministic diagnostic engine, cause identification by KPI type
- `backend/app/rca/kpi_tracker.py` — 19 KPI definitions, threshold tracking, anomaly detection, trend simulation
- `backend/app/utils/__init__.py`
- `backend/app/utils/json_contracts.py` — Validation helpers for React Flow payload and chart config

### Frontend (React + Vite + Tailwind)
- `frontend/Dockerfile` — Node 20 alpine, npm install, dev server on 5173
- `frontend/package.json` — react, react-router-dom, @xyflow/react, recharts, axios, lucide-react
- `frontend/vite.config.js` — React plugin, API proxy to backend:8000
- `frontend/tailwind.config.js` — Content paths, SAP color theme extension
- `frontend/postcss.config.js` — tailwindcss + autoprefixer
- `frontend/index.html` — Root div, module entry
- `frontend/src/__init__.py` — N/A, placeholder
- `frontend/src/main.jsx` — React root, BrowserRouter wrapper
- `frontend/src/App.jsx` — Routes: /, /process-mining, /dashboards, /rca
- `frontend/src/index.css` — Tailwind directives, React Flow custom styles, dark theme
- `frontend/src/api/client.js` — Axios instance, all API endpoint methods
- `frontend/src/components/Layout/Layout.jsx` — Sidebar + Header + Outlet
- `frontend/src/components/Layout/Sidebar.jsx` — Nav links: Dashboard, Process Mining, KPI Dashboards, RCA
- `frontend/src/components/Layout/Header.jsx` — Title + connection status
- `frontend/src/components/NLQuery/QueryInput.jsx` — Text input + submit button
- `frontend/src/components/NLQuery/QueryResult.jsx` — Answer text + Recharts bar chart
- `frontend/src/components/shared/LoadingSpinner.jsx` — Animated spinner
- `frontend/src/pages/Dashboard.jsx` — NL query page, calls queryAPI.processQuery
- `frontend/src/pages/ProcessMining.jsx` — Process type selector, discover button, renders ProcessFlow
- `frontend/src/pages/KPIDashboard.jsx` — Fetches 19 KPI list, renders KPIGrid
- `frontend/src/pages/RCA.jsx` — NL query for root cause, renders diagnostic steps
- `frontend/src/features/process-mining/ProcessFlow.jsx` — React Flow wrapper with Controls, MiniMap, Background
- `frontend/src/features/process-mining/CustomNode.jsx` — Custom node with frequency, duration, color by type
- `frontend/src/features/dashboards/KPIGrid.jsx` — Grid of KPI cards, click to expand
- `frontend/src/features/dashboards/KPIChart.jsx` — Recharts line chart with threshold reference line

---

## 19 KPI Dashboards
1. Procure-to-Pay Cycle Time
2. Order-to-Cash Cycle Time
3. AR Aging > 30 Days
4. AR Aging > 60 Days
5. AR Aging > 90 Days
6. Inventory Turnover Ratio
7. PO Approval Time
8. On-Time Delivery Rate
9. Invoice Accuracy Rate
10. GR/IR Mismatch Count
11. Avg Vendor Lead Time
12. Production Yield Rate
13. Quality Rejection Rate
14. Maverick Spend Ratio
15. Budget Variance
16. Cash Conversion Cycle
17. Backorder Rate
18. Customer Return Rate
19. Process Compliance Rate

---

## Multi-Agent Flow (LangGraph)
```
User Query → Orchestrator (classify intent)
  ├── "process/flow/cycle/bottleneck" → Process Mining Agent → UI Agent
  ├── "why/root cause/spike/anomaly" → RCA Agent → UI Agent
  └── default → SAP Data Agent → UI Agent
```

## Guardrails
- No UPDATE/DELETE on SAP — read-only connectors only
- Table allowlist: VBAK, VBAP, VBKD, EKKO, EKPO, EKET, LIKP, LIPS, BKPF, BSEG, CDHDR, CDPOS, MARA, MARC, MAKT, KNA1, LFA1, T001
- All API responses validated through Pydantic models
- Process mining and dashboard features fully decoupled
