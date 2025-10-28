"""
Prompt Templates for AI Analysis
Professional prompts for resume analysis using LLMs
"""

from typing import List, Dict


class PromptTemplates:
    """Collection of prompts for resume analysis"""
    
    @staticmethod
    def get_overall_analysis_prompt(resume_text: str) -> str:
        """Get prompt for overall resume analysis"""
        return f"""You are an expert resume reviewer and career coach with 15+ years of experience. 
Analyze the following resume and provide a comprehensive quality assessment.

RESUME:
{resume_text}

Please analyze this resume and provide:

1. OVERALL SCORE (0-100): Rate the overall quality of this resume
2. FORMATTING ASSESSMENT: Evaluate the structure, organization, and readability
3. KEY OBSERVATIONS: Note what stands out (both positive and negative)

Provide your response in this format:

SCORE: [0-100]

FORMATTING:
- [Point 1]
- [Point 2]
- [Point 3]

Be specific, actionable, and honest in your assessment. Focus on helping the candidate improve."""

    @staticmethod
    def get_strengths_prompt(resume_text: str) -> str:
        """Get prompt for identifying strengths"""
        return f"""As an experienced recruiter, identify the TOP 5-7 STRENGTHS of this resume.

RESUME:
{resume_text}

Focus on:
- Standout achievements and accomplishments
- Strong skills and experience
- Well-articulated value propositions
- Impressive career progression
- Relevant certifications or education
- Quantifiable results and metrics

STRENGTHS:
- [Strength 1]
- [Strength 2]
- [Strength 3]
- [Strength 4]
- [Strength 5]

Be specific and reference actual content from the resume."""

    @staticmethod
    def get_weaknesses_prompt(resume_text: str) -> str:
        """Get prompt for identifying weaknesses"""
        return f"""As an experienced hiring manager, identify the TOP 5-7 WEAKNESSES or areas for improvement in this resume.

RESUME:
{resume_text}

Look for:
- Missing or unclear information
- Gaps in employment or skills
- Weak or vague descriptions
- Lack of quantifiable achievements
- Formatting or structure issues
- Overused buzzwords without substance
- Missing keywords for ATS

WEAKNESSES:
- [Weakness 1]
- [Weakness 2]
- [Weakness 3]
- [Weakness 4]
- [Weakness 5]

Be constructive and focus on actionable improvements."""

    @staticmethod
    def get_skills_analysis_prompt(resume_text: str, skills: List[str]) -> str:
        """Get prompt for skills analysis"""
        skills_list = ", ".join(skills) if skills else "None explicitly listed"
        
        return f"""Analyze the skills section and overall technical competencies in this resume.

RESUME:
{resume_text}

EXTRACTED SKILLS: {skills_list}

Please provide:

1. SKILL CATEGORIZATION:
   - Technical Skills: [list]
   - Soft Skills: [list]
   - Domain-Specific Skills: [list]

2. PROFICIENCY ASSESSMENT:
   - Expert Level: [skills]
   - Intermediate Level: [skills]
   - Beginner Level: [skills]

3. MISSING SKILLS:
   - High-demand skills that would strengthen this profile: [list]

4. SKILL PRESENTATION:
   - How well are skills demonstrated through experience?
   - Are skills backed by concrete examples?

Be thorough and industry-aware in your assessment."""

    @staticmethod
    def get_experience_analysis_prompt(resume_text: str, experience: List[Dict]) -> str:
        """Get prompt for experience analysis"""
        return f"""Analyze the work experience section of this resume.

RESUME:
{resume_text}

Evaluate:

1. CAREER PROGRESSION:
   - Trajectory: [upward/lateral/varied]
   - Growth indicators: [specific examples]

2. ACHIEVEMENTS:
   - Most impressive accomplishments: [list top 3-5]
   - Quantifiable results: [identify metrics]

3. GAPS OR CONCERNS:
   - Employment gaps: [if any]
   - Job hopping patterns: [if concerning]
   - Missing information: [what's unclear]

4. RECOMMENDATIONS:
   - How to better showcase experience
   - Missing context or details
   - Stronger action verbs to use

Provide specific, actionable feedback."""

    @staticmethod
    def get_education_analysis_prompt(resume_text: str, education: List[Dict]) -> str:
        """Get prompt for education analysis"""
        return f"""Analyze the education section of this resume.

RESUME:
{resume_text}

Assess:

1. EDUCATION LEVEL: [highest degree]
2. RELEVANCE: [0-100 score] How relevant is the education to the career path?
3. STRENGTHS:
   - [Point 1]
   - [Point 2]

4. RECOMMENDATIONS:
   - Additional certifications to pursue
   - How to better present education
   - Missing details (GPA, honors, relevant coursework)

Be concise and practical."""

    @staticmethod
    def get_ats_analysis_prompt(resume_text: str) -> str:
        """Get prompt for ATS compatibility analysis"""
        return f"""You are an ATS (Applicant Tracking System) expert. Analyze this resume for ATS compatibility.

RESUME:
{resume_text}

Evaluate:

1. ATS SCORE: [0-100] How likely is this resume to pass ATS screening?

2. FORMAT ISSUES:
   - [Issue 1]
   - [Issue 2]
   (if any)

3. MISSING KEYWORDS:
   - Industry-standard keywords missing: [list]
   - Important buzzwords absent: [list]

4. ATS IMPROVEMENTS:
   - [Specific recommendation 1]
   - [Specific recommendation 2]
   - [Specific recommendation 3]

5. KEYWORD DENSITY:
   - Are relevant keywords used appropriately throughout?
   - Any keyword stuffing concerns?

Focus on practical, implementable advice."""

    @staticmethod
    def get_job_title_suggestion_prompt(resume_text: str) -> str:
        """Get prompt for job title suggestions"""
        return f"""Based on this resume, suggest 5-8 job titles that would be an excellent fit for this candidate.

RESUME:
{resume_text}

Consider:
- Current skills and experience level
- Career trajectory and aspirations
- Industry trends and demand
- Natural career progression paths

JOB TITLES:
- [Title 1]
- [Title 2]
- [Title 3]
- [Title 4]
- [Title 5]
- [Title 6]
- [Title 7]
- [Title 8]

Suggest specific, realistic titles with growth potential."""

    @staticmethod
    def get_improvement_suggestions_prompt(resume_text: str) -> str:
        """Get prompt for improvement suggestions"""
        return f"""As a professional resume writer, provide 8-10 specific, actionable improvement suggestions for this resume.

RESUME:
{resume_text}

Suggestions should be:
- Specific and actionable
- Prioritized by impact
- Easy to implement
- Professional and constructive

IMPROVEMENTS:
- [Improvement 1]
- [Improvement 2]
- [Improvement 3]
- [Improvement 4]
- [Improvement 5]
- [Improvement 6]
- [Improvement 7]
- [Improvement 8]
- [Improvement 9]
- [Improvement 10]

Focus on high-impact changes that will significantly improve the resume's effectiveness."""

    @staticmethod
    def get_job_matching_prompt(resume_text: str, job_description: str) -> str:
        """Get prompt for matching resume to job"""
        return f"""Analyze how well this resume matches the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide:

1. MATCH SCORE: [0-100]

2. MATCHED QUALIFICATIONS:
   - [Qualification 1]
   - [Qualification 2]
   - [Qualification 3]

3. MISSING QUALIFICATIONS:
   - [Missing 1]
   - [Missing 2]
   - [Missing 3]

4. TAILORING RECOMMENDATIONS:
   - [Specific suggestion 1]
   - [Specific suggestion 2]
   - [Specific suggestion 3]

5. LIKELIHOOD OF SUCCESS: [Low/Medium/High]

6. KEY TALKING POINTS:
   - What to emphasize in cover letter/interview
   - Unique value propositions for this role

Be realistic and specific in your assessment."""

    @staticmethod
    def get_summary_generation_prompt(resume_text: str) -> str:
        """Get prompt for generating professional summary"""
        return f"""Write a compelling 3-4 sentence professional summary for this resume.

RESUME:
{resume_text}

The summary should:
- Highlight key strengths and unique value
- Include years of experience
- Mention top skills
- Be tailored to the candidate's target roles
- Use strong, confident language
- Be concise and impactful

PROFESSIONAL SUMMARY:
[Your generated summary here]

Make it powerful and attention-grabbing."""

    @staticmethod
    def get_achievement_enhancement_prompt(achievement: str) -> str:
        """Get prompt for enhancing achievement descriptions"""
        return f"""Rewrite this achievement statement to be more impactful and quantifiable:

ORIGINAL:
{achievement}

Provide 3 enhanced versions:

VERSION 1 (Action-focused):
[Enhanced version emphasizing action verbs and leadership]

VERSION 2 (Results-focused):
[Enhanced version emphasizing measurable outcomes]

VERSION 3 (Balanced):
[Enhanced version balancing action, result, and impact]

Use the STAR method (Situation, Task, Action, Result) and include specific metrics where possible."""

    @staticmethod
    def get_cover_letter_prompt(resume_text: str, job_description: str, company: str) -> str:
        """Get prompt for cover letter generation"""
        return f"""Write a professional cover letter for this candidate applying to {company}.

CANDIDATE RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

The cover letter should:
- Be 3-4 paragraphs
- Highlight relevant experience
- Show enthusiasm for the role
- Demonstrate cultural fit
- Include a strong call-to-action
- Be professional yet personable

COVER LETTER:
[Generated cover letter here]

Make it compelling and authentic."""