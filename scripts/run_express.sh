#!/bin/bash
echo "🧠 Starting Express backend..."

BASE_DIR=$(cd "$(dirname "$0")/.."; pwd)
cd "$BASE_DIR/Backend" || { echo "❌ Express server folder not found!"; exit 1; }

npm install
node server.js
