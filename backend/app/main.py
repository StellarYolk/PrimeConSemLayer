from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query_router, prefix="/api/query", tags=["query"])
app.include_router(process_mining_router, prefix="/api/process-mining", tags=["process-mining"])
app.include_router(dashboards_router, prefix="/api/dashboards", tags=["dashboards"])
app.include_router(rca_router, prefix="/api/rca", tags=["rca"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
