import streamlit as st
import os
from dotenv import load_dotenv

# Load .env for local development
load_dotenv()

# Support Streamlit Cloud secrets as well
groq_key = os.environ.get("GROQ_API_KEY")
if not groq_key:
    try:
        groq_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        pass
if groq_key:
    os.environ["GROQ_API_KEY"] = groq_key

st.set_page_config(
    page_title="AI Study Buddy 🎓",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Custom CSS for premium look ----
st.markdown("""
<style>
    .hero-container {
        background: linear-gradient(135deg, #1a1a3e 0%, #2d2b7a 50%, #1a1a3e 100%);
        border-radius: 16px;
        padding: 3rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(124, 58, 237, 0.4);
        box-shadow: 0 0 40px rgba(124, 58, 237, 0.2);
    }
    .hero-title { font-size: 3rem; font-weight: 800; color: #FFFFFF; margin-bottom: 0.5rem; letter-spacing: -1px; }
    .hero-subtitle { font-size: 1.25rem; color: #C4B5FD; margin-bottom: 1.5rem; }
    .hero-badge {
        display: inline-block;
        background: rgba(124,58,237,0.35);
        border: 1px solid #7C3AED;
        border-radius: 20px;
        padding: 4px 16px;
        font-size: 0.85rem;
        color: #DDD6FE;
        margin: 4px;
    }
    .feature-card {
        background: linear-gradient(145deg, #1A1A2E, #16213E);
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .feature-icon { font-size: 2.5rem; }
    .feature-title { font-size: 1.2rem; font-weight: 700; color: #E0E0FF; margin: 0.5rem 0 0.25rem; }
    .feature-desc { font-size: 0.9rem; color: #A0A0C0; }
    .stat-card {
        background: rgba(124,58,237,0.15);
        border: 1px solid rgba(124,58,237,0.3);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stat-number { font-size: 2rem; font-weight: 800; color: #A78BFA; }
    .stat-label { font-size: 0.85rem; color: #C4B5FD; }
</style>
""", unsafe_allow_html=True)

# ---- Hero ----
st.markdown("""
<div class="hero-container">
    <div class="hero-title">🎓 AI-Powered Study Buddy</div>
    <div class="hero-subtitle">Your Intelligent Academic Assistant</div>
    <span class="hero-badge">⚡ Powered by Groq + Llama 3.3 70B</span>
    <span class="hero-badge">🧠 NLP & Generative AI</span>
    <span class="hero-badge">📚 AICTE – IBM SkillsBuild Internship</span>
</div>
""", unsafe_allow_html=True)

# ---- API Key Status ----
if not groq_key:
    st.error("⚠️ **GROQ_API_KEY** not found! Please add it to your `.env` file.")
else:
    st.success("✅ Groq AI (Llama 3.3 70B) is connected and ready!")

# ---- Feature Cards ----
st.subheader("✨ What can I do for you?")
col1, col2, col3, col4 = st.columns(4)
features = [
    ("📖", "Concept Explanation", "Get simple, clear explanations for any complex academic topic."),
    ("📝", "Note Summarization", "Paste notes or upload a PDF and get an instant AI summary."),
    ("❓", "Quiz Generator", "Test your knowledge with AI-generated MCQ quizzes with scoring."),
    ("💬", "AI Chat", "Have a full multi-turn conversation to clarify any academic doubt."),
]
for (icon, title, desc), col in zip(features, [col1, col2, col3, col4]):
    with col:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

# ---- Stats ----
st.divider()
st.subheader("📊 Project Stats")
s1, s2, s3, s4 = st.columns(4)
for (num, label), col in zip([("4","AI Features"),("Llama 3.3","AI Model"),("∞","Topics Supported"),("0₹","Cost to Run")], [s1, s2, s3, s4]):
    with col:
        st.markdown(f'<div class="stat-card"><div class="stat-number">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

# ---- How to use ----
st.divider()
st.subheader("🚀 How to Get Started")
st.markdown("""
1. 👈 **Click a page from the left sidebar** to choose your tool.
2. **📖 Explanation** — Type any concept and click *Explain to Me*.
3. **📝 Summarize** — Paste your notes or upload a PDF.
4. **❓ Quiz** — Enter a topic and test yourself with MCQs.
5. **💬 Chat** — Ask follow-up questions in a real-time AI chat.
""")

# ---- Footer ----
st.divider()
st.markdown("""
<div style='text-align:center; color: #6060A0; font-size: 0.85rem; padding: 1rem 0;'>
    🎓 Built by <strong>Dasari Sai Manasa Nikhita</strong> | Aditya College of Engineering & Technology, CSE <br>
    AICTE – IBM SkillsBuild Internship | Powered by Groq AI (Llama 3.3 70B)
</div>
""", unsafe_allow_html=True)
