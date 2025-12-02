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
st.title("🔍 Global Job Search (AI Enhanced)")
st.write("Search remote, hybrid, or on-site jobs worldwide.")
st.write("---")

# ----------------------------------------------------
# SEARCH INPUTS
# ----------------------------------------------------
query = st.text_input("Enter Job Title / Keyword", placeholder="e.g., Data Analyst")
location_filter = st.text_input("Filter by Country (Optional)", placeholder="e.g., Nigeria, USA, Europe, Africa")

remote_filter = st.selectbox(
    "Select Job Type",
    ["Remote Only", "Onsite + Hybrid + Remote"],
    index=0
)

remote_only = remote_filter == "Remote Only"

num_pages = st.selectbox("Number of pages to fetch", [1, 2, 3, 4, 5], index=0)

# INIT SESSION STORAGE
if "jobs" not in st.session_state:
    st.session_state.jobs = []


# ----------------------------------------------------
# SEARCH BUTTON
# ----------------------------------------------------
if st.button("Search Jobs"):
    if not query.strip():
        st.warning("Please enter a job keyword.")
        st.stop()

    increment_jobs_searched(user["id"])

    with st.spinner("Fetching global job listings..."):
        results = search_jobs(
            query=query,
            location_filter=location_filter,    # ✔ FIXED ARGUMENT
            remote_only=remote_only,
            page=1,
            num_pages=num_pages
        )

    st.session_state.jobs = results
    st.success(f"Found {len(results)} jobs worldwide.")
    st.rerun()


# ----------------------------------------------------
# DISPLAY RESULTS
# ----------------------------------------------------
jobs = st.session_state.jobs

if jobs:

    for idx, job in enumerate(jobs):

        job_id = str(job.get("job_id", f"job_{idx}"))
        key_prefix = f"job_{idx}"

        # Log category
        log_job_category(user["id"], query, job.get("job_title", "Unknown"))

        # Display job card
        job_card(job, key_prefix=key_prefix, show_actions=True)

        # SAVE JOB
        if st.session_state.get(f"{key_prefix}_save_btn"):
            if is_job_saved(user["id"], job_id):
                st.info("Already saved.")
            else:
                save_job(user["id"], job)
                increment_jobs_saved(user["id"])
                st.success("Job saved.")
            st.session_state[f"{key_prefix}_save_btn"] = False
            st.rerun()

        # AI MATCH SCORE
        if st.session_state.get(f"{key_prefix}_match_btn"):
            st.subheader("📊 AI Job Match Score")
            resume = st.text_area(
                f"Paste your resume (Job ID: {job_id})",
                key=f"resume_match_{idx}"
            )

            if resume:
                with st.spinner("Analyzing..."):
                    result = job_match_score(job.get("job_description", ""), resume)
                increment_ai_tools_used(user["id"])
                st.code(result)
            else:
                st.warning("Paste your resume first.")

        # AI COVER LETTER
        if st.session_state.get(f"{key_prefix}_cover_btn"):
            st.subheader("✉️ AI Cover Letter Generator")
            resume = st.text_area(
                f"Paste your resume (Job ID: {job_id})",
                key=f"resume_cover_{idx}"
            )

            if resume:
                with st.spinner("Generating letter..."):
                    letter = cover_letter(
                        job.get("job_title", ""),
                        job.get("employer_name", ""),
                        job.get("job_description", ""),
                        resume
                    )
                increment_ai_tools_used(user["id"])
                st.write(letter)
            else:
                st.warning("Paste your resume please.")

        # AI ELIGIBILITY
        with st.expander("🌍 Country Eligibility (AI)"):
            with st.spinner("Analyzing eligibility..."):
                eligibility = extract_eligibility(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(eligibility)

        # AI SKILLS
        with st.expander("🧠 Required Skills (AI)"):
            with st.spinner("Extracting skills..."):
                skills = extract_skills(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(skills)

        st.write("----")
