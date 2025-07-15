import streamlit as st
import time
from streamlit_extras.add_vertical_space import add_vertical_space
from PyPDF2 import PdfReader
from google import genai
import warnings
warnings.filterwarnings('ignore')

class resume_analyzer:

    def pdf_to_text(pdf):
        """
        Extract text from PDF file
        """
        # read pdf and it returns memory address
        pdf_reader = PdfReader(pdf)

        # extract text from each page separately
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        return text


    def gemini_analyze_simple(gemini_api_key, resume_text, analyze_prompt):
        """
        Simple analysis using Google Gemini without vector search
        """
        # Create the prompt with full resume context
        prompt = f"""
        Resume Content:
        {resume_text}
        
        Analysis Request: {analyze_prompt}
        
        Please provide a detailed and comprehensive analysis based on the resume content above.
        """
        
        # Initialize Gemini client
        client = genai.Client(api_key=gemini_api_key)
        
        # Generate response using Gemini
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp", 
            contents=prompt
        )
        
        return response.text


    def summary_prompt():
        """
        Create prompt for resume summary
        """
        query = '''Please provide a detailed summarization of this resume including:
                    - Personal information and contact details
                    - Educational background
                    - Work experience and achievements
                    - Technical skills and competencies
                    - Key projects and accomplishments
                    - Overall professional profile
                    Finally, provide a conclusion about the candidate's profile.
                    '''
        return query


    def strength_prompt():
        """
        Create prompt for resume strengths analysis
        """
        query = '''Please provide a detailed analysis of the strengths of this resume including:
                    - Technical skills and expertise
                    - Professional experience highlights
                    - Educational qualifications
                    - Project achievements
                    - Industry knowledge
                    - Soft skills demonstrated
                    Finally, conclude with the main competitive advantages of this candidate.
                    '''
        return query


    def weakness_prompt():
        """
        Create prompt for resume weaknesses analysis
        """
        query = '''Please provide a detailed analysis of the weaknesses of this resume and suggestions for improvement:
                    - Areas that need more detail or clarification
                    - Missing information or skills
                    - Formatting or presentation issues
                    - Experience gaps or concerns
                    - Skills that could be better highlighted
                    - Specific recommendations for improvement
                    Finally, provide actionable steps to make this resume stronger.
                    '''
        return query


    def job_title_prompt():
        """
        Create prompt for job title suggestions
        """
        query = '''Based on this resume, what are the most suitable job roles this candidate can apply for on LinkedIn? Please provide:
                    - Primary job titles that match perfectly
                    - Secondary job titles that could be a good fit
                    - Industries and company types to target
                    - Required skills to highlight in applications
                    - Career progression opportunities
                    Finally, rank the top 5 most suitable positions for this candidate.
                    '''
        return query


    def resume_summary():
        """
        Generate resume summary using Gemini
        """
        with st.form(key='Summary'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Gemini API Key
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):

                        # Extract text from PDF
                        resume_text = resume_analyzer.pdf_to_text(pdf)

                        # Get summary prompt
                        summary_prompt = resume_analyzer.summary_prompt()

                        # Generate summary using Gemini
                        summary = resume_analyzer.gemini_analyze_simple(
                            gemini_api_key=gemini_api_key, 
                            resume_text=resume_text, 
                            analyze_prompt=summary_prompt
                        )

                    st.markdown(f'<h4 style="color: orange;">Summary:</h4>', unsafe_allow_html=True)
                    st.write(summary)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Gemini API Key</h5>', unsafe_allow_html=True)


    def resume_strength():
        """
        Analyze resume strengths using Gemini
        """
        with st.form(key='Strength'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Gemini API Key
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)

        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        # Extract text from PDF
                        resume_text = resume_analyzer.pdf_to_text(pdf)

                        # Get strength prompt
                        strength_prompt = resume_analyzer.strength_prompt()

                        # Generate strength analysis using Gemini
                        strength = resume_analyzer.gemini_analyze_simple(
                            gemini_api_key=gemini_api_key, 
                            resume_text=resume_text, 
                            analyze_prompt=strength_prompt
                        )

                    st.markdown(f'<h4 style="color: orange;">Strengths:</h4>', unsafe_allow_html=True)
                    st.write(strength)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Gemini API Key</h5>', unsafe_allow_html=True)


    def resume_weakness():
        """
        Analyze resume weaknesses using Gemini
        """
        with st.form(key='Weakness'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Gemini API Key
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)
        
        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        # Extract text from PDF
                        resume_text = resume_analyzer.pdf_to_text(pdf)

                        # Get weakness prompt
                        weakness_prompt = resume_analyzer.weakness_prompt()

                        # Generate weakness analysis using Gemini
                        weakness = resume_analyzer.gemini_analyze_simple(
                            gemini_api_key=gemini_api_key, 
                            resume_text=resume_text, 
                            analyze_prompt=weakness_prompt
                        )

                    st.markdown(f'<h4 style="color: orange;">Weaknesses and Suggestions:</h4>', unsafe_allow_html=True)
                    st.write(weakness)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Gemini API Key</h5>', unsafe_allow_html=True)


    def job_title_suggestion():
        """
        Generate job title suggestions using Gemini
        """
        with st.form(key='Job Titles'):

            # User Upload the Resume
            add_vertical_space(1)
            pdf = st.file_uploader(label='Upload Your Resume', type='pdf')
            add_vertical_space(1)

            # Enter Gemini API Key
            col1, col2 = st.columns([0.6, 0.4])
            with col1:
                gemini_api_key = st.text_input(label='Enter Google Gemini API Key', type='password')
            add_vertical_space(2)

            # Click on Submit Button
            submit = st.form_submit_button(label='Submit')
            add_vertical_space(1)

        add_vertical_space(3)
        if submit:
            if pdf is not None and gemini_api_key != '':
                try:
                    with st.spinner('Processing...'):
                    
                        # Extract text from PDF
                        resume_text = resume_analyzer.pdf_to_text(pdf)

                        # Get job title prompt
                        job_title_prompt = resume_analyzer.job_title_prompt()

                        # Generate job title suggestions using Gemini
                        job_title = resume_analyzer.gemini_analyze_simple(
                            gemini_api_key=gemini_api_key, 
                            resume_text=resume_text, 
                            analyze_prompt=job_title_prompt
                        )

                    st.markdown(f'<h4 style="color: orange;">Job Title Suggestions:</h4>', unsafe_allow_html=True)
                    st.write(job_title)

                except Exception as e:
                    st.markdown(f'<h5 style="text-align: center;color: orange;">{e}</h5>', unsafe_allow_html=True)

            elif pdf is None:
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Upload Your Resume</h5>', unsafe_allow_html=True)
            
            elif gemini_api_key == '':
                st.markdown(f'<h5 style="text-align: center;color: orange;">Please Enter Gemini API Key</h5>', unsafe_allow_html=True)