import streamlit as st
from components.sidebar import show_sidebar
from services.job_api import search_jobs
from components.job_card import job_card

from services.utils import (
    save_job,
    is_job_saved,
    increment_jobs_searched,
    increment_jobs_saved,
    increment_ai_tools_used,
    log_job_category
)

from services.ai_engine import (
    job_match_score,
    cover_letter,
    extract_eligibility,
    extract_skills
)

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or not st.session_state.user:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("🌍 Global Job Search (AI Enhanced)")
st.write("Search global remote, hybrid, and on-site jobs — with full AI analysis.")
st.write("---")

# ----------------------------------------------------
# SEARCH INPUTS
# ----------------------------------------------------
query = st.text_input("Enter Job Title / Keyword", placeholder="e.g., Data Analyst")

location_filter = st.text_input(
    "Filter by Country (Optional)",
    placeholder="e.g., Nigeria, UK, Germany, Africa"
)

job_type = st.selectbox(
    "Job Type",
    ["All Jobs (Default)", "Remote Only"],
    index=0
)

num_pages = st.selectbox("Number of pages to fetch", [1, 2, 3, 4, 5], index=0)

# Ensure session storage exists
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# ----------------------------------------------------
# SEARCH BUTTON
# ----------------------------------------------------
if st.button("Search Jobs"):
    if not query.strip():
        st.warning("Please enter a keyword.")
        st.stop()

    increment_jobs_searched(user["id"])
    st.session_state.jobs = []  # clear old results

    remote_only = (job_type == "Remote Only")

    with st.spinner("Fetching jobs globally..."):
        results = search_jobs(
            query=query,
            location=location_filter,
            remote_only=remote_only,
            page=1,
            num_pages=num_pages
        )

    st.session_state.jobs = results
    st.success(f"Found {len(results)} jobs across the world.")
    st.rerun()

# ----------------------------------------------------
# SHOW RESULTS
# ----------------------------------------------------
if st.session_state.jobs:
    jobs = st.session_state.jobs

    for idx, job in enumerate(jobs):

        job_id = str(job.get("job_id", f"job_{idx}"))
        key_prefix = f"job_{idx}"

        # Log category for analytics
        log_job_category(user["id"], query, job.get("job_title", "Unknown"))

        # Render job card with buttons
        job_card(job, key_prefix=key_prefix, show_actions=True)

        # ------------------------------------------------
        # SAVE JOB
        # ------------------------------------------------
        if st.session_state.get(f"{key_prefix}_save_btn"):
            if is_job_saved(user["id"], job_id):
                st.info("This job is already saved.")
            else:
                save_job(user["id"], job)
                increment_jobs_saved(user["id"])
                st.success("Job saved successfully.")

            st.session_state[f"{key_prefix}_save_btn"] = False
            st.rerun()

        # ------------------------------------------------
        # AI MATCH SCORE
        # ------------------------------------------------
        if st.session_state.get(f"{key_prefix}_match_btn"):

            st.subheader("📊 AI Job Match Score")

            resume = st.text_area(
                "Paste your resume below:",
                key=f"resume_match_{idx}",
            )

            if resume:
                with st.spinner("Analyzing resume vs job..."):
                    result = job_match_score(job.get("job_description", ""), resume)

                increment_ai_tools_used(user["id"])
                st.code(result)
            else:
                st.warning("Please paste your resume to continue.")

        # ------------------------------------------------
        # AI COVER LETTER
        # ------------------------------------------------
        if st.session_state.get(f"{key_prefix}_cover_btn"):

            st.subheader("✉️ AI Cover Letter Generator")

            resume = st.text_area(
                "Paste your resume below:",
                key=f"resume_cover_{idx}",
            )

            if resume:
                with st.spinner("Generating AI cover letter..."):
                    letter = cover_letter(
                        job.get("job_title", ""),
                        job.get("employer_name", ""),
                        job.get("job_description", ""),
                        resume,
                    )

                increment_ai_tools_used(user["id"])
                st.write(letter)
            else:
                st.warning("Please paste your resume first.")

        # ------------------------------------------------
        # AI ELIGIBILITY
        # ------------------------------------------------
        with st.expander("🌍 Country Eligibility (AI Extracted)"):
            with st.spinner("Extracting eligibility..."):
                eligibility = extract_eligibility(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(eligibility)

        # ------------------------------------------------
        # AI SKILLS EXTRACTION
        # ------------------------------------------------
        with st.expander("🧠 Required Skills (AI Extracted)"):
            with st.spinner("Extracting skills..."):
                skills = extract_skills(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(skills)

        st.write("----")
