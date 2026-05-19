from typing import Optional, Any
from app.connectors.sap_rfc import rfc_connector


def sap_data_agent_execute(query: str) -> dict[str, Any]:
    table_mapping = {
        "sales order": "VBAK",
        "order": "VBAK",
        "order item": "VBAP",
        "purchase order": "EKKO",
        "po": "EKKO",
        "po item": "EKPO",
        "vendor": "LFA1",
        "customer": "KNA1",
        "material": "MARA",
        "invoice": "BKPF",
        "delivery": "LIKP",
    }

    query_lower = query.lower()
    matched_table = None
    for keyword, table in table_mapping.items():
        if keyword in query_lower:
            matched_table = table
            break

    if matched_table:
        try:
            df = rfc_connector.read_table(matched_table)
            records = df.to_dict(orient="records")
            return {
                "type": "data",
                "table": matched_table,
                "row_count": len(records),
                "data": records[:20],
                "answer": f"Retrieved {len(records)} records from SAP table {matched_table}.",
            }
        except Exception as e:
            return {
                "type": "error",
                "answer": f"Error accessing SAP data: {str(e)}",
            }

    return {
        "type": "general",
        "answer": f"Processed query: '{query}'. Connect to SAP ECC/S4HANA to retrieve live data. Configure SAP connection settings in .env file.",
    }
