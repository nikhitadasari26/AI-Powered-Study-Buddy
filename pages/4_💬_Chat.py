import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.ai_agent import get_chat_response

st.set_page_config(
    page_title="Chat - AI Study Buddy",
    page_icon="💬",
    layout="wide"
)

st.title("💬 Conversational Doubt Clarification")
st.markdown("Ask any academic question and have a **multi-turn conversation** with your AI Study Buddy.")
st.divider()

# Chat history: list of {"role": "user"|"assistant", "content": "..."}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display all previous messages
for message in st.session_state.chat_history:
    role = message["role"]
    content = message["content"]
    avatar = "🧑‍🎓" if role == "user" else "🤖"
    with st.chat_message(role, avatar=avatar):
        st.markdown(content)

# Chat input box at the bottom
user_input = st.chat_input(
    "Ask me anything about your studies... (e.g., 'What is DNA?', 'Explain recursion')"
)

if user_input:
    # Show the user's message immediately
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(user_input)

    # Call Groq and get AI response
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤔 Thinking..."):
            ai_response = get_chat_response(
                chat_history=st.session_state.chat_history,
                user_message=user_input
            )
        st.markdown(ai_response)

    # Save both turns
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})

# Sidebar controls
with st.sidebar:
    st.subheader("💬 Chat Controls")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.divider()
    num_messages = len(st.session_state.chat_history) // 2
    st.info(f"💬 **{num_messages}** message{'s' if num_messages != 1 else ''} in this session.")

    st.subheader("💡 Sample Questions")
    samples = [
        "Explain the water cycle",
        "What is machine learning?",
        "How does a CPU work?",
        "Explain Newton's 3 laws",
        "What is osmosis?",
        "What is Big O notation?",
    ]
    for q in samples:
        st.caption(f"▶ *{q}*")

st.divider()
st.caption("💡 Tip: You can ask follow-up questions! The AI remembers the full conversation context.")
