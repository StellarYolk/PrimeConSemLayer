from pydantic import BaseModel
from enum import Enum
from typing import Optional, Any


class ProcessType(str, Enum):
    procure_to_pay = "procure-to-pay"
    order_to_cash = "order-to-cash"
    record_to_report = "record-to-report"


class ReactFlowNode(BaseModel):
    id: str
    type: str = "custom"
    position: dict[str, float]
    data: dict[str, Any]


class ReactFlowEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    animated: bool = False
    style: Optional[dict[str, Any]] = None


class ProcessMiningRequest(BaseModel):
    process_type: ProcessType
    mode: str = "discover"
    sample_data: bool = True


class ProcessMiningResponse(BaseModel):
    nodes: list[ReactFlowNode]
    edges: list[ReactFlowEdge]
    process_type: ProcessType
    metrics: dict[str, Any] = {}
