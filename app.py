import os
import sys
import builtins

# --- Critical: Must be first before any Streamlit imports ---
os.environ["STREAMLIT_GLOBAL_METRICS"] = "0"  # Completely disable metrics
os.environ["STREAMLIT_CONFIG_DIR"] = "/tmp/.streamlit"
os.environ["STREAMLIT_CACHE_DIR"] = "/tmp/.streamlit-cache"
os.environ["STREAMLIT_BROWSER_GATHERUSAGESTATS"] = "false"
os.environ["HOME"] = "/tmp"

# Create required directories
os.makedirs("/tmp/.streamlit", exist_ok=True)
os.makedirs("/tmp/.streamlit-cache", exist_ok=True)

# Create minimal config file
CONFIG_PATH = "/tmp/.streamlit/config.toml"
if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w") as f:
        f.write("""
[server]
enableXsrfProtection = false
enableCORS = false
headless = true
port = 7860  # Hugging Face requires port 7860

[browser]
gatherUsageStats = false
""")

# Save the original os.makedirs function
original_makedirs = os.makedirs

# Define our safe directory creation function
def safe_makedirs(path, mode=0o777, exist_ok=False):
    # Redirect any attempts to create /.streamlit to /tmp/.streamlit
    if path.startswith('/.streamlit'):
        path = path.replace('/.streamlit', '/tmp/.streamlit', 1)
    return original_makedirs(path, mode, exist_ok=exist_ok)

# Apply the monkey patch
os.makedirs = safe_makedirs

import streamlit as st
from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.title("📰 News Summarizer")
st.write("Paste a news article below and get a short summary!")

article_text = st.text_area("Enter your article text here", height=300)

if st.button("Summarize"):
    if article_text.strip():
        with st.spinner("Summarizing..."):
            summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
        st.subheader("Summary")
        st.write(summary[0]['summary_text'])
    else:
        st.warning("Please paste some article text first.")
