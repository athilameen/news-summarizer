import os
import sys
import streamlit as st
from transformers import pipeline

# ===== PREVENT DEFAULT CACHE ACCESS =====
# Block access to problematic directories
os.environ['NO_DEFAULT_CACHE'] = "1"
os.environ['HF_HOME'] = "/tmp/hf_home"
os.environ['TRANSFORMERS_CACHE'] = "/tmp/transformers_cache"

# ===== MODEL LOADING WITH EXPLICIT CACHE =====
@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,  # Force CPU
                # Force cache to our custom location
                cache_dir="/tmp/hf_cache",
                local_files_only=False
            )
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

# ===== MAIN APP =====
def main():
    st.title("📰 News Summarizer")
    st.info("This app uses a temporary cache that resets after each session")
    
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