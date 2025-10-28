"""
Job Card Component
Displays job information in a card format
"""

import streamlit as st
from typing import Optional


def render_job_card(job, show_actions: bool = True, compact: bool = False):
    """
    Render a job posting card
    
    Args:
        job: Job object
        show_actions: Show action buttons
        compact: Use compact layout
    """
    with st.container():
        # Header
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"### {job.title}")
            st.markdown(f"**{job.company}**")
        
        with col2:
            if job.remote:
                st.markdown("🏠 **Remote**")
        
        if not compact:
            st.markdown("---")
            
            # Details
            detail_cols = st.columns(3)
            
            with detail_cols[0]:
                st.markdown(f"**📍 Location**")
                st.text(job.location if job.location else "Not specified")
            
            with detail_cols[1]:
                st.markdown(f"**💼 Type**")
                st.text(job.job_type.value if job.job_type else "Not specified")
            
            with detail_cols[2]:
                st.markdown(f"**📊 Level**")
                st.text(job.experience_level.value if job.experience_level else "Not specified")
            
            # Salary
            if job.salary_min or job.salary_max:
                st.markdown(f"**💰 Salary:** {job.get_salary_range()}")
            
            # Posted date
            if job.posted_date:
                days_ago = job.days_since_posted()
                if days_ago is not None:
                    st.caption(f"Posted {days_ago} days ago")
            
            # Description
            if job.description and not compact:
                with st.expander("📄 View Description"):
                    description = job.description[:500] + "..." if len(job.description) > 500 else job.description
                    st.markdown(description)
            
            # Skills
            if job.required_skills:
                st.markdown("**🎯 Required Skills:**")
                skills_text = " • ".join(job.required_skills[:8])
                st.markdown(f"*{skills_text}*")
                
                if len(job.required_skills) > 8:
                    st.caption(f"+ {len(job.required_skills) - 8} more skills")
        
        # Actions
        if show_actions:
            st.markdown("---")
            action_cols = st.columns(4)
            
            with action_cols[0]:
                if job.url and st.button("🔗 View Job", key=f"view_{job.job_id}", use_container_width=True):
                    st.markdown(f"[Open Job Posting]({job.url})")
            
            with action_cols[1]:
                if st.button("💾 Save", key=f"save_{job.job_id}", use_container_width=True):
                    st.success("Job saved!")
            
            with action_cols[2]:
                if st.button("🎯 Match", key=f"match_{job.job_id}", use_container_width=True):
                    st.session_state.selected_job = job
                    st.switch_page("pages/3_🎯_Job_Matching.py")
            
            with action_cols[3]:
                if st.button("📤 Share", key=f"share_{job.job_id}", use_container_width=True):
                    st.info("Share functionality coming soon!")
