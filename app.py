import streamlit as st
from services.auth import login_user
from components.sidebar import redirect_to_dashboard

st.set_page_config(
    page_title="Chumcred Job Engine",
    page_icon="🌍",
    layout="centered"
)

# Initialize session state
if "user" not in st.session_state:
    st.session_state.user = None

# If already logged in → go to Dashboard immediately
if st.session_state.user:
    redirect_to_dashboard()

# --------------------------
# LOGIN PAGE UI
# --------------------------
st.title("🔐 Chumcred Job Engine Login")
st.write("Enter your credentials below to continue.")

email = st.text_input("Email Address")
password = st.text_input("Password", type="password")

if st.button("Login"):
    user, error = login_user(email, password)
    if error:
        st.error(error)
    else:
        st.session_state.user = user
        st.success("Login successful! Redirecting...")
        redirect_to_dashboard()

# Footer
st.write("---")
st.caption("Powered by Chumcred Limited © 2025")

