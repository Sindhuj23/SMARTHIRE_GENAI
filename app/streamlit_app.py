import sys
from pathlib import Path
import math

# Automatically resolve project root regardless of whether app.py is placed in root or a subfolder
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR if (CURRENT_DIR / "src").exists() else CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import streamlit as st

from src.parsing.loader import load_resume
from src.parsing.resume_parser import parse_resume
from src.search.job_search import match_jobs
from src.generate.cv_suggestions import generate_cv_suggestions
from src.mentor.rag_chain import ask_mentor


# Helper function to prevent pandas NaN/None values from rendering as 'nan' or 'None'
def get_clean_field(row, field, default=""):
    val = row.get(field, default)
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return default
    val_str = str(val).strip()
    if val_str.lower() in ("nan", "none", "<na>", "null", ""):
        return default
    return val_str


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="SmartHire GenAI — Career Portal & AI Mentor",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# SESSION STATE
# =========================================================

if "profile" not in st.session_state:
    st.session_state.profile = None

if "resume_text" not in st.session_state:
    st.session_state.resume_text = None

if "cv_suggestions" not in st.session_state:
    st.session_state.cv_suggestions = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "job_results" not in st.session_state:
    st.session_state.job_results = None


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0e1117;
    }

    .block-container {
        padding-top: 2rem !important;
    }

    /* =====================================================
       MAIN TITLE
       ===================================================== */

   .main-title {
    font-size: 40px !important;
    font-weight: 800 !important;
    text-align: center !important;
    margin-top: 0px !important;
    margin-bottom: 5px !important;
    background: linear-gradient(90deg, #7C3AED, #C084FC) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    text-shadow: none !important;
    box-shadow: none !important;
    filter: none !important;
}

    /* =====================================================
       SUBTITLE
       ===================================================== */

    .subtitle {
        text-align: center;
        font-size: 18px;
        font-weight: 600;
        color: #c4b5fd !important;
        margin-top: 0px;
        margin-bottom: 15px;
        text-shadow: none !important;
    }

    /* =====================================================
       SECTION TITLES
       ===================================================== */

    .section-title {
        color: #8b5cf6 !important;
        font-size: 30px !important;
        font-weight: 800 !important;
        margin-top: 10px !important;
        margin-bottom: 15px !important;
    }

    /* =====================================================
       DASHBOARD CARDS
       ===================================================== */

    .card {
        background-color: #161b22;
        padding: 18px;
        border-radius: 18px;
        border: 1px solid #30363d;
        margin-bottom: 12px;
    }

    /* =====================================================
       SKILL TAGS
       ===================================================== */

    .skill {
        display: inline-block;
        padding: 7px 12px;
        margin: 4px;
        border-radius: 20px;
        background-color: #21262d;
        border: 1px solid #30363d;
    }

    /* =====================================================
       SIDEBAR TITLE
       ===================================================== */

    [data-testid="stSidebar"] h2 {
        color: #d8b4fe !important;
        text-shadow: none !important;
        box-shadow: none !important;
        filter: none !important;
    }

    /* =====================================================
       RESUME IMPROVEMENT RESULT BOX
       ===================================================== */

    .improvement-box {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-left: 4px solid #8b5cf6;
        border-radius: 12px;
        padding: 18px;
        margin-top: 15px;
        margin-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🗝️ SmartHire")

    st.markdown("---")

    page = st.radio(
        "🧭 Navigation",
        [
            "🏠 Dashboard",
            "📄 Resume Analyzer",
            "👤 My Profile",
            "💼 Job Matches",
            "✨ Resume Improvement",
            "🤖 AI Career Mentor",
            "📊 System Evaluation"
        ]
    )

    st.markdown("---")

    if st.session_state.profile is not None:

        st.success("✅ Resume profile loaded.")

    else:

        st.info(
            "💡 Analyze your resume first to unlock personalized features."
        )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="main-title">
        🚀 SmartHire GenAI — Career Portal &amp; AI Mentor
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="subtitle">
        🤖 AI-Powered Resume &amp; Career Assistant
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="card">
            <h2>👋 Welcome to SmartHire!</h2>
            <p>
            SmartHire is an AI-powered career assistant that analyzes
            resumes, matches jobs, improves CVs, provides career
            guidance and evaluates system performance.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 📄")
        st.markdown("**Resume Analyzer**")
        st.write(
            "Extract skills, education, experience and projects."
        )

    with col2:

        st.markdown("### 👤")
        st.markdown("**My Profile**")
        st.write(
            "View your extracted resume profile."
        )

    with col3:

        st.markdown("### 💼")
        st.markdown("**Job Matching**")
        st.write(
            "Match your profile with suitable jobs."
        )

    col4, col5, col6 = st.columns(3)

    with col4:

        st.markdown("### 🤖")
        st.markdown("**AI Career Mentor**")
        st.write(
            "Ask questions about careers and learning paths."
        )

    with col5:

        st.markdown("### ✨")
        st.markdown("**Resume Improvement**")
        st.write(
            "Get AI suggestions to improve your resume."
        )

    with col6:

        st.markdown("### 📊")
        st.markdown("**System Evaluation**")
        st.write(
            "Evaluate the quality and performance of SmartHire."
        )


# =========================================================
# RESUME ANALYZER
# =========================================================

elif page == "📄 Resume Analyzer":

    st.markdown(
        '<div class="section-title">📄 Resume Analyzer</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Upload your PDF or DOCX resume."
    )

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx"]
    )

    if uploaded_file:

        st.success(
            f"✅ {uploaded_file.name} uploaded."
        )

        if st.button(
            "🔍 Analyze Resume",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Analyzing your resume..."
            ):

                try:

                    file_bytes = uploaded_file.getvalue()

                    resume_text = load_resume(
                        file_bytes,
                        uploaded_file.name
                    )

                    if not resume_text.strip():

                        st.error(
                            "❌ No readable text found."
                        )

                    else:

                        profile = parse_resume(
                            resume_text
                        )

                        st.session_state.profile = profile
                        st.session_state.resume_text = resume_text

                        # Clear previous AI suggestions & job results
                        st.session_state.cv_suggestions = None
                        st.session_state.job_results = None

                        st.success(
                            "Resume analyzed successfully!"
                        )

                        st.info(
                            "✅ Your resume profile is saved. "
                            "You can now open My Profile or Job Matches."
                        )

                except Exception as e:

                    st.error(
                        f"❌ Resume analysis failed: {e}"
                    )


# =========================================================
# MY PROFILE
# =========================================================

elif page == "👤 My Profile":

    st.markdown(
        '<div class="section-title">👤 My AI Profile</div>',
        unsafe_allow_html=True
    )

    if st.session_state.profile is None:

        st.info(
            "📄 Analyze your resume first."
        )

    else:

        profile = st.session_state.profile

        name = getattr(
            profile,
            "name",
            "Not available"
        )

        target_role = getattr(
            profile,
            "target_role",
            "Not available"
        )

        email = getattr(
            profile,
            "email",
            "Not available"
        )

        phone = getattr(
            profile,
            "phone",
            "Not available"
        )

        st.markdown(
            f"""
            <div class="card">
                <h2>👋 {name}</h2>
                <p>🎯 <b>Target Role:</b> {target_role}</p>
                <p>📧 <b>Email:</b> {email}</p>
                <p>📱 <b>Phone:</b> {phone}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        # =================================================
        # SKILLS
        # =================================================

        st.subheader("🛠️ Skills")

        skills = getattr(
            profile,
            "skills",
            []
        )

        if skills:

            for skill in skills:

                st.markdown(
                    f'<span class="skill">🔹 {skill}</span>',
                    unsafe_allow_html=True
                )

        else:

            st.info(
                "No skills detected."
            )

        # =================================================
        # EDUCATION
        # =================================================

        st.subheader("🎓 Education")

        education = getattr(
            profile,
            "education",
            []
        )

        if education:

            for item in education:

                st.write(
                    f"🎓 {item}"
                )

        else:

            st.info(
                "No education information found."
            )

        # =================================================
        # EXPERIENCE
        # =================================================

        st.subheader("💼 Experience")

        experience = getattr(
            profile,
            "experience",
            []
        )

        if experience:

            for item in experience:

                st.write(
                    f"💼 {item}"
                )

        else:

            st.info(
                "No experience found."
            )

        # =================================================
        # PROJECTS
        # =================================================

        st.subheader("🚀 Projects")

        projects = getattr(
            profile,
            "projects",
            []
        )

        if projects:

            for item in projects:

                st.write(
                    f"🔹 {item}"
                )

        else:

            st.info(
                "No projects found."
            )

        # =================================================
        # CERTIFICATIONS
        # =================================================

        st.subheader("🏆 Certifications")

        certifications = getattr(
            profile,
            "certifications",
            []
        )

        if certifications:

            for item in certifications:

                st.write(
                    f"🏆 {item}"
                )

        else:

            st.info(
                "No certifications found."
            )

        # =================================================
        # DELETE PROFILE
        # =================================================

        st.markdown("---")

        st.subheader("⚙️ Profile Management")

        st.write(
            "Your profile remains available while this session is active."
        )

        if st.button(
            "🗑️ Delete Resume & Profile",
            use_container_width=True
        ):

            st.session_state.profile = None
            st.session_state.resume_text = None
            st.session_state.cv_suggestions = None
            st.session_state.messages = []
            st.session_state.job_results = None

            st.success(
                "✅ Resume and profile deleted successfully."
            )

            st.rerun()


# =========================================================
# JOB MATCHES
# =========================================================

elif page == "💼 Job Matches":

    st.markdown(
        '<div class="section-title">💼 AI Job Matches</div>',
        unsafe_allow_html=True
    )

    if st.session_state.profile is None:

        st.info(
            "📄 Please analyze your resume first."
        )

    else:

        profile = st.session_state.profile

        skills = getattr(
            profile,
            "skills",
            []
        )

        target_role = getattr(
            profile,
            "target_role",
            ""
        )

        st.success(
            "✅ Your resume profile is ready for job matching."
        )

        st.subheader("🎯 Job Search")

        job_role = st.text_input(
            "Enter the job role you want",
            value=target_role
        )

        location = st.text_input(
            "Preferred location",
            value="India"
        )

        number_of_jobs = st.slider(
            "Number of jobs to display",
            min_value=5,
            max_value=25,
            value=10
        )

        if st.button(
            "🔎 Find Matching Jobs",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 Searching available jobs..."
            ):

                try:

                    results = match_jobs(
                        skills=skills,
                        target_role=job_role,
                        location=location,
                        top_n=number_of_jobs
                    )

                    st.session_state.job_results = results

                except Exception as e:

                    st.error(
                        f"❌ Job matching failed: {e}"
                    )

        # Render results if available
        results = st.session_state.job_results

        if results is not None:

            if results.empty:

                st.error(
                    f"❌ **Job Role Not Found!** No jobs matching **'{job_role}'** were found in the dataset."
                )
                st.info(
                    "💡 **Tip:** Try searching for standard job roles like **Data Analyst**, **Software Engineer**, **Data Scientist**, **Web Developer**, or **Java Developer**."
                )

            else:

                st.success(
                    f" Found {len(results)} matching jobs for '{job_role}'!"
                )

                for _, row in results.iterrows():

                    job_title = get_clean_field(
                        row,
                        "jobtitle",
                        "Job Title Not Available"
                    )

                    company = get_clean_field(
                        row,
                        "company",
                        "Company Not Available"
                    )

                    job_location = get_clean_field(
                        row,
                        "joblocation_address",
                        "Location Not Available"
                    )

                    score = row.get(
                        "match_score",
                        0
                    )

                    job_skills = get_clean_field(
                        row,
                        "skills",
                        ""
                    )

                    description = get_clean_field(
                        row,
                        "jobdescription",
                        ""
                    )

                    education = get_clean_field(
                        row,
                        "education",
                        ""
                    )

                    experience = get_clean_field(
                        row,
                        "experience",
                        ""
                    )

                    payrate = get_clean_field(
                        row,
                        "payrate",
                        ""
                    )

                    with st.container(
                        border=True
                    ):

                        st.subheader(
                            f"💼 {job_title}"
                        )

                        st.write(
                            f"🏢 **Company:** {company}"
                        )

                        st.write(
                            f"📍 **Location:** {job_location}"
                        )

                        st.write(
                            f"🎯 **Match Score:** {score}"
                        )

                        if education:

                            st.write(
                                f"🎓 **Education:** {education}"
                            )

                        if experience:

                            st.write(
                                f"💼 **Experience:** {experience}"
                            )

                        if payrate:

                            st.write(
                                f"💰 **Pay:** {payrate}"
                            )

                        if job_skills:

                            st.write(
                                f"🛠️ **Required Skills:** {job_skills}"
                            )

                        if description:

                            if len(description) > 500:

                                description = (
                                    description[:500]
                                    + "..."
                                )

                            st.write(
                                f"📝 **Description:** {description}"
                            )


# =========================================================
# RESUME IMPROVEMENT
# =========================================================

elif page == "✨ Resume Improvement":

    st.markdown(
        '<div class="section-title">✨ AI Resume Improvement</div>',
        unsafe_allow_html=True
    )

    if st.session_state.resume_text is None:

        st.info(
            "📄 Please upload and analyze your resume first."
        )

    else:

        st.success(
            "✅ Resume is ready for AI improvement."
        )

        if st.button(
            "✨ Improve My Resume",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 AI is analyzing your resume..."
            ):

                try:

                    suggestions = generate_cv_suggestions(
                        st.session_state.resume_text
                    )

                    st.session_state.cv_suggestions = suggestions

                    st.success(
                        "Resume improvement suggestions generated!"
                    )

                except Exception as e:

                    st.error(
                        f"❌ Could not generate resume suggestions: {e}"
                    )

        # =================================================
        # DISPLAY RESULT ONLY ONCE
        # =================================================

        if st.session_state.cv_suggestions is not None:

            st.markdown("---")

            st.markdown(
                """
                <div class="improvement-box">
                    <div class="section-title"
                         style="font-size:24px !important;
                                margin-top:0px !important;">
                        💡 AI Resume Improvement
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                st.session_state.cv_suggestions
            )


# =========================================================
# AI CAREER MENTOR
# =========================================================

elif page == "🤖 AI Career Mentor":

    st.markdown(
        '<div class="section-title">🤖 AI Career Mentor</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Ask questions about careers, jobs, skills, interviews, "
        "projects and learning paths."
    )

    if st.button(
        "🗑️ Clear Chat"
    ):

        st.session_state.messages = []

        st.rerun()

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"]
        ):

            st.markdown(
                message["content"]
            )

    question = st.chat_input(
        "💬 Ask your career question..."
    )

    if question:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):

            st.markdown(
                question
            )

        with st.chat_message("assistant"):

            with st.spinner(
                "🤖 Thinking..."
            ):

                try:

                    answer = ask_mentor(
                        question
                    )

                    st.markdown(
                        answer
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": answer
                        }
                    )

                except Exception as e:

                    error_message = (
                        f"❌ Mentor error: {e}"
                    )

                    st.error(
                        error_message
                    )

                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "content": error_message
                        }
                    )


