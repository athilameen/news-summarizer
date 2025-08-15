FROM python:3.9-slim

# Install minimal dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create the official cache directory with proper permissions
RUN mkdir -p /home/user/.cache/huggingface && \
    chmod -R 777 /home/user/.cache

EXPOSE 7860
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]