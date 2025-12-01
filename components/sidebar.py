import streamlit as st
from services.auth import is_admin

# -------------------------------------------------------
# REDIRECT TO DASHBOARD
# -------------------------------------------------------
def redirect_to_dashboard():
    """Redirect the logged-in user to the Dashboard page."""
    st.switch_page("pages/1_Dashboard.py")


# -------------------------------------------------------
# SIDEBAR MENU
# -------------------------------------------------------
def show_sidebar(user):
    """Display the sidebar menu with role-based options."""

    st.sidebar.title("🌍 Chumcred Job Engine")
    st.sidebar.caption("Powered by Chumcred Limited")

    # ---------------------------
    # USER INFO SECTION
    # ---------------------------
    st.sidebar.markdown(f"**👤 {user['full_name']}**")
    st.sidebar.markdown(f"**Role:** {user['role'].capitalize()}")
    st.sidebar.write("---")

    # ---------------------------
    # COMMON MENU ITEMS
    # ---------------------------
    st.sidebar.page_link("pages/1_Dashboard.py", label="🏠 Dashboard")
    st.sidebar.page_link("pages/2_Job_Search.py", label="🔍 Job Search")
    st.sidebar.page_link("pages/3_Saved_Jobs.py", label="💾 Saved Jobs")
    st.sidebar.page_link("pages/6_Profile.py", label="👤 Profile")

    # ---------------------------
    # ADMIN MENU ITEMS
    # ---------------------------
    if is_admin(user):
        st.sidebar.write("---")
        st.sidebar.page_link("pages/4_Admin_Panel.py", label="🛠 Admin Panel")
        st.sidebar.page_link("pages/5_Settings.py", label="⚙ Settings")

    st.sidebar.write("---")

    # ---------------------------
    # LOGOUT
    # ---------------------------
    if st.sidebar.button("Logout 🚪"):
        st.session_state.user = None
        st.rerun()
