import streamlit as st
from components.sidebar import show_sidebar

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access your profile.")
    st.stop()

user = st.session_state.user

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("👤 Profile")
st.write("Manage your personal information and account settings.")

st.write("---")

# ----------------------------------------------------
# PROFILE CARD
# ----------------------------------------------------
st.subheader("📄 Account Information")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown(f"### **{user['full_name']}**")
    st.markdown(f"**📧 Email:** {user['email']}")
    st.markdown(f"**🔑 Role:** {user['role'].capitalize()}")
    st.markdown(f"**🟢 Status:** {'Active' if user['status']=='active' else 'Blocked'}")

with col2:
    st.image(
        "https://api.dicebear.com/7.x/initials/svg?seed=" + user['full_name'],
        caption="Profile Avatar",
        width=130
    )

st.write("---")

# ----------------------------------------------------
# PASSWORD UPDATE (COMING SOON)
# ----------------------------------------------------
st.subheader("🔒 Password Management")

st.info("Password reset & update functionality will be added soon.")

with st.expander("Why can't I update my password yet?"):
    st.write("""
        - Password update requires additional Supabase configurations  
        - Requires secure email verification workflow  
        - Will be added in the next development update  
    """)

st.write("---")

# ----------------------------------------------------
# ACCOUNT META DATA (FUTURE)
# ----------------------------------------------------
st.subheader("🧾 Account Activity (Coming Soon)")
st.caption("This will include login history, job search statistics, AI usage statistics, and more.")

st.write("---")

st.caption("Chumcred Job Engine — Profile Page © 2025")
