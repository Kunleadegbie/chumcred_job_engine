import streamlit as st
from services.utils import clean_text

def job_card(job_data, key_prefix="", show_actions=False):

    st.subheader(job_data.get("job_title", "Untitled Role"))

    company = job_data.get("employer_name", "Unknown")
    country = job_data.get("job_country", "N/A")
    city = job_data.get("job_city", "")
    remote = job_data.get("job_is_remote", False)

    st.markdown(f"**🏢 Company:** {company}")
    st.markdown(f"**🌍 Country:** {country}")
    if city:
        st.markdown(f"**📍 City:** {city}")

    st.markdown("**💻 Remote:** Yes" if remote else "**🏢 Remote:** No")
    st.write("---")

    desc = clean_text(job_data.get("job_description", ""))[:350]
    st.markdown("### 📄 Job Summary")
    st.write(desc + "...")
    st.write("---")

    # APPLY LINK
    link = job_data.get("job_apply_link") or job_data.get("job_apply_url")
    if link:
        st.markdown(f"[🔗 Apply Here]({link})", unsafe_allow_html=True)
    else:
        st.warning("No application link available.")

    st.write("---")

    if show_actions:
        s1, s2, s3 = st.columns(3)

        # SAVE BUTTON
        if s1.button("Save Job", key=f"{key_prefix}_save_btn"):
            st.session_state[f"{key_prefix}_save"] = True

        # MATCH SCORE BUTTON
        if s2.button("AI Match Score", key=f"{key_prefix}_score_btn"):
            st.session_state[f"{key_prefix}_score"] = True

        # COVER LETTER BUTTON
        if s3.button("Cover Letter", key=f"{key_prefix}_cover_btn"):
            st.session_state[f"{key_prefix}_cover"] = True

    st.write("----")
