import os
import streamlit as st
from transformers import pipeline
import time

# ===== CRITICAL CACHE CONFIGURATION =====
os.environ['TRANSFORMERS_CACHE'] = '/tmp/huggingface_cache'
os.environ['HF_HOME'] = '/tmp/huggingface_cache'
os.environ['XDG_CACHE_HOME'] = '/tmp/xdg_cache'
os.makedirs('/tmp/huggingface_cache', exist_ok=True)
os.makedirs('/tmp/xdg_cache', exist_ok=True)

# ===== STREAMLIT CONFIG =====
st.set_page_config(
    page_title="📰 News Summarizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== MODEL LOADING =====
@st.cache_resource(ttl=24*3600)  # Cache for 24 hours
def load_model():
    try:
        # Show loading progress
        with st.spinner("🚀 Loading summarization model (first time may take 2-3 minutes)..."):
            return pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=-1  # Use CPU
            )
    except Exception as e:
        st.error(f"❌ Model loading failed: {str(e)}")
        st.error("Please try again later or contact support")
        st.stop()

# ===== MAIN APP =====
def main():
    st.title("📰 News Summarizer")
    st.caption("Paste a news article below and get an instant summary")
    
    article_text = st.text_area(
        "Article Text",
        height=300,
        placeholder="Paste your news article here..."
    )
    
    if st.button("Generate Summary", type="primary"):
        if not article_text.strip():
            st.warning("Please enter some text to summarize")
            return
            
        try:
            # Load model (cached after first load)
            model = load_model()
            
            with st.spinner("✍️ Generating summary..."):
                start_time = time.time()
                summary = model(
                    article_text,
                    max_length=130,
                    min_length=30,
                    do_sample=False
                )
                processing_time = time.time() - start_time
                
            st.subheader("📝 Summary")
            st.success(summary[0]['summary_text'])
            st.caption(f"Processed in {processing_time:.2f} seconds")
            
        except Exception as e:
            st.error(f"Error during summarization: {str(e)}")

if __name__ == "__main__":
    main()