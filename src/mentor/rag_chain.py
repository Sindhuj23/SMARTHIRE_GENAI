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

    # Primary model + fallback model
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

            except genai_errors.ClientError as e:

                last_exception = e

                # Retry temporary Gemini errors
                if e.code in [429, 503]:

                    if attempt < 2:

                        # 3 sec → 6 sec → 12 sec
                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Current model failed.
                    # Move to fallback model.
                    break

                # Other Gemini errors should not be
                # repeatedly retried.
                return (
                    f"❌ Gemini request failed "
                    f"({e.code}): {e.message}"
                )

            except Exception as e:

                last_exception = e

                error = str(e)

                # Handle temporary service errors
                if (
                    "503" in error
                    or "UNAVAILABLE" in error
                    or "429" in error
                    or "RESOURCE_EXHAUSTED" in error
                ):

                    if attempt < 2:

                        time.sleep(
                            3 * (2 ** attempt)
                        )

                        continue

                    # Try fallback model
                    break

                return f"❌ Unexpected mentor error: {e}"

    return (
        "⚠️ Gemini is temporarily unavailable. "
        "The AI Career Mentor automatically tried "
        "again and used its fallback model, but the "
        "request could not be completed right now. "
        "Please try again in a moment."
    )
