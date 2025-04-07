#!/bin/bash
echo "🚀 Running Docker AI container..."

docker stop ai-server 2>/dev/null
docker rm ai-server 2>/dev/null

docker run -d --rm --name ai-server -p 5001:5000 app sh -c "python training_script.py && python recognition_server.py"

echo "✅ AI server is running at http://localhost:5001"
