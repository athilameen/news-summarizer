FROM python:3.9-slim

# ===== SYSTEM SETUP =====
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ===== CACHE DIRECTORY SETUP =====
RUN mkdir -p /tmp/huggingface_cache && \
    mkdir -p /tmp/xdg_cache && \
    chmod -R 777 /tmp

# ===== APP SETUP =====
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# ===== HEALTH CHECK =====
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:7860/_stcore/health || exit 1

EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]