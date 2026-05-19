from fastapi import APIRouter, HTTPException
from app.api.schemas.dashboard import DashboardResponse, KPIListResponse, KPIInfo
from app.rca.kpi_tracker import get_all_kpis, get_kpi, get_kpi_trend

router = APIRouter()


@router.get("/list", response_model=KPIListResponse)
def list_kpis():
    kpis = get_all_kpis()
    kpi_infos = [KPIInfo(**kpi) for kpi in kpis]
    return KPIListResponse(kpis=kpi_infos)


@router.get("/{kpi_id}", response_model=DashboardResponse)
def get_kpi_dashboard(kpi_id: str):
    kpi = get_kpi(kpi_id)
    if not kpi:
        raise HTTPException(status_code=404, detail=f"KPI '{kpi_id}' not found")
    return DashboardResponse(kpi=KPIInfo(**kpi))


@router.get("/{kpi_id}/trend")
def get_kpi_trend_data(kpi_id: str):
    trend = get_kpi_trend(kpi_id)
    if not trend:
        raise HTTPException(status_code=404, detail=f"KPI '{kpi_id}' not found")
    return {"kpi_id": kpi_id, "trend": trend}
