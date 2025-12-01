import streamlit as st
from components.sidebar import show_sidebar
from services.utils import get_saved_jobs, format_datetime

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("💾 Saved Jobs")
st.write("Jobs you have saved for later review.")

st.write("---")

# ----------------------------------------------------
# FETCH SAVED JOBS
# ----------------------------------------------------
jobs = get_saved_jobs(user["id"])

if not jobs:
    st.info("You have not saved any jobs yet.")
    st.stop()

# ----------------------------------------------------
# DISPLAY SAVED JOBS
# ----------------------------------------------------
for job in jobs:

    job_data = job.get("job_data", {})

    st.subheader(job_data.get("job_title", "Unknown Role"))

    st.write(f"**Company:** {job_data.get('employer_name', 'Unknown')}")
    st.write(f"**Country:** {job_data.get('job_country', 'N/A')}")

    created_at = job.get("created_at", "")
    st.write(f"**Saved On:** {format_datetime(created_at)}")

    st.write("---")

    st.write(job_data.get("job_description", "")[:300] + "...")

    st.write("---")

    apply_link = job_data.get("job_apply_link") or job_data.get("job_apply_url")
    if apply_link:
        st.markdown(f"[🔗 Apply Here]({apply_link})", unsafe_allow_html=True)

    st.write("----")
