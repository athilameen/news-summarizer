FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1 \
    HF_HOME=/data/.cache/huggingface \
    HUGGINGFACE_HUB_CACHE=/data/.cache/huggingface/hub \
    HOME=/home/user

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /data/.cache/huggingface /home/user && \
    chmod -R 777 /data /home/user

WORKDIR /app

COPY requirements.txt .
# Force a clean, exact install of the pinned versions
RUN pip install --no-cache-dir --upgrade --force-reinstall -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
