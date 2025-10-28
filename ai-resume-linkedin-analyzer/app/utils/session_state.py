"""
Session State Management
Manages Streamlit session state variables
"""

import streamlit as st
from datetime import datetime
from typing import Any, Dict, Optional


def init_session_state():
    """Initialize all session state variables"""
    
    # Resume analysis
    if 'current_resume' not in st.session_state:
        st.session_state.current_resume = None
    
    if 'current_analysis' not in st.session_state:
        st.session_state.current_analysis = None
    
    if 'analyzed_resumes' not in st.session_state:
        st.session_state.analyzed_resumes = []
    
    # Job matching
    if 'current_matches' not in st.session_state:
        st.session_state.current_matches = []
    
    if 'matched_resume' not in st.session_state:
        st.session_state.matched_resume = None
    
    if 'selected_job' not in st.session_state:
        st.session_state.selected_job = None
    
    # Scraping
    if 'scraped_jobs' not in st.session_state:
        st.session_state.scraped_jobs = []
    
    if 'scraping_in_progress' not in st.session_state:
        st.session_state.scraping_in_progress = False
    
    # Statistics
    if 'total_resumes_analyzed' not in st.session_state:
        st.session_state.total_resumes_analyzed = 0
    
    if 'total_jobs_scraped' not in st.session_state:
        st.session_state.total_jobs_scraped = 0
    
    if 'total_matches' not in st.session_state:
        st.session_state.total_matches = 0
    
    if 'jobs_scraped_today' not in st.session_state:
        st.session_state.jobs_scraped_today = 0
    
    if 'resumes_today' not in st.session_state:
        st.session_state.resumes_today = 0
    
    if 'avg_match_score' not in st.session_state:
        st.session_state.avg_match_score = 0.0
    
    if 'success_rate' not in st.session_state:
        st.session_state.success_rate = 0.0
    
    # Recent activities
    if 'recent_activities' not in st.session_state:
        st.session_state.recent_activities = []
    
    # User preferences
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    
    if 'ai_provider' not in st.session_state:
        st.session_state.ai_provider = 'openai'
    
    # UI state
    if 'show_debug' not in st.session_state:
        st.session_state.show_debug = False
    
    if 'last_update' not in st.session_state:
        st.session_state.last_update = datetime.now()


def update_session_stats(stat_name: str, increment: int = 1):
    """
    Update session statistics
    
    Args:
        stat_name: Name of the statistic to update
        increment: Amount to increment by
    """
    if stat_name in st.session_state:
        st.session_state[stat_name] += increment
    else:
        st.session_state[stat_name] = increment
    
    st.session_state.last_update = datetime.now()


def add_activity(title: str, description: str, activity_type: str = "info"):
    """
    Add activity to recent activities
    
    Args:
        title: Activity title
        description: Activity description
        activity_type: Type of activity (info, success, warning, error)
    """
    if 'recent_activities' not in st.session_state:
        st.session_state.recent_activities = []
    
    activity = {
        'title': title,
        'description': description,
        'type': activity_type,
        'time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'timestamp': datetime.now()
    }
    
    st.session_state.recent_activities.insert(0, activity)
    
    # Keep only last 50 activities
    st.session_state.recent_activities = st.session_state.recent_activities[:50]


def clear_session_data(data_type: str = "all"):
    """
    Clear session data
    
    Args:
        data_type: Type of data to clear (all, resume, jobs, matches)
    """
    if data_type == "all":
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        init_session_state()
    
    elif data_type == "resume":
        st.session_state.current_resume = None
        st.session_state.current_analysis = None
        st.session_state.analyzed_resumes = []
    
    elif data_type == "jobs":
        st.session_state.scraped_jobs = []
        st.session_state.jobs_scraped_today = 0
    
    elif data_type == "matches":
        st.session_state.current_matches = []
        st.session_state.matched_resume = None


def get_session_info() -> Dict[str, Any]:
    """Get session information"""
    return {
        'total_resumes': st.session_state.get('total_resumes_analyzed', 0),
        'total_jobs': st.session_state.get('total_jobs_scraped', 0),
        'total_matches': st.session_state.get('total_matches', 0),
        'last_update': st.session_state.get('last_update', datetime.now()),
        'current_resume': st.session_state.get('current_resume') is not None,
        'current_analysis': st.session_state.get('current_analysis') is not None,
    }
