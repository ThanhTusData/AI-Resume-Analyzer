"""
Resume Analyzer Page
Streamlit interface for analyzing resumes
"""

import streamlit as st
import sys
from pathlib import Path
import time
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.parsers.parser_factory import ParserFactory
from src.extractors.text_cleaner import TextCleaner
from src.extractors.skill_extractor import SkillExtractor
from src.extractors.experience_extractor import ExperienceExtractor
from src.extractors.education_extractor import EducationExtractor
from src.ai_analyzer.resume_analyzer import ResumeAnalyzer
from src.ai_analyzer.llm_client import LLMClient
from src.models.resume import Resume, FileType
from src.database.resume_repository import ResumeRepository
from app.config import get_config
from app.components.score_gauge import render_score_gauge

st.set_page_config(page_title="Resume Analyzer", page_icon="📄", layout="wide")

# Initialize
config = get_config()
resume_repo = ResumeRepository()

def main():
    st.title("📄 AI Resume Analyzer")
    st.markdown("Upload your resume for comprehensive AI-powered analysis and insights.")
    st.markdown("---")
    
    # Check API keys
    if not config.OPENAI_API_KEY and not config.GOOGLE_API_KEY:
        st.error("⚠️ No AI API keys configured!")
        st.info("Please add OPENAI_API_KEY or GOOGLE_API_KEY to your .env file")
        st.stop()
    
    # Sidebar - Settings
    with st.sidebar:
        st.header("⚙️ Analysis Settings")
        
        ai_provider = st.selectbox(
            "AI Provider",
            ["OpenAI (GPT-4)", "Google (Gemini)"],
            index=0 if config.OPENAI_API_KEY else 1
        )
        
        analysis_depth = st.select_slider(
            "Analysis Depth",
            options=["Quick", "Standard", "Comprehensive"],
            value="Standard"
        )
        
        st.markdown("---")
        
        st.subheader("📋 Analysis Includes:")
        st.markdown("""
        - ✅ Overall resume score
        - ✅ Strengths & weaknesses
        - ✅ Skills assessment
        - ✅ Experience analysis
        - ✅ ATS compatibility
        - ✅ Improvement suggestions
        - ✅ Job title recommendations
        """)
        
        st.markdown("---")
        
        # Recent analyses
        st.subheader("📚 Recent Analyses")
        recent_resumes = resume_repo.get_recent_resumes(limit=5)
        if recent_resumes:
            for resume in recent_resumes:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.caption(resume.filename[:30])
                    with col2:
                        if st.button("📂", key=f"load_{resume.resume_id}"):
                            st.session_state.selected_resume = resume
                            st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📤 Upload & Analyze", "📊 Results", "💡 Insights"])
    
    with tab1:
        display_upload_section()
    
    with tab2:
        display_results_section()
    
    with tab3:
        display_insights_section()


def display_upload_section():
    """Display file upload and analysis section"""
    st.subheader("Upload Your Resume")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'docx', 'doc', 'txt', 'png', 'jpg', 'jpeg'],
            help="Supported formats: PDF, DOCX, DOC, TXT, Images"
        )
        
        if uploaded_file is not None:
            # Display file info
            file_details = {
                "Filename": uploaded_file.name,
                "File size": f"{uploaded_file.size / 1024:.2f} KB",
                "File type": uploaded_file.type
            }
            
            st.json(file_details)
            
            # Analyze button
            if st.button("🚀 Analyze Resume", type="primary", use_container_width=True):
                analyze_resume(uploaded_file)
    
    with col2:
        st.info("""
        **Tips for best results:**
        - Use PDF format when possible
        - Ensure text is not in images
        - Keep format clean and simple
        - Include all relevant sections
        - Use standard fonts
        """)


