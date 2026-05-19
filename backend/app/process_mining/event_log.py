import pandas as pd
import random
from datetime import datetime, timedelta


def generate_sample_event_log(process_type: str, num_cases: int = 50) -> pd.DataFrame:
    events = []
    case_id = 1000

    process_flows = {
        "procure-to-pay": [
            "Create Purchase Requisition",
            "Approve Purchase Requisition",
            "Create Purchase Order",
            "Send PO to Vendor",
            "Goods Receipt",
            "Invoice Receipt",
            "Payment Processing",
        ],
        "order-to-cash": [
            "Create Sales Order",
            "Check Credit Limit",
            "Pick & Pack",
            "Goods Issue",
            "Create Billing Document",
            "Post Incoming Payment",
        ],
        "record-to-report": [
            "Post Journal Entry",
            "Run Depreciation",
            "Reconcile Accounts",
            "Run Cost Allocation",
            "Generate Financial Statement",
            "Close Period",
        ],
    }

    flow = process_flows.get(process_type, process_flows["order-to-cash"])

    for _ in range(num_cases):
        case_id += 1
        base_time = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 90))
        for step_idx, activity in enumerate(flow):
            if random.random() < 0.1:
                continue
            timestamp = base_time + timedelta(hours=step_idx * random.randint(2, 48))
            events.append({
                "case_id": f"CASE-{case_id}",
                "activity": activity,
                "timestamp": timestamp,
                "resource": f"User-{random.randint(1, 20)}",
                "cost": round(random.uniform(10, 500), 2),
            })

    df = pd.DataFrame(events)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["case_id", "timestamp"]).reset_index(drop=True)
    return df


def extract_event_log_from_sap(table_prefix: str) -> pd.DataFrame:
    return generate_sample_event_log(table_prefix)
