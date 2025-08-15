import os

# Set env BEFORE importing transformers
os.environ.setdefault("HF_HOME", "/data/.cache/huggingface")
os.environ.setdefault("HUGGINGFACE_HUB_CACHE", "/data/.cache/huggingface/hub")

import streamlit as st
from transformers.pipelines import pipeline
import textwrap

st.set_page_config(page_title="News Summarizer", layout="centered")

@st.cache_resource(ttl=24*3600)
def load_model():
    with st.spinner("🚀 Loading model (first time may take a couple minutes)..."):
        return pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1,   # CPU
        )

def chunk_text(s: str, max_chars: int = 2800, overlap: int = 200):
    """
    Simple char-based chunking to avoid truncation.
    BART context ~1024 tokens ≈ ~3500 chars, so 2800 with small overlap is safe.
    """
    s = s.strip()
    if len(s) <= max_chars:
        return [s]
    chunks = []
    i = 0
    while i < len(s):
        end = min(len(s), i + max_chars)
        chunks.append(s[i:end])
        if end == len(s):
            break
        i = end - overlap  # step back a bit to keep continuity
    return chunks

def summarize_text(model, text: str):
    parts = chunk_text(text)
    partials = []
    for p in parts:
        out = model(p, max_length=130, min_length=30, do_sample=False, truncation=True)
        partials.append(out[0]["summary_text"])
    # If we had multiple chunks, do a final pass to compress the stitched summary
    combined = " ".join(partials)
    if len(parts) > 1 and len(combined) > 2000:
        out = model(combined, max_length=160, min_length=50, do_sample=False, truncation=True)
        return out[0]["summary_text"]
    return combined

def main():
    st.title("📰 News Summarizer")
    st.caption("Uses Spaces’ persistent `/data` cache. CPU-only build.")

    # Optional: helpful for debugging Spaces images
    try:
        import transformers, huggingface_hub
        st.caption(f"transformers={transformers.__version__}, hub={huggingface_hub.__version__}")
    except Exception:
        pass

    article_text = st.text_area("Paste article here", height=300, placeholder="Paste the full article text...")

    if st.button("Summarize"):
        if not article_text.strip():
            st.warning("Please enter text")
            st.stop()

        try:
            model = load_model()
            with st.spinner("Generating summary..."):
                summary = summarize_text(model, article_text)
            st.subheader("Summary")
            st.write(summary)
        except Exception as e:
            st.error(f"Summarization failed: {e}")

if __name__ == "__main__":
    main()
