from app.rca.kpi_tracker import KPI_DEFINITIONS


RCA_CAUSES = {
    "procure-to-pay-cycle": [
        {"cause": "Delayed PO Approval", "description": "Purchase orders stuck in approval workflow due to missing cost center assignments.", "severity": "high"},
        {"cause": "Vendor Response Time", "description": "Vendors taking longer than SLA to acknowledge and confirm purchase orders.", "severity": "medium"},
        {"cause": "Goods Receipt Delays", "description": "Warehouse not posting GR within expected timeframe after delivery.", "severity": "medium"},
        {"cause": "Invoice Processing Bottleneck", "description": "Three-way match failures causing manual invoice review cycles.", "severity": "high"},
    ],
    "order-to-cash-cycle": [
        {"cause": "Credit Hold Blocks", "description": "Orders blocked due to credit limit exceeded, requiring manual release.", "severity": "high"},
        {"cause": "Pick & Pack Delays", "description": "Warehouse picking operations exceeding standard time due to stock location issues.", "severity": "medium"},
        {"cause": "Billing Document Errors", "description": "Incorrect pricing conditions causing billing document rework.", "severity": "high"},
        {"cause": "Payment Posting Delays", "description": "Incoming payments not matched to open items promptly.", "severity": "low"},
    ],
    "ar-aging-30": [
        {"cause": "Customer Payment Terms", "description": "Extended payment terms negotiated with key customers pushing aging buckets.", "severity": "medium"},
        {"cause": "Disputed Invoices", "description": "Open disputes preventing payment posting on affected invoices.", "severity": "high"},
    ],
    "ar-aging-60": [
        {"cause": "Collection Process Gaps", "description": "Dunning procedures not triggered at optimal intervals.", "severity": "high"},
        {"cause": "Customer Financial Distress", "description": "Key accounts experiencing cash flow issues.", "severity": "critical"},
    ],
    "ar-aging-90": [
        {"cause": "Bad Debt Risk", "description": "Aging receivables approaching write-off threshold requiring provisioning.", "severity": "critical"},
        {"cause": "Legal Hold", "description": "Disputed amounts under legal review preventing resolution.", "severity": "high"},
    ],
    "inventory-turnover": [
        {"cause": "Overstocking", "description": "Safety stock levels set too high relative to actual demand variability.", "severity": "medium"},
        {"cause": "Slow-Moving Items", "description": "SKU proliferation with low-velocity items inflating average inventory.", "severity": "medium"},
    ],
    "po-approval-time": [
        {"cause": "Approval Matrix Complexity", "description": "Multi-level approval chains causing delays for high-value POs.", "severity": "high"},
        {"cause": "Missing Delegation", "description": "Approvers on leave without delegation rules configured.", "severity": "medium"},
    ],
    "on-time-delivery": [
        {"cause": "Vendor Performance", "description": "Key vendors consistently missing confirmed delivery dates.", "severity": "high"},
        {"cause": "Transportation Delays", "description": "Logistics provider capacity constraints affecting delivery schedules.", "severity": "medium"},
    ],
    "invoice-accuracy": [
        {"cause": "Pricing Condition Errors", "description": "Incorrect condition records applied during invoice creation.", "severity": "high"},
        {"cause": "Tax Calculation Issues", "description": "Tax jurisdiction mismatches causing incorrect tax amounts.", "severity": "medium"},
    ],
    "gr-ir-mismatch": [
        {"cause": "Quantity Variance", "description": "Goods received quantities not matching PO quantities.", "severity": "high"},
        {"cause": "Price Variance", "description": "Invoice prices differing from PO prices beyond tolerance.", "severity": "high"},
    ],
    "avg-vendor-lead-time": [
        {"cause": "Supply Chain Disruption", "description": "Raw material shortages extending vendor production cycles.", "severity": "high"},
        {"cause": "Customs Delays", "description": "Import clearance times increasing for international vendors.", "severity": "medium"},
    ],
    "production-yield": [
        {"cause": "Machine Downtime", "description": "Unplanned equipment failures reducing effective production time.", "severity": "critical"},
        {"cause": "Material Defects", "description": "Incoming raw material quality issues affecting output quality.", "severity": "high"},
    ],
    "quality-rejection": [
        {"cause": "Process Parameter Drift", "description": "Manufacturing process parameters outside control limits.", "severity": "high"},
        {"cause": "Inspection Criteria Changes", "description": "Updated quality standards increasing rejection thresholds.", "severity": "medium"},
    ],
    "maverick-spend": [
        {"cause": "Off-Contract Purchasing", "description": "Buyers placing orders outside negotiated contracts.", "severity": "high"},
        {"cause": "Emergency Purchases", "description": "Urgent requirements bypassing standard procurement process.", "severity": "medium"},
    ],
    "budget-variance": [
        {"cause": "Unplanned Expenses", "description": "Cost center overspend due to unexpected operational requirements.", "severity": "high"},
        {"cause": "Revenue Shortfall", "description": "Lower than projected revenue impacting budget ratios.", "severity": "medium"},
    ],
    "cash-conversion-cycle": [
        {"cause": "Extended DSO", "description": "Days Sales Outstanding increasing due to slower collections.", "severity": "high"},
        {"cause": "Inventory Days Increase", "description": "Inventory holding periods extending beyond target.", "severity": "medium"},
    ],
    "backorder-rate": [
        {"cause": "Stock-Out Events", "description": "Insufficient safety stock for high-demand SKUs.", "severity": "high"},
        {"cause": "Demand Forecast Error", "description": "Forecast model underestimating actual demand patterns.", "severity": "medium"},
    ],
    "customer-return-rate": [
        {"cause": "Product Quality Issues", "description": "Defective products reaching customers causing returns.", "severity": "critical"},
        {"cause": "Order Accuracy", "description": "Wrong items shipped due to picking errors.", "severity": "high"},
    ],
    "process-compliance": [
        {"cause": "Process Deviations", "description": "Users bypassing standard workflow steps.", "severity": "high"},
        {"cause": "Segregation of Duties Violations", "description": "Same user performing incompatible activities.", "severity": "critical"},
    ],
}


