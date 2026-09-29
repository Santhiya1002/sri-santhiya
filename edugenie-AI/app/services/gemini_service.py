import time
from functools import lru_cache
from typing import Type

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.config import get_settings


class GeminiServiceError(RuntimeError):
    pass


@lru_cache
def get_client() -> genai.Client:
    settings = get_settings()

    if not settings.gemini_api_key:
        raise GeminiServiceError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(api_key=settings.gemini_api_key)


def _is_temporary_error(exc: Exception) -> bool:
    """
    Check whether the Gemini error is temporary and worth retrying.
    """
    error_text = str(exc).upper()

    temporary_errors = [
        "503",
        "UNAVAILABLE",
        "429",
        "RESOURCE_EXHAUSTED",
        "500",
        "INTERNAL",
        "DEADLINE_EXCEEDED",
    ]

    return any(error in error_text for error in temporary_errors)


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None
) -> str:

    settings = get_settings()

    config = types.GenerateContentConfig(
        max_output_tokens=2048,
        system_instruction=system_instruction,
    )

    last_error = None

    # Try up to 3 times
    for attempt in range(3):

        try:
            response = get_client().models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            text = (response.text or "").strip()

            if not text:
                raise GeminiServiceError(
                    "Gemini returned an empty response."
                )

            return text

        except GeminiServiceError:
            raise

        except Exception as exc:

            last_error = exc

            if _is_temporary_error(exc):

                if attempt < 2:
                    # Wait 3 seconds, then 6 seconds
                    wait_time = 3 * (2 ** attempt)

                    print(
                        f"Gemini temporary error. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            raise GeminiServiceError(
                f"Gemini request failed: {exc}"
            ) from exc

    raise GeminiServiceError(
        f"Gemini request failed after retries: {last_error}"
    )


def generate_structured(
    prompt: str,
    schema: Type[BaseModel]
) -> BaseModel:

    settings = get_settings()

    config = types.GenerateContentConfig(
        max_output_tokens=2500,
        response_mime_type="application/json",
        response_schema=schema,
    )

    last_error = None

    # Try up to 3 times
    for attempt in range(3):

        try:

            response = get_client().models.generate_content(
                model=settings.gemini_model,
                contents=prompt,
                config=config,
            )

            parsed = getattr(response, "parsed", None)

            if parsed is not None:
                return parsed

            text = (response.text or "").strip()

            if not text:
                raise GeminiServiceError(
                    "Gemini returned empty structured output."
                )

            return schema.model_validate_json(text)

        except GeminiServiceError:
            raise

        except Exception as exc:

            last_error = exc

            if _is_temporary_error(exc):

                if attempt < 2:
                    wait_time = 3 * (2 ** attempt)

                    print(
                        f"Gemini temporary error. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)
                    continue

            raise GeminiServiceError(
                f"Gemini structured request failed: {exc}"
            ) from exc

    raise GeminiServiceError(
        f"Gemini structured request failed after retries: {last_error}"
    )