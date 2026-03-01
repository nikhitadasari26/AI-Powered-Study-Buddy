import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from utils.ai_agent import get_summary

try:
    import PyPDF2
    PDF_SUPPORT = True
except ImportError:
    PDF_SUPPORT = False

st.set_page_config(
    page_title="Note Summarization - AI Study Buddy",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Note Summarization")
st.markdown("Paste your notes **or** upload a PDF file, and get an AI-generated structured summary instantly.")

st.divider()

tab1, tab2 = st.tabs(["📋 Paste Text", "📂 Upload PDF"])

with tab1:
    text_input = st.text_area(
        "Paste your notes here:",
        height=300,
        placeholder="Paste your lecture notes, textbook paragraphs, or any academic text here..."
    )
    if st.button("📝 Summarize Text", use_container_width=True, type="primary", key="summarize_text_btn"):
        if text_input.strip():
            if len(text_input.strip()) < 50:
                st.warning("⚠️ Please paste more text (at least 50 characters) for a meaningful summary.")
            else:
                with st.spinner("📖 Reading and summarizing your notes..."):
                    summary = get_summary(text_input)
                st.success("✅ Summary ready!")
                st.markdown(summary)
                st.download_button(
                    label="⬇️ Download Summary",
                    data=summary,
                    file_name="notes_summary.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        else:
            st.warning("⚠️ Please paste some text before summarizing.")

with tab2:
    if not PDF_SUPPORT:
        st.error("PyPDF2 is not installed. Please run: `pip install PyPDF2`")
    else:
        uploaded_file = st.file_uploader("Upload your PDF notes:", type=["pdf"])
        if uploaded_file is not None:
            st.info(f"📄 File uploaded: **{uploaded_file.name}** ({uploaded_file.size / 1024:.1f} KB)")
            if st.button("📄 Summarize PDF", use_container_width=True, type="primary", key="summarize_pdf_btn"):
                with st.spinner("📖 Extracting text from PDF..."):
                    try:
                        reader = PyPDF2.PdfReader(uploaded_file)
                        pdf_text = ""
                        for page_num, page in enumerate(reader.pages):
                            pdf_text += page.extract_text() + "\n"
                        
                        if not pdf_text.strip():
                            st.error("❌ Could not extract text from this PDF. It might be a scanned image PDF.")
                        else:
                            st.write(f"✅ Extracted text from **{len(reader.pages)} pages**.")
                            with st.spinner("🤔 AI is summarizing your PDF..."):
                                summary = get_summary(pdf_text[:8000])  # Limit to avoid token limits
                            st.success("✅ PDF Summary ready!")
                            st.markdown(summary)
                            st.download_button(
                                label="⬇️ Download PDF Summary",
                                data=summary,
                                file_name=f"{uploaded_file.name.replace('.pdf','')}_summary.txt",
                                mime="text/plain",
                                use_container_width=True
                            )
                    except Exception as e:
                        st.error(f"❌ Error reading PDF: {e}")

st.divider()
st.caption("💡 Tip: For best results, paste clean text from a document rather than a scanned image.")
