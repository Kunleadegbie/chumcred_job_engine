# services/auth.py  (FINAL REST VERSION)

import streamlit as st
from services.supabase_client import (
    supabase_rest_query,
    supabase_rest_insert,
)

# ----------------------------------------------------
# LOGIN FUNCTION
# ----------------------------------------------------
def login_user(email, password):
    """
    Authenticates a user using Supabase REST.
    Always returns ONLY the user dictionary or None.
    """

    response = supabase_rest_query(
        table="users",
        filters={
            "email": email,
            "password": password,
            "status": "active"
        }
    )

    # If Supabase returned error
    if isinstance(response, dict) and "error" in response:
        return None

    # If no matching user
    if not isinstance(response, list) or len(response) == 0:
        return None

    # SUCCESS — return user dict
    return response[0]

# ----------------------------------------------------
# CREATE USER (Admin Only)
# ----------------------------------------------------
def create_user(full_name, email, password, role="user", status="active"):
    payload = {
        "full_name": full_name,
        "email": email,
        "password": password,
        "role": role,
        "status": status,
    }

    return supabase_rest_insert("users", payload)


# ----------------------------------------------------
# CHECK ADMIN
# ----------------------------------------------------
def is_admin(user):
    return user.get("role", "") == "admin"
