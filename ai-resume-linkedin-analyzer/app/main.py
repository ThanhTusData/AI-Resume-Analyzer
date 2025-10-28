"""
Main Streamlit Application Entry Point
AI Resume & LinkedIn Analyzer
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import AppConfig
from app.utils.session_state import init_session_state
from app.components.sidebar import render_sidebar

# Page configuration
st.set_page_config(
    page_title="AI Resume & LinkedIn Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-resume-analyzer',
        'Report a bug': 'https://github.com/yourusername/ai-resume-analyzer/issues',
        'About': "# AI Resume Analyzer\nPowered by AI to help you land your dream job!"
    }
)

# Custom CSS
def load_custom_css():
    css_file = Path(__file__).parent.parent / "assets" / "styles" / "custom.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        .main {
            padding-top: 2rem;
        }
        .stButton>button {
            width: 100%;
            border-radius: 5px;
            height: 3em;
            background-color: #FF4B4B;
            color: white;
        }
        .stButton>button:hover {
            background-color: #FF3333;
            border-color: #FF3333;
        }
        div.stMetric {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 5px;
        }
        .upload-text {
            text-align: center;
            color: #666;
        }
        </style>
        """, unsafe_allow_html=True)

def main():
    """Main application logic"""
    
    # Initialize session state
    init_session_state()
    
    # Load custom styling
    load_custom_css()
    
    # Render sidebar
    render_sidebar()
    
    # Main content
    st.title("🎯 AI Resume & LinkedIn Analyzer")
    st.markdown("---")
    
    # Welcome section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔍 LinkedIn Scraper
        Extract job postings from LinkedIn with advanced filtering and search capabilities.
        """)
        if st.button("Start Scraping", key="scrape_btn"):
            st.switch_page("pages/1_🔍_LinkedIn_Scraper.py")
    
    with col2:
        st.markdown("""
        ### 📄 Resume Analyzer
        Upload your resume for AI-powered analysis, insights, and improvement suggestions.
        """)
        if st.button("Analyze Resume", key="analyze_btn"):
            st.switch_page("pages/2_📄_Resume_Analyzer.py")
    
    with col3:
        st.markdown("""
        ### 🎯 Job Matching
        Match your resume with scraped jobs and get personalized recommendations.
        """)
        if st.button("Find Matches", key="match_btn"):
            st.switch_page("pages/3_🎯_Job_Matching.py")
    
    st.markdown("---")
    
    # Statistics Dashboard
    st.subheader("📊 Quick Stats")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Resumes Analyzed",
            value=st.session_state.get('total_resumes_analyzed', 0),
            delta=f"+{st.session_state.get('resumes_today', 0)} today"
        )
    
    with col2:
        st.metric(
            label="Jobs Scraped",
            value=st.session_state.get('total_jobs_scraped', 0),
            delta=f"+{st.session_state.get('jobs_today', 0)} today"
        )
    
    with col3:
        st.metric(
            label="Matches Found",
            value=st.session_state.get('total_matches', 0),
            delta=f"{st.session_state.get('avg_match_score', 0):.1f}% avg score"
        )
    
    with col4:
        st.metric(
            label="Success Rate",
            value=f"{st.session_state.get('success_rate', 0):.1f}%",
            delta="High confidence"
        )
    
    # Feature highlights
    st.markdown("---")
    st.subheader("✨ Key Features")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### 🤖 AI-Powered Analysis
        - GPT-4 and Gemini integration
        - Intelligent skill extraction
        - Personalized recommendations
        - Strength and weakness analysis
        
        #### 📊 Advanced Matching
        - Semantic similarity matching
        - FAISS vector search
        - Custom ranking algorithms
        - Real-time scoring
        """)
    
    with col2:
        st.markdown("""
        #### 🔒 Privacy & Security
        - Local data processing
        - Encrypted storage
        - No data sharing
        - GDPR compliant
        
        #### 🚀 Multiple Formats
        - PDF, DOCX, TXT support
        - Image OCR processing
        - Batch processing
        - Export capabilities
        """)
    
    # Recent activity
    st.markdown("---")
    st.subheader("🕐 Recent Activity")
    
    if st.session_state.get('recent_activities'):
        for activity in st.session_state['recent_activities'][:5]:
            with st.expander(f"📌 {activity.get('title', 'Activity')} - {activity.get('time', 'Just now')}"):
                st.write(activity.get('description', 'No description'))
    else:
        st.info("No recent activity. Start by scraping jobs or analyzing a resume!")
    
    # Footer
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("📚 [Documentation](https://docs.example.com)")
    with col2:
        st.markdown("💬 [Support](https://support.example.com)")
    with col3:
        st.markdown("⭐ [GitHub](https://github.com/yourusername/ai-resume-analyzer)")
    
    # Info message
    with st.sidebar:
        st.info("""
        **💡 Quick Tips:**
        - Use high-quality PDF resumes for best results
        - LinkedIn scraping requires valid credentials
        - Job matching works best with detailed resumes
        """)
        
        # System status
        st.markdown("### System Status")
        
        config = AppConfig()
        
        status_items = [
            ("OpenAI API", "✅" if config.OPENAI_API_KEY else "❌"),
            ("Database", "✅" if config.DATABASE_URL else "❌"),
            ("Scraper", "✅" if config.LINKEDIN_EMAIL else "❌"),
            ("Vector Store", "✅")
        ]
        
        for item, status in status_items:
            st.markdown(f"**{item}:** {status}")

if __name__ == "__main__":
    main()