def analyze_rca(kpi_id: str) -> dict:
    from app.rca.kpi_tracker import get_kpi
    kpi = get_kpi(kpi_id)
    if not kpi:
        return {"error": f"KPI '{kpi_id}' not found"}

    causes = RCA_CAUSES.get(kpi_id, [])
    steps = []
    for i, cause in enumerate(causes, 1):
        steps.append({
            "step_number": i,
            "title": cause["cause"],
            "description": cause["description"],
            "finding": _generate_finding(cause, kpi),
            "severity": cause["severity"],
        })

    summary = _generate_summary(kpi, causes)
    return {
        "kpi_id": kpi_id,
        "kpi_name": kpi["name"],
        "current_value": kpi["value"],
        "threshold": kpi["threshold"],
        "status": kpi["status"],
        "steps": steps,
        "summary": summary,
    }


def _generate_finding(cause: dict, kpi: dict) -> str:
    severity = cause["severity"]
    if severity == "critical":
        return f"Immediate action required. This factor contributes approximately 40-50% to the current KPI deviation of {abs(kpi['value'] - kpi['threshold']):.1f} {kpi['unit']}."
    elif severity == "high":
        return f"Significant impact detected. Addressing this could improve KPI by 20-30% toward the threshold of {kpi['threshold']} {kpi['unit']}."
    elif severity == "medium":
        return f"Moderate contributor. Remediation would yield 10-15% improvement toward target."
    else:
        return f"Minor factor. Monitor for escalation but lower priority for immediate action."


def _generate_summary(kpi: dict, causes: list[dict]) -> str:
    critical_count = sum(1 for c in causes if c["severity"] == "critical")
    high_count = sum(1 for c in causes if c["severity"] == "high")
    direction = "above" if kpi["value"] > kpi["threshold"] else "below"
    summary = f"KPI '{kpi['name']}' is currently {direction} threshold by {abs(kpi['value'] - kpi['threshold']):.1f} {kpi['unit']}. "
    summary += f"Root cause analysis identified {len(causes)} contributing factors: {critical_count} critical, {high_count} high priority. "
    if critical_count > 0:
        summary += "Immediate attention required for critical factors."
    return summary
