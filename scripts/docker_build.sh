#!/bin/bash
echo "🐳 Building Docker image..."

BASE_DIR=$(cd "$(dirname "$0")/.."; pwd)
cd "$BASE_DIR/AI" || { echo "❌ AI folder not found!"; exit 1; }

docker build -t app .

echo "✅ Docker image built as: app"
