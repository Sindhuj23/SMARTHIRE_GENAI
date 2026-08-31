# SmartHire GenAI — Final Project Report

## 1. Project Title

**SmartHire GenAI — AI-Powered Career, Resume and Job Search Assistant**

---

## 2. Introduction

SmartHire GenAI is an AI-powered career assistance system designed to help students and job seekers with resume analysis, career guidance, job recommendations, interview preparation, and general career-related questions.

The system combines Generative AI, semantic search, embeddings, FAISS vector search, and Retrieval-Augmented Generation (RAG) to provide useful and personalized responses.

The main goal of the project is to provide a single platform where users can upload a resume, understand their skills, receive suitable job recommendations, and obtain career guidance based on a curated career knowledge base.

---

## 3. Problem Statement

Students and job seekers often face difficulties in:

- Understanding which career role matches their skills.
- Finding suitable job opportunities.
- Identifying missing skills in their resume.
- Preparing for interviews.
- Creating effective resumes.
- Getting reliable career guidance.

Traditional job search systems mainly depend on keyword matching and may not understand the semantic meaning of a candidate's skills and experience.

SmartHire GenAI addresses this problem using semantic embeddings and Generative AI.

---

## 4. Objectives

The main objectives of SmartHire GenAI are:

1. Extract useful information from uploaded resumes.
2. Identify candidate skills, education, experience, and target role.
3. Recommend relevant jobs using semantic similarity.
4. Provide AI-based career guidance.
5. Build a RAG-based career mentor using curated career notes.
6. Reduce hallucination by grounding mentor responses in retrieved career information.
7. Provide a simple web interface using Streamlit.
8. Evaluate retrieval relevance and answer quality.

---

## 5. Technologies Used

### Programming Language

- Python

### Generative AI

- Google Gemini API

### AI / Machine Learning

- Gemini Embeddings
- Semantic Similarity
- Retrieval-Augmented Generation (RAG)

### Vector Search

- FAISS

### NLP

- Text processing
- Text chunking
- Embeddings
- Semantic retrieval

### Frameworks and Libraries

- Streamlit
- LangChain
- NumPy
- Pandas
- python-dotenv
- PyPDF
- Python-docx

### Development Tools

- Visual Studio Code
- Google Colab
- Jupyter Notebook
- GitHub

---

# 6. System Architecture

The SmartHire GenAI system consists of several major components.

```text
                         SmartHire GenAI
                               |
              +----------------+----------------+
              |                |                |
         Resume Parser     Job Search      AI Career Mentor
              |                |                |
          Resume File       Job CSV          Career Notes
              |                |                |
          Text Extract      Job Text       Text Chunking
              |                |                |
          Gemini LLM       Embeddings       Embeddings
              |                |                |
        Structured JSON      FAISS            FAISS
              |                |                |
              +----------------+----------------+
                               |
                         Streamlit App
                               |
                              User
```

---

# 7. Resume Parser

The resume parser accepts a resume document and extracts important candidate information.

The extracted profile contains fields such as:

- Name
- Email
- Phone
- Target role
- Skills
- Education
- Experience
- Projects
- Certifications

The extracted information is returned as structured JSON.

Example:

```json
{
  "name": "SINDHU",
  "email": "example@gmail.com",
  "target_role": "AI/ML Engineer",
  "skills": ["Python", "SQL", "Machine Learning", "Deep Learning"]
}
```

The structured profile can then be used by the job search and career guidance components.

---

# 8. Semantic Job Search

The system uses a job dataset containing information such as:

- Job title
- Skills
- Job description
- Company
- Location
- Industry
- Experience
- Education

The job title, skills, and job description are combined into a single text representation.

Example:

```text
Job Title + Skills + Job Description
```

These job descriptions are converted into embeddings using the Gemini embedding model.

The embeddings are stored in a FAISS vector index.

When a candidate profile is provided, the profile is also converted into an embedding.

FAISS then searches for the most semantically similar jobs.

