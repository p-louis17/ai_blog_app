# Official Python base image
FROM python:3.12-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# System dependencies 
RUN apt-get update && apt-get install -y \
    git netcat-openbsd gcc postgresql-client libpq-dev && \
    apt-get clean

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . .

# Expose port
EXPOSE 8080

# Start server 
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]
