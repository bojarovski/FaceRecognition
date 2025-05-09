# 1. Use an official Python base image
FROM python:3.8-slim

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies
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

# 4. Copy your requirements file first (for better caching)
COPY requirements.txt .

# 5. Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your app (including recognition_server.py, known_faces.pkl, etc.)
COPY . .

# 7. Expose port 5000 (where Flask server listens)
EXPOSE 5000
 
# 8. Default command: start the Flask face recognition server
CMD ["python", "recognition_server.py"]
