#!/bin/bash

set -e

echo "🚀 Deploying HuggingFace Music Inference API..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Build the image
echo "📦 Building Docker image..."
docker build -t music-inference-api:latest .

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose down || true

# Start services
echo "▶️ Starting services..."
docker compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 45

# Health check
echo "🔍 Checking API health..."
for i in {1..15}; do
    if curl -f http://localhost/api/v1/health > /dev/null 2>&1; then
        echo "✅ API is healthy!"
        break
    else
        echo "⏳ Waiting for API... (attempt $i/15)"
        sleep 10
    fi
    
    if [ $i -eq 15 ]; then
        echo "❌ API health check failed after 150 seconds"
        echo "📋 Container logs:"
        docker compose logs
        exit 1
    fi
done

echo ""
echo "🎉 Deployment successful!"
echo "📖 API Documentation: http://localhost/docs"
echo "🔍 Health Check: http://localhost/api/v1/health"
echo "📊 Model Info: http://localhost/api/v1/models/info"
echo ""
echo "🧪 To run the demo notebook:"
echo "   cd notebooks && jupyter notebook demo.ipynb"