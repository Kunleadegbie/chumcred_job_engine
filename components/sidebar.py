import streamlit as st

# ----------------------------------------------------
# SIDEBAR MENU
# ----------------------------------------------------
def show_sidebar(user):

    with st.sidebar:

        st.markdown(f"### 👋 Welcome, {user['full_name']}")
        st.markdown(f"**Role:** {user['role']}")

        st.write("---")

        # ---- MAIN MENU ----
        st.page_link("pages/1_Dashboard.py", label="📊 Dashboard")
        st.page_link("pages/2_Job_Search.py", label="🔍 Job Search")
        st.page_link("pages/3_Saved_Jobs.py", label="💾 Saved Jobs")
        st.page_link("pages/5_Settings.py", label="⚙️ Settings")
        st.page_link("pages/6_Profile.py", label="👤 My Profile")

        # ---- ADMIN MENU ----
        if user["role"] == "admin":
            st.write("---")
            st.markdown("### 🛠️ Admin Tools")
            st.page_link("pages/4_Admin_Panel.py", label="🧑‍💼 Manage Users")
            st.page_link("pages/7_Admin_Analytics.py", label="📈 Analytics Dashboard")

        st.write("---")

        # ---- LOGOUT ----
        if st.button("🚪 Log Out"):
            st.session_state.user = None
            st.rerun()
