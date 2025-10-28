"""
Job Matching Page
Streamlit interface for matching resumes with jobs
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.matching.job_matcher import JobMatcher, MatchingConfig
from src.database.resume_repository import ResumeRepository
from src.database.job_repository import JobRepository
from app.config import get_config

st.set_page_config(page_title="Job Matching", page_icon="🎯", layout="wide")

# Initialize
config = get_config()
resume_repo = ResumeRepository()
job_repo = JobRepository()
matcher = JobMatcher()

def main():
    st.title("🎯 Job Matching Engine")
    st.markdown("Match your resume with relevant job opportunities using AI-powered semantic matching.")
    st.markdown("---")
    
    # Sidebar - Configuration
    with st.sidebar:
        st.header("⚙️ Matching Configuration")
        
        # Resume selection
        st.subheader("Select Resume")
        resumes = resume_repo.get_all_resumes()
        
        if not resumes:
            st.error("No resumes found. Please analyze a resume first!")
            if st.button("Go to Resume Analyzer"):
                st.switch_page("pages/2_📄_Resume_Analyzer.py")
            st.stop()
        
        resume_options = {f"{r.filename} (Score: {r.overall_score:.0f})": r for r in resumes}
        selected_resume_name = st.selectbox("Choose resume", list(resume_options.keys()))
        selected_resume = resume_options[selected_resume_name]
        
        st.markdown("---")
        
        # Matching parameters
        st.subheader("Matching Parameters")
        
        similarity_threshold = st.slider(
            "Minimum Match Score",
            min_value=50,
            max_value=90,
            value=70,
            step=5,
            help="Filter jobs below this match score"
        )
        
        top_k = st.slider(
            "Number of Results",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )
        
        st.markdown("---")
        
        # Weight customization
        st.subheader("Scoring Weights")
        
        with st.expander("Customize Weights"):
            skills_weight = st.slider("Skills", 0.0, 1.0, 0.35, 0.05)
            experience_weight = st.slider("Experience", 0.0, 1.0, 0.25, 0.05)
            education_weight = st.slider("Education", 0.0, 1.0, 0.15, 0.05)
            semantic_weight = st.slider("Semantic Similarity", 0.0, 1.0, 0.25, 0.05)
            
            total = skills_weight + experience_weight + education_weight + semantic_weight
            if abs(total - 1.0) > 0.01:
                st.warning(f"⚠️ Weights sum to {total:.2f}, not 1.0")
        
        weights = {
            'skills': skills_weight,
            'experience': experience_weight,
            'education': education_weight,
            'semantic': semantic_weight
        }
        
        st.markdown("---")
        
        # Match button
        match_button = st.button("🚀 Find Matches", type="primary", use_container_width=True)
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🎯 Matches", "📊 Analysis", "🔍 Job Pool"])
    
    with tab1:
        display_matches_tab(selected_resume, match_button, similarity_threshold, top_k, weights)
    
    with tab2:
        display_analysis_tab()
    
    with tab3:
        display_job_pool_tab()


def display_matches_tab(resume, match_button, threshold, top_k, weights):
    """Display job matches"""
    
    if match_button:
        # Get all jobs
        with st.spinner("🔍 Loading jobs from database..."):
            jobs = job_repo.get_all_jobs()
        
        if not jobs:
            st.warning("No jobs found in database. Please scrape jobs first!")
            if st.button("Go to LinkedIn Scraper"):
                st.switch_page("pages/1_🔍_LinkedIn_Scraper.py")
            return
        
        st.info(f"Found {len(jobs)} jobs in database. Starting matching process...")
        
        # Configure matcher
        config = MatchingConfig(
            similarity_threshold=threshold / 100,
            top_k=top_k,
            weights=weights
        )
        matcher_instance = JobMatcher(config=config)
        
        # Perform matching
        with st.spinner("🤖 Analyzing matches with AI..."):
            progress_bar = st.progress(0)
            
            matches = matcher_instance.match_resume_to_jobs(
                resume=resume,
                jobs=jobs,
                top_k=top_k
            )
            
            progress_bar.progress(100)
            progress_bar.empty()
        
        if not matches:
            st.warning("No matches found above the threshold. Try lowering the minimum match score.")
            return
        
        # Store in session state
        st.session_state.current_matches = matches
        st.session_state.matched_resume = resume
        
        # Success message
        st.success(f"✅ Found {len(matches)} matching jobs!")
        st.balloons()
    
    # Display matches
    if 'current_matches' in st.session_state and st.session_state.current_matches:
        display_match_results(st.session_state.current_matches)
    else:
        st.info("👆 Configure matching parameters and click 'Find Matches' to start")
        
        # Show sample statistics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Available Jobs", job_repo.count_all())
        with col2:
            st.metric("Analyzed Resumes", resume_repo.count_all())
        with col3:
            st.metric("Previous Matches", len(st.session_state.get('current_matches', [])))


def display_match_results(matches):
    """Display match results with detailed cards"""
    
    st.markdown("### 🎯 Top Matches")
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    avg_score = sum(m.overall_score for m in matches) / len(matches)
    high_matches = sum(1 for m in matches if m.overall_score >= 80)
    avg_skills_match = sum(m.skills_match_score for m in matches) / len(matches)
    
    with col1:
        st.metric("Average Match", f"{avg_score:.1f}%")
    with col2:
        st.metric("High Matches (≥80%)", high_matches)
    with col3:
        st.metric("Avg Skills Match", f"{avg_skills_match:.1f}%")
    with col4:
        st.metric("Total Results", len(matches))
    
    st.markdown("---")
    
    # Match cards
    for idx, match in enumerate(matches, 1):
        with st.expander(
            f"**#{idx} - {match.job.title}** at **{match.job.company}** - {match.overall_score:.1f}% Match",
            expanded=(idx <= 3)
        ):
            display_match_card(match)


def display_match_card(match):
    """Display detailed match card"""
    
    # Header with job info
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(f"### {match.job.title}")
        st.markdown(f"**{match.job.company}** • {match.job.location}")
        if match.job.remote:
            st.markdown("🏠 **Remote**")
    
    with col2:
        # Match score gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=match.overall_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Match Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 75], 'color': "yellow"},
                    {'range': [75, 100], 'color': "lightgreen"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.markdown("**Confidence**")
        st.markdown(f"### {match.confidence_level}")
        
        if match.job.salary_min or match.job.salary_max:
            st.markdown("**Salary**")
            st.markdown(match.job.get_salary_range())
    
    st.markdown("---")
    
    # Score breakdown
    st.markdown("### 📊 Score Breakdown")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Skills Match", f"{match.skills_match_score:.0f}%")
    with col2:
        st.metric("Experience Match", f"{match.experience_match_score:.0f}%")
    with col3:
        st.metric("Education Match", f"{match.education_match_score:.0f}%")
    with col4:
        st.metric("Semantic Match", f"{match.semantic_similarity_score:.0f}%")
    
    # Detailed breakdown visualization
    scores_df = pd.DataFrame({
        'Category': ['Skills', 'Experience', 'Education', 'Semantic'],
        'Score': [
            match.skills_match_score,
            match.experience_match_score,
            match.education_match_score,
            match.semantic_similarity_score
        ]
    })
    
    fig = px.bar(
        scores_df,
        x='Category',
        y='Score',
        color='Score',
        color_continuous_scale='Blues',
        title='Match Score Components'
    )
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Skills analysis
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Matched Skills")
        if match.matched_skills:
            for skill in match.matched_skills[:10]:
                st.success(f"✓ {skill}")
        else:
            st.info("No exact skill matches found")
    
    with col2:
        st.markdown("### ⚠️ Missing Skills")
        if match.missing_skills:
            for skill in match.missing_skills[:10]:
                st.warning(f"• {skill}")
            
            if len(match.missing_skills) > 10:
                st.caption(f"+ {len(match.missing_skills) - 10} more")
        else:
            st.success("All required skills matched!")
    
    # Job details
    st.markdown("---")
    st.markdown("### 📄 Job Description")
    
    with st.expander("View Full Description"):
        if match.job.description:
            st.markdown(match.job.description)
        else:
            st.info("No description available")
    
    with st.expander("View Requirements"):
        if match.job.requirements:
            st.markdown(match.job.requirements)
        else:
            st.info("No requirements listed")
    
    # AI Explanation
    st.markdown("---")
    st.markdown("### 🤖 AI Analysis")
    st.info(match.explanation)
    
    # Actions
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if match.job.url:
            st.link_button("🔗 View Job", match.job.url, use_container_width=True)
    
    with col2:
        if st.button("📧 Generate Cover Letter", key=f"cover_{match.match_id}", use_container_width=True):
            st.info("Cover letter generation coming soon!")
    
    with col3:
        if st.button("💾 Save Match", key=f"save_{match.match_id}", use_container_width=True):
            st.success("Match saved!")
    
    with col4:
        if st.button("📊 Detailed Analysis", key=f"detail_{match.match_id}", use_container_width=True):
            st.session_state.detailed_match = match
            st.rerun()


def display_analysis_tab():
    """Display match analysis visualizations"""
    
    if 'current_matches' not in st.session_state or not st.session_state.current_matches:
        st.info("No matches available. Run matching first!")
        return
    
    matches = st.session_state.current_matches
    
    st.subheader("📊 Match Analysis Dashboard")
    
    # Prepare data
    match_data = []
    for match in matches:
        match_data.append({
            'Job': f"{match.job.title[:30]}...",
            'Company': match.job.company,
            'Overall Score': match.overall_score,
            'Skills': match.skills_match_score,
            'Experience': match.experience_match_score,
            'Education': match.education_match_score,
            'Semantic': match.semantic_similarity_score,
            'Remote': 'Yes' if match.job.remote else 'No'
        })
    
    df = pd.DataFrame(match_data)
    
    # Overall score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df,
            x='Overall Score',
            nbins=20,
            title='Match Score Distribution',
            labels={'Overall Score': 'Match Score (%)', 'count': 'Number of Jobs'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            df,
            y='Overall Score',
            title='Match Score Statistics',
            labels={'Overall Score': 'Match Score (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Score component comparison
    component_df = df[['Job', 'Skills', 'Experience', 'Education', 'Semantic']].head(10)
    component_df_melted = component_df.melt(id_vars=['Job'], var_name='Component', value_name='Score')
    
    fig = px.bar(
        component_df_melted,
        x='Job',
        y='Score',
        color='Component',
        title='Top 10 Jobs - Score Components',
        barmode='group'
    )
    fig.update_layout(height=400, xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Remote vs Non-remote
    remote_stats = df.groupby('Remote')['Overall Score'].mean().reset_index()
    
    fig = px.pie(
        df,
        names='Remote',
        title='Remote vs Non-Remote Distribution',
        hole=0.3
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Company analysis
    st.markdown("---")
    st.subheader("🏢 Companies with Best Matches")
    
    company_stats = df.groupby('Company').agg({
        'Overall Score': 'mean',
        'Job': 'count'
    }).reset_index()
    company_stats.columns = ['Company', 'Avg Match Score', 'Number of Jobs']
    company_stats = company_stats.sort_values('Avg Match Score', ascending=False).head(10)
    
    st.dataframe(company_stats, use_container_width=True, hide_index=True)


def display_job_pool_tab():
    """Display available job pool"""
    
    st.subheader("🔍 Available Job Pool")
    
    jobs = job_repo.get_all_jobs()
    
    if not jobs:
        st.warning("No jobs in database. Start by scraping some jobs!")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("Search jobs", placeholder="e.g., Python Developer")
    
    with col2:
        location_filter = st.text_input("Location", placeholder="e.g., San Francisco")
    
    with col3:
        remote_filter = st.selectbox("Remote", ["All", "Remote Only", "Non-Remote"])
    
    # Apply filters
    filtered_jobs = jobs
    
    if search_term:
        filtered_jobs = [
            j for j in filtered_jobs
            if search_term.lower() in j.title.lower() or search_term.lower() in j.company.lower()
        ]
    
    if location_filter:
        filtered_jobs = [j for j in filtered_jobs if location_filter.lower() in j.location.lower()]
    
    if remote_filter == "Remote Only":
        filtered_jobs = [j for j in filtered_jobs if j.remote]
    elif remote_filter == "Non-Remote":
        filtered_jobs = [j for j in filtered_jobs if not j.remote]
    
    st.markdown(f"**Showing {len(filtered_jobs)} of {len(jobs)} jobs**")
    
    # Display jobs table
    job_data = []
    for job in filtered_jobs[:50]:  # Limit to 50 for performance
        job_data.append({
            'Title': job.title,
            'Company': job.company,
            'Location': job.location,
            'Remote': '✅' if job.remote else '❌',
            'Posted': job.days_since_posted() if job.posted_date else 'N/A',
            'Type': job.job_type.value if job.job_type else 'N/A',
            'Level': job.experience_level.value if job.experience_level else 'N/A'
        })
    
    df = pd.DataFrame(job_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


if __name__ == "__main__":
    main()