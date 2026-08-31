# Evaluation Report — Answer Quality & Retrieval

## 1. Retrieval Relevance — Semantic Job Search

The semantic job search was tested using sample candidate profiles. The system retrieves jobs based on the similarity between the candidate profile and job descriptions, skills, and job titles.

| Sample Profile            | Top Job 1    | Relevant? | Top Job 2        | Relevant? | Top Job 3      | Relevant? | Top Job 4          | Relevant? | Top Job 5     | Relevant? | Hit Rate |
| ------------------------- | ------------ | --------- | ---------------- | --------- | -------------- | --------- | ------------------ | --------- | ------------- | --------- | -------- |
| Python + SQL fresher      | Data Analyst | Yes       | Business Analyst | Yes       | Data Engineer  | Yes       | Software Developer | Yes       | ML Engineer   | Yes       | 100%     |
| Machine Learning + Python | ML Engineer  | Yes       | GenAI Engineer   | Yes       | Data Scientist | Yes       | Data Analyst       | Yes       | AI Engineer   | Yes       | 100%     |
| Power BI + SQL + Excel    | Data Analyst | Yes       | Business Analyst | Yes       | BI Developer   | Yes       | Reporting Analyst  | Yes       | Data Engineer | Yes       | 100%     |

### Hit Rate

Hit Rate = Number of relevant retrieved jobs / Total retrieved jobs × 100

The retrieved jobs were generally related to the skills and target roles in the sample profiles.

---

## 2. Answer Quality — AI Career Mentor

The AI Career Mentor was tested using questions related to the career notes.

| Question                                                             | Correct? | Grounded in Notes? | Helpful? | Notes                                                      |
| -------------------------------------------------------------------- | -------- | ------------------ | -------- | ---------------------------------------------------------- |
| How can I become a Data Analyst?                                     | Yes      | Yes                | Yes      | The answer used the Data Analyst career guide.             |
| What skills are required for a Business Analyst?                     | Yes      | Yes                | Yes      | The answer was based on the Business Analyst career guide. |
| What skills are useful for both a Data Analyst and Business Analyst? | Yes      | Yes                | Yes      | Information from both career guides was retrieved.         |

---

## 3. Prompt Comparison — Before / After

### Before

The initial prompt allowed the model to answer questions generally without strictly restricting the response to the career notes.

Example:

```text
Answer the user's question about careers and provide useful career guidance.
```

### After

The RAG prompt was improved to make the mentor answer only from the retrieved career notes.

```text
You are SmartHire AI Career Mentor.

Answer the user's question using ONLY the career notes provided below.

If the answer cannot be found in the career notes, say:
"I don't know based on the provided career notes."

Do not invent information.
Do not use outside knowledge.

Career notes:
{context}

User question:
{question}

Answer clearly and practically.
```

### What changed and why

The improved prompt explicitly restricts the model to the retrieved career notes. It also provides a fixed response for questions that cannot be answered from the notes.

This reduces the possibility of hallucination and makes the Career Mentor more grounded in the provided knowledge base.

---

## 4. Hallucination Check

An out-of-scope question was used to test whether the mentor would generate information that was not present in the career notes.

| Out-of-scope Question               | Did it Refuse? |
| ----------------------------------- | -------------- |
| Who is the Prime Minister of India? | Yes            |

### Expected behavior

The mentor should respond:

```text
I don't know based on the provided career notes.
```

The system should not use outside knowledge to answer questions that are not covered by the career notes.

---

## 5. Overall Evaluation

The evaluation showed that:

- FAISS successfully retrieved semantically related job and career-note content.
- Data Analyst queries retrieved Data Analyst information as the highest-ranked result.
- Related roles such as Business Analyst were also retrieved when appropriate.
- The Career Mentor generated answers using retrieved career-note context.
- The out-of-scope test was used to check hallucination.
- The improved prompt provides stronger grounding by restricting answers to the retrieved notes.

## Conclusion

The SmartHire GenAI prototype successfully combines semantic search, Gemini embeddings, FAISS retrieval, and a RAG-based Career Mentor. The evaluation demonstrates that the system can retrieve relevant information and generate career guidance grounded in the provided career notes.
