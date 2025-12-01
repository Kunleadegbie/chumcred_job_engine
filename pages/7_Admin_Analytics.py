import streamlit as st
import pandas as pd
import plotly.express as px
from components.sidebar import show_sidebar
from services.supabase_client import supabase
from io import BytesIO

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user

if user["role"] != "admin":
    st.error("Unauthorized access. Admins only.")
    st.stop()

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("📊 Admin Analytics Dashboard (Full Suite)")
st.write("Advanced insights, trends, and exportable analytics for administrators.")
st.write("---")

# ----------------------------------------------------
# FETCH USERS + STATS
# ----------------------------------------------------
users = supabase.table("users").select("*").execute().data
stats = supabase.table("user_stats").select("*").execute().data

users_df = pd.DataFrame(users)
stats_df = pd.DataFrame(stats)

# Merge users with their stats
merged = users_df.merge(stats_df, left_on="id", right_on="user_id", how="left")

# ----------------------------------------------------
# HIGH-LEVEL USER METRICS
# ----------------------------------------------------
st.subheader("👥 User Metrics Overview")

total_users = len(users_df)
active_users = len(users_df[users_df["status"] == "active"])
blocked_users = len(users_df[users_df["status"] == "blocked"])
admin_users = len(users_df[users_df["role"] == "admin"])
regular_users = total_users - admin_users

col1, col2, col3 = st.columns(3)
col1.metric("Total Users", total_users)
col2.metric("Active Users", active_users)
col3.metric("Blocked Users", blocked_users)

col4, col5 = st.columns(2)
col4.metric("Admin Accounts", admin_users)
col5.metric("Regular Users", regular_users)

st.write("---")

# ----------------------------------------------------
# PLATFORM-WIDE USAGE METRICS
# ----------------------------------------------------
st.subheader("📈 Platform Usage Metrics")

total_searches = merged["jobs_searched"].sum()
total_saved = merged["jobs_saved"].sum()
total_ai = merged["ai_tools_used"].sum()

avg_searches = merged["jobs_searched"].mean().round(2)
avg_saved = merged["jobs_saved"].mean().round(2)
avg_ai = merged["ai_tools_used"].mean().round(2)

col1, col2, col3 = st.columns(3)
col1.metric("🔍 Total Jobs Searched", total_searches)
col2.metric("💾 Total Jobs Saved", total_saved)
col3.metric("🤖 Total AI Tools Used", total_ai)

col4, col5, col6 = st.columns(3)
col4.metric("Avg Searches/User", avg_searches)
col5.metric("Avg Saves/User", avg_saved)
col6.metric("Avg AI Tools/User", avg_ai)

st.write("---")

# ----------------------------------------------------
# CHARTS SECTION
# ----------------------------------------------------
st.subheader("📊 Visual Analytics (Charts)")

# Bar chart: Jobs searched by user
fig1 = px.bar(
    merged,
    x="full_name",
    y="jobs_searched",
    title="Jobs Searched by User",
    labels={"full_name": "User", "jobs_searched": "Jobs Searched"},
)
st.plotly_chart(fig1, use_container_width=True)

# Bar chart: AI tools used by user
fig2 = px.bar(
    merged,
    x="full_name",
    y="ai_tools_used",
    title="AI Tools Used by User",
)
st.plotly_chart(fig2, use_container_width=True)

# Pie chart: Active vs Blocked Users
fig3 = px.pie(
    users_df,
    names="status",
    title="Active vs Blocked Users",
)
st.plotly_chart(fig3, use_container_width=True)

st.write("---")

# ----------------------------------------------------
# LEADERBOARDS
# ----------------------------------------------------
st.subheader("🏆 Leaderboards")

def leaderboard(title, column):
    st.write(f"### {title}")
    top = merged.sort_values(by=column, ascending=False).head(10)
    for idx, row in top.iterrows():
        st.write(f"**{row['full_name']}** — {row[column]}")
    st.write("")

leaderboard("Top Job Searchers", "jobs_searched")
leaderboard("Top Job Savers", "jobs_saved")
leaderboard("Top AI Tool Users", "ai_tools_used")

st.write("---")

# ----------------------------------------------------
# JOB CATEGORY ANALYTICS
# ----------------------------------------------------
st.subheader("🗂️ Job Category Analytics")

job_cat = supabase.table("job_categories").select("*").execute().data
job_cat_df = pd.DataFrame(job_cat)

if len(job_cat_df) == 0:
    st.info("No job category analytics available yet.")
else:
    # Count categories
    category_counts = job_cat_df["category"].value_counts().reset_index()
    category_counts.columns = ["Category", "Count"]

    # Bar chart of categories
    fig_cat = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Most Common Job Categories",
        color="Category",
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    # Top job titles
    st.write("### 🔝 Top Job Titles Searched")
    top_titles = job_cat_df["job_title"].value_counts().head(10)
    st.table(top_titles)

    # Top search queries
    st.write("### 🔍 Most Popular Search Queries")
    top_queries = job_cat_df["search_query"].value_counts().head(10)
    st.table(top_queries)

st.write("---")

# ----------------------------------------------------
# EXPORT ANALYTICS (CSV & EXCEL)
# ----------------------------------------------------
st.subheader("📥 Export Analytics")

def download_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Analytics")
    return output.getvalue()

col1, col2 = st.columns(2)

col1.download_button(
    label="⬇️ Download CSV",
    data=merged.to_csv(index=False),
    file_name="analytics_data.csv",
    mime="text/csv"
)

col2.download_button(
    label="⬇️ Download Excel",
    data=download_excel(merged),
    file_name="analytics_data.xlsx",
    mime="application/vnd.ms-excel"
)

st.write("---")

# ----------------------------------------------------
# RAW DATA (for transparency)
# ----------------------------------------------------
st.subheader("📋 Raw Data Tables")

with st.expander("View Users Table"):
    st.dataframe(users_df)

with st.expander("View User Stats Table"):
    st.dataframe(stats_df)

with st.expander("View Job Category Logs"):
    if len(job_cat_df) > 0:
        st.dataframe(job_cat_df)
    else:
        st.write("No job category logs found.")
