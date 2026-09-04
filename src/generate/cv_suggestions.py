import time

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

    models_to_try = [
        MODEL_NAME,
        "gemini-2.5-flash-lite"
    ]

    last_exception = None

    for model_id in models_to_try:

        for attempt in range(3):

            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )

                return response.text

            except Exception as e:

                last_exception = e
                error = str(e)

                # Retry temporary 503 errors
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "high demand" in error.lower()
                ):
                    if attempt < 2:
                        time.sleep(5 * (attempt + 1))
                        continue

                    # Try the next model
                    break

                # Don't hide other errors
                raise

    raise RuntimeError(
        f"Could not generate resume suggestions: {last_exception}"
    )


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
