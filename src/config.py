import os
from pathlib import Path

from dotenv import load_dotenv


# =========================================================
# PROJECT ROOT
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

load_dotenv(PROJECT_ROOT / ".env")


# =========================================================
# GEMINI
# =========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-3.5-flash"
)


# =========================================================
# DATA DIRECTORIES
# =========================================================

DATA_DIR = PROJECT_ROOT / "data"

JOBS_DIR = DATA_DIR / "jobs"

RESUMES_DIR = DATA_DIR / "resumes"

CAREER_NOTES_DIR = DATA_DIR / "career_notes"


# =========================================================
# CREATE DIRECTORIES
# =========================================================

JOBS_DIR.mkdir(
    parents=True,
    exist_ok=True
)

RESUMES_DIR.mkdir(
    parents=True,
    exist_ok=True
)

CAREER_NOTES_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# =========================================================
# API KEY CHECK
# =========================================================

if not GEMINI_API_KEY:
    print(
        "WARNING: GEMINI_API_KEY is not set."
    )