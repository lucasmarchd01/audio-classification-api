# HuggingFace Music Inference API

A production-ready, scalable API for music genre classification using HuggingFace models. Built with FastAPI, Docker, and NGINX for enterprise deployment.

## 🎵 Features

- **Music Information Retrieval**: Genre classification using GTZAN-trained models
- **Async Processing**: Handle multiple concurrent requests efficiently
- **Batch Processing**: Optimized endpoint for multiple files
- **Health Monitoring**: Comprehensive health checks and system metrics
- **Production Ready**: Docker + NGINX + Load balancing
- **AWS Compatible**: Ready for ECS, EKS, or EC2 deployment

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- Python 3.11+ (for local development)

### Run with Docker

```bash
# Clone the repository
git clone <your-repo>
cd huggingface-inference-server

# Start the services
docker-compose up -d

# Check if services are running
docker-compose ps
```

### Access the API

- **API Documentation**: http://localhost/docs
- **Health Check**: http://localhost/api/v1/health
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

Run the comprehensive demo in `notebooks/parallel_requests_demo.ipynb`:

```bash
jupyter notebook notebooks/parallel_requests_demo.ipynb
```

The notebook demonstrates:
- API health checks
- Single and batch requests
- Parallel processing performance
- Stress testing
- Results visualization

## 🏗️ Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   NGINX     │────│  FastAPI    │────│ HuggingFace │
│Load Balancer│    │   Server    │    │   Model     │
└─────────────┘    └─────────────┘    └─────────────┘
```

## 🔧 Configuration

Environment variables in `.env`:

```env
MODEL_NAME=marsyas/gtzan-ft-music-speech-moods-fma-gtzan
DEVICE=cpu
MAX_FILE_SIZE=52428800
```

## 📊 Model Information

**Model**: `marsyas/gtzan-ft-music-speech-moods-fma-gtzan`

**Why this model?**
- Industry-standard GTZAN dataset
- Multi-domain training (GTZAN + FMA + moods)
- Real-world genre classification
- Used by streaming platforms

**Supported Genres**: Rock, Jazz, Classical, Country, Pop, Reggae, Blues, Hip-hop, Metal, Disco

## 🚀 AWS Deployment

### Using AWS ECS

1. Build and push to ECR:
```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account>.dkr.ecr.us-east-1.amazonaws.com
docker build -t music-inference-api .
docker tag music-inference-api:latest <account>.dkr.ecr.us-east-1.amazonaws.com/music-inference-api:latest
docker push <account>.dkr.ecr.us-east-1.amazonaws.com/music-inference-api:latest
```

2. Create ECS task definition and service
3. Configure Application Load Balancer
4. Set up auto-scaling policies

### Using AWS Lambda (for lighter workloads)

```bash
# Package for Lambda deployment
pip install -r requirements.txt -t ./lambda-package
```

## 🔍 Monitoring

### Health Endpoints

- `/api/v1/health` - Basic health check
- `/api/v1/health/detailed` - System metrics
- `/api/v1/ready` - Kubernetes readiness probe

### Metrics Available

- CPU usage
- Memory usage
- GPU utilization (if available)
- Request latency
- Model performance

## 🧪 Testing

```bash
# Run tests
pytest

# Load testing
python -m locust -f tests/load_test.py
```

## 📈 Performance

- **Concurrent Requests**: Handles 50+ concurrent requests
- **Latency**: <2s average response time
- **Throughput**: 10+ requests/second per instance
- **Memory**: ~2GB per instance

## 🔒 Security

- Rate limiting (10 req/s per IP)
- File size validation (50MB max)
- CORS protection
- Input sanitization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

For issues and questions:
- Check the [documentation](http://localhost/docs)
- Review health endpoints
- Check Docker logs: `docker-compose logs`