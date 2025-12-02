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
st.title("🌍 Global Remote Job Search (AI Enhanced)")
st.write("Search remote jobs **worldwide** — Africa, Europe, Asia, Americas, Middle East, and Australia.")
st.write("---")

# ----------------------------------------------------
# SEARCH INPUTS
# ----------------------------------------------------
query = st.text_input("Enter Job Title / Keyword", placeholder="e.g., Data Analyst, Cloud Engineer")
location_filter = st.text_input("Filter by Country or Region (Optional)", placeholder="e.g., Nigeria, UK, Europe")
remote_only = st.checkbox("Remote jobs only", value=True)
num_results = st.selectbox("Number of pages to fetch", [1, 2, 3, 4, 5], index=0)

# State handling
if "job_actions" not in st.session_state:
    st.session_state.job_actions = {}

if "jobs" not in st.session_state:
    st.session_state.jobs = []

# ----------------------------------------------------
# SEARCH BUTTON LOGIC
# ----------------------------------------------------
if st.button("Search Jobs"):
    if not query.strip():
        st.warning("Please enter a job keyword.")
        st.stop()

    increment_jobs_searched(user["id"])

    with st.spinner("Searching global remote jobs…"):
        results = search_jobs(
            query=query,
            location_filter=location_filter,
            remote_only=remote_only,
            page=1,
            num_pages=num_results
        )

    st.session_state.jobs = results
    st.session_state.job_actions = {}
    st.success(f"Found {len(results)} jobs globally.")

    st.rerun()

# ----------------------------------------------------
# DISPLAY RESULTS
# ----------------------------------------------------
if st.session_state.jobs:
    jobs = st.session_state.jobs

    for idx, job in enumerate(jobs):
        job_id = str(job.get("job_id", f"job_{idx}"))
        key_prefix = f"job_{idx}"

        # Analytics
        log_job_category(user["id"], query, job.get("job_title", "Unknown"))

        # Job Card UI
        job_card(job, key_prefix=key_prefix, show_actions=True)

        # ======================================================
        # BUTTON HANDLERS
        # ======================================================

        # 1. SAVE JOB
        if st.session_state.get(f"{key_prefix}_save_btn"):
            if is_job_saved(user["id"], job_id):
                st.info("This job is already saved.")
            else:
                save_job(user["id"], job)
                increment_jobs_saved(user["id"])
                st.success("Job saved!")

            st.session_state[f"{key_prefix}_save_btn"] = False
            st.rerun()

        # 2. AI MATCH SCORE
        if st.session_state.get(f"{key_prefix}_match_btn"):
            st.subheader("📊 AI Job Match Score")
            resume = st.text_area(
                f"Paste your resume (Job ID: {job_id})",
                key=f"resume_match_{idx}"
            )
            if resume:
                with st.spinner("Analyzing…"):
                    score = job_match_score(job.get("job_description", ""), resume)
                increment_ai_tools_used(user["id"])
                st.code(score)
            else:
                st.warning("Paste your resume to continue.")

        # 3. AI COVER LETTER GENERATOR
        if st.session_state.get(f"{key_prefix}_cover_btn"):
            st.subheader("✉️ AI Cover Letter Generator")
            resume = st.text_area(
                f"Paste your resume to generate cover letter (Job ID: {job_id})",
                key=f"resume_cover_{idx}"
            )
            if resume:
                with st.spinner("Generating…"):
                    letter = cover_letter(
                        job.get("job_title", ""),
                        job.get("employer_name", ""),
                        job.get("job_description", ""),
                        resume,
                    )
                increment_ai_tools_used(user["id"])
                st.write(letter)
            else:
                st.warning("Paste your resume to continue.")

        # ======================================================
        # AI EXPANDERS
        # ======================================================

        # COUNTRY ELIGIBILITY
        with st.expander("🌍 Country Eligibility (AI Extracted)"):
            with st.spinner("Analyzing eligibility…"):
                eligibility = extract_eligibility(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(eligibility)

        # REQUIRED SKILLS
        with st.expander("🧠 Required Skills (AI Extracted)"):
            with st.spinner("Analyzing skills…"):
                skills = extract_skills(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(skills)

        st.write("---")
