import datetime
from services.supabase_client import supabase

# ------------------------------------------------------
# CLEAN TEXT
# ------------------------------------------------------
def clean_text(text: str):
    if not text:
        return ""
    return (
        text.replace("<br>", "\n")
            .replace("<br/>", "\n")
            .replace("<p>", "")
            .replace("</p>", "")
            .strip()
    )

# ------------------------------------------------------
# SAVE JOB (final fix)
# ------------------------------------------------------
def save_job(user_id: str, job_data: dict):
    """
    Saves a job into saved_jobs table using proper JSON format.
    """
    job_id = str(job_data.get("job_id", ""))

    payload = {
        "user_id": user_id,
        "job_id": job_id,
        "job_title": job_data.get("job_title"),
        "company": job_data.get("employer_name"),
        "job_data": job_data,  # JSON saved safely
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    supabase.table("saved_jobs").insert(payload).execute()

# ------------------------------------------------------
# CHECK IF JOB IS ALREADY SAVED (final fix)
# ------------------------------------------------------
def is_job_saved(user_id: str, job_id: str):
    """
    Check if job already saved — fixed JSON path error.
    """
    result = (
        supabase.table("saved_jobs")
        .select("id")
        .eq("user_id", user_id)
        .eq("job_id", job_id)  # use plain column, NOT JSON path
        .execute()
    )
    return len(result.data) > 0

# ------------------------------------------------------
# GET SAVED JOBS
# ------------------------------------------------------
def get_saved_jobs(user_id: str):
    result = (
        supabase.table("saved_jobs")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []

# ------------------------------------------------------
# FORMAT DATETIME
# ------------------------------------------------------
def format_datetime(dt_str: str):
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", ""))
        return dt.strftime("%b %d, %Y • %I:%M %p")
    except:
        return dt_str

# ------------------------------------------------------
# USER STATS
# ------------------------------------------------------
def create_user_stats(user_id: str):
    supabase.table("user_stats").insert({
        "user_id": user_id,
        "jobs_searched": 0,
        "jobs_saved": 0,
        "ai_tools_used": 0
    }).execute()

def get_user_stats(user_id: str):
    res = (
        supabase.table("user_stats")
        .select("*")
        .eq("user_id", user_id)
        .single()
        .execute()
    )
    return res.data

def increment_jobs_searched(user_id: str):
    supabase.rpc("increment_jobs_searched", {"userid": user_id}).execute()

def increment_jobs_saved(user_id: str):
    supabase.rpc("increment_jobs_saved", {"userid": user_id}).execute()

def increment_ai_tools_used(user_id: str):
    supabase.rpc("increment_ai_tools_used", {"userid": user_id}).execute()

# ------------------------------------------------------
# LOG CATEGORY (NEW)
# ------------------------------------------------------
def log_job_category(user_id: str, search_term: str, job_title: str):
    """
    Logs job search categories for analytics.
    Stores what users are searching for and what jobs appear.
    """
    try:
        supabase.table("job_categories").insert({
            "user_id": user_id,
            "search_term": search_term,
            "job_title": job_title
        }).execute()
    except Exception as e:
        print("Error logging job category:", e)

