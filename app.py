import streamlit as st
from transformers import pipeline

# Load summarization pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

st.title("📰 News Summarizer")
st.write("Paste a news article below and get a short summary!")

# Text input
article_text = st.text_area("Enter your article text here", height=300)

if st.button("Summarize"):
    if article_text.strip():
        with st.spinner("Summarizing..."):
            summary = summarizer(article_text, max_length=130, min_length=30, do_sample=False)
        st.subheader("Summary")
        st.write(summary[0]['summary_text'])
    else:
        st.warning("Please paste some article text first.")
