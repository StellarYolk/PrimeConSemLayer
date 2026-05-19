from pydantic import BaseModel
from typing import Optional, Any


class RCAStep(BaseModel):
    step_number: int
    title: str
    description: str
    finding: str
    severity: str = "info"


class RCAResponse(BaseModel):
    kpi_id: str
    kpi_name: str
    current_value: float
    threshold: float
    status: str
    steps: list[RCAStep]
    summary: str


class KPIInfo(BaseModel):
    id: str
    name: str
    value: float
    threshold: float
    unit: str
    status: str
    trend: list[dict[str, Any]] = []


class KPIListResponse(BaseModel):
    kpis: list[KPIInfo]


class DashboardResponse(BaseModel):
    kpi: KPIInfo
