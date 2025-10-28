# app.py
import streamlit as st
from src.parsers.factory import parse_resume_to_record
from src.ai_resume_analyzer.scoring.simple_score import simple_score
import tempfile

st.set_page_config(page_title="AI Resume Analyzer - Demo", layout="centered")

st.title("AI Resume Analyzer — Demo (Day 5)")

uploaded = st.file_uploader("Upload resume (pdf/docx/png/jpg)", type=["pdf","docx","png","jpg","jpeg"])
jd_text = st.text_area("Paste Job Description (optional)", height=200)

if st.button("Analyze (local)"):
    if uploaded is None and not jd_text:
        st.warning("Please upload a resume or paste a job description.")
    else:
        if uploaded:
            # streamlit's UploadedFile has .getvalue()
            content = uploaded.getvalue()
            rec = parse_resume_to_record(content, filename=uploaded.name)
        else:
            rec = {"source_file": "jd", "raw_text": jd_text, "name": "", "emails": [], "phones": [], "skills": [], "experiences": []}
        score, explain = simple_score(rec, jd_text or rec.get("raw_text",""))
        st.subheader("Parsed record")
        st.json(rec)
        st.subheader("Score")
        st.write(score)
        st.subheader("Explain")
        st.json(explain)

        if st.checkbox("Show raw text"):
            st.text(rec.get("raw_text",""))
