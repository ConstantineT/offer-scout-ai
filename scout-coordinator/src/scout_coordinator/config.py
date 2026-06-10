import json
from functools import lru_cache
from typing import Any

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


def _parse_json_secret(value: str, name: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"{name} must be valid JSON") from exc

    if not isinstance(parsed, dict):
        raise ValueError(f"{name} must be a JSON object")

    return parsed


class Settings(BaseSettings):
    resend_credentials: str = ""
    resend_api_key: str = ""
    resend_webhook_secret: str = ""
    resend_from_email: str = "Offer Scout <scout@your-domain>"
    resend_base_url: str = "https://api.resend.com"
    resend_timeout_seconds: float = 30.0

    scout_agent_base_url: str = "http://localhost:8080"
    scout_agent_timeout_seconds: float = 120.0
    scout_agent_auth_mode: str = "none"
    scout_agent_audience: str = ""
    profile_context: str = "Software engineer interested in remote work."

    task_backend: str = "local"
    cloud_tasks_project: str = ""
    cloud_tasks_location: str = ""
    cloud_tasks_queue: str = ""
    cloud_tasks_target_url: str = ""
    cloud_tasks_service_account_email: str = ""
    cloud_tasks_oidc_audience: str = ""
    cloud_tasks_dispatch_deadline_seconds: int = 600
    max_attachment_bytes: int = 5 * 1024 * 1024
    max_offer_text_chars: int = 50_000
    local_task_retry_attempts: int = 3

    app_name: str = "scout-coordinator"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    @model_validator(mode="after")
    def apply_combined_credentials(self):
        if self.resend_credentials:
            credentials = _parse_json_secret(self.resend_credentials, "RESEND_CREDENTIALS")
            self.resend_api_key = str(credentials.get("api_key") or self.resend_api_key)
            self.resend_webhook_secret = str(credentials.get("webhook_secret") or self.resend_webhook_secret)
            self.resend_from_email = str(credentials.get("from_email") or self.resend_from_email)

        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
