# HuggingFace Audio Classification API

A production-ready, scalable API for audio classification using HuggingFace models. Built with FastAPI, Docker, and NGINX for enterprise deployment.

## 🎵 Features

- **Audio Event Classification**: Uses Audio Spectrogram Transformer (AST) for 527 audio event types
- **Async Processing**: Handle multiple concurrent requests efficiently
- **Batch Processing**: Optimized endpoint for multiple files
- **Health Monitoring**: Comprehensive health checks and system metrics
- **Production Ready**: Docker + NGINX + Load balancing
- **AWS Compatible**: Ready for ECS, EKS, or EC2 deployment

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### Easy Deployment

Use the automated deployment script:

```bash
# Clone the repository
git clone <your-repo>
cd audio-classification-api

# Deploy everything automatically
chmod +x deploy.sh
./deploy.sh
```

### Manual Deployment

```bash
# Start the services
docker-compose up -d

# Check if services are running
docker-compose ps

# Wait for model to load (2-3 minutes)
# Check health: curl http://localhost/api/v1/health
```

### Access the API

- **API Documentation**: http://localhost/docs
- **Health Check**: http://localhost/api/v1/health/detailed
- **Model Info**: http://localhost/api/v1/models/info

## 📚 Usage

### Single File Inference

```python
import requests

with open('audio.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost/api/v1/inference', files=files)
    result = response.json()
    print(result['results']['predictions'])
```

### Batch Processing

```python
files = [
    ('files', ('audio1.wav', open('audio1.wav', 'rb'), 'audio/wav')),
    ('files', ('audio2.wav', open('audio2.wav', 'rb'), 'audio/wav'))
]
response = requests.post('http://localhost/api/v1/batch-inference', files=files)
```

## 🧪 Demo Notebook

Run the comprehensive demo:

```bash
# Start Jupyter (requires local Python environment)
cd notebooks
jupyter notebook demo.ipynb
```

The notebook demonstrates:
- API health checks
- Parallel requests with asyncio
- Stress testing with concurrent requests
- Response analysis and visualization

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   NGINX     │────│  FastAPI    │────│ HuggingFace │
│Load Balancer│    │   Server    │    │ AST Model   │
│Rate Limiting│    │Async/Await  │    │(AudioSet)   │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔧 Configuration

Environment variables in [`.env`](.env):

```env
MODEL_NAME=MIT/ast-finetuned-audioset-10-10-0.4593
DEVICE=cpu
MAX_FILE_SIZE=52428800
MODEL_CACHE_DIR=./model_cache
```

## 📊 Model Information

**Model**: `MIT/ast-finetuned-audioset-10-10-0.4593`

**Why this model?**
- **Audio Spectrogram Transformer (AST)**: State-of-the-art architecture for audio classification
- **AudioSet Training**: Trained on Google's AudioSet with 527 audio event classes
- **Versatile**: Handles music, speech, environmental sounds, and more
- **Production Ready**: Optimized for real-world audio classification tasks

**Supported Audio Types**: 
- Music genres and instruments
- Speech and vocal sounds  
- Environmental sounds (rain, traffic, etc.)
- Animal sounds
- Mechanical sounds
- And 520+ more audio event categories

## 🚀 AWS Deployment

### Using AWS ECS

1. Build and push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t audio-classification-api .
docker tag audio-classification-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/audio-classification-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/audio-classification-api:latest
```

2. Create ECS task definition and service
3. Configure Application Load Balancer
4. Set up auto-scaling policies

## 🔍 Monitoring

### Health Endpoints

- `/api/v1/health` - Basic health check
- `/api/v1/health/detailed` - System metrics (CPU, memory, GPU)
- `/api/v1/ready` - Kubernetes readiness probe

### Metrics Available

- CPU and memory usage
- GPU utilization (if available)
- Request latency and throughput
- Model performance metrics

## 📈 Performance

- **Concurrent Requests**: Handles 50+ concurrent requests via NGINX + asyncio
- **Latency**: ~3-5s average response time (includes model inference)
- **Throughput**: 10+ requests/second per instance
- **Memory**: ~3-6GB per instance (configurable in docker-compose.yml)

## 🔒 Security

- **Rate limiting**: 10 req/s per IP with burst capacity
- **File validation**: Size limits (50MB) and format validation
- **CORS protection**: Configurable origin policies
- **Input sanitization**: Audio file validation and preprocessing

## 🛠️ Development

### Local Setup

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python -m uvicorn src.app:app --reload --host 0.0.0.0 --port 8000
```

### Testing

```bash
# Run tests
pytest

# Manual testing with curl
curl -X POST "http://localhost/api/v1/inference" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@audio_sample.wav"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [API documentation](http://localhost/docs)
- Review health endpoints for diagnostics
- Check container logs: `docker-compose logs`
- Use the automated [`deploy.sh`](deploy.sh) script for quick setup