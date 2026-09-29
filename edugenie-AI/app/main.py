from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import get_settings

from app.schemas.models import (
    ExplainRequest,
    HealthResponse,
    LearningPathRequest,
    QARequest,
    QuizResponse,
    SummaryRequest,
    TextResponse,
)

from app.services.explanation_module import explain_topic
from app.services.gemini_service import GeminiServiceError
from app.services.learning_path import get_learning_recommendations
from app.services.qna import answer_question
from app.services.quiz_module import generate_quiz
from app.services.summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent.parent

settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "EduGenie - Google Gemini powered "
        "AI educational learning assistant."
    ),
)


# Static files
app.mount(
    "/static",
    StaticFiles(
        directory=BASE_DIR / "static"
    ),
    name="static",
)


# Templates
templates = Jinja2Templates(
    directory=BASE_DIR / "Templates"
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get(
    "/",
    response_class=HTMLResponse,
)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "app_name": settings.app_name
        },
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get(
    "/health",
    response_model=HealthResponse,
)
async def health():

    return HealthResponse(
        status="ok",
        gemini_configured=bool(
            settings.gemini_api_key
        ),
        model=settings.gemini_model,
    )


# --------------------------------------------------
# Q&A
# --------------------------------------------------

@app.post(
    "/qa",
    response_model=TextResponse,
)
async def qa(request: QARequest):

    try:

        answer = answer_question(
            request.text
        )

        return TextResponse(
            result=answer
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# --------------------------------------------------
# EXPLAIN
# --------------------------------------------------

@app.post(
    "/explain",
    response_model=TextResponse,
)
async def explain(request: ExplainRequest):

    try:

        explanation = explain_topic(
            request.text
        )

        return TextResponse(
            result=explanation
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# --------------------------------------------------
# QUIZ
# --------------------------------------------------

@app.post(
    "/quiz",
    response_model=QuizResponse,
)
async def quiz(request: SummaryRequest):

    try:

        return generate_quiz(
            request.text
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

@app.post(
    "/summarize",
    response_model=TextResponse,
)
async def summarize(request: SummaryRequest):

    try:

        summary = summarize_text(
            request.text
        )

        return TextResponse(
            result=summary
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post(
    "/learn/recommendations",
    response_model=TextResponse,
)
async def learn(
    request: LearningPathRequest,
):

    try:

        recommendations = get_learning_recommendations(
            request.text,
            request.level,
        )

        return TextResponse(
            result=recommendations
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        )