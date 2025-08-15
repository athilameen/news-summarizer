import streamlit as st
from transformers import pipeline
import time

# Configure Streamlit
st.set_page_config(page_title="📰 News Summarizer", layout="wide")

# Health check
if "ready" not in st.session_state:
    st.session_state.ready = False

@st.cache_resource(show_spinner=False)
def load_model():
    """Cache the model to avoid reloading"""
    try:
        # Use a smaller model for Hugging Face Spaces
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
                start_time = time.time()
                model = load_model()
                summary = model(
                    article_text,
                    max_length=130,
                    min_length=30,
                    do_sample=False
                )
                st.subheader("Summary")
                st.write(summary[0]['summary_text'])
                st.info(f"Processing time: {time.time() - start_time:.2f} seconds")
            except Exception as e:
                st.error(f"Error during summarization: {str(e)}")

# Initialize only when needed
if not st.session_state.ready:
    with st.spinner("Loading model (first time may take a few minutes)..."):
        load_model()
        st.session_state.ready = True
        st.experimental_rerun()

if __name__ == "__main__":
    main()