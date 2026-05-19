from pydantic import BaseModel
from typing import Optional, Any


class ChartConfig(BaseModel):
    chart_type: str = "bar"
    x_key: str = ""
    y_key: str = ""
    title: str = ""
    data: list[dict[str, Any]] = []


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    answer: str
    chart: Optional[ChartConfig] = None
    raw_data: Optional[list[dict[str, Any]]] = None
