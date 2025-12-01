import streamlit as st
from components.sidebar import show_sidebar
from services.auth import create_user, is_admin
from services.supabase_client import (
    supabase_rest_query,
    supabase_rest_update
)

# ----------------------------------------------------
# ACCESS CONTROL
# ----------------------------------------------------
if "user" not in st.session_state or st.session_state.user is None:
    st.error("You must log in to access this page.")
    st.stop()

user = st.session_state.user

if not is_admin(user):
    st.error("Unauthorized access. Admins only.")
    st.stop()

# Sidebar
show_sidebar(user)

# ----------------------------------------------------
# PAGE HEADER
# ----------------------------------------------------
st.title("🛠️ Admin Panel")
st.write("Manage users: create accounts, block/unblock users, view roles.")

st.write("---")

# ----------------------------------------------------
# FETCH USERS
# ----------------------------------------------------
users = supabase_rest_query("users")

if isinstance(users, dict) and "error" in users:
    st.error("Failed to load users.")
    st.stop()

st.subheader("👥 User Accounts")

for u in users:

    st.write(f"### {u['full_name']}")

    col1, col2, col3, col4 = st.columns(4)

    col1.write(f"**Email:** {u['email']}")
    col2.write(f"**Role:** {u['role']}")
    col3.write(f"**Status:** {u['status']}")

    with col4:
        if u["status"] == "active":
            if st.button("Block User", key=f"block_{u['id']}"):
                supabase_rest_update(
                    "users",
                    {"id": u["id"]},
                    {"status": "blocked"}
                )
                st.success("User blocked.")
                st.rerun()
        else:
            if st.button("Unblock User", key=f"unblock_{u['id']}"):
                supabase_rest_update(
                    "users",
                    {"id": u["id"]},
                    {"status": "active"}
                )
                st.success("User unblocked.")
                st.rerun()

    st.write("---")

# ----------------------------------------------------
# CREATE NEW USER (ADMIN)
# ----------------------------------------------------
st.subheader("➕ Create New User")

with st.form("create_user_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    status = "active"

    submitted = st.form_submit_button("Create User")

    if submitted:
        response = create_user(full_name, email, password, role, status)

        if isinstance(response, dict) and "error" in response:
            st.error("Error creating user.")
        else:
            st.success("User created successfully.")
            st.rerun()
