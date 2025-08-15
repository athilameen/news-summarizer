# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set work directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose port 7860 (required by Hugging Face Spaces)
EXPOSE 7860

# Run the application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]