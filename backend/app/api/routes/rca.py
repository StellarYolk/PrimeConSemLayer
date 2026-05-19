from fastapi import APIRouter, HTTPException
from app.api.schemas.dashboard import RCAResponse, RCAStep
from app.agents.orchestrator import orchestrator
from app.rca.engine import analyze_rca

router = APIRouter()


@router.post("/analyze", response_model=RCAResponse)
def analyze_rca_endpoint(request: dict):
    query = request.get("query", "")
    initial_state = {"query": query, "intent": "", "result": None, "formatted_response": None}
    result = orchestrator.invoke(initial_state)
    formatted = result.get("formatted_response", {})
    rca_data = formatted.get("rca", {})
    if not rca_data:
        raise HTTPException(status_code=400, detail="Could not perform RCA. Specify a valid KPI.")
    steps = [RCAStep(**s) for s in rca_data.get("steps", [])]
    return RCAResponse(
        kpi_id=rca_data.get("kpi_id", ""),
        kpi_name=rca_data.get("kpi_name", ""),
        current_value=rca_data.get("current_value", 0),
        threshold=rca_data.get("threshold", 0),
        status=rca_data.get("status", ""),
        steps=steps,
        summary=rca_data.get("summary", ""),
    )


@router.post("/diagnose/{kpi_id}", response_model=RCAResponse)
def diagnose_kpi(kpi_id: str):
    rca_data = analyze_rca(kpi_id)
    if "error" in rca_data:
        raise HTTPException(status_code=404, detail=rca_data["error"])
    steps = [RCAStep(**s) for s in rca_data.get("steps", [])]
    return RCAResponse(
        kpi_id=rca_data.get("kpi_id", ""),
        kpi_name=rca_data.get("kpi_name", ""),
        current_value=rca_data.get("current_value", 0),
        threshold=rca_data.get("threshold", 0),
        status=rca_data.get("status", ""),
        steps=steps,
        summary=rca_data.get("summary", ""),
    )
