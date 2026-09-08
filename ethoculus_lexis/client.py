from typing import Any

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import get_settings
from .jsonpath import extract_dot_path


class LexisConfigurationError(RuntimeError):
    pass


class LexisClient:
    """
    Thin model/API adapter for LexisNexis.

    IMPORTANT:
    Endpoint paths and JSON fields must come from the
    customer's LexisNexis Developer Portal documentation.
    """

    def __init__(self):
        self.settings = get_settings()

        if not self.settings.lexis_api_base_url:
            raise LexisConfigurationError(
                "LEXIS_API_BASE_URL is not configured."
            )

        if not self.settings.lexis_protege_ask_path:
            raise LexisConfigurationError(
                "LEXIS_PROTEGE_ASK_PATH is not configured."
            )

        if not self.settings.lexis_prompt_field:
            raise LexisConfigurationError(
                "LEXIS_PROMPT_FIELD is not configured."
            )

        if not self.settings.lexis_access_token:
            raise LexisConfigurationError(
                "LEXIS_ACCESS_TOKEN is not configured. "
                "Obtain a token using the OAuth flow documented "
                "for your LexisNexis API account."
            )

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.settings.lexis_access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _url(self, path: str) -> str:
        return (
            self.settings.lexis_api_base_url.rstrip("/")
            + "/"
            + path.lstrip("/")
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=8),
        reraise=True,
    )
    def ask(self, prompt: str) -> dict[str, Any]:
        payload = {
            self.settings.lexis_prompt_field: prompt
        }

        with httpx.Client(
            timeout=self.settings.lexis_timeout_seconds
        ) as client:
            response = client.post(
                self._url(self.settings.lexis_protege_ask_path),
                headers=self._headers(),
                json=payload,
            )

            response.raise_for_status()

            data = response.json()

        answer = extract_dot_path(
            data,
            self.settings.lexis_response_text_path,
        )

        return {
            "answer": answer,
            "raw": data,
            "http_status": response.status_code,
            "request_id": (
                response.headers.get("x-request-id")
                or response.headers.get("request-id")
                or response.headers.get("correlation-id")
            ),
        }
