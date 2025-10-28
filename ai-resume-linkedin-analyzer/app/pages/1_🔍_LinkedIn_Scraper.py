"""
LinkedIn Job Scraper Page
Streamlit interface for scraping LinkedIn jobs
"""

import streamlit as st
import sys
from pathlib import Path
import pandas as pd
from datetime import datetime
import json

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.scraper.linkedin_scraper import LinkedInScraper, SearchParams
from src.models.job import Job
from src.database.job_repository import JobRepository
from app.config import get_config
from app.utils.validators import validate_email

st.set_page_config(page_title="LinkedIn Scraper", page_icon="🔍", layout="wide")

# Initialize
config = get_config()
job_repo = JobRepository()

def main():
    st.title("🔍 LinkedIn Job Scraper")
    st.markdown("Search and scrape job postings from LinkedIn with advanced filters.")
    st.markdown("---")
    
    # Check configuration
    if not config.LINKEDIN_EMAIL or not config.LINKEDIN_PASSWORD:
        st.error("⚠️ LinkedIn credentials not configured!")
        st.info("Please add LINKEDIN_EMAIL and LINKEDIN_PASSWORD to your .env file")
        st.stop()
    
    # Sidebar - Search Parameters
    with st.sidebar:
        st.header("🎯 Search Filters")
        
        keywords = st.text_input(
            "Job Keywords *",
            placeholder="e.g., Data Scientist, Python Developer",
            help="Enter job title or keywords"
        )
        
        location = st.text_input(
            "Location",
            placeholder="e.g., San Francisco, CA",
            help="Leave empty for all locations"
        )
        
        st.subheader("Experience Level")
        experience_levels = st.multiselect(
            "Select levels",
            ["Entry", "Mid-Senior", "Director", "Executive"],
            default=["Mid-Senior"]
        )
        
        st.subheader("Job Type")
        job_types = st.multiselect(
            "Select types",
            ["Full-time", "Part-time", "Contract", "Internship"],
            default=["Full-time"]
        )
        
        remote = st.checkbox("Remote only", value=False)
        
        posted_within = st.selectbox(
            "Posted within",
            ["day", "week", "month"],
            index=1
        )
        
        max_results = st.slider(
            "Maximum results",
            min_value=5,
            max_value=100,
            value=25,
            step=5
        )
        
        st.markdown("---")
        
        scrape_button = st.button("🚀 Start Scraping", type="primary", use_container_width=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Scraping Status")
        status_container = st.empty()
        
    with col2:
        st.subheader("📈 Statistics")
        stats_container = st.container()
        
        with stats_container:
            stat_col1, stat_col2 = st.columns(2)
            with stat_col1:
                st.metric("Jobs Today", st.session_state.get('jobs_scraped_today', 0))
            with stat_col2:
                st.metric("Total Jobs", job_repo.count_all())
    
    # Results area
    st.markdown("---")
    results_container = st.container()
    
    # Handle scraping
    if scrape_button:
        if not keywords:
            st.error("Please enter job keywords")
            return
        
        with status_container:
            st.info("🔄 Initializing scraper...")
            
            # Create search parameters
            search_params = SearchParams(
                keywords=keywords,
                location=location,
                experience_level=experience_levels if experience_levels else None,
                job_type=job_types if job_types else None,
                remote=remote,
                posted_within=posted_within,
                max_results=max_results
            )
            
            # Progress tracking
            progress_bar = st.progress(0)
            progress_text = st.empty()
            
            try:
                # Initialize scraper
                with LinkedInScraper(
                    email=config.LINKEDIN_EMAIL,
                    password=config.LINKEDIN_PASSWORD,
                    headless=config.SCRAPER_HEADLESS
                ) as scraper:
                    
                    progress_text.text("Logging in to LinkedIn...")
                    progress_bar.progress(10)
                    
                    # Login
                    if not scraper.login():
                        st.error("❌ Failed to login to LinkedIn. Check credentials.")
                        return
                    
                    progress_text.text("Searching for jobs...")
                    progress_bar.progress(30)
                    
                    # Search jobs
                    jobs = scraper.search_jobs(search_params)
                    
                    progress_bar.progress(80)
                    
                    if not jobs:
                        st.warning("No jobs found matching your criteria.")
                        return
                    
                    progress_text.text("Saving jobs to database...")
                    
                    # Save to database
                    saved_count = 0
                    for job in jobs:
                        if job_repo.save_job(job):
                            saved_count += 1
                    
                    progress_bar.progress(100)
                    progress_text.empty()
                    progress_bar.empty()
                    
                    # Success message
                    st.success(f"✅ Successfully scraped {len(jobs)} jobs! ({saved_count} new)")
                    
                    # Update session state
                    if 'scraped_jobs' not in st.session_state:
                        st.session_state.scraped_jobs = []
                    st.session_state.scraped_jobs = jobs
                    st.session_state.jobs_scraped_today = saved_count
                    
                    # Display results
                    display_results(jobs, results_container)
                    
            except Exception as e:
                st.error(f"❌ Scraping error: {str(e)}")
                st.exception(e)
    
    # Display existing results if available
    elif 'scraped_jobs' in st.session_state and st.session_state.scraped_jobs:
        display_results(st.session_state.scraped_jobs, results_container)
    
    # Recent scrapes section
    st.markdown("---")
    st.subheader("📚 Recent Scrapes")
    
    recent_jobs = job_repo.get_recent_jobs(limit=10)
    if recent_jobs:
        display_recent_jobs(recent_jobs)
    else:
        st.info("No recent scrapes. Start scraping to see results here!")


def display_results(jobs: list, container):
    """Display scraped jobs in the container"""
    with container:
        st.subheader(f"🎯 Found {len(jobs)} Jobs")
        
        # Filter and sort options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sort_by = st.selectbox(
                "Sort by",
                ["Relevance", "Date Posted", "Company", "Title"]
            )
        
        with col2:
            filter_remote = st.checkbox("Remote only", value=False, key="filter_remote")
        
        with col3:
            export_button = st.download_button(
                label="📥 Export CSV",
                data=jobs_to_csv(jobs),
                file_name=f"jobs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        # Filter jobs
        filtered_jobs = jobs
        if filter_remote:
            filtered_jobs = [j for j in jobs if j.remote]
        
        # Display each job
        for idx, job in enumerate(filtered_jobs):
            with st.expander(f"**{job.title}** - {job.company}", expanded=(idx < 3)):
                display_job_card(job)


def display_job_card(job: Job):
    """Display a single job card"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**📍 Location:** {job.location}")
        if job.remote:
            st.markdown("🏠 **Remote**")
        
        if job.job_type:
            st.markdown(f"**💼 Type:** {job.job_type.value}")
        
        if job.experience_level:
            st.markdown(f"**📊 Level:** {job.experience_level.value}")
        
        if job.salary_min or job.salary_max:
            st.markdown(f"**💰 Salary:** {job.get_salary_range()}")
    
    with col2:
        if job.posted_date:
            days_ago = job.days_since_posted()
            if days_ago is not None:
                st.metric("Posted", f"{days_ago}d ago")
        
        if job.applicant_count > 0:
            st.metric("Applicants", job.applicant_count)
    
    # Description
    if job.description:
        st.markdown("**Description:**")
        st.markdown(job.description[:500] + "..." if len(job.description) > 500 else job.description)
    
    # Skills
    if job.required_skills:
        st.markdown("**Required Skills:**")
        skills_text = " • ".join(job.required_skills[:10])
        st.markdown(f"*{skills_text}*")
    
    # Requirements
    if job.requirements:
        with st.expander("View Requirements"):
            st.markdown(job.requirements)
    
    # Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if job.url:
            st.link_button("🔗 View Job", job.url)
    with col2:
        if st.button("💾 Save", key=f"save_{job.job_id}"):
            st.success("Job saved!")
    with col3:
        if st.button("🎯 Match Resume", key=f"match_{job.job_id}"):
            st.session_state.selected_job = job
            st.switch_page("pages/3_🎯_Job_Matching.py")


def display_recent_jobs(jobs: list):
    """Display recent jobs in a compact format"""
    df_data = []
    for job in jobs:
        df_data.append({
            "Title": job.title,
            "Company": job.company,
            "Location": job.location,
            "Remote": "✅" if job.remote else "❌",
            "Posted": job.days_since_posted() if job.posted_date else "N/A",
            "Scraped": job.scraped_date.strftime("%Y-%m-%d %H:%M")
        })
    
    df = pd.DataFrame(df_data)
    st.dataframe(df, use_container_width=True, hide_index=True)


def jobs_to_csv(jobs: list) -> str:
    """Convert jobs list to CSV string"""
    df_data = []
    for job in jobs:
        df_data.append({
            "Title": job.title,
            "Company": job.company,
            "Location": job.location,
            "Remote": job.remote,
            "Job Type": job.job_type.value if job.job_type else "",
            "Experience Level": job.experience_level.value if job.experience_level else "",
            "Required Skills": ", ".join(job.required_skills),
            "Salary Range": job.get_salary_range(),
            "Posted Date": job.posted_date.isoformat() if job.posted_date else "",
            "URL": job.url,
            "Description": job.description
        })
    
    df = pd.DataFrame(df_data)
    return df.to_csv(index=False)


if __name__ == "__main__":
    main()