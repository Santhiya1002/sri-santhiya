from functools import lru_cache

from app.config import get_settings
from app.services.gemini_service import generate_text


@lru_cache
def _get_local_pipeline():

    from transformers import pipeline

    settings = get_settings()

    return pipeline(
        "text2text-generation",
        model=settings.local_explainer_model,
        max_new_tokens=180,
    )


def _local_explain(topic: str) -> str:

    prompt = (
        "Explain this topic simply for a beginner. "
        "Use a short definition, an analogy, "
        "and one example: "
        + topic
    )

    result = _get_local_pipeline()(prompt)

    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:

    settings = get_settings()

    if settings.use_local_explainer:

        try:
            return _local_explain(topic)

        except Exception:
            pass

    prompt = f"""
Explain the following topic to a beginner.

Topic:
{topic}

Use this structure:

1. Simple definition
2. How it works
3. Easy analogy
4. One concrete example
5. One-line recap

Make the explanation easy to understand.
Avoid unnecessary technical jargon.
"""

    return generate_text(
        prompt,
        system_instruction=(
            "You are a patient educational tutor "
            "who simplifies complex concepts."
        ),
    )
