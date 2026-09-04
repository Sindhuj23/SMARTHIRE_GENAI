import pandas as pd
from pathlib import Path
import re


# =========================================================
# PROJECT PATH
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = DATA_DIR / "jobs"


# =========================================================
# FIND JOB DATASET
# =========================================================

def find_job_file():
    """
    Find the first CSV file inside data/jobs.
    """

    csv_files = list(JOBS_DIR.glob("*.csv"))

    if not csv_files:
        return None

    return csv_files[0]


# =========================================================
# LOAD JOB DATASET
# =========================================================

def load_jobs():
    """
    Load jobs from the CSV dataset.
    """

    job_file = find_job_file()

    if job_file is None:
        return pd.DataFrame()

    try:

        df = pd.read_csv(
            job_file,
            encoding="utf-8",
            on_bad_lines="skip"
        )

    except UnicodeDecodeError:

        df = pd.read_csv(
            job_file,
            encoding="latin1",
            on_bad_lines="skip"
        )

    except Exception:

        return pd.DataFrame()

    # Clean column names
    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    return df


# =========================================================
# FIND RELEVANT TEXT COLUMNS
# =========================================================

def get_text_columns(df):

    possible_columns = [
        "job_title",
        "title",
        "job",
        "position",
        "role",
        "designation",
        "skills",
        "skill",
        "description",
        "job_description",
        "requirements",
        "location",
        "company",
        "company_name"
    ]

    columns = []

    for column in df.columns:

        column_lower = column.lower()

        for possible in possible_columns:

            if possible in column_lower:

                columns.append(column)
                break

    return list(dict.fromkeys(columns))


# =========================================================
# FIND LOCATION-SPECIFIC COLUMNS
# =========================================================

def get_location_columns(df):
    """
    Identify columns that represent job location specifically.
    """

    columns = [
        column
        for column in df.columns
        if "location" in column.lower()
        or "city" in column.lower()
        or "country" in column.lower()
        or "address" in column.lower()
    ]

    return columns


# =========================================================
# NORMALIZE TEXT
# =========================================================

def normalize_text(text):

    if pd.isna(text):
        return ""

    text = str(text).lower()

    text = re.sub(
        r"[^a-z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# JOB MATCHING
# =========================================================

def match_jobs(
    skills=None,
    target_role="",
    location="India",
    top_n=10
):
    """
    Match a user's profile against jobs in the dataset strictly for India.
    Location is locked to India regardless of user input.
    """

    # STRICTLY FORCE LOCATION TO INDIA
    location = "india"

    df = load_jobs()

    if df.empty:
        return pd.DataFrame()

    # -----------------------------------------------------
    # User profile text
    # -----------------------------------------------------

    skills = skills or []

    user_skills = [
        normalize_text(skill)
        for skill in skills
        if skill
    ]

    target_role = normalize_text(
        target_role
    )

    # -----------------------------------------------------
    # Dataset text columns
    # -----------------------------------------------------

    text_columns = get_text_columns(df)

    if not text_columns:

        text_columns = [
            column
            for column in df.columns
            if df[column].dtype == "object"
        ]

    location_columns = get_location_columns(df)

    if not location_columns:

        location_columns = text_columns

    # -----------------------------------------------------
    # STRICT INDIA LOCATION FILTER
    # -----------------------------------------------------

    def location_matches(row):

        location_text = " ".join(
            normalize_text(row[column])
            for column in location_columns
        )

        # Recognize India or any Indian city/state in the dataset
        indian_locations = [
            "india", "bangalore", "bengaluru", "mumbai", "delhi", "pune",
            "hyderabad", "chennai", "noida", "gurgaon", "gurugram", "kolkata",
            "ahmedabad", "surat", "jaipur", "chandigarh", "indore", "kochi",
            "kerala", "coimbatore", "vadodara", "nagpur", "ghaziabad"
        ]

        return any(loc in location_text for loc in indian_locations)

    filtered_df = df[df.apply(location_matches, axis=1)]

    # Keep filtered Indian jobs if matches found
    if not filtered_df.empty:
        df = filtered_df

    # -----------------------------------------------------
    # Calculate score (role + skills)
    # -----------------------------------------------------

    scores = []

    for _, row in df.iterrows():

        job_text = " ".join(
            normalize_text(row[column])
            for column in text_columns
        )

        score = 0

        # Target role matching
        if target_role:

            role_words = target_role.split()

            for word in role_words:

                if len(word) > 2 and word in job_text:
                    score += 20

        # Skill matching
        matched_skills = []

        for skill in user_skills:

            if skill and skill in job_text:

                score += 10
                matched_skills.append(skill)

        scores.append(
            {
                "score": score,
                "matched_skills": matched_skills
            }
        )

    # -----------------------------------------------------
    # Add scores to dataframe
    # -----------------------------------------------------

    df = df.copy()

    df["match_score"] = [
        item["score"]
        for item in scores
    ]

    df["matched_skills"] = [
        ", ".join(item["matched_skills"])
        for item in scores
    ]

    # -----------------------------------------------------
    # Sort
    # -----------------------------------------------------

    df = df.sort_values(
        by="match_score",
        ascending=False
    )

    # Return top jobs
    return df.head(top_n)


# =========================================================
# SIMPLE SEARCH FUNCTION
# =========================================================

def search_jobs(
    query,
    location="India",
    top_n=10
):
    """
    Search jobs using a text query strictly for India.
    """

    # STRICTLY FORCE LOCATION TO INDIA
    location = "india"

    df = load_jobs()

    if df.empty:
        return pd.DataFrame()

    query = normalize_text(query)

    text_columns = get_text_columns(df)

    if not text_columns:

        text_columns = [
            column
            for column in df.columns
            if df[column].dtype == "object"
        ]

    location_columns = get_location_columns(df)

    if not location_columns:

        location_columns = text_columns

    # -----------------------------------------------------
    # STRICT INDIA LOCATION FILTER
    # -----------------------------------------------------

    def location_matches(row):

        location_text = " ".join(
            normalize_text(row[column])
            for column in location_columns
        )

        indian_locations = [
            "india", "bangalore", "bengaluru", "mumbai", "delhi", "pune",
            "hyderabad", "chennai", "noida", "gurgaon", "gurugram", "kolkata",
            "ahmedabad", "surat", "jaipur", "chandigarh", "indore", "kochi",
            "kerala", "coimbatore", "vadodara", "nagpur", "ghaziabad"
        ]

        return any(loc in location_text for loc in indian_locations)

    filtered_df = df[df.apply(location_matches, axis=1)]

    if not filtered_df.empty:
        df = filtered_df

    scores = []

    for _, row in df.iterrows():

        job_text = " ".join(
            normalize_text(row[column])
            for column in text_columns
        )

        score = 0

        for word in query.split():

            if len(word) > 2 and word in job_text:

                score += 1

        scores.append(score)

    df = df.copy()

    df["match_score"] = scores

    df = df.sort_values(
        by="match_score",
        ascending=False
    )

    return df.head(top_n)
