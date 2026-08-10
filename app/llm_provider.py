"""LLM adapter with an OpenAI provider and a local mock fallback."""

from __future__ import annotations

from functools import lru_cache

from .config import get_settings
from utils.mock_llm import generate_reply as generate_mock_reply


class LLMProviderError(RuntimeError):
    """A provider call failed without exposing provider details to clients."""


@lru_cache(maxsize=1)
def _get_openai_client(api_key: str):
    from openai import OpenAI

    return OpenAI(api_key=api_key)


def _usage_value(usage, name: str) -> int:
    value = getattr(usage, name, 0) if usage is not None else 0
    return int(value or 0)


def generate_reply(message: str, history: list[dict] | None = None) -> dict:
    """Generate a reply while preserving the contract used by the chat route.

    An ``OPENAI_API_KEY`` selects the real provider. Without it, tests and local
    development remain deterministic through the existing mock implementation.
    """
    settings = get_settings()
    if not settings.openai_api_key:
        return generate_mock_reply(message, history)

    messages = [
        {
            "role": "system",
            "content": "Bạn là trợ lý hữu ích. Trả lời rõ ràng, ngắn gọn bằng tiếng Việt.",
        },
        *(history or []),
        {"role": "user", "content": message},
    ]

    try:
        response = _get_openai_client(settings.openai_api_key).responses.create(
            model=settings.openai_model,
            input=messages,
        )
    except Exception as exc:  # SDK errors vary by transport and API status.
        raise LLMProviderError("OpenAI request failed") from exc

    prompt_tokens = _usage_value(response.usage, "input_tokens")
    completion_tokens = _usage_value(response.usage, "output_tokens")
    cost = (
        prompt_tokens / 1000 * settings.openai_input_price_per_1k
        + completion_tokens / 1000 * settings.openai_output_price_per_1k
    )
    return {
        "text": response.output_text,
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "usd_cost": round(cost, 8),
    }
