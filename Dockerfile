# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first (for caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables (optional, can also pass via docker-compose)
ENV PYTHONUNBUFFERED=1

# Default command to run your main.py
CMD ["python", "main.py"]
