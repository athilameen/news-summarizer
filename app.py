import os
import sys
import streamlit as st
from transformers import pipeline

# ===== NUCLEAR CACHE SOLUTION =====
# Set all possible cache locations to /tmp
os.environ["TRANSFORMERS_CACHE"] = "/tmp/huggingface"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["XDG_CACHE_HOME"] = "/tmp/xdg_cache"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/tmp/huggingface"

# Create cache directories with full permissions
cache_dirs = [
    "/tmp/huggingface",
    "/tmp/xdg_cache",
    "/tmp/huggingface/hub",
    "/tmp/huggingface/transformers"
]

for dir_path in cache_dirs:
    try:
        os.makedirs(dir_path, exist_ok=True)
        os.chmod(dir_path, 0o777)  # Full permissions
    except Exception as e:
        st.error(f"Failed to create cache directory: {str(e)}")
        st.stop()

# ===== MODEL LOADING =====
@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Force CPU
            )
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

# ===== MAIN APP =====
def main():
    st.title("📰 News Summarizer")
    article_text = st.text_area("Paste article here", height=300)
    
    if st.button("Summarize"):
        if not article_text.strip():
            st.warning("Please enter text")
            return
            
        try:
            model = load_model()
            with st.spinner("Generating summary..."):
                summary = model(article_text, max_length=130, min_length=30)
            st.success(summary[0]['summary_text'])
        except Exception as e:
            st.error(f"Summarization failed: {str(e)}")

if __name__ == "__main__":
    main()