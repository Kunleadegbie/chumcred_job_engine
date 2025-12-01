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
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("🔍 Global Remote Job Search (AI Enhanced)")
st.write("Search remote jobs across the world and analyze them using AI tools.")
st.write("---")

# ----------------------------------------------------
# SEARCH INPUTS
# ----------------------------------------------------
query = st.text_input("Enter Job Title / Keyword", placeholder="e.g., Data Analyst remote")
location_filter = st.text_input("Filter by Country (Optional)", placeholder="e.g., Nigeria, Africa, USA")
remote_only = st.checkbox("Remote jobs only", value=True)
num_results = st.selectbox("Number of pages to fetch", [1, 2, 3, 4, 5], index=0)

# ----------------------------------------------------
# SEARCH BUTTON
# ----------------------------------------------------
if st.button("Search Jobs"):
    if not query.strip():
        st.warning("Please enter a job keyword.")
        st.stop()

    increment_jobs_searched(user["id"])

    with st.spinner("Fetching job listings..."):
        jobs = search_jobs(query, location_filter, remote_only, page=1, num_pages=num_results)

    st.session_state["search_results"] = jobs
    st.success(f"Found {len(jobs)} matching jobs.")
    st.write("---")

# ----------------------------------------------------
# SHOW SEARCH RESULTS
# ----------------------------------------------------
results = st.session_state.get("search_results", [])

for idx, job in enumerate(results):

    job_id = str(job.get("job_id", f"job_{idx}"))
    key_prefix = f"{job_id}_{idx}"

    # Log category
    log_job_category(user["id"], query, job.get("job_title", ""))

    # --- Job card ---
    job_card(job, key_prefix=key_prefix, show_actions=False)

    # ----------------------------------------------------
    # ACTION FORM (Fix: forms prevent full refresh!)
    # ----------------------------------------------------
    with st.form(key=f"actions_form_{key_prefix}"):

        st.write("### Available Actions")

        col1, col2, col3 = st.columns(3)

        with col1:
            save_btn = st.form_submit_button("💾 Save Job")

        with col2:
            score_btn = st.form_submit_button("📊 Match Score")

        with col3:
            cover_btn = st.form_submit_button("✉️ Cover Letter")

        st.write("")

        # Additional AI Tools
        elig_btn = st.form_submit_button("🌍 Country Eligibility")
        skills_btn = st.form_submit_button("🧠 Required Skills")

        # ------------------------------------------------
        # SAVE JOB
        # ------------------------------------------------
        if save_btn:
            if is_job_saved(user["id"], job_id):
                st.info("This job is already saved.")
            else:
                save_job(user["id"], job)
                increment_jobs_saved(user["id"])
                st.success("Job saved successfully!")

        # ------------------------------------------------
        # MATCH SCORE TOOL
        # ------------------------------------------------
        if score_btn:
            st.subheader("📊 AI Job Match Score")
            resume = st.text_area(f"Paste your resume below (Job ID: {job_id})", key=f"resume_score_{key_prefix}")

            if resume:
                with st.spinner("Evaluating match score..."):
                    result = job_match_score(job.get("job_description", ""), resume)

                increment_ai_tools_used(user["id"])
                st.code(result)
            else:
                st.warning("Please paste your resume.")

        # ------------------------------------------------
        # COVER LETTER TOOL
        # ------------------------------------------------
        if cover_btn:
            st.subheader("✉️ AI Cover Letter Generator")
            resume = st.text_area(f"Paste your resume below (Job ID: {job_id})", key=f"resume_cover_{key_prefix}")

            if resume:
                with st.spinner("Generating cover letter..."):
                    letter = cover_letter(
                        job.get("job_title", ""),
                        job.get("employer_name", ""),
                        job.get("job_description", ""),
                        resume
                    )
                increment_ai_tools_used(user["id"])
                st.write(letter)
            else:
                st.warning("Please paste your resume.")

        # ------------------------------------------------
        # AI ELIGIBILITY EXTRACTION
        # ------------------------------------------------
        if elig_btn:
            st.subheader("🌍 Country Eligibility (AI Extracted)")
            with st.spinner("Analyzing eligibility..."):
                eligibility = extract_eligibility(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(eligibility)

        # ------------------------------------------------
        # SKILL EXTRACTION
        # ------------------------------------------------
        if skills_btn:
            st.subheader("🧠 Required Skills (AI Extracted)")
            with st.spinner("Extracting skills..."):
                skills = extract_skills(job.get("job_description", ""))
            increment_ai_tools_used(user["id"])
            st.code(skills)

    st.write("----")
