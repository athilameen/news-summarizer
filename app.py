import os
import sys
import tempfile
import streamlit as st
from transformers import pipeline

# ===== NUCLEAR CACHE SOLUTION =====
# Create a temporary directory that's guaranteed writable
temp_cache = tempfile.mkdtemp(prefix="hf_cache_")

# Override ALL possible cache locations
os.environ["TRANSFORMERS_CACHE"] = temp_cache
os.environ["HF_HOME"] = temp_cache
os.environ["XDG_CACHE_HOME"] = temp_cache
os.environ["HUGGINGFACE_HUB_CACHE"] = temp_cache

# Verify we can write to the directory
test_file = os.path.join(temp_cache, "test.txt")
try:
    with open(test_file, "w") as f:
        f.write("test")
    os.remove(test_file)
except Exception as e:
    st.error(f"❌ Cache setup failed: {str(e)}")
    st.stop()

# ===== MODEL LOADING =====
@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            # Force model to use our temp directory
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,  # Force CPU
                local_files_only=False,
                cache_dir=temp_cache
            )
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.stop()

# ===== MAIN APP =====
def main():
    st.title("📰 News Summarizer")
    st.info(f"Using cache directory: {temp_cache}")
    
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