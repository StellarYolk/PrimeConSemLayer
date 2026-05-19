from fastapi import APIRouter
from app.api.schemas.process_mining import ProcessMiningRequest, ProcessMiningResponse, ReactFlowNode, ReactFlowEdge
from app.agents.orchestrator import orchestrator

router = APIRouter()


@router.post("/discover", response_model=ProcessMiningResponse)
def discover_process(request: ProcessMiningRequest):
    query = f"Discover {request.process_type} process flow"
    initial_state = {"query": query, "intent": "", "result": None, "formatted_response": None}
    result = orchestrator.invoke(initial_state)
    formatted = result.get("formatted_response", {})
    nodes = [ReactFlowNode(**n) for n in formatted.get("nodes", [])]
    edges = [ReactFlowEdge(**e) for e in formatted.get("edges", [])]
    return ProcessMiningResponse(
        nodes=nodes,
        edges=edges,
        process_type=request.process_type,
        metrics=formatted.get("metrics", {}),
    )


@router.post("/conformance", response_model=ProcessMiningResponse)
def check_conformance(request: ProcessMiningRequest):
    query = f"Check conformance for {request.process_type} process"
    initial_state = {"query": query, "intent": "", "result": None, "formatted_response": None}
    result = orchestrator.invoke(initial_state)
    formatted = result.get("formatted_response", {})
    nodes = [ReactFlowNode(**n) for n in formatted.get("nodes", [])]
    edges = [ReactFlowEdge(**e) for e in formatted.get("edges", [])]
    return ProcessMiningResponse(
        nodes=nodes,
        edges=edges,
        process_type=request.process_type,
        metrics=formatted.get("metrics", {}),
    )
