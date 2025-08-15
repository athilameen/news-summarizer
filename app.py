import os
import streamlit as st
from transformers import pipeline

# ===== 100% RELIABLE CACHE SETUP =====
cache_dir = "/tmp/hf_cache"
os.makedirs(cache_dir, exist_ok=True)
os.environ["TRANSFORMERS_CACHE"] = cache_dir
os.environ["HF_HOME"] = cache_dir
os.environ["XDG_CACHE_HOME"] = cache_dir

# Verify cache directory is writable
try:
    test_file = os.path.join(cache_dir, "test.txt")
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
except Exception as e:
    st.error(f"Cache setup failed: {str(e)}")
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