from typing import Optional
import httpx
import pandas as pd
from app.config import settings


class SAPODataConnector:
    def __init__(self):
        self.client: Optional[httpx.AsyncClient] = None
        self.enabled = settings.sap_odata_enabled

    async def connect(self):
        if not self.enabled:
            raise RuntimeError("SAP OData connector is disabled")
        self.client = httpx.AsyncClient(
            base_url=settings.sap_odata_base_url,
            auth=(settings.sap_odata_user or "", settings.sap_odata_passwd or ""),
            timeout=30.0,
        )

    async def get_entity_set(self, entity_set: str, top: int = 100, filter_expr: Optional[str] = None) -> pd.DataFrame:
        if not self.enabled or not self.client:
            return self._generate_sample_data(entity_set)
        params = {"$top": top, "$format": "json"}
        if filter_expr:
            params["$filter"] = filter_expr
        response = await self.client.get(f"/{entity_set}", params=params)
        response.raise_for_status()
        data = response.json()
        results = data.get("d", {}).get("results", data.get("value", data.get("results", [])))
        return pd.DataFrame(results)

    def _generate_sample_data(self, entity_set: str) -> pd.DataFrame:
        sample_schemas = {
            "C_PurchaseOrderTP": {"PurchaseOrder": ["4500001", "4500002"], "CompanyCode": ["1000", "1000"], "CreationDate": ["2024-01-10", "2024-01-12"]},
            "C_SalesOrderTP": {"SalesOrder": ["1001", "1002"], "SalesOrganization": ["1000", "1000"], "CreationDate": ["2024-01-15", "2024-01-16"]},
            "C_InvoiceTP": {"Invoice": ["9000001", "9000002"], "CompanyCode": ["1000", "1000"], "PostingDate": ["2024-01-20", "2024-01-21"]},
        }
        if entity_set in sample_schemas:
            return pd.DataFrame(sample_schemas[entity_set])
        return pd.DataFrame({"entity": [entity_set], "sample": [True]})

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None


odata_connector = SAPODataConnector()
