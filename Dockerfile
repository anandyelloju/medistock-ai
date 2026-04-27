# Base Image: Use a slim Python 3.10 image for efficiency
FROM python:3.10-slim

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app

# Working Directory
WORKDIR $APP_HOME

# Install System Dependencies (for SQLite and networking)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Project Files
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Expose ports
EXPOSE 8501
EXPOSE 8000

# Entrypoint for Cloud Deployment
ENTRYPOINT ["./entrypoint.sh"]
