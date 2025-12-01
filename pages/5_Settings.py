import streamlit as st
from components.sidebar import show_sidebar
from services.auth import is_admin

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user

if not is_admin(user):
    st.error("Access Denied. You must be an admin to view this page.")
    st.stop()

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("⚙️ System Settings (Admin Only)")
st.write("Configure platform-wide settings. Future features will appear here.")

st.write("---")

# ----------------------------------------------------
# API KEYS PREVIEW (ENCRYPTED FOR SAFETY)
# ----------------------------------------------------
st.subheader("🔐 API Configuration (Read-Only)")

st.info(
    "These values are stored in Streamlit **Secrets** and are required for "
    "API access and system operation. They cannot be changed here."
)

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Supabase URL:**")
    st.code(st.secrets.get("SUPABASE_URL", "Not Set"))

    st.markdown("**OpenAI Key:**")
    st.code("sk-..." if st.secrets.get("OPENAI_API_KEY") else "Not Set")

with col2:
    st.markdown("**RapidAPI Key:**")
    st.code("rapidapi-..." if st.secrets.get("RAPIDAPI_KEY") else "Not Set")

    st.markdown("**Supabase Key:**")
    st.code("sb-..." if st.secrets.get("SUPABASE_KEY") else "Not Set")

st.write("---")

# ----------------------------------------------------
# SYSTEM ANNOUNCEMENT (Admin Broadcast)
# ----------------------------------------------------
st.subheader("📢 System Announcement")

announcement = st.text_area(
    "Write a broadcast message (for future build: send to all users).",
    placeholder="E.g., New AI features launching next week!"
)

if st.button("Save Announcement (Not Yet Live)"):
    st.success("Announcement saved (placeholder). Full messaging system will be added in future updates.")

st.write("---")

# ----------------------------------------------------
# FUTURE SETTINGS PLACEHOLDERS
# ----------------------------------------------------
st.subheader("🧩 Future Configuration Options")

st.checkbox("Enable WhatsApp Job Alerts (Coming Soon)", value=False, disabled=True)
st.checkbox("Enable Email Digest (Coming Soon)", value=False, disabled=True)
st.checkbox("Enable Advanced AI Resume Builder (Coming Soon)", value=False, disabled=True)
st.checkbox("Enable Multi–Job API Integration (Coming Soon)", value=False, disabled=True)

st.write("---")
st.caption("Chumcred Job Engine — Admin Settings © 2025")
