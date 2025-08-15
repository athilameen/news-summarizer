import os
import streamlit as st
from transformers import pipeline
import time

# Set Hugging Face cache to writable directory
os.environ["TRANSFORMERS_CACHE"] = "/tmp/.cache/huggingface/hub"
os.environ["HF_HOME"] = "/tmp/.cache/huggingface"

# Create cache directory if it doesn't exist
os.makedirs(os.environ["TRANSFORMERS_CACHE"], exist_ok=True)

# Streamlit configuration
st.set_page_config(page_title="📰 News Summarizer", layout="wide")

@st.cache_resource(show_spinner=False)
def load_model():
    """Cache the model to avoid reloading"""
    try:
        return pipeline("summarization", model="facebook/bart-large-cnn")
    except Exception as e:
        st.error(f"Model loading failed: {str(e)}")
        st.stop()

def main():
    st.title("📰 News Summarizer")
    st.write("Paste a news article below and get a short summary!")

    article_text = st.text_area("Enter your article text here", height=300)

    if st.button("Summarize"):
        if not article_text.strip():
            st.warning("Please paste some article text first.")
            return

        with st.spinner("Summarizing..."):
            try:
                model = load_model()
                summary = model(
                    article_text,
                    max_length=130,
                    min_length=30,
                    do_sample=False
                )
                st.subheader("Summary")
                st.write(summary[0]['summary_text'])
            except Exception as e:
                st.error(f"Error during summarization: {str(e)}")

if __name__ == "__main__":
    main()