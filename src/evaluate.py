from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

JOBS_FILE = PROJECT_ROOT / "data" / "jobs" / "naukri_com-job_sample.csv"


def evaluate_system():
    results = {}

    try:
        from src.parsing.loader import load_resume
        from src.parsing.resume_parser import parse_resume
        results["Resume Analyzer"] = "Available"
    except Exception:
        results["Resume Analyzer"] = "Error"

    try:
        from src.search.job_search import match_jobs
        results["Job Matching"] = "Available"
    except Exception:
        results["Job Matching"] = "Error"

    try:
        from src.generate.cv_suggestions import generate_cv_suggestions
        results["Resume Improvement"] = "Available"
    except Exception:
        results["Resume Improvement"] = "Error"

    try:
        from src.mentor.rag_chain import ask_mentor
        results["Career Mentor"] = "Available"
    except Exception:
        results["Career Mentor"] = "Error"

    try:
        if JOBS_FILE.exists():
            df = pd.read_csv(JOBS_FILE)
            results["Job Database Rows"] = len(df)
        else:
            results["Job Database Rows"] = "File not found"
    except Exception:
        results["Job Database Rows"] = "Error"

    available = sum(
        1
        for key, value in results.items()
        if value == "Available"
    )

    results["Modules Available"] = f"{available}/4"

    if available == 4:
        results["Overall Status"] = "System Ready"
    else:
        results["Overall Status"] = "Some Modules Need Attention"

    return results