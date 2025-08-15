# app.py
import os

# ---- set env FIRST, then import anything from transformers ----
os.environ.setdefault("HF_HOME", "/data/.cache/huggingface")
os.environ.setdefault("TRANSFORMERS_CACHE", "/data/.cache/huggingface/transformers")
os.environ.setdefault("HUGGINGFACE_HUB_CACHE", "/data/.cache/huggingface/hub")

import streamlit as st
from transformers import pipeline

CACHE_DIR = os.environ["TRANSFORMERS_CACHE"]  # single source of truth

@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,              # CPU
                cache_dir=CACHE_DIR     # ensure downloads go to /data
            )
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

def main():
    st.title("📰 News Summarizer")
    st.info("This app uses Spaces’ persistent /data cache")

    article_text = st.text_area("Paste article here", height=300)

    if st.button("Summarize"):
        if not article_text.strip():
            st.warning("Please enter text")
            return
        try:
            model = load_model()
            with st.spinner("Generating summary..."):
                summary = model(article_text, max_length=130, min_length=30)
            st.success(summary[0]["summary_text"])
        except Exception as e:
            st.error(f"Summarization failed: {str(e)}")

if __name__ == "__main__":
    main()