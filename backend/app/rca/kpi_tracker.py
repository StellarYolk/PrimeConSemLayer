from typing import Optional


KPI_DEFINITIONS = {
    "procure-to-pay-cycle": {"name": "Procure-to-Pay Cycle Time", "threshold": 14.0, "unit": "days", "direction": "lower"},
    "order-to-cash-cycle": {"name": "Order-to-Cash Cycle Time", "threshold": 10.0, "unit": "days", "direction": "lower"},
    "ar-aging-30": {"name": "AR Aging > 30 Days", "threshold": 15.0, "unit": "%", "direction": "lower"},
    "ar-aging-60": {"name": "AR Aging > 60 Days", "threshold": 8.0, "unit": "%", "direction": "lower"},
    "ar-aging-90": {"name": "AR Aging > 90 Days", "threshold": 3.0, "unit": "%", "direction": "lower"},
    "inventory-turnover": {"name": "Inventory Turnover Ratio", "threshold": 6.0, "unit": "ratio", "direction": "higher"},
    "po-approval-time": {"name": "PO Approval Time", "threshold": 2.0, "unit": "days", "direction": "lower"},
    "on-time-delivery": {"name": "On-Time Delivery Rate", "threshold": 95.0, "unit": "%", "direction": "higher"},
    "invoice-accuracy": {"name": "Invoice Accuracy Rate", "threshold": 98.0, "unit": "%", "direction": "higher"},
    "gr-ir-mismatch": {"name": "GR/IR Mismatch Count", "threshold": 5.0, "unit": "count", "direction": "lower"},
    "avg-vendor-lead-time": {"name": "Avg Vendor Lead Time", "threshold": 7.0, "unit": "days", "direction": "lower"},
    "production-yield": {"name": "Production Yield Rate", "threshold": 95.0, "unit": "%", "direction": "higher"},
    "quality-rejection": {"name": "Quality Rejection Rate", "threshold": 2.0, "unit": "%", "direction": "lower"},
    "maverick-spend": {"name": "Maverick Spend Ratio", "threshold": 5.0, "unit": "%", "direction": "lower"},
    "budget-variance": {"name": "Budget Variance", "threshold": 3.0, "unit": "%", "direction": "lower"},
    "cash-conversion-cycle": {"name": "Cash Conversion Cycle", "threshold": 45.0, "unit": "days", "direction": "lower"},
    "backorder-rate": {"name": "Backorder Rate", "threshold": 5.0, "unit": "%", "direction": "lower"},
    "customer-return-rate": {"name": "Customer Return Rate", "threshold": 3.0, "unit": "%", "direction": "lower"},
    "process-compliance": {"name": "Process Compliance Rate", "threshold": 90.0, "unit": "%", "direction": "higher"},
}


def get_all_kpis() -> list[dict]:
    import random
    from datetime import datetime, timedelta
    result = []
    for kpi_id, kpi_def in KPI_DEFINITIONS.items():
        threshold = kpi_def["threshold"]
        is_higher_better = kpi_def["direction"] == "higher"
        if is_higher_better:
            value = round(threshold * random.uniform(0.85, 1.10), 2)
        else:
            value = round(threshold * random.uniform(0.5, 1.5), 2)
        status = _compute_status(kpi_id, value)
        trend = _generate_trend(kpi_id, threshold, is_higher_better)
        result.append({
            "id": kpi_id,
            "name": kpi_def["name"],
            "value": value,
            "threshold": threshold,
            "unit": kpi_def["unit"],
            "status": status,
            "trend": trend,
        })
    return result


def get_kpi(kpi_id: str) -> Optional[dict]:
    if kpi_id not in KPI_DEFINITIONS:
        return None
    import random
    kpi_def = KPI_DEFINITIONS[kpi_id]
    threshold = kpi_def["threshold"]
    is_higher_better = kpi_def["direction"] == "higher"
    if is_higher_better:
        value = round(threshold * random.uniform(0.85, 1.10), 2)
    else:
        value = round(threshold * random.uniform(0.5, 1.5), 2)
    status = _compute_status(kpi_id, value)
    trend = _generate_trend(kpi_id, threshold, is_higher_better)
    return {
        "id": kpi_id,
        "name": kpi_def["name"],
        "value": value,
        "threshold": threshold,
        "unit": kpi_def["unit"],
        "status": status,
        "trend": trend,
    }


def get_kpi_trend(kpi_id: str) -> list[dict]:
    if kpi_id not in KPI_DEFINITIONS:
        return []
    kpi_def = KPI_DEFINITIONS[kpi_id]
    is_higher_better = kpi_def["direction"] == "higher"
    return _generate_trend(kpi_id, kpi_def["threshold"], is_higher_better)


def _compute_status(kpi_id: str, value: float) -> str:
    kpi_def = KPI_DEFINITIONS[kpi_id]
    threshold = kpi_def["threshold"]
    is_higher_better = kpi_def["direction"] == "higher"
    if is_higher_better:
        if value >= threshold:
            return "healthy"
        elif value >= threshold * 0.9:
            return "warning"
        else:
            return "critical"
    else:
        if value <= threshold:
            return "healthy"
        elif value <= threshold * 1.15:
            return "warning"
        else:
            return "critical"


def _generate_trend(kpi_id: str, threshold: float, is_higher_better: bool) -> list[dict]:
    import random
    from datetime import datetime, timedelta
    trend = []
    base = datetime(2024, 1, 1)
    current_value = threshold * (0.8 if is_higher_better else 1.2)
    for i in range(12):
        drift = random.uniform(-0.05, 0.08) if is_higher_better else random.uniform(-0.08, 0.05)
        current_value *= (1 + drift)
        trend.append({
            "date": (base + timedelta(days=30 * i)).strftime("%Y-%m"),
            "value": round(current_value, 2),
        })
    return trend
