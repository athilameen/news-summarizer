FROM python:3.9-slim

# Create cache directories with FULL permissions at build time
RUN mkdir -p /tmp/huggingface/hub && \
    mkdir -p /tmp/xdg_cache && \
    chmod -R 777 /tmp

# Install minimal build tools
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]