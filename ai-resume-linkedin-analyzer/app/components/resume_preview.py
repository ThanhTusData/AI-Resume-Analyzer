"""
Resume Preview Component
Displays resume content in a preview format
"""

import streamlit as st


def render_resume_preview(resume, detailed: bool = False):
    """
    Render resume preview
    
    Args:
        resume: Resume object
        detailed: Show detailed view
    """
    st.markdown("### 📄 Resume Preview")
    
    # Header with file info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("File", resume.filename)
    with col2:
        st.metric("Words", f"{resume.word_count:,}")
    with col3:
        st.metric("Score", f"{resume.overall_score:.0f}/100" if resume.overall_score > 0 else "Not analyzed")
    
    st.markdown("---")
    
    # Personal Information
    if resume.personal_info:
        st.markdown("#### 👤 Personal Information")
        
        info_cols = st.columns(2)
        
        with info_cols[0]:
            if resume.personal_info.get('name'):
                st.markdown(f"**Name:** {resume.personal_info['name']}")
            if resume.personal_info.get('email'):
                st.markdown(f"**Email:** {resume.personal_info['email']}")
            if resume.personal_info.get('phone'):
                st.markdown(f"**Phone:** {resume.personal_info['phone']}")
        
        with info_cols[1]:
            if resume.personal_info.get('location'):
                st.markdown(f"**Location:** {resume.personal_info['location']}")
            if resume.personal_info.get('linkedin'):
                st.markdown(f"**LinkedIn:** {resume.personal_info['linkedin']}")
            if resume.personal_info.get('website'):
                st.markdown(f"**Website:** {resume.personal_info['website']}")
        
        st.markdown("---")
    
    # Summary
    if resume.summary:
        st.markdown("#### 📝 Professional Summary")
        summary_text = resume.summary if detailed else resume.summary[:200] + "..."
        st.markdown(summary_text)
        st.markdown("---")
    
    # Skills
    if resume.skills:
        st.markdown("#### 🎯 Skills")
        
        # Display skills in chips
        skills_html = ""
        for skill in resume.skills[:20]:
            skills_html += f"""
            <span style='
                background-color: #e3f2fd;
                color: #1976d2;
                padding: 4px 12px;
                border-radius: 16px;
                margin: 4px;
                display: inline-block;
                font-size: 14px;
            '>{skill}</span>
            """
        
        st.markdown(skills_html, unsafe_allow_html=True)
        
        if len(resume.skills) > 20:
            st.caption(f"+ {len(resume.skills) - 20} more skills")
        
        st.markdown("---")
    
    # Experience
    if resume.experience:
        st.markdown("#### 💼 Work Experience")
        
        for idx, exp in enumerate(resume.experience[:5 if not detailed else None]):
            with st.expander(
                f"{exp.get('title', 'Position')} at {exp.get('company', 'Company')}",
                expanded=(idx == 0 and detailed)
            ):
                if exp.get('duration'):
                    st.caption(f"📅 {exp['duration']}")
                if exp.get('description'):
                    st.markdown(exp['description'])
        
        if len(resume.experience) > 5 and not detailed:
            st.caption(f"+ {len(resume.experience) - 5} more positions")
        
        st.markdown("---")
    
    # Education
    if resume.education:
        st.markdown("#### 🎓 Education")
        
        for edu in resume.education:
            st.markdown(f"**{edu.get('degree', 'Degree')}**")
            st.markdown(f"*{edu.get('institution', 'Institution')}*")
            if edu.get('year'):
                st.caption(f"Year: {edu['year']}")
            st.markdown("")
        
        st.markdown("---")
    
    # Certifications
    if resume.certifications:
        st.markdown("#### 📜 Certifications")
        for cert in resume.certifications:
            st.markdown(f"- {cert}")
