import streamlit as st
from openai import OpenAI

# ------------------------------------------------------
# OPENAI INITIALIZATION
# ------------------------------------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

MODEL = "gpt-4o-mini"   # Free/cheap and works well


# ------------------------------------------------------
# GENERIC AI HELPER
# ------------------------------------------------------
def ai_chat(prompt):
    """Universal function for sending prompts to OpenAI."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}]
        )

        # NEW FORMAT (2025 SDK)
        return response.choices[0].message.content

    except Exception as e:
        return f"AI Error: {str(e)}"


# ------------------------------------------------------
# JOB MATCH SCORE
# ------------------------------------------------------
def job_match_score(job_description, resume_text):
    prompt = f"""
    You are an ATS scoring engine. Compare the job description and resume.

    JOB DESCRIPTION:
    {job_description}

    RESUME:
    {resume_text}

    Respond in this format ONLY:

    SCORE: <0-100>
    STRENGTHS:
    - strength 1
    - strength 2
    - strength 3

    WEAKNESSES:
    - weakness 1
    - weakness 2
    - weakness 3
    """
    return ai_chat(prompt)


# ------------------------------------------------------
# COVER LETTER GENERATOR
# ------------------------------------------------------
def cover_letter(job_title, company, job_description, resume_text):
    prompt = f"""
    Write a concise, powerful cover letter for this role.

    Job Title: {job_title}
    Company: {company}

    Resume:
    {resume_text}

    Job Requirements:
    {job_description}

    Rules:
    - MAX 250 words
    - ATS friendly
    - confident tone
    - highlight fit with job
    """
    return ai_chat(prompt)


# ------------------------------------------------------
# COUNTRY ELIGIBILITY
# ------------------------------------------------------
def extract_eligibility(job_description):
    prompt = f"""
    Based on the job description, extract:

    - Allowed countries
    - Visa sponsorship (Yes/No/Unclear)
    - Remote type (fully, hybrid, country restricted)
    - Time zone restrictions

    JOB DESCRIPTION:
    {job_description}

    Format:

    ALLOWED COUNTRIES:
    - ...

    VISA SPONSORSHIP:
    <Yes/No/Unclear>

    REMOTE TYPE:
    <type>

    TIME ZONE RESTRICTIONS:
    <text or 'None'>
    """
    return ai_chat(prompt)


# ------------------------------------------------------
# SKILLS EXTRACTION
# ------------------------------------------------------
def extract_skills(job_description):
    prompt = f"""
    Extract the top required skills and categorize them.

    TECHNICAL SKILLS:
    - ...

    SOFT SKILLS:
    - ...

    JOB DESCRIPTION:
    {job_description}
    """
    return ai_chat(prompt)
