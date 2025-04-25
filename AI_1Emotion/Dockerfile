# emotion/Dockerfile
FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1-mesa-glx libglib2.0-0 ca-certificates && \
    rm -rf /var/lib/apt/lists/*

COPY requirements_emotion.txt .
RUN pip install --no-cache-dir -r requirements_emotion.txt

COPY emotion_server.py .

EXPOSE 5002
ENTRYPOINT ["python", "emotion_server.py"]
