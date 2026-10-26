# PrimeCon Semantic Layer

PrimeCon Semantic Layer is an enterprise analytics application that connects business questions with SAP-oriented data insights. It combines natural-language querying, process mining, KPI monitoring, and root-cause analysis in a single, modern web experience.

**Live architecture:** React frontend on Vercel · FastAPI backend on Render

## What it does

- Turns business questions such as “Show me sales orders” into structured SAP data insights.
- Discovers and visualizes Order-to-Cash, Procure-to-Pay, and Record-to-Report process flows.
- Tracks 19 enterprise KPIs across finance, procurement, operations, inventory, and compliance.
- Produces structured root-cause analysis for KPI deviations.
- Supports SAP ECC RFC and SAP S/4HANA OData connector patterns with an allowlisted, read-only data-access model.

## Product highlights

| Area | Capability |
| --- | --- |
| Natural-language analytics | Routes business queries to data, process-mining, or RCA workflows |
| Process intelligence | Uses `pm4py` to discover directly-follows graphs and returns React Flow-compatible JSON |
| KPI command center | Presents 19 KPI cards with thresholds, health states, and trend charts |
| Root-cause analysis | Provides prioritized, step-by-step diagnostic findings |
| SAP integration layer | Includes ECC RFC and S/4HANA OData connector abstractions |
| Responsive UI | Built with React, Tailwind CSS, Recharts, and React Flow |

## Architecture

```text
Browser (Vercel)
        │
        ▼
React + Vite + Tailwind
        │  /api
        ▼
FastAPI (Render)
        │
        ├── LangGraph request orchestrator
        ├── SAP data agent
        ├── Process-mining agent (pandas + pm4py)
        └── KPI / RCA agent
                │
                ▼
      SAP ECC / S/4HANA connector layer
```

The backend exposes typed JSON contracts, keeping the frontend independent from SAP-specific data handling.

## Technology stack

**Frontend:** React 18, Vite, Tailwind CSS, React Router, React Flow, Recharts, Axios, Lucide

**Backend:** Python, FastAPI, Pydantic, LangGraph, pandas, pm4py, NetworkX, SQLAlchemy, Redis

**Deployment:** Vercel (frontend), Render (backend), Docker Compose (local services)

## Local setup

### Prerequisites

- Docker Desktop and Docker Compose, or
- Python 3.11+ and Node.js 20+

### Run with Docker

1. Clone the repository and enter it.

   ```bash
   git clone https://github.com/StellarYolk/PrimeConSemLayer.git
   cd PrimeConSemLayer
   ```

2. Create your local environment file.

   ```bash
   cp .env.example .env
   ```

3. Build and start the stack.

   ```bash
   docker compose up --build
   ```

4. Open the application at [http://localhost:5173](http://localhost:5173). The API health endpoint is available at [http://localhost:8000/health](http://localhost:8000/health).

### Run services directly

Start the API:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

In a second terminal, start the frontend:

```bash
cd frontend
npm install
VITE_API_URL=http://localhost:8000 npm run dev
```

## Environment configuration

Copy `.env.example` to `.env` for local work. Do not commit credentials.

| Variable | Purpose |
| --- | --- |
| `CORS_ORIGINS` | Comma-separated allowed frontend origins |
| `VITE_API_URL` | Public backend URL used by the frontend, without `/api` |
| `SAP_ECC_ENABLED` | Enables SAP ECC RFC connectivity |
| `SAP_ODATA_ENABLED` | Enables SAP S/4HANA OData connectivity |
| `OPENROUTER_API_KEY` | Optional LLM-provider API key |

## Deployment

### Backend — Render

Create a Render Web Service from this repository with:

```text
Root directory: backend
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set `CORS_ORIGINS` to the Vercel production URL (and any required preview URL). Add SAP and provider credentials through Render’s encrypted environment-variable settings.

### Frontend — Vercel

Import the repository into Vercel and configure:

```text
Root directory: frontend
Build command: npm run build
Output directory: dist
```

Add a `VITE_API_URL` environment variable pointing to the Render service, for example `https://your-service.onrender.com`. The client automatically prefixes API calls with `/api`.

## API overview

| Method | Endpoint | Purpose |
| --- | --- | --- |
| `GET` | `/health` | Service health check |
| `POST` | `/api/query/` | Natural-language business query |
| `POST` | `/api/process-mining/discover` | Process-flow discovery |
| `POST` | `/api/process-mining/conformance` | Process conformance workflow |
| `GET` | `/api/dashboards/list` | All KPI cards |
| `GET` | `/api/dashboards/{kpi_id}` | One KPI dashboard |
| `POST` | `/api/rca/analyze` | Root-cause analysis from a query |
| `POST` | `/api/rca/diagnose/{kpi_id}` | Root-cause analysis for a KPI |

## Project structure

```text
backend/
  app/
    agents/           # Orchestration, SAP, process-mining, RCA, and UI agents
    api/              # FastAPI routes and typed request/response schemas
    connectors/       # SAP RFC and OData integrations
    process_mining/   # Event logs, pm4py discovery, React Flow conversion
    rca/              # KPI definitions and root-cause engine
frontend/
  src/
    components/       # Shared layout and query UI
    features/         # Process-flow and KPI visualizations
    pages/            # Dashboard, process mining, KPI, and RCA screens
```

## Security principles

- SAP table access is constrained through an allowlist.
- Connector operations are designed for read-only data extraction.
- Credentials are supplied through environment variables rather than source control.
- API responses are modeled as typed JSON contracts.

## License

Created as part of an enterprise AI and SAP analytics assignment.
