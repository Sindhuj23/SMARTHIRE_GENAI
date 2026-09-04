import time
from google import genai
from pydantic import BaseModel, Field
from typing import List
from src.config import GEMINI_API_KEY, MODEL_NAME


client = genai.Client(api_key=GEMINI_API_KEY)


class ResumeProfile(BaseModel):

    name: str = Field(
        description="Full name of the candidate"
    )

    email: str = Field(
        description="Email address of the candidate"
    )

    phone: str = Field(
        description="Phone number of the candidate"
    )

    target_role: str = Field(
        description="Most suitable target job role"
    )

    skills: List[str] = Field(
        description="Technical and professional skills"
    )

    education: List[str] = Field(
        description="Education qualifications"
    )

    experience: List[str] = Field(
        description=(
            "Work experience entries. Each list item must represent "
            "exactly ONE job/internship (one company + role + date "
            "range), combining ALL of that job's responsibilities and "
            "achievements into a single string. Do NOT create a "
            "separate list item for each bullet point or "
            "responsibility under the same job — group them together "
            "under one entry per company."
        )
    )

    projects: List[str] = Field(
        description="Projects mentioned in the resume"
    )

    certifications: List[str] = Field(
        description="Certifications mentioned in the resume"
    )


def parse_resume(resume_text):

    prompt = f"""
You are an expert resume information extraction system.

Extract information from the following resume.

IMPORTANT:
- Do not invent information.
- If information is missing, return an empty string or empty list.
- Keep the extracted information faithful to the resume.
- Identify the most suitable target role based only on the resume.

CRITICAL RULE FOR EXPERIENCE:
- Each experience entry must represent ONE job/internship only
  (one company, one role, one date range).
- If a job has multiple responsibilities or achievements listed
  as bullet points in the resume, merge ALL of them into a single
  combined string for that one job.
- Do NOT repeat the same company name and role across multiple
  list entries. Each distinct job should appear exactly once in
  the experience list.

Resume:

{resume_text}
"""

    # Backup models if primary MODEL_NAME experiences high demand / 503 errors
    fallback_models = [MODEL_NAME, "gemini-1.5-flash", "gemini-2.0-flash"]
    models_to_try = list(dict.fromkeys(fallback_models))

    last_exception = None

    for model_id in models_to_try:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_id,
                    contents=prompt,
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": ResumeProfile,
                    },
                )
                return ResumeProfile.model_validate_json(response.text)

            except Exception as e:
                last_exception = e
                err_str = str(e)
                # Retry if server is unavailable (503) or rate-limited (429)
                if "503" in err_str or "UNAVAILABLE" in err_str or "429" in err_str:
                    time.sleep(2 * (attempt + 1))  # Exponential delay (2s, 4s, 6s)
                    continue
                else:
                    raise e

    raise RuntimeError(
        f"Resume parsing failed due to high server load: {last_exception}"
    )
