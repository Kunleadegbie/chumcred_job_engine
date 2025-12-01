import json
import datetime
from services.supabase_client import (
    supabase_rest_query,
    supabase_rest_insert,
    supabase_rest_update
)

# -------------------------------------------------------------
# CLEAN TEXT (remove HTML)
# -------------------------------------------------------------
def clean_text(text: str):
    if not text:
        return ""

    cleaned = (
        text.replace("<br>", "\n")
            .replace("<br/>", "\n")
            .replace("<p>", "")
            .replace("</p>", "")
            .replace("<li>", "- ")
            .replace("</li>", "")
            .strip()
    )
    return cleaned


# -------------------------------------------------------------
# FORMAT DATETIME
# -------------------------------------------------------------
def format_datetime(dt_str: str):
    try:
        dt = datetime.datetime.fromisoformat(dt_str.replace("Z", ""))
        return dt.strftime("%b %d, %Y • %I:%M %p")
    except:
        return dt_str


# -------------------------------------------------------------
# SAVE JOB (REST)
# -------------------------------------------------------------
def save_job(user_id: str, job_data: dict):

    payload = {
        "user_id": user_id,
        "job_id": job_data.get("job_id", "unknown"),
        "company": job_data.get("employer_name", ""),
        "job_title": job_data.get("job_title", ""),
        "job_data": json.dumps(job_data),
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    return supabase_rest_insert("saved_jobs", payload)


# -------------------------------------------------------------
# GET SAVED JOBS (REST)
# -------------------------------------------------------------
def get_saved_jobs(user_id: str):

    rows = supabase_rest_query("saved_jobs", filters={"user_id": user_id})

    if not rows or isinstance(rows, dict) and "error" in rows:
        return []

    # Sort newest first
    rows = sorted(rows, key=lambda x: x.get("created_at", ""), reverse=True)

    # Decode job JSON
    for row in rows:
        try:
            if isinstance(row.get("job_data"), str):
                row["job_data"] = json.loads(row["job_data"])
        except:
            pass

    return rows


# -------------------------------------------------------------
# CHECK IF JOB IS ALREADY SAVED
# -------------------------------------------------------------
def is_job_saved(user_id: str, job_id: str):

    rows = supabase_rest_query(
        "saved_jobs",
        filters={"user_id": user_id, "job_id": job_id}
    )

    return isinstance(rows, list) and len(rows) > 0


# -------------------------------------------------------------
# CREATE USER STATS ENTRY
# -------------------------------------------------------------
def create_user_stats(user_id: str):

    payload = {
        "user_id": user_id,
        "jobs_searched": 0,
        "jobs_saved": 0,
        "ai_tools_used": 0
    }

    supabase_rest_insert("user_stats", payload)


# -------------------------------------------------------------
# GET A USER'S STATS
# -------------------------------------------------------------
def get_user_stats(user_id: str):

    rows = supabase_rest_query("user_stats", filters={"user_id": user_id})

    if not rows:
        return None

    return rows[0]


# -------------------------------------------------------------
# INCREMENT JOBS SEARCHED
# -------------------------------------------------------------
def increment_jobs_searched(user_id: str):

    stats = get_user_stats(user_id)
    if not stats:
        return

    updated = {
        "jobs_searched": stats["jobs_searched"] + 1
    }

    supabase_rest_update("user_stats", {"user_id": user_id}, updated)


# -------------------------------------------------------------
# INCREMENT JOBS SAVED
# -------------------------------------------------------------
def increment_jobs_saved(user_id: str):

    stats = get_user_stats(user_id)
    if not stats:
        return

    updated = {
        "jobs_saved": stats["jobs_saved"] + 1
    }

    supabase_rest_update("user_stats", {"user_id": user_id}, updated)


# -------------------------------------------------------------
# INCREMENT AI TOOLS USED
# -------------------------------------------------------------
def increment_ai_tools_used(user_id: str):

    stats = get_user_stats(user_id)
    if not stats:
        return

    updated = {
        "ai_tools_used": stats["ai_tools_used"] + 1
    }

    supabase_rest_update("user_stats", {"user_id": user_id}, updated)


# -------------------------------------------------------------
# LOG JOB CATEGORY
# -------------------------------------------------------------
def log_job_category(user_id: str, search_term: str, job_title: str):

    payload = {
        "user_id": user_id,
        "search_term": search_term,
        "job_title": job_title,
        "created_at": datetime.datetime.utcnow().isoformat()
    }

    supabase_rest_insert("job_categories", payload)
