import streamlit as st
from components.sidebar import show_sidebar
from components.job_card import job_card
from services.utils import get_saved_jobs, format_datetime

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access Saved Jobs.")
    st.stop()

user = st.session_state.user

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("💾 Saved Jobs")
st.write("Here are the jobs you've saved for later review.")

st.write("---")

# ----------------------------------------------------
# FETCH SAVED JOBS
# ----------------------------------------------------
saved = get_saved_jobs(user["id"])

if not saved:
    st.info("You have not saved any jobs yet. Try searching for jobs and saving them.")
    st.stop()

# ----------------------------------------------------
# DISPLAY SAVED JOBS
# ----------------------------------------------------
for idx, item in enumerate(saved):

    job_data = item.get("job_data")
    saved_date = format_datetime(item.get("created_at", ""))

    st.markdown(f"🕒 **Saved on:** {saved_date}")

    # Render job card WITHOUT action buttons
    job_card(job_data, key_prefix=f"saved_{idx}", show_actions=False)

    st.write("---")
