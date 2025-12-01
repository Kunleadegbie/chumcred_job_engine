import streamlit as st
from components.sidebar import show_sidebar
from services.utils import get_user_stats
from datetime import datetime

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
st.title("📊 Dashboard Overview")
st.write("Track your job search activities and AI usage.")

st.write("---")

# ----------------------------------------------------
# FETCH USER STATS
# ----------------------------------------------------
stats = get_user_stats(user["id"])

# If stats do not exist (older users), create them
if not stats:
    create_user_stats(user["id"])
    stats = get_user_stats(user["id"])

jobs_searched = stats.get("jobs_searched", 0)
jobs_saved = stats.get("jobs_saved", 0)
ai_tools_used = stats.get("ai_tools_used", 0)

# ----------------------------------------------------
# LIVE METRICS
# ----------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("🔍 Jobs Searched", jobs_searched)
col2.metric("💾 Jobs Saved", jobs_saved)
col3.metric("🤖 AI Tools Used", ai_tools_used)

st.write("---")

# ----------------------------------------------------
# USER INFO SECTION
# ----------------------------------------------------
st.subheader("👤 User Profile Summary")

st.write(f"**Name:** {user.get('full_name')}")
st.write(f"**Email:** {user.get('email')}")
st.write(f"**Role:** {user.get('role')}")
st.write(f"**Status:** {user.get('status')}")

st.write("---")

# ----------------------------------------------------
# ACTIVITY SUMMARY
# ----------------------------------------------------
st.subheader("📈 Activity Insights")

if jobs_searched == 0 and jobs_saved == 0 and ai_tools_used == 0:
    st.info("No activity yet. Start searching for jobs to see insights here.")
else:
    st.success("You're actively using the platform. Keep going!")

st.write("---")

st.write("Last updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
