from typing import Optional
import pandas as pd
from app.config import settings


class SAPRFCConnector:
    def __init__(self):
        self.connection = None
        self.enabled = settings.sap_ecc_enabled

    def connect(self):
        if not self.enabled:
            raise RuntimeError("SAP ECC RFC connector is disabled")
        try:
            from pyrfc import Connection
            self.connection = Connection(
                ashost=settings.sap_ecc_ashost,
                sysnr=settings.sap_ecc_sysnr,
                client=settings.sap_ecc_client,
                user=settings.sap_ecc_user,
                passwd=settings.sap_ecc_passwd,
                lang=settings.sap_ecc_lang,
            )
        except ImportError:
            raise RuntimeError("pyrfc is not installed. Install with: pip install pyrfc")

    def read_table(self, table_name: str, fields: Optional[list[str]] = None, options: Optional[str] = None, rowcount: int = 1000) -> pd.DataFrame:
        if table_name not in settings.SAP_TABLE_ALLOWLIST:
            raise ValueError(f"Table '{table_name}' is not in the allowlist")
        if not self.enabled or not self.connection:
            return self._generate_sample_data(table_name)
        try:
            result = self.connection.call(
                "RFC_READ_TABLE",
                QUERY_TABLE=table_name,
                DELIMITER="|",
                ROWCOUNT=rowcount,
                FIELDS=[{"FIELDNAME": f} for f in fields] if fields else [],
                OPTIONS=[{"TEXT": options}] if options else [],
            )
            data = [row["WA"].split("|") for row in result["DATA"]]
            field_names = [f["FIELDNAME"] for f in result["FIELDS"]]
            return pd.DataFrame(data, columns=field_names)
        except Exception as e:
            raise RuntimeError(f"RFC_READ_TABLE failed for {table_name}: {e}")

    def _generate_sample_data(self, table_name: str) -> pd.DataFrame:
        sample_schemas = {
            "VBAK": {"VBELN": ["1001", "1002", "1003"], "AUART": ["TA", "TA", "RE"], "NETWR": [1500.0, 2300.0, 890.0], "ERDAT": ["2024-01-15", "2024-01-16", "2024-01-17"]},
            "VBAP": {"VBELN": ["1001", "1001", "1002"], "POSNR": ["10", "20", "10"], "MATNR": ["M-01", "M-02", "M-01"], "KWMENG": [10, 5, 20]},
            "EKKO": {"EBELN": ["4500001", "4500002", "4500003"], "BUKRS": ["1000", "1000", "2000"], "AEDAT": ["2024-01-10", "2024-01-12", "2024-01-14"]},
            "EKPO": {"EBELN": ["4500001", "4500001", "4500002"], "EBELP": ["10", "20", "10"], "MATNR": ["M-10", "M-11", "M-10"], "MENGE": [100, 50, 200]},
        }
        if table_name in sample_schemas:
            return pd.DataFrame(sample_schemas[table_name])
        return pd.DataFrame({"column": ["sample"]})

    def close(self):
        if self.connection:
            try:
                self.connection.close()
            except Exception:
                pass
            self.connection = None


rfc_connector = SAPRFCConnector()
