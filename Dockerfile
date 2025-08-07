# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create instance directory for SQLite fallback
RUN mkdir -p instance

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PYTHONPATH=/app
ENV FLASK_APP=main.py
ENV FLASK_ENV=production
ENV OFFLINE_MODE=true
ENV DATABASE_URL=postgresql://erp_user:erp_secure_pass_2025@postgres:5432/battery_repair_db
ENV SESSION_SECRET=battery_erp_secret_key_hardcoded_2025_production

# Ensure offline styles are available
RUN cp static/offline-styles.css static/offline-styles.css.bak || true

# Create a non-root user
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /app
USER app

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--reload", "main:app"]