# =========================================================
# SYSTEM EVALUATION
# =========================================================

elif page == "📊 System Evaluation":

    st.markdown(
        '<div class="section-title">📊 System Evaluation</div>',
        unsafe_allow_html=True
    )

    st.write(
        "Evaluate the performance and quality of the SmartHire GenAI system."
    )

    st.markdown("---")

    st.subheader("🧪 Evaluation Modules")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 📄 Resume Analysis

            Evaluates whether important resume information
            can be extracted correctly.
            """
        )

        st.markdown(
            """
            ### 💼 Job Matching

            Evaluates whether relevant jobs are returned
            for the user's skills and target role.
            """
        )

    with col2:

        st.markdown(
            """
            ### ✨ Resume Improvement

            Evaluates the usefulness and relevance of
            AI-generated resume suggestions.
            """
        )

        st.markdown(
            """
            ### 🤖 Career Mentor

            Evaluates whether career questions receive
            useful and relevant answers.
            """
        )

    st.markdown("---")

    st.subheader("📈 Run System Evaluation")

    if st.button(
        "▶️ Run Evaluation",
        use_container_width=True
    ):

        with st.spinner(
            "📊 Evaluating SmartHire system..."
        ):

            try:

                from src.evaluate import evaluate_system

                evaluation = evaluate_system()

                st.success(
                    "✅ System evaluation completed."
                )

                if isinstance(
                    evaluation,
                    dict
                ):

                    if len(evaluation) > 0:

                        metric_cols = st.columns(
                            len(evaluation)
                        )

                        for index, (
                            key,
                            value
                        ) in enumerate(
                            evaluation.items()
                        ):

                            with metric_cols[index]:

                                st.metric(
                                    label=str(key),
                                    value=str(value)
                                )

                    else:

                        st.info(
                            "ℹ️ No evaluation metrics were returned."
                        )

                else:

                    st.markdown(
                        str(evaluation)
                    )

            except ImportError:

                st.warning(
                    "⚠️ System Evaluation is available, "
                    "but evaluate_system() was not found "
                    "in src/evaluate.py."
                )

            except Exception as e:

                st.error(
                    f"❌ Evaluation failed: {e}"
                )
