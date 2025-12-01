# 🌍 Chumcred Job Engine (AI-Powered Remote Job Search)

The **Chumcred Job Engine** is a powerful AI-driven platform designed to help users search, analyze, and apply for global remote jobs.  
Built with **Streamlit + Supabase + OpenAI**, it offers advanced tools that go far beyond traditional job portals like LinkedIn or Indeed.

---

## 🚀 Key Features

### 🔍 Global Job Search (via RapidAPI – JSearch)
- Search remote or global jobs by keywords  
- Filter jobs by country or region  
- Multi-page API results (1–5 pages)  

### 🤖 AI-Powered Tools
- **Resume–Job Match Score (0–100)**  
- **AI Cover Letter Generator**  
- **Country Eligibility Detection**  
- **Visa Sponsorship Classification**  
- **Skill Extraction (Hard + Soft Skills)**  

### 💾 Save Jobs
- Bookmark jobs for later  
- Saved jobs dashboard  
- API-linked job data stored in Supabase  

### 🔐 Authentication System
- Login with email + password  
- SHA256 hashed password security  
- Supabase database backend  

### 👥 Admin Panel (RBAC)
Admins can:
- View all users  
- Block / Unblock user accounts  
- View roles & status  

### ⚙️ Settings Page (Admin Only)
- API configuration preview  
- System announcements  
- Future feature toggles  

### 👤 User Profile Page
- View account information  
- Avatar  
- Role & status  
- Password update (coming soon)  

---

## 🗂 Project Structure
chumcred_job_engine/
│
├── app.py
├── README.md
├── requirements.txt
│
├── .streamlit/
│ └── config.toml
│
├── config/
│ └── settings.py
│
├── services/
│ ├── supabase_client.py
│ ├── auth.py
│ ├── job_api.py
│ ├── ai_engine.py
│ └── utils.py
│
├── components/
│ ├── sidebar.py
│ ├── job_card.py
│ └── styles.css
│
└── pages/
├── 1_Dashboard.py
├── 2_Job_Search.py
├── 3_Saved_Jobs.py
├── 4_Admin_Panel.py
├── 5_Settings.py
└── 6_Profile.py


---

## 🔐 Environment Variables (Streamlit Secrets)

Add the following:

```toml
SUPABASE_URL = "https://your.supabase.co"
SUPABASE_KEY = "service_role_key"
OPENAI_API_KEY = "sk-xxxx"
RAPIDAPI_KEY = "your_rapidapi_key"

🏢 Powered by Chumcred Limited

This platform is part of Chumcred’s mission to empower global job seekers with AI, intelligence, and opportunity visibility.


