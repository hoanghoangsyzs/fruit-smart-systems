from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "sqlite:///./data/mit_system.db"
    secret_key: str = "dev-secret-change-in-production"
    mock_inference: bool = True
    artifacts_dir: str = "../ml/artifacts"
    upload_dir: str = "./uploads"
    gemini_api_key: str = ""
    gemini_model: str = "gemini-2.5-flash"
    roboflow_api_key: str = ""
    roboflow_model_id: str = ""
    roboflow_model_version: str = "1"
    roboflow_confidence: float = 0.35
    cors_origins: str = (
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5174,http://127.0.0.1:5174"
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def artifacts_path(self) -> Path:
        return Path(self.artifacts_dir).resolve()

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir).resolve()


settings = Settings()
