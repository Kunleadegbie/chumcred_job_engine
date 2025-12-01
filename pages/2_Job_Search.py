import streamlit as st
from components.sidebar import show_sidebar
from services.job_api import search_jobs
from components.job_card import job_card
from services.supabase_client import supabase_rest_query
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
st.title("🔍 Global Remote Job Search (AI Enhanced)")
st.write("Search remote jobs worldwide and analyze them using AI.")
st.write("---")

# ----------------------------------------------------
# SEARCH INPUTS
# ----------------------------------------------------
query = st.text_input("Enter Job Title / Keyword", placeholder="e.g., Data Analyst")
location_filter = st.text_input("Filter by Country (Optional)", placeholder="e.g., Nigeria, USA, Africa")
remote_only = st.checkbox("Remote jobs only", value=True)
num_results = st.selectbox("Number of pages to fetch", [1, 2, 3, 4, 5], index=0)

# Initialize session_state storage for action handlers
if "job_actions" not in st.session_state:
    st.session_state.job_actions = {}

# ----------------------------------------------------
# SEARCH BUTTON
# ----------------------------------------------------
if st.button("Search Jobs"):
    if not query.strip():
        st.warning("Please enter a job keyword.")
        st.stop()

    increment_jobs_searched(user["id"])
    st.session_state.jobs = []  # reset results
    st.session_state.job_actions = {}  # reset action memory

    with st.spinner("Fetching remote jobs..."):
        results = search_jobs(query, location_filter, remote_only, page=1, num_pages=num_results)

    st.session_state.jobs = results
    st.success(f"Found {len(results)} jobs.")
    st.rerun()

# ----------------------------------------------------
# SHOW SEARCH RESULTS
# ----------------------------------------------------
if "jobs" in st.session_state and st.session_state.jobs:

    jobs = st.session_state.jobs

    for idx, job in enumerate(jobs):

        job_id = str(job.get("job_id", f"job_{idx}"))

        # Unique key namespace
        key_prefix = f"job_{idx}"

        # Log category
        log_job_category(user["id"], query, job.get("job_title", "Unknown"))

        # Render job card
        job_card(job, key_prefix=key_prefix, show_actions=True)

        # ------------------------------------------------
        # PROCESS BUTTON ACTION
        # ------------------------------------------------

        # SAVE JOB BUTTON
        if st.session_state.get(f"{key_prefix}_save_btn"):
            if is_job_saved(user["id"], job_id):
                st.info("This job is already saved.")
            else:
                save_job(user["id"], job)
                increment_jobs_saved(user["id"])
                st.success("Job saved successfully.")
            st.session_state[f"{key_prefix}_save_btn"] = False
            st.rerun()

        # AI MATCH SCORE
        if st.session_state.get(f"{key_prefix}_match_btn"):
            st.subheader("📊 AI Job Match Score")
            resume = st.text_area(
                f"Paste your resume to evaluate job match (Job ID: {job_id})",
                key=f"resume_match_{idx}",
            )

            if resume:
                with st.spinner("Analyzing resume..."):
                    result = job_match_score(job.get("job_description", ""), resume)
                increment_ai_tools_used(user["id"])
                st.code(result)
            else:
                st.warning("Please paste your resume.")

        # AI COVER LETTER
        if st.session_state.get(f"{key_prefix}_cover_btn"):
            st.subheader("✉️ AI Cover Letter Generator")
            resume = st.text_area(
                f"Paste your resume to generate cover letter (Job ID: {job_id})",
                key=f"resume_cover_{idx}",
            )

            if resume:
                with st.spinner("Generating cover letter..."):
                    letter = cover_letter(
                        job.get("job_title", ""),
                        job.get("employer_name", ""),
                        job.get("job_description", ""),
                        resume,
                    )
                increment_ai_tools_used(user["id"])
                st.write(letter)
            else:
                st.warning("Please paste your resume.")

        # ------------------------------------------------
        # AI ELIGIBILITY EXTRACTION
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
