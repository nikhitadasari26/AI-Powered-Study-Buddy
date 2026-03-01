import os
import json
from groq import Groq
from dotenv import load_dotenv
from utils.prompts import (
    CONCEPT_EXPLANATION_PROMPT,
    NOTE_SUMMARIZATION_PROMPT,
    QUIZ_GENERATION_PROMPT,
    CHAT_SYSTEM_PROMPT
)

load_dotenv()

# Model to use - Llama 3.3 70B is powerful and free on Groq
MODEL_NAME = "llama-3.3-70b-versatile"

def _get_client():
    """Returns a configured Groq client."""
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            api_key = st.secrets.get("GROQ_API_KEY", "")
        except Exception:
            pass
    if not api_key:
        raise ValueError("GROQ_API_KEY not set. Please add it to your .env file.")
    return Groq(api_key=api_key)

def get_explanation(concept: str) -> str:
    """Generates a simple explanation for a given concept using Groq."""
    try:
        client = _get_client()
        prompt = CONCEPT_EXPLANATION_PROMPT.format(concept=concept)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert AI Study Buddy for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating explanation: {e}"

def get_summary(text: str) -> str:
    """Summarizes the provided text using Groq."""
    try:
        client = _get_client()
        prompt = NOTE_SUMMARIZATION_PROMPT.format(text=text)
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert AI Study Buddy that summarizes notes for students."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating summary: {e}"

def generate_quiz(topic: str) -> list:
    """Generates a 3-question quiz and parses the JSON from the response."""
    import re
    try:
        client = _get_client()
        prompt = f"""Generate a multiple-choice quiz about "{topic}" with exactly 3 questions.

Output ONLY a valid JSON array like this (no extra text before or after):
[
  {{
    "question": "Question text here?",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "answer": "Option A",
    "explanation": "Brief explanation why this is correct."
  }}
]

Topic: {topic}"""

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a quiz generator. Output ONLY a JSON array. No markdown, no explanation, just the JSON array."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1500,
        )
        raw = response.choices[0].message.content.strip()

        # Remove markdown code fences if present (```json ... ```)
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.MULTILINE)
        raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
        raw = raw.strip()

        # Try to parse directly as an array
        if raw.startswith("["):
            return json.loads(raw)

        # If wrapped in an object, find the first array value
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return parsed
        for key in parsed:
            if isinstance(parsed[key], list):
                return parsed[key]

        return []
    except Exception as e:
        print(f"Error generating quiz: {e}")
        return []


def get_chat_response(chat_history: list, user_message: str) -> str:
    """
    Gets a chat response from Groq maintaining full conversation history.
    chat_history: list of {"role": "user"|"assistant", "content": "..."} dicts
    """
    try:
        client = _get_client()
        messages = [{"role": "system", "content": CHAT_SYSTEM_PROMPT}]
        messages.extend(chat_history)
        messages.append({"role": "user", "content": user_message})
        
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=0.7,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ An error occurred: {e}"
