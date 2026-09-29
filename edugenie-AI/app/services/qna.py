from app.services.gemini_service import generate_text


SYSTEM = """
You are EduGenie, a careful educational assistant.

Your job is to answer academic and educational questions.

Rules:
1. Give accurate information.
2. Use simple language.
3. Give the direct answer first.
4. Add a short explanation when useful.
5. Give examples when they help understanding.
6. Do not invent facts.
7. If the question is ambiguous, clearly state your assumption.
8. Avoid unnecessary jargon.
"""


def answer_question(question: str) -> str:

    prompt = f"""
Answer the following learner question.

Question:
{question}

Give the direct answer first.

Then provide:
- a short explanation
- an example if useful
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM
    )
