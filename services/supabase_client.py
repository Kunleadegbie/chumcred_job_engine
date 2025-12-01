import streamlit as st
from supabase.client import Client, create_client

# ---------------------------------------------------
# SUPABASE INITIALIZATION
# ---------------------------------------------------
# Make sure your Streamlit secrets contain:
# SUPABASE_URL
# SUPABASE_KEY
#
# st.secrets["SUPABASE_URL"] = "https://xyzcompany.supabase.co"
# st.secrets["SUPABASE_KEY"] = "service_role_key"
# ---------------------------------------------------

def init_supabase() -> Client:
    """Initialize and return the Supabase client."""
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        client = create_client(url, key)
        return client
    except Exception as e:
        st.error(f"Supabase initialization failed: {str(e)}")
        st.stop()

# Global supabase instance
supabase = init_supabase()
