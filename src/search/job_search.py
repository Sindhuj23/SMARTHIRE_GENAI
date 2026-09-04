import pandas as pd
import numpy as np
import re
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JOBS_CSV = DATA_DIR / "jobs" / "naukri_com-job_sample.csv"


def normalize_text(text):
    if pd.isna(text):
        return ""
    text = str(text).lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def load_naukri_dataset():
    """Load and clean dataset."""
    if not JOBS_CSV.exists():
        csv_files = list((DATA_DIR / "jobs").glob("*.csv"))
        if not csv_files:
            return pd.DataFrame()
        job_file = csv_files[0]
    else:
        job_file = JOBS_CSV

    try:
        df = pd.read_csv(job_file, encoding="utf-8", on_bad_lines="skip")
    except UnicodeDecodeError:
        df = pd.read_csv(job_file, encoding="latin1", on_bad_lines="skip")

    df['jobtitle'] = df['jobtitle'].fillna('')
    df['company'] = df['company'].fillna('Not Disclosed')
    df['joblocation_address'] = df['joblocation_address'].fillna('India')
    df['skills'] = df['skills'].fillna('')
    df['jobdescription'] = df['jobdescription'].fillna('')
    df['experience'] = df['experience'].fillna('N/A')
    df['payrate'] = df['payrate'].fillna('Not Disclosed')

    return df


def filter_by_role(df, target_role):
    """
    Strictly filter by target role words in the job title.
    If no matches exist, returns an empty DataFrame instead of falling back to unrelated jobs.
    """
    if not target_role or not str(target_role).strip():
        return pd.DataFrame()

    norm_role = normalize_text(target_role)
    role_words = [w for w in norm_role.split() if len(w) > 1]

    if not role_words:
        return pd.DataFrame()

    # STRICT MATCH: ALL keywords typed by user must exist in the job title
    def strict_title_match(title):
        norm_title = normalize_text(title)
        return all(word in norm_title for word in role_words)

    filtered = df[df['jobtitle'].apply(strict_title_match)].copy()

    # If role doesn't exist in the dataset, return empty DataFrame (Do NOT fall back to full df)
    if filtered.empty:
        return pd.DataFrame()

    return filtered


def match_jobs(skills=None, target_role="Data Analyst", location="India", top_n=10):
    """
    Match candidate profile strictly against target role in India.
    Returns empty DataFrame if the role is not found.
    """
    # PERMANENTLY LOCK LOCATION TO INDIA
    location = "India"

    df = load_naukri_dataset()
    if df.empty:
        return pd.DataFrame()

    # Strict role filter
    df_matched = filter_by_role(df, target_role)

    # IF ROLE NOT FOUND IN DATASET, RETURN EMPTY DATAFRAME IMMEDIATELY
    if df_matched.empty:
        return pd.DataFrame()

    skills_list = skills if isinstance(skills, list) else []
    norm_skills = [normalize_text(s) for s in skills_list if s]

    # Calculate match score for found jobs
    scores = []
    norm_target_role = normalize_text(target_role)

    for _, row in df_matched.iterrows():
        job_title = normalize_text(row['jobtitle'])
        job_text = normalize_text(f"{row['jobdescription']} {row['skills']} {row['company']}")

        score = 60  # Base score for passing exact title match

        if norm_target_role == job_title:
            score += 20

        for skill in norm_skills:
            if skill and (skill in job_text or skill in job_title):
                score += 5

        scores.append(min(score, 100))

    df_matched = df_matched.copy()
    df_matched["match_score"] = scores

    df_sorted = df_matched.sort_values(by="match_score", ascending=False)
    return df_sorted.head(top_n)
