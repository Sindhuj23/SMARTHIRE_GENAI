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
    return combined_notes if combined_notes.strip() else "No specific documents loaded."


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

    try:

        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )

        return response.text

    except genai_errors.ClientError as e:

        if e.code == 429:

            return (
                "⚠️ The AI mentor has hit its daily free-tier "
                "quota with Gemini. Please try again later, or "
                "switch to a model/plan with a higher limit."
            )

        return f"❌ Gemini request failed ({e.code}): {e.message}"

    except Exception as e:

        return f"❌ Unexpected mentor error: {e}"