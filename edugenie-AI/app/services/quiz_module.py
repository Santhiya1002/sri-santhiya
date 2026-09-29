from app.schemas.models import QuizResponse
from app.services.gemini_service import generate_structured


def generate_quiz(text: str) -> QuizResponse:

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational passage below.

Requirements:

1. Generate exactly 3 questions.
2. Every question must have exactly 4 options.
3. Each option must be different.
4. There must be exactly one correct answer.
5. The correct_answer must exactly match one option.
6. Questions must be based only on the supplied passage.
7. Do not invent information.
8. Make the distractors plausible.
9. Test understanding rather than only copying sentences.

Passage:
{text}
"""

    result = generate_structured(
        prompt,
        QuizResponse
    )

    if not isinstance(result, QuizResponse):
        result = QuizResponse.model_validate(result)

    return result
