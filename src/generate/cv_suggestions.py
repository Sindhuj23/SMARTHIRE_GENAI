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
        "gemini-3.1-flash-lite"
    ]

    # Remove duplicate model names
    models_to_try = list(dict.fromkeys(
        str(model).replace("models/", "").strip()
        for model in models_to_try
        if model
    ))

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

                # Retry temporary Gemini errors
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    if attempt < 2:

                        # 3 sec → 6 sec → 12 sec
                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Current model failed.
                    # Move to fallback model.
                    break

                # Do not hide other errors
                raise

    raise RuntimeError(
        f"Could not generate resume suggestions: "
        f"{last_exception}"
    )


def generate_cover_letter(resume, job):

    prompt = COVER_LETTER_PROMPT.format(
        resume=resume,
        job=job
    )

    models_to_try = [
        MODEL_NAME,
        "gemini-3.1-flash-lite"
    ]

    # Remove duplicate model names
    models_to_try = list(dict.fromkeys(
        str(model).replace("models/", "").strip()
        for model in models_to_try
        if model
    ))

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

                # Retry temporary Gemini errors
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    if attempt < 2:

                        # 3 sec → 6 sec → 12 sec
                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Try fallback model
                    break

                # Do not hide other errors
                raise

    raise RuntimeError(
        f"Could not generate cover letter: "
        f"{last_exception}"
    )
