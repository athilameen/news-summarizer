import os
import streamlit as st
from transformers import pipeline

# ===== HUGGING FACE SPECIFIC CACHE SOLUTION =====
# Use Hugging Face's built-in environment variables
os.environ["HF_HOME"] = "/tmp/hf_home"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers_cache"
os.environ["HUGGINGFACE_HUB_CACHE"] = "/tmp/huggingface_hub"

# ===== MODEL LOADING =====
@st.cache_resource(ttl=24*3600)
def load_model():
    try:
        with st.spinner("🚀 Loading model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1,  # Force CPU
                # Hugging Face will automatically use the env variables
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