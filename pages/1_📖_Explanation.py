import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.ai_agent import get_explanation

st.set_page_config(
    page_title="Concept Explanation - AI Study Buddy",
    page_icon="📖",
    layout="wide"
)

st.title("📖 Concept Explanation")
st.markdown("Enter any academic concept and get an instant, simple explanation powered by AI.")

st.divider()

with st.form("explanation_form"):
    concept = st.text_input(
        "Enter a concept or topic:",
        placeholder="e.g., Photosynthesis, Newton's Second Law, TCP/IP Protocol, Machine Learning...",
        help="Type any topic you're studying and the AI will explain it clearly."
    )
    difficulty = st.select_slider(
        "Explanation Level:",
        options=["Beginner (5th grade)", "Intermediate (High School)", "Advanced (College)"],
        value="Intermediate (High School)"
    )
    submitted = st.form_submit_button("✨ Explain to Me", use_container_width=True, type="primary")

if submitted:
    if concept.strip():
        with st.spinner(f"🤔 Thinking about *{concept}*..."):
            # Append level context to concept
            full_concept = f"{concept} (Explain at {difficulty} level)"
            result = get_explanation(full_concept)
        
        st.success("Here is your explanation:")
        st.markdown(result)
        
        # Download button for the explanation
        st.download_button(
            label="⬇️ Download Explanation",
            data=result,
            file_name=f"{concept.replace(' ', '_')}_explanation.txt",
            mime="text/plain",
            use_container_width=True
        )
    else:
        st.warning("⚠️ Please enter a concept before submitting.")

st.divider()
st.caption("💡 Tip: Be specific in your query! Instead of 'Physics', try 'Newton's Third Law of Motion'.")
