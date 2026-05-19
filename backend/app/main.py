from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

from app.config import settings
from app.api.routes.query import router as query_router
from app.api.routes.process_mining import router as process_mining_router
from app.api.routes.dashboards import router as dashboards_router
from app.api.routes.rca import router as rca_router

app = FastAPI(
    title="PrimeConSemLayer",
    description="AI-driven semantic layer bridging SAP ECC/S4HANA with modern frontend",
    version="0.1.0",
)

# --- ROBUST CORS ORIGINS CLEANUP ---
raw_origins = settings.cors_origins_list
processed_origins = []

# Handle cases where Render interprets the env variable as a raw string instead of a Python list
if isinstance(raw_origins, str):
    try:
        processed_origins = json.loads(raw_origins)
    except json.JSONDecodeError:
        # Fallback if it's a comma-separated string: "https://site1.com, https://site2.com"
        processed_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]
elif isinstance(raw_origins, list):
    processed_origins = raw_origins

# CRITICAL: Browsers send Origins WITHOUT a trailing slash (e.g., 'https://app.vercel.app').
# If your env variable configuration has a '/', it will fail to match. Let's strip them safely:
final_origins = [str(origin).rstrip("/") for origin in processed_origins]

app.add_middleware(
    CORSMiddleware,
    allow_origins=final_origins,
    # Safety net: Automatically allows all Vercel preview & production deployments 
    allow_origin_regex=r"https://.*\.vercel\.app", 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -----------------------------------

app.include_router(query_router, prefix="/api/query", tags=["query"])
app.include_router(process_mining_router, prefix="/api/process-mining", tags=["process-mining"])
app.include_router(dashboards_router, prefix="/api/dashboards", tags=["dashboards"])
app.include_router(rca_router, prefix="/api/rca", tags=["rca"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
