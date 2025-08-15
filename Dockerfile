FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create .streamlit directory with permissions
RUN mkdir -p /app/.streamlit

# Add config to prevent permission + telemetry issues
COPY .streamlit /app/.streamlit

# Copy the rest of the app
COPY . .

EXPOSE 7860

CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]