def analyze_resume(uploaded_file):
    """Analyze the uploaded resume"""
    start_time = time.time()
    
    # Progress tracking
    progress_container = st.container()
    
    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Save file
            status_text.text("📥 Saving file...")
            progress_bar.progress(10)
            
            file_path = config.get_upload_path(uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Step 2: Parse resume
            status_text.text("📄 Parsing resume...")
            progress_bar.progress(20)
            
            parser_factory = ParserFactory()
            parser = parser_factory.get_parser(uploaded_file.name)
            raw_text = parser.parse(str(file_path))
            
            # Step 3: Clean text
            status_text.text("🧹 Cleaning text...")
            progress_bar.progress(30)
            
            text_cleaner = TextCleaner()
            cleaned_text = text_cleaner.clean(raw_text)
            
            # Step 4: Extract information
            status_text.text("🔍 Extracting information...")
            progress_bar.progress(40)
            
            # Extract skills
            skill_extractor = SkillExtractor()
            skills = skill_extractor.extract(cleaned_text)
            
            # Extract experience
            exp_extractor = ExperienceExtractor()
            experience = exp_extractor.extract(cleaned_text)
            
            # Extract education
            edu_extractor = EducationExtractor()
            education = edu_extractor.extract(cleaned_text)
            
            progress_bar.progress(60)
            
            # Step 5: Create Resume object
            status_text.text("📋 Creating resume object...")
            
            file_ext = uploaded_file.name.rsplit('.', 1)[-1].lower()
            resume = Resume(
                filename=uploaded_file.name,
                file_type=FileType(file_ext if file_ext in ['pdf', 'docx', 'doc', 'txt'] else 'pdf'),
                raw_text=cleaned_text,
                skills=skills,
                experience=experience,
                education=education,
                word_count=len(cleaned_text.split()),
                parsed_date=datetime.now()
            )
            
            progress_bar.progress(70)
            
            # Step 6: AI Analysis
            status_text.text("🤖 Running AI analysis...")
            
            llm_client = LLMClient(
                provider=config.AI_PROVIDER,
                api_key=config.OPENAI_API_KEY or config.GOOGLE_API_KEY
            )
            analyzer = ResumeAnalyzer(llm_client=llm_client)
            
            analysis = analyzer.analyze_resume(resume)
            
            progress_bar.progress(90)
            
            # Step 7: Save to database
            status_text.text("💾 Saving results...")
            
            resume.analysis_completed = True
            resume.analysis_date = datetime.now()
            resume.overall_score = analysis.overall_score
            
            resume_repo.save_resume(resume)
            
            # Save analysis results
            st.session_state.current_resume = resume
            st.session_state.current_analysis = analysis
            
            progress_bar.progress(100)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Clear progress indicators
            time.sleep(0.5)
            progress_bar.empty()
            status_text.empty()
            
            # Success message
            st.success(f"✅ Analysis complete! (Processing time: {processing_time:.2f}s)")
            st.balloons()
            
            # Switch to results tab
            st.rerun()
            
        except Exception as e:
            progress_bar.empty()
            status_text.empty()
            st.error(f"❌ Analysis failed: {str(e)}")
            st.exception(e)


def display_results_section():
    """Display analysis results"""
    if 'current_analysis' not in st.session_state:
        st.info("👆 Upload and analyze a resume to see results here")
        return
    
    analysis = st.session_state.current_analysis
    resume = st.session_state.current_resume
    
    st.subheader(f"Analysis Results: {resume.filename}")
    st.markdown("---")
    
    # Overall Score
    st.markdown("### 🎯 Overall Score")
    render_score_gauge(analysis.overall_score, "Overall Resume Quality")
    
    # Score breakdown
    st.markdown("### 📊 Score Breakdown")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Overall Score", f"{analysis.overall_score:.0f}/100")
    with col2:
        st.metric("ATS Score", f"{analysis.ats_compatibility.get('ats_score', 0):.0f}/100")
    with col3:
        st.metric("Skills Match", f"{len(analysis.skill_assessment.get('technical_skills', []))}")
    with col4:
        st.metric("Experience", f"{resume.get_total_experience_years():.1f} years")
    
    st.markdown("---")
    
    # Strengths and Weaknesses
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Strengths")
        for strength in analysis.strengths:
            st.success(f"✓ {strength}")
    
    with col2:
        st.markdown("### ⚠️ Areas for Improvement")
        for weakness in analysis.weaknesses:
            st.warning(f"• {weakness}")
    
    st.markdown("---")
    
    # Detailed Analysis
    with st.expander("🔍 Detailed Skills Analysis", expanded=True):
        skills = analysis.skill_assessment
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Technical Skills:**")
            tech_skills = skills.get('technical_skills', [])
            if tech_skills:
                for skill in tech_skills:
                    st.markdown(f"- {skill}")
            else:
                st.info("No technical skills identified")
        
        with col2:
            st.markdown("**Soft Skills:**")
            soft_skills = skills.get('soft_skills', [])
            if soft_skills:
                for skill in soft_skills:
                    st.markdown(f"- {skill}")
            else:
                st.info("No soft skills identified")
        
        # Missing skills
        missing = skills.get('missing_skills', [])
        if missing:
            st.markdown("**Recommended Skills to Add:**")
            st.info(", ".join(missing))
    
    with st.expander("💼 Experience Analysis"):
        exp_analysis = analysis.experience_analysis
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Years", f"{exp_analysis.get('total_years', 0):.1f}")
        with col2:
            st.metric("Career Trajectory", exp_analysis.get('career_progression', 'N/A'))
        
        achievements = exp_analysis.get('achievements', [])
        if achievements:
            st.markdown("**Key Achievements:**")
            for achievement in achievements:
                st.markdown(f"🏆 {achievement}")
    
    with st.expander("🎓 Education Analysis"):
        edu_analysis = analysis.education_analysis
        
        st.markdown(f"**Highest Degree:** {edu_analysis.get('highest_degree', 'Not specified')}")
        st.metric("Relevance Score", f"{edu_analysis.get('relevance', 0):.0f}/100")
        
        recommendations = edu_analysis.get('recommendations', [])
        if recommendations:
            st.markdown("**Recommendations:**")
            for rec in recommendations:
                st.info(rec)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Download Report", use_container_width=True):
            st.info("Download feature coming soon!")
    
    with col2:
        if st.button("🎯 Find Matching Jobs", use_container_width=True):
            st.switch_page("pages/3_🎯_Job_Matching.py")
    
    with col3:
        if st.button("🔄 Analyze Another", use_container_width=True):
            del st.session_state.current_analysis
            del st.session_state.current_resume
            st.rerun()


def display_insights_section():
    """Display actionable insights"""
    if 'current_analysis' not in st.session_state:
        st.info("👆 Analyze a resume to see personalized insights")
        return
    
    analysis = st.session_state.current_analysis
    
    st.subheader("💡 Actionable Insights")
    st.markdown("---")
    
    # Improvement suggestions
    st.markdown("### 🎯 Improvement Suggestions")
    for idx, suggestion in enumerate(analysis.suggested_improvements, 1):
        with st.container():
            st.markdown(f"**{idx}. {suggestion}**")
            st.markdown("")
    
    # Job title suggestions
    st.markdown("### 💼 Recommended Job Titles")
    st.info("Based on your skills and experience, you're a good fit for:")
    
    cols = st.columns(3)
    for idx, title in enumerate(analysis.suggested_job_titles[:6]):
        with cols[idx % 3]:
            st.button(f"🎯 {title}", key=f"job_title_{idx}", use_container_width=True)
    
    # ATS Compatibility
    st.markdown("### 🤖 ATS Compatibility Report")
    ats = analysis.ats_compatibility
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("ATS Score", f"{ats.get('ats_score', 0):.0f}/100")
        
        st.markdown("**Format Issues:**")
        format_issues = ats.get('format_issues', [])
        if format_issues:
            for issue in format_issues:
                st.warning(f"⚠️ {issue}")
        else:
            st.success("✅ No major format issues detected")
    
    with col2:
        st.markdown("**Missing Keywords:**")
        missing_keywords = analysis.missing_keywords
        if missing_keywords:
            keywords_text = ", ".join(missing_keywords[:10])
            st.info(f"Consider adding: {keywords_text}")
        else:
            st.success("✅ Good keyword coverage")
    
    # Summary
    st.markdown("### 📝 Executive Summary")
    st.markdown(analysis.summary)


if __name__ == "__main__":
    main()