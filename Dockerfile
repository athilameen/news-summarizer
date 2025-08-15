FROM python:3.9-slim

# Block access to problematic directories at the OS level
RUN echo "tmpfs /.cache tmpfs rw,nosuid,nodev,noexec,size=1M 0 0" >> /etc/fstab && \
    mkdir -p /.cache && mount /.cache

# Create writable cache directories
RUN mkdir -p /tmp/hf_home /tmp/transformers_cache /tmp/hf_cache && \
    chmod -R 777 /tmp

# Install minimal dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]