This approach allows the system to identify related jobs even when the exact keywords are different.

---

# 9. FAISS Vector Search

FAISS is used as the vector similarity search engine.

The process is:

```text
Job Dataset
     ↓
Combine Job Information
     ↓
Generate Embeddings
     ↓
Create FAISS Index
     ↓
Store Job Vectors
     ↓
Candidate Profile
     ↓
Generate Candidate Embedding
     ↓
Search FAISS
     ↓
Top-N Relevant Jobs
```

The system returns the closest jobs along with similarity or distance scores.

---

# 10. AI Career Mentor

The Career Mentor provides career guidance using a Retrieval-Augmented Generation approach.

Career notes are stored in:

```text
data/career_notes/
```

The current career knowledge base includes guides such as:

- Data Analyst
- Business Analyst
- GenAI Engineer
- ML Engineer
- Interview Roadmap

The notes are loaded and divided into smaller chunks.

Each chunk is converted into a Gemini embedding and stored in a FAISS index.

---

# 11. RAG Pipeline

The Career Mentor follows this process:

```text
User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Retrieve Top-K Career Note Chunks
      ↓
Add Retrieved Context to Prompt
      ↓
Gemini
      ↓
Grounded Career Answer
```

For example, when the user asks:

```text
How can I become a Data Analyst?
```

the system retrieves the Data Analyst career notes and uses them as context for generating the answer.

---

# 12. Grounding and Hallucination Prevention

A strict mentor prompt was created to ensure that the Career Mentor uses the provided career notes.

The prompt instructs the model to:

- Use only the retrieved career notes.
- Avoid inventing information.
- Refuse questions that cannot be answered from the notes.
- Clearly state when the information is unavailable.

For example, an out-of-scope question such as:

```text
Who is the Prime Minister of India?
```

should result in:

```text
I don't know based on the provided career notes.
```

This provides a basic hallucination control mechanism.

---

# 13. Career Knowledge Base

The career notes provide focused information about different roles.

### Data Analyst

The guide contains information about:

- SQL
- Excel
- Python
- Power BI
- Tableau
- Statistics
- Portfolio projects
- Interviews
- Common beginner weaknesses

### Business Analyst

The guide covers:

- Requirement gathering
- Documentation
- SQL
- Excel
- Process mapping
- Communication
- Agile/Scrum
- Interview preparation

### GenAI Engineer

The guide provides information about the skills and learning path relevant to Generative AI engineering.

### ML Engineer

The guide provides information about machine learning engineering skills and career preparation.

### Interview Roadmap

The interview roadmap provides guidance for preparing for technical and career interviews.

---

# 14. General AI Assistant

In addition to the Career Mentor, SmartHire GenAI includes a general AI engine.

The general AI assistant can answer questions related to:

- Programming
- Python
- SQL
- Machine Learning
- Artificial Intelligence
- Data Science
- Education
- Projects
- Resume writing
- Interview preparation
- Career guidance
- Emails
- Cover letters
- Study plans
- General explanations

Therefore, the application is not restricted only to the career roles present in the career notes.

---

# 15. Streamlit Application

Streamlit is used to provide a simple web interface.

The application allows users to interact with the SmartHire GenAI system without directly running Python code.

The application integrates the major components:

```text
Streamlit UI
    |
    +---- Resume Upload
    |
    +---- Resume Parser
    |
    +---- Candidate Profile
    |
    +---- Job Search
    |
    +---- Career Mentor
    |
    +---- General AI Assistant
```

---

# 16. Project Structure

