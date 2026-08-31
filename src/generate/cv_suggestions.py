from google import genai

from src.config import GEMINI_API_KEY, MODEL_NAME
from src.generate.prompts import (
    CV_PROMPT,
    COVER_LETTER_PROMPT
)


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_cv_suggestions(resume):

    prompt = CV_PROMPT.format(
        resume=resume
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text


def generate_cover_letter(resume, job):

    prompt = COVER_LETTER_PROMPT.format(
        resume=resume,
        job=job
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
