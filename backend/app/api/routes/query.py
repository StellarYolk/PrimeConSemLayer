from fastapi import APIRouter
from app.api.schemas.query import QueryRequest, QueryResponse
from app.agents.orchestrator import orchestrator

router = APIRouter()


@router.post("/", response_model=QueryResponse)
def process_query(request: QueryRequest):
    initial_state = {"query": request.query, "intent": "", "result": None, "formatted_response": None}
    result = orchestrator.invoke(initial_state)
    formatted = result.get("formatted_response", {})
    return QueryResponse(
        answer=formatted.get("answer", ""),
        chart=formatted.get("chart"),
        raw_data=formatted.get("raw_data"),
    )
