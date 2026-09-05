
import time

from google import genai
from google.genai import errors as genai_errors

from src.config import (
    GEMINI_API_KEY,
    MODEL_NAME,
    CAREER_NOTES_DIR
)

from src.generate.prompts import MENTOR_PROMPT


# ============================================================
# GEMINI CLIENT
# ============================================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ============================================================
# LOAD CAREER NOTES
# ============================================================

def load_career_notes():
    """
    Read all .txt files from the data/career_notes folder.
    """

    notes = []

    if not CAREER_NOTES_DIR.exists():
        return "No specific documents loaded."

    for file in CAREER_NOTES_DIR.glob("*.txt"):

        try:

            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

            if text.strip():

                notes.append(
                    f"--- {file.name} ---\n{text}"
                )

        except Exception as e:

            print(
                f"Could not read {file.name}: {e}"
            )

    combined_notes = "\n\n".join(notes)

    return (
        combined_notes
        if combined_notes.strip()
        else "No specific documents loaded."
    )


# ============================================================
# AI CAREER MENTOR
# ============================================================

def ask_mentor(question):
    """
    Answer a user's career-related question
    using career notes + Gemini.
    """

    context = load_career_notes()

    prompt = MENTOR_PROMPT.format(
        question=question,
        context=context
    )


    # ========================================================
    # PRIMARY MODEL + FALLBACK MODEL
    # ========================================================

    models_to_try = [
        MODEL_NAME,
        "gemini-3.1-flash-lite"
    ]


    # Remove duplicate model names
    models_to_try = list(dict.fromkeys(
        str(model)
        .replace("models/", "")
        .strip()
        for model in models_to_try
        if model
    ))


    last_exception = None


    # ========================================================
    # TRY EACH MODEL
    # ========================================================

    for model_id in models_to_try:

        for attempt in range(3):

            try:

                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt
                )

                return response.text


            # ====================================================
            # GEMINI CLIENT ERROR
            # ====================================================

            except genai_errors.ClientError as e:

                last_exception = e

                # -----------------------------------------------
                # RETRY 429 / 503
                # -----------------------------------------------

                if e.code in [429, 503]:

                    if attempt < 2:

                        # 3 sec → 6 sec → 12 sec
                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Current model failed.
                    # Try fallback model.
                    break


                # -----------------------------------------------
                # OTHER CLIENT ERRORS
                # -----------------------------------------------

                return (
                    f"❌ Gemini request failed "
                    f"({e.code}): {e.message}"
                )


            # ====================================================
            # OTHER ERRORS
            # ====================================================

            except Exception as e:

                last_exception = e

                error = str(e)


                # -----------------------------------------------
                # TEMPORARY SERVICE / QUOTA ERRORS
                # -----------------------------------------------

                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                    or "high demand" in error.lower()
                ):

                    if attempt < 2:

                        # 3 sec → 6 sec → 12 sec
                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Current model failed.
                    # Try fallback model.
                    break


                # -----------------------------------------------
                # MODEL NOT FOUND
                # -----------------------------------------------

                if (
                    "404" in error
                    or "NOT_FOUND" in error
                ):

                    # Try fallback model
                    break


                # -----------------------------------------------
                # OTHER UNEXPECTED ERROR
                # -----------------------------------------------

                return (
                    f"❌ Unexpected mentor error: {e}"
                )


    # ========================================================
    # ALL MODELS FAILED
    # ========================================================

    return (
        "❌ Gemini failed after trying all available models.\n\n"
        f"Last error: {last_exception}"
    )

