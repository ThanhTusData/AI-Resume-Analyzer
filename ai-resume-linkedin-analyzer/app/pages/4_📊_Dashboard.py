"""
Analytics Dashboard Page
Comprehensive analytics and visualizations
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.database.resume_repository import ResumeRepository
from src.database.job_repository import JobRepository
from app.config import get_config

st.set_page_config(page_title="Analytics Dashboard", page_icon="📊", layout="wide")

# Initialize
config = get_config()
resume_repo = ResumeRepository()
job_repo = JobRepository()


def main():
    st.title("📊 Analytics Dashboard")
    st.markdown("Comprehensive insights into resume analysis and job matching performance")
    st.markdown("---")
    
    # Top metrics
    display_top_metrics()
    
    st.markdown("---")
    
    # Tabs for different analytics sections
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Resume Analytics",
        "💼 Job Analytics",
        "🎯 Matching Performance",
        "📈 Trends"
    ])
    
    with tab1:
        display_resume_analytics()
    
    with tab2:
        display_job_analytics()
    
    with tab3:
        display_matching_analytics()
    
    with tab4:
        display_trends()


def display_top_metrics():
    """Display top-level KPI metrics"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Get data
    total_resumes = resume_repo.count_all()
    total_jobs = job_repo.count_all()
    
    # Calculate additional metrics
    resumes = resume_repo.get_all_resumes()
    analyzed_resumes = sum(1 for r in resumes if r.analysis_completed)
    avg_score = sum(r.overall_score for r in resumes if r.overall_score > 0) / max(analyzed_resumes, 1)
    
    with col1:
        st.metric(
            "Total Resumes",
            total_resumes,
            delta=f"+{st.session_state.get('resumes_today', 0)} today"
        )
    
    with col2:
        st.metric(
            "Analyzed",
            analyzed_resumes,
            delta=f"{(analyzed_resumes/max(total_resumes,1)*100):.0f}%"
        )
    
    with col3:
        st.metric(
            "Avg Score",
            f"{avg_score:.1f}/100",
            delta="Good" if avg_score >= 70 else "Needs Work"
        )
    
    with col4:
        st.metric(
            "Total Jobs",
            total_jobs,
            delta=f"+{st.session_state.get('jobs_today', 0)} today"
        )
    
    with col5:
        matches = st.session_state.get('total_matches', 0)
        st.metric(
            "Total Matches",
            matches,
            delta=f"{st.session_state.get('avg_match_score', 0):.0f}% avg"
        )


