# Use specific Python version
FROM python:3.11-slim

# Set working directory to root (matches your repo root)
WORKDIR /root

# Copy requirements.txt first for caching
COPY requirements.txt .

# Install system dependencies needed for building packages
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files (everything is in root)
COPY . .

# Expose the port FastAPI will use
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
