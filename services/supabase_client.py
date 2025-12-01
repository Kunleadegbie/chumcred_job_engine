# REST-based Supabase client (no supabase-py dependency)
import httpx
import json
import streamlit as st

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

client = httpx.Client(
    base_url=f"{SUPABASE_URL}/rest/v1",
    headers={
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
    },
    timeout=30
)

def supabase_rest_query(table: str, filters: dict = None):
    params = {"select": "*"}

    if filters:
        for col, val in filters.items():
            params[col] = f"eq.{val}"

    res = client.get(f"/{table}", params=params)

    if res.status_code != 200:
        raise Exception(f"REST GET Error: {res.text}")

    return res.json()

def supabase_rest_insert(table: str, payload: dict):
    """
    Insert a row using Supabase REST API.
    Returns JSON if available, else returns True.
    """

    url = f"{SUPABASE_URL}/rest/v1/{table}"

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"   # 🔥 THIS IS THE FIX
    }

    res = httpx.post(url, headers=headers, json=payload)

    if res.status_code >= 400:
        # return error for debugging
        try:
            return {"error": res.json()}
        except:
            return {"error": res.text}

    # Supabase ALWAYS returns JSON now
    try:
        return res.json()
    except:
        return True

def supabase_rest_update(table: str, filters: dict, data: dict):
    params = {col: f"eq.{val}" for col, val in filters.items()}

    res = client.patch(
        f"/{table}",
        params=params,
        content=json.dumps(data),
        headers={"Content-Type": "application/json"}
    )

    if res.status_code not in (200, 204):
        raise Exception(f"REST UPDATE Error: {res.text}")

    return res.json() if res.text else {}

def supabase_rest_delete(table: str, filters: dict):
    params = {col: f"eq.{val}" for col, val in filters.items()}

    res = client.delete(f"/{table}", params=params)

    if res.status_code not in (200, 204):
        raise Exception(f"REST DELETE Error: {res.text}")

    return True
