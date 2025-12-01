from services.supabase_client import supabase

# ----------------------------------------------------
# LOGIN FUNCTION (PLAIN PASSWORD)
# ----------------------------------------------------
def login_user(email: str, password: str):
    try:
        response = (
            supabase
            .table("users")
            .select("*")
            .eq("email", email)
            .eq("password", password)   # PLAIN TEXT CHECK
            .execute()
        )

        if response.data:
            return response.data[0], None  # <-- return (user, error)

        return None, "Invalid email or password."

    except Exception as e:
        return None, f"Login error: {str(e)}"


# ----------------------------------------------------
# ADMIN CHECK
# ----------------------------------------------------
def is_admin(user):
    return user.get("role", "").lower() == "admin"


# ----------------------------------------------------
# GET ALL USERS
# ----------------------------------------------------
def get_all_users():
    res = supabase.table("users").select("*").execute()
    return res.data if res.data else []


# ----------------------------------------------------
# BLOCK USER
# ----------------------------------------------------
def block_user(user_id):
    supabase.table("users").update({"status": "blocked"}).eq("id", user_id).execute()


# ----------------------------------------------------
# UNBLOCK USER
# ----------------------------------------------------
def unblock_user(user_id):
    supabase.table("users").update({"status": "active"}).eq("id", user_id).execute()
