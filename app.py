import os
import streamlit as st
from transformers import pipeline

# ===== CACHE SOLUTION THAT ALWAYS WORKS =====
# Set cache to /tmp directory (always writable in Spaces)
cache_dir = "/tmp/hf_cache"
os.environ["HF_HOME"] = cache_dir
os.environ["TRANSFORMERS_CACHE"] = cache_dir
os.environ["HUGGINGFACE_HUB_CACHE"] = cache_dir

# ===== MODEL LOADING =====
@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,  # Force CPU
                cache_dir=cache_dir  # Explicitly set cache
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