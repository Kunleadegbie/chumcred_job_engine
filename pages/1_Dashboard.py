import streamlit as st
from components.sidebar import show_sidebar
from services.utils import (
    get_user_stats,
    create_user_stats
)
from services.supabase_client import supabase_rest_query

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
st.title("🏠 User Dashboard")
st.write(f"Welcome, **{user['full_name']}**!")

st.write("---")

# ----------------------------------------------------
# LOAD USER STATS (REST)
# ----------------------------------------------------
stats = get_user_stats(user["id"])

# If user has no stats record, create one
if stats is None:
    create_user_stats(user["id"])
    stats = get_user_stats(user["id"])

# Safety: Default values if partial record exists
jobs_searched = stats.get("jobs_searched", 0)
jobs_saved = stats.get("jobs_saved", 0)
ai_used = stats.get("ai_tools_used", 0)

# ----------------------------------------------------
# DISPLAY USER ANALYTICS
# ----------------------------------------------------
st.subheader("📊 Your Usage Statistics")

col1, col2, col3 = st.columns(3)

col1.metric("Jobs Searched", jobs_searched)
col2.metric("Jobs Saved", jobs_saved)
col3.metric("AI Tools Used", ai_used)

st.write("---")

# ----------------------------------------------------
# SHORTCUT LINKS
# ----------------------------------------------------
st.subheader("🚀 Quick Actions")

colA, colB, colC = st.columns(3)

with colA:
    if st.button("🔍 Search Jobs"):
        st.switch_page("pages/2_Job_Search.py")

with colB:
    if st.button("💾 View Saved Jobs"):
        st.switch_page("pages/3_Saved_Jobs.py")

with colC:
    if st.button("🤖 Try AI Tools"):
        st.switch_page("pages/2_Job_Search.py")

st.write("---")

# FOOTER
st.caption("Powered by **Chumcred Job Engine** — AI-enhanced global job search platform.")