```text
smarthire-genai/
│
├── .streamlit/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── jobs/
│   │   └── naukrijobs.csv
│   │
│   └── career_notes/
│       ├── career_guide.txt
│       ├── data_analyst.txt
│       ├── business_analyst.txt
│       ├── genai_engineer.txt
│       ├── ml_engineer.txt
│       └── interview_roadmap.txt
│
├── notebooks/
│   ├── 01_embeddings_explore.ipynb
│   ├── 02_build_faiss.ipynb
│   └── 03_rag_prototype.ipynb
│
├── reports/
│   ├── answer_quality.md
│   └── final_report.md
│
├── src/
│   ├── parsing/
│   ├── search/
│   ├── generate/
│   ├── mentor/
│   └── safety/
│
├── vectorstore/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 17. Notebook Prototypes

Three notebooks were developed as prototypes.

## Notebook 1 — Embeddings & Resume Parser

File:

```text
notebooks/01_embeddings_explore.ipynb
```

This notebook demonstrates:

- Resume text extraction
- Resume parsing
- Structured JSON generation
- Gemini embeddings
- Cosine similarity
- Comparison of related and unrelated sentences

---

## Notebook 2 — FAISS Job Search

File:

```text
notebooks/02_build_faiss.ipynb
```

This notebook demonstrates:

- Loading the job CSV
- Combining job information
- Generating job embeddings
- Building the FAISS index
- Candidate profile embedding
- Top-N semantic job retrieval

---

## Notebook 3 — RAG Career Mentor

File:

```text
notebooks/03_rag_prototype.ipynb
```

This notebook demonstrates:

- Loading career notes
- Chunking career notes
- Creating embeddings
- Building the FAISS notes index
- Retrieving relevant career information
- Creating the RAG prompt
- Generating grounded answers
- Testing out-of-scope questions

---

# 18. Evaluation

The system was evaluated using retrieval relevance and Career Mentor answer quality.

### Retrieval Evaluation

Sample candidate profiles were used to determine whether the retrieved jobs were relevant to the candidate's skills and target role.

### Mentor Evaluation

The Career Mentor was tested using:

1. A question answerable from the career notes.
2. An out-of-scope question.
3. A question requiring information from multiple career notes.

The evaluation results are documented separately in:

```text
reports/answer_quality.md
```

---

# 19. Results

The prototype successfully demonstrated the following:

- Resume information can be extracted into structured JSON.
- Gemini embeddings can represent resume, job, and career-note text.
- FAISS can retrieve semantically similar jobs.
- Data Analyst queries retrieved Data Analyst information as the highest-ranked result.
- Related Business Analyst information was also retrieved for related queries.
- Career notes can be used as a knowledge source for RAG.
- The Career Mentor can generate answers using retrieved context.
- The system includes a prompt-based mechanism to reduce hallucination.
- A general AI engine can answer questions beyond the predefined career roles.

---

# 20. Limitations

The current prototype has some limitations:

- Job recommendations depend on the quality and coverage of the job dataset.
- Career Mentor answers are limited by the information available in the career notes.
- Embedding generation can take time for large datasets.
- Gemini API usage may have rate limits or costs.
- The hallucination guardrail is primarily prompt-based in the current prototype.
- Evaluation was performed on a relatively small set of test cases.

---

# 21. Future Improvements

Future versions can include:

1. More career roles and detailed career knowledge.
2. Larger and regularly updated job datasets.
3. Better candidate-job ranking using multiple features.
4. Resume improvement suggestions.
5. Skill-gap analysis.
6. Personalized learning plans.
7. Interview question generation based on the candidate's resume.
8. Stronger safety and hallucination detection.
9. User authentication and profile storage.
10. Deployment as a production web application.
11. Multilingual career guidance.
12. Job recommendations based on location, experience, and salary preferences.

---

# 22. Conclusion

SmartHire GenAI demonstrates how Generative AI, embeddings, FAISS, semantic search, and Retrieval-Augmented Generation can be combined to build an intelligent career assistance platform.

The system can analyze resumes, recommend semantically relevant jobs, and provide grounded career guidance using a curated knowledge base.

The project also demonstrates the importance of evaluation and hallucination control in Generative AI applications.

Overall, SmartHire GenAI provides a foundation for a practical AI-powered career assistant that can be further improved with larger datasets, stronger evaluation, additional career roles, and production-level deployment.
