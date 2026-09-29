from app.services.gemini_service import generate_text


SYSTEM = """
You are EduGenie's summarization tutor.

Your task is to summarize educational content.

Rules:
1. Preserve important facts.
2. Do not introduce facts that aren't in the source.
3. Remove unnecessary repetition.
4. Use simple learner-friendly language.
5. Keep the core meaning intact.
"""


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational passage.

Passage:

{text}

Return:

1. A short overview in 1-2 sentences.
2. 3-6 important key points.
3. Important terms if necessary.

Make the summary useful for quick revision.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM
    )
