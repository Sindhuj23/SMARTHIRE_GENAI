import os
from pathlib import Path
from dotenv import load_dotenv
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# 1. API Key retrieval
if "GEMINI_API_KEY" in st.secrets:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
else:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 2. Default to gemini-1.5-flash to prevent 503 capacity issues
if "MODEL_NAME" in st.secrets:
    MODEL_NAME = st.secrets["MODEL_NAME"]
else:
    MODEL_NAME = os.getenv("MODEL_NAME", "gemini-1.5-flash")

# Data directories setup
DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = DATA_DIR / "jobs"
RESUMES_DIR = DATA_DIR / "resumes"
CAREER_NOTES_DIR = DATA_DIR / "career_notes"

for directory in [JOBS_DIR, RESUMES_DIR, CAREER_NOTES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