def display_resume_analytics():
    """Display resume analytics"""
    st.subheader("📄 Resume Analytics")
    
    resumes = resume_repo.get_all_resumes()
    
    if not resumes:
        st.info("No resumes to analyze. Upload some resumes to see analytics!")
        return
    
    # Prepare data
    resume_data = []
    for resume in resumes:
        resume_data.append({
            'Filename': resume.filename,
            'Score': resume.overall_score,
            'Word Count': resume.word_count,
            'Skills': len(resume.skills),
            'Experience': len(resume.experience),
            'Education': len(resume.education),
            'Upload Date': resume.upload_date,
            'Analyzed': 'Yes' if resume.analysis_completed else 'No'
        })
    
    df = pd.DataFrame(resume_data)
    
    # Score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df,
            x='Score',
            nbins=20,
            title='Resume Score Distribution',
            labels={'Score': 'Resume Score', 'count': 'Number of Resumes'},
            color_discrete_sequence=['#1f77b4']
        )
        fig.add_vline(x=df['Score'].mean(), line_dash="dash", line_color="red",
                      annotation_text=f"Avg: {df['Score'].mean():.1f}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            df,
            y='Score',
            title='Resume Score Statistics',
            labels={'Score': 'Resume Score'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Skills analysis
    st.markdown("### Skills Distribution")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='Skills',
            y='Score',
            size='Word Count',
            title='Skills vs Score',
            labels={'Skills': 'Number of Skills', 'Score': 'Resume Score'},
            hover_data=['Filename']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.scatter(
            df,
            x='Experience',
            y='Score',
            size='Skills',
            title='Experience vs Score',
            labels={'Experience': 'Number of Positions', 'Score': 'Resume Score'},
            hover_data=['Filename']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top skills across all resumes
    st.markdown("### Most Common Skills")
    
    all_skills = []
    for resume in resumes:
        all_skills.extend(resume.skills)
    
    if all_skills:
        skill_counts = pd.Series(all_skills).value_counts().head(20)
        
        fig = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title='Top 20 Skills Across All Resumes',
            labels={'x': 'Count', 'y': 'Skill'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("### Resume Details")
    st.dataframe(
        df.sort_values('Score', ascending=False),
        use_container_width=True,
        hide_index=True
    )


def display_job_analytics():
    """Display job analytics"""
    st.subheader("💼 Job Analytics")
    
    jobs = job_repo.get_all_jobs()
    
    if not jobs:
        st.info("No jobs to analyze. Scrape some jobs to see analytics!")
        return
    
    # Prepare data
    job_data = []
    for job in jobs:
        job_data.append({
            'Title': job.title,
            'Company': job.company,
            'Location': job.location,
            'Remote': job.remote,
            'Type': job.job_type.value if job.job_type else 'N/A',
            'Level': job.experience_level.value if job.experience_level else 'N/A',
            'Skills': len(job.required_skills),
            'Posted': job.days_since_posted() if job.posted_date else None,
            'Scraped': job.scraped_date
        })
    
    df = pd.DataFrame(job_data)
    
    # Remote vs On-site
    col1, col2 = st.columns(2)
    
    with col1:
        remote_counts = df['Remote'].value_counts()
        fig = px.pie(
            values=remote_counts.values,
            names=['Remote' if x else 'On-site' for x in remote_counts.index],
            title='Remote vs On-site Distribution',
            color_discrete_sequence=['#00D9FF', '#FF6B6B']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        type_counts = df['Type'].value_counts()
        fig = px.pie(
            values=type_counts.values,
            names=type_counts.index,
            title='Job Type Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Experience level distribution
    col1, col2 = st.columns(2)
    
    with col1:
        level_counts = df['Level'].value_counts()
        fig = px.bar(
            x=level_counts.index,
            y=level_counts.values,
            title='Experience Level Distribution',
            labels={'x': 'Experience Level', 'y': 'Number of Jobs'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        location_counts = df['Location'].value_counts().head(10)
        fig = px.bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            title='Top 10 Locations',
            labels={'x': 'Number of Jobs', 'y': 'Location'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Top companies
    st.markdown("### Top Companies")
    company_counts = df['Company'].value_counts().head(15)
    
    fig = px.bar(
        x=company_counts.index,
        y=company_counts.values,
        title='Top 15 Companies by Job Postings',
        labels={'x': 'Company', 'y': 'Number of Jobs'}
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Most in-demand skills
    st.markdown("### Most In-Demand Skills")
    
    all_skills = []
    for job in jobs:
        all_skills.extend(job.required_skills)
    
    if all_skills:
        skill_counts = pd.Series(all_skills).value_counts().head(20)
        
        fig = px.bar(
            x=skill_counts.values,
            y=skill_counts.index,
            orientation='h',
            title='Top 20 Required Skills',
            labels={'x': 'Count', 'y': 'Skill'},
            color=skill_counts.values,
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig, use_container_width=True)


def display_matching_analytics():
    """Display matching performance analytics"""
    st.subheader("🎯 Matching Performance")
    
    if 'current_matches' not in st.session_state or not st.session_state.current_matches:
        st.info("No matching data available. Run job matching to see analytics!")
        return
    
    matches = st.session_state.current_matches
    
    # Prepare data
    match_data = []
    for match in matches:
        match_data.append({
            'Job': match.job.title,
            'Company': match.job.company,
            'Overall': match.overall_score,
            'Skills': match.skills_match_score,
            'Experience': match.experience_match_score,
            'Education': match.education_match_score,
            'Semantic': match.semantic_similarity_score,
            'Matched Skills': len(match.matched_skills),
            'Missing Skills': len(match.missing_skills),
            'Confidence': match.confidence_level
        })
    
    df = pd.DataFrame(match_data)
    
    # Overall performance
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Average Match Score", f"{df['Overall'].mean():.1f}%")
    with col2:
        high_matches = len(df[df['Overall'] >= 80])
        st.metric("High Matches (≥80%)", high_matches)
    with col3:
        st.metric("Best Match", f"{df['Overall'].max():.1f}%")
    
    # Score distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.histogram(
            df,
            x='Overall',
            nbins=20,
            title='Match Score Distribution',
            labels={'Overall': 'Match Score (%)', 'count': 'Number of Matches'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        confidence_counts = df['Confidence'].value_counts()
        fig = px.pie(
            values=confidence_counts.values,
            names=confidence_counts.index,
            title='Confidence Level Distribution'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Component analysis
    st.markdown("### Score Component Analysis")
    
    components = df[['Skills', 'Experience', 'Education', 'Semantic']].mean()
    
    fig = go.Figure(data=[
        go.Bar(
            x=components.index,
            y=components.values,
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A']
        )
    ])
    fig.update_layout(
        title='Average Scores by Component',
        xaxis_title='Component',
        yaxis_title='Average Score (%)',
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Skills gap analysis
    st.markdown("### Skills Gap Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.scatter(
            df,
            x='Matched Skills',
            y='Overall',
            size='Missing Skills',
            color='Confidence',
            title='Skills Match Impact',
            labels={'Matched Skills': 'Number of Matched Skills', 'Overall': 'Overall Score (%)'},
            hover_data=['Job', 'Company']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.box(
            df,
            y='Skills',
            title='Skills Score Distribution',
            labels={'Skills': 'Skills Match Score (%)'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("### Match Details")
    st.dataframe(
        df.sort_values('Overall', ascending=False),
        use_container_width=True,
        hide_index=True
    )


def display_trends():
    """Display trends over time"""
    st.subheader("📈 Trends & Insights")
    
    # Simulated time-series data (would be real data from database in production)
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    
    # Resume upload trend
    st.markdown("### Resume Upload Trend")
    resumes = resume_repo.get_all_resumes()
    
    if resumes:
        # Group by date
        resume_dates = [r.upload_date.date() for r in resumes if r.upload_date]
        resume_df = pd.DataFrame({'date': resume_dates})
        resume_counts = resume_df.groupby('date').size().reset_index(name='count')
        
        fig = px.line(
            resume_counts,
            x='date',
            y='count',
            title='Resume Uploads Over Time',
            labels={'date': 'Date', 'count': 'Number of Uploads'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Job scraping trend
    st.markdown("### Job Scraping Trend")
    jobs = job_repo.get_all_jobs()
    
    if jobs:
        job_dates = [j.scraped_date.date() for j in jobs if j.scraped_date]
        job_df = pd.DataFrame({'date': job_dates})
        job_counts = job_df.groupby('date').size().reset_index(name='count')
        
        fig = px.line(
            job_counts,
            x='date',
            y='count',
            title='Jobs Scraped Over Time',
            labels={'date': 'Date', 'count': 'Number of Jobs'},
            color_discrete_sequence=['#00D9FF']
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Score trends
    st.markdown("### Score Trends")
    
    if resumes:
        analyzed_resumes = [r for r in resumes if r.analysis_completed and r.analysis_date]
        
        if analyzed_resumes:
            score_data = [{
                'date': r.analysis_date.date(),
                'score': r.overall_score,
                'filename': r.filename
            } for r in analyzed_resumes]
            
            score_df = pd.DataFrame(score_data)
            
            fig = px.scatter(
                score_df,
                x='date',
                y='score',
                title='Resume Scores Over Time',
                labels={'date': 'Analysis Date', 'score': 'Resume Score'},
                hover_data=['filename'],
                trendline='lowess'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Insights summary
    st.markdown("---")
    st.markdown("### 💡 Key Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Resume Insights:**")
        if resumes:
            analyzed = sum(1 for r in resumes if r.analysis_completed)
            avg_score = sum(r.overall_score for r in resumes if r.overall_score > 0) / max(analyzed, 1)
            
            st.markdown(f"- {analyzed}/{len(resumes)} resumes analyzed ({analyzed/len(resumes)*100:.0f}%)")
            st.markdown(f"- Average resume score: {avg_score:.1f}/100")
            st.markdown(f"- {'Good' if avg_score >= 70 else 'Needs improvement'} overall quality")
        else:
            st.info("No data available")
    
    with col2:
        st.markdown("**Job Market Insights:**")
        if jobs:
            remote_pct = sum(1 for j in jobs if j.remote) / len(jobs) * 100
            st.markdown(f"- {len(jobs)} total job postings")
            st.markdown(f"- {remote_pct:.0f}% remote opportunities")
            st.markdown(f"- Market trends: {'Strong' if len(jobs) > 50 else 'Growing'}")
        else:
            st.info("No data available")


if __name__ == "__main__":
    main()