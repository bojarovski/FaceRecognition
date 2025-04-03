FROM python:3.8-slim

WORKDIR /app

# Install system dependencies + core utilities
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libopenblas-dev \
    liblapack-dev \
    libgl1-mesa-glx \
    libx11-dev \
    curl \
    vim \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Default command when container starts
CMD ["/bin/bash"]