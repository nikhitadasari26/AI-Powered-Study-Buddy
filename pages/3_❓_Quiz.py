import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.ai_agent import generate_quiz

st.set_page_config(
    page_title="Quiz Generator - AI Study Buddy",
    page_icon="❓",
    layout="wide"
)

st.title("❓ Quiz & Flashcard Generator")
st.markdown("Enter a topic to get an AI-generated **multiple-choice quiz** to test your knowledge.")

st.divider()

# --- Quiz Generation Form ---
with st.form("quiz_form"):
    topic = st.text_input(
        "Enter the topic for your quiz:",
        placeholder="e.g., Photosynthesis, World War II, Python Loops, Newton's Laws..."
    )
    submitted = st.form_submit_button("🎯 Generate Quiz", use_container_width=True, type="primary")

if submitted:
    if topic.strip():
        with st.spinner(f"🧠 Generating a quiz on *{topic}*..."):
            quiz_questions = generate_quiz(topic)

        if not quiz_questions:
            st.error("❌ Failed to generate the quiz. Please try again.")
        else:
            st.success(f"✅ Quiz generated on: **{topic}**  |  📋 {len(quiz_questions)} questions")
            st.divider()

            # Initialize session state to store answers and submission status
            if "quiz_answers" not in st.session_state or st.session_state.get("quiz_topic") != topic:
                st.session_state.quiz_answers = {}
                st.session_state.quiz_submitted = False
                st.session_state.quiz_topic = topic
                st.session_state.quiz_questions = quiz_questions

            st.session_state.quiz_questions = quiz_questions

            # Display each question
            for i, q_data in enumerate(st.session_state.quiz_questions):
                with st.container():
                    st.markdown(f"### Question {i+1}")
                    st.markdown(f"**{q_data.get('question', 'N/A')}**")
                    options = q_data.get("options", [])
                    
                    user_choice = st.radio(
                        f"Select your answer for Q{i+1}:",
                        options=options,
                        key=f"q_{i}",
                        label_visibility="collapsed"
                    )
                    st.session_state.quiz_answers[i] = user_choice
                    st.markdown("---")

            # Submit and check answers button
            if st.button("📊 Submit & Check Answers", use_container_width=True, type="secondary"):
                st.session_state.quiz_submitted = True

            # Show results if submitted
            if st.session_state.quiz_submitted:
                st.subheader("📊 Your Results")
                score = 0
                for i, q_data in enumerate(st.session_state.quiz_questions):
                    correct = q_data.get("answer")
                    user_ans = st.session_state.quiz_answers.get(i)
                    explanation = q_data.get("explanation", "")
                    if user_ans == correct:
                        score += 1
                        st.success(f"**Q{i+1}:** ✅ Correct! — {q_data.get('question')}")
                    else:
                        st.error(f"**Q{i+1}:** ❌ Wrong — Your answer: `{user_ans}` | Correct: `{correct}`")
                    if explanation:
                        with st.expander(f"💡 Explanation for Q{i+1}"):
                            st.info(explanation)

                st.divider()
                st.metric(label="🏆 Your Score", value=f"{score} / {len(st.session_state.quiz_questions)}")
                if score == len(st.session_state.quiz_questions):
                    st.balloons()
                    st.success("🎉 Perfect Score! Great job!")
                elif score >= len(st.session_state.quiz_questions) // 2:
                    st.info("👍 Good effort! Review the explanations above to improve.")
                else:
                    st.warning("📚 Keep studying! Try the quiz again after reviewing the topic.")
    else:
        st.warning("⚠️ Please enter a topic to generate a quiz.")

st.divider()
st.caption("💡 Tip: Be specific with your topic (e.g., 'Mitosis and Meiosis' instead of just 'Biology') for better quiz quality.")
