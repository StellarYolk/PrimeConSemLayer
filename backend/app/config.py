from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    llm_provider: str = "openrouter"
    llm_model: str = "google/gemma-4-31b-it:free"
    openrouter_api_key: Optional[str] = None
    openrouter_base_url: str = "https://openrouter.ai/api/v1"

    sap_ecc_enabled: bool = False
    sap_ecc_ashost: Optional[str] = None
    sap_ecc_sysnr: Optional[str] = None
    sap_ecc_client: Optional[str] = None
    sap_ecc_user: Optional[str] = None
    sap_ecc_passwd: Optional[str] = None
    sap_ecc_lang: str = "EN"

    sap_odata_enabled: bool = False
    sap_odata_base_url: Optional[str] = None
    sap_odata_user: Optional[str] = None
    sap_odata_passwd: Optional[str] = None

    database_url: str = "postgresql+asyncpg://primecon:primecon_secret@localhost:5432/primecon"
    redis_url: str = "redis://localhost:6379/0"
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    SAP_TABLE_ALLOWLIST: list[str] = [
        "VBAK", "VBAP", "VBKD", "EKKO", "EKPO", "EKET",
        "LIKP", "LIPS", "BKPF", "BSEG", "CDHDR", "CDPOS",
        "MARA", "MARC", "MAKT", "KNA1", "LFA1", "T001",
    ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=self.llm_model,
            openai_api_key=self.openrouter_api_key,
            openai_api_base=self.openrouter_base_url,
            temperature=0.1,
        )


settings = Settings()
