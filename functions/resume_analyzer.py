import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from google import genai
import warnings
from src.parsers.factory import parse_resume_to_record, extract_text_from_file
import math

warnings.filterwarnings('ignore')

class resume_analyzer:

    def extract_text_generic(uploaded_file):
        """
        Use parser factory to extract text from uploaded file.
        Accepts Streamlit UploadedFile or file-like.
        """
        try:
            record = parse_resume_to_record(uploaded_file, filename=getattr(uploaded_file, "name", None))
            return record
        except Exception as e:
            raise

    def _call_gemini(api_key: str, prompt: str) -> str:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=prompt
        )
        return response.text

    def _chunk_and_call_gemini(api_key: str, resume_text: str, analyze_prompt: str) -> str:
        """
        Gemini may have token limits; chunk the resume_text into ~3000 char blocks and send with prompt aggregate.
        (Simple naive chunking)
        """
        if not resume_text:
            return "No text extracted from resume."
        max_chars = 3000
        chunks = [resume_text[i:i+max_chars] for i in range(0, len(resume_text), max_chars)]
        answers = []
        for i, chunk in enumerate(chunks):
            prompt = f"Resume chunk {i+1}/{len(chunks)}:\n{chunk}\n\nAnalysis Request: {analyze_prompt}"
            try:
                ans = resume_analyzer._call_gemini(api_key, prompt)
                answers.append(ans)
            except Exception as e:
                answers.append(f"[ERROR calling Gemini on chunk {i+1}: {e}]")
        # naive aggregation
        return "\n\n".join(answers)

    # keep the original prompt builders
    def summary_prompt():
        return '''Please provide a detailed summarization of this resume including:
                    - Personal information and contact details
                    - Educational background
                    - Work experience and achievements
                    - Technical skills and competencies
                    - Key projects and accomplishments
                    - Overall professional profile
                    Finally, provide a conclusion about the candidate's profile.
                    '''

    def strength_prompt():
        return '''Please provide a detailed analysis of the strengths of this resume including:
                    - Technical skills and expertise
                    - Professional experience highlights
                    - Educational qualifications
                    - Project achievements
                    - Industry knowledge
                    - Soft skills demonstrated
                    Finally, conclude with the main competitive advantages of this candidate.
                    '''

    def weakness_prompt():
        return '''Please provide a detailed analysis of the weaknesses of this resume and suggestions for improvement:
                    - Areas that need more detail or clarification
                    - Missing information or skills
                    - Formatting or presentation issues
                    - Experience gaps or concerns
                    - Skills that could be better highlighted
                    - Specific recommendations for improvement
                    Finally, provide actionable steps to make this resume stronger.
                    '''

    def job_title_prompt():
        return '''Based on this resume, what are the most suitable job roles this candidate can apply for on LinkedIn? Please provide:
                    - Primary job titles that match perfectly
                    - Secondary job titles that could be a good fit
                    - Industries and company types to target
                    - Required skills to highlight in applications
                    - Career progression opportunities
                    Finally, rank the top 5 most suitable positions for this candidate.
                    '''

    # Generic wrapper for Streamlit forms to reduce repetition
    def _run_analysis_form(form_key: str, prompt_getter, title):
        with st.form(key=form_key):
            add_vertical_space(1)
            uploaded = st.file_uploader(label='Upload Your Resume (pdf/docx/png/jpg)', type=['pdf','docx','doc','png','jpg','jpeg'])
            add_vertical_space(1)
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)

        add_vertical_space(3)
        if submit:
            if uploaded is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                        record = resume_analyzer.extract_text_generic(uploaded)
                        resume_text = record.get("raw_text", "")
                        prompt = prompt_getter()
                        answer = resume_analyzer._chunk_and_call_gemini(gemini_api_key, resume_text, prompt)
                    st.markdown(f'<h4 style="color: orange;">{title}:</h4>', unsafe_allow_html=True)
                    st.write(answer)
                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)
            elif uploaded is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Gemini API Key</h5>', unsafe_allow_html=True)

    def resume_summary():
        return resume_analyzer._run_analysis_form('Summary', resume_analyzer.summary_prompt, "Summary")

    def resume_strength():
        return resume_analyzer._run_analysis_form('Strength', resume_analyzer.strength_prompt, "Strengths")

    def resume_weakness():
        return resume_analyzer._run_analysis_form('Weakness', resume_analyzer.weakness_prompt, "Weaknesses and Suggestions")

    def job_title_suggestion():
        return resume_analyzer._run_analysis_form('Job Titles', resume_analyzer.job_title_prompt, "Job Title Suggestions")
