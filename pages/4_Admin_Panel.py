import streamlit as st
from components.sidebar import show_sidebar
from services.auth import get_all_users, block_user, unblock_user
from services.utils import create_user_stats
from services.supabase_client import supabase

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
st.title("🛠️ Admin Panel")
st.write("Manage users, access controls, and system administration.")

st.write("---")

# ----------------------------------------------------
# SECTION 1: CREATE NEW USER
# ----------------------------------------------------
st.subheader("➕ Create New User")

with st.form("create_user_form"):
    full_name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    password = st.text_input("Password", type="password")
    role = st.selectbox("Role", ["user", "admin"])
    status = st.selectbox("Status", ["active", "blocked"])

    submit_user = st.form_submit_button("Create User")

if submit_user:
    if not full_name or not email or not password:
        st.warning("All fields except role/status are required.")
    else:
        try:
            # Insert into Supabase
            res = supabase.table("users").insert({
                "full_name": full_name,
                "email": email,
                "password": password,
                "role": role,
                "status": status
            }).execute()

            if res.data:
                new_user_id = res.data[0]["id"]

                # 🔥 Automatically create stats
                create_user_stats(new_user_id)

                st.success(f"User '{full_name}' created successfully.")
                st.rerun()
            else:
                st.error("Failed to create user. Try again.")

        except Exception as e:
            st.error(f"Error: {str(e)}")

st.write("---")

# ----------------------------------------------------
# SECTION 2: MANAGE USERS
# ----------------------------------------------------
st.subheader("👥 Manage Users")

users = get_all_users()

if not users:
    st.info("No users found.")
else:
    for u in users:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.write(f"**{u['full_name']}** ({u['email']})")
            st.write(f"Role: {u['role']}")

        with col2:
            if u["status"] == "active":
                st.markdown("<span style='color: green; font-weight: bold;'>Active</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span style='color: red; font-weight: bold;'>Blocked</span>", unsafe_allow_html=True)

        with col3:
            if u["id"] == user["id"]:
                st.write("⛔ Cannot modify self")
            else:
                if u["status"] == "active":
                    if st.button(f"Block {u['full_name']}", key=f"block_{u['id']}"):
                        block_user(u["id"])
                        st.success(f"User {u['full_name']} blocked.")
                        st.rerun()
                else:
                    if st.button(f"Unblock {u['full_name']}", key=f"unblock_{u['id']}"):
                        unblock_user(u["id"])
                        st.success(f"User {u['full_name']} unblocked.")
                        st.rerun()

        with col4:
            st.write(f"ID: {u['id']}")

        st.write("---")
