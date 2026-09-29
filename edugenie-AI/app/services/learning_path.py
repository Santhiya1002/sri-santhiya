from app.services.gemini_service import generate_text


SYSTEM = """
You are EduGenie, an educational curriculum-planning assistant.

Create practical learning paths.

Do not invent specific URLs.

When suggesting resources, prefer:
- official documentation
- established books
- well-known learning platforms
- general video/course recommendations
"""


def get_learning_recommendations(
    topic: str,
    level: str
) -> str:

    prompt = f"""
Create a structured learning path for:

Topic:
{topic}

Learner level:
{level}

Structure the answer as:

1. Learning goal
2. Prerequisites
3. Stage 1 - Foundations
4. Stage 2 - Intermediate concepts
5. Stage 3 - Advanced concepts
6. Practice exercises
7. Mini projects
8. Revision checkpoints
9. Recommended resources
10. Suggested weekly timeline

Make the plan practical and achievable.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM
    )
