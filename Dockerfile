FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Expose port 7860 (HF Spaces default)
EXPOSE 7860

# Run gunicorn
CMD ["gunicorn", "AskZohaib_Server.wsgi:application", "--bind", "0.0.0.0:7860"]
