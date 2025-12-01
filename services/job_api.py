import requests
import streamlit as st

RAPIDAPI_KEY = st.secrets["RAPIDAPI_KEY"]

API_URL = "https://jsearch.p.rapidapi.com/search"

HEADERS = {
    "x-rapidapi-key": RAPIDAPI_KEY,
    "x-rapidapi-host": "jsearch.p.rapidapi.com"
}

def search_jobs(query, location="", remote_only=True, page=1, num_pages=1):
    """
    Search global jobs using JSearch (RapidAPI).
    """

    params = {
        "query": query,
        "page": page,
    }

    # Optional filters
    if location:
        params["country"] = location

    if remote_only:
        params["remote_jobs_only"] = "true"

    try:
        res = requests.get(API_URL, headers=HEADERS, params=params)
        res.raise_for_status()
        data = res.json()

        if "data" not in data:
            return []

        jobs = []

        for item in data["data"]:
            jobs.append({
                "job_id": item.get("job_id"),
                "job_title": item.get("job_title"),
                "employer_name": item.get("employer_name"),
                "job_description": item.get("job_description"),
                "job_country": item.get("job_country"),
                "job_city": item.get("job_city"),
                "job_posted_at": item.get("job_posted_at"),
                "job_is_remote": item.get("job_is_remote"),
                "job_apply_link": item.get("job_apply_link"),
                "employer_logo": item.get("employer_logo")
            })

        return jobs

    except Exception as e:
        print("Error fetching jobs from API:", e)
        return []
