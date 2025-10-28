"""
Sidebar Component
Application navigation and status
"""

import streamlit as st
from app.config import get_config


def render_sidebar():
    """Render application sidebar with navigation and status"""
    
    config = get_config()
    
    with st.sidebar:
        # Logo/Title
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h1 style='color: #1976d2; margin: 0;'>🎯</h1>
            <h3 style='margin: 5px 0;'>Resume Analyzer</h3>
            <p style='color: #666; font-size: 0.9em;'>Powered by AI</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Navigation
        st.markdown("### 🧭 Navigation")
        
        # Page buttons
        if st.button("🏠 Home", use_container_width=True):
            st.switch_page("app/main.py")
        
        if st.button("🔍 LinkedIn Scraper", use_container_width=True):
            st.switch_page("pages/1_🔍_LinkedIn_Scraper.py")
        
        if st.button("📄 Resume Analyzer", use_container_width=True):
            st.switch_page("pages/2_📄_Resume_Analyzer.py")
        
        if st.button("🎯 Job Matching", use_container_width=True):
            st.switch_page("pages/3_🎯_Job_Matching.py")
        
        if st.button("📊 Dashboard", use_container_width=True):
            st.switch_page("pages/4_📊_Dashboard.py")
        
        st.markdown("---")
        
        # Quick Stats
        st.markdown("### 📊 Quick Stats")
        
        stats_data = [
            ("Resumes", st.session_state.get('total_resumes_analyzed', 0)),
            ("Jobs", st.session_state.get('total_jobs_scraped', 0)),
            ("Matches", st.session_state.get('total_matches', 0))
        ]
        
        for label, value in stats_data:
            st.metric(label, value)
        
        st.markdown("---")
        
        # System Status
        st.markdown("### ⚙️ System Status")
        
        status_items = [
            ("OpenAI API", "🟢" if config.OPENAI_API_KEY else "🔴"),
            ("Database", "🟢" if config.DATABASE_URL else "🔴"),
            ("Scraper", "🟢" if config.LINKEDIN_EMAIL else "🔴"),
        ]
        
        for item, status in status_items:
            st.markdown(f"{status} {item}")
        
        st.markdown("---")
        
        # Tips
        with st.expander("💡 Quick Tips"):
            st.markdown("""
            - Use PDF format for best results
            - Include quantifiable achievements
            - List 5-10 relevant skills
            - Keep resume to 1-2 pages
            """)
        
        st.markdown("---")
        
        # Footer
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.8em;'>
            <p>v1.0.0 | 2025</p>
            <p>Made with ❤️ and AI</p>
        </div>
        """, unsafe_allow_html=True)