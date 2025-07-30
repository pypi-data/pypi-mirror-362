# OpenSearchEval: Ultimate Search Evaluation Platform

<div align="center">

[![PyPI version](https://badge.fury.io/py/opensearcheval.svg)](https://badge.fury.io/py/opensearcheval)
[![Python versions](https://img.shields.io/pypi/pyversions/opensearcheval.svg)](https://pypi.org/project/opensearcheval/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://github.com/llamasearchai/OpenSearchEval/workflows/CI/badge.svg)](https://github.com/llamasearchai/OpenSearchEval/actions)
[![Coverage Status](https://coveralls.io/repos/github/llamasearchai/OpenSearchEval/badge.svg?branch=main)](https://coveralls.io/github/llamasearchai/OpenSearchEval?branch=main)
[![Documentation Status](https://readthedocs.org/projects/opensearcheval/badge/?version=latest)](https://opensearcheval.readthedocs.io/en/latest/?badge=latest)

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Type checking: mypy](https://img.shields.io/badge/%20type_checker-mypy-%231674b1?style=flat)](https://mypy-lang.org/)
[![Security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)

[![Downloads](https://pepy.tech/badge/opensearcheval)](https://pepy.tech/project/opensearcheval)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/opensearcheval)](https://pypi.org/project/opensearcheval/)
[![GitHub stars](https://img.shields.io/github/stars/llamasearchai/OpenSearchEval?style=social)](https://github.com/llamasearchai/OpenSearchEval/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/llamasearchai/OpenSearchEval?style=social)](https://github.com/llamasearchai/OpenSearchEval/network/members)

</div>

## Overview

OpenSearchEval is a comprehensive, production-ready platform for evaluating search quality, conducting A/B tests, and analyzing user behavior. Built with modern Python technologies and featuring agent architecture, FastAPI endpoints, and MLX integration for Apple Silicon optimization.

### Key Features

- **Search Quality Metrics**: MRR, NDCG, Precision@K, Recall@K, and more
- **A/B Testing Framework**: Design, run, and analyze experiments with statistical significance
- **User Behavior Analytics**: Click tracking, dwell time, satisfaction metrics, and journey analysis
- **Agent Architecture**: Distributed processing with asynchronous task handling
- **MLX Integration**: Optimized ML components for Apple Silicon with GPU acceleration
- **LLM-as-Judge**: AI-powered qualitative evaluation of search results
- **FastAPI Endpoints**: Production-ready REST API with automatic documentation
- **Rich Visualizations**: Interactive charts, dashboards, and reporting tools
- **Extensible Design**: Plugin architecture for custom metrics and data sources
- **Performance Monitoring**: Real-time metrics collection and alerting

## Quick Start

### Installation

```bash
# Install from PyPI
pip install opensearcheval

# Or install with all optional dependencies
pip install opensearcheval[all]

# For development
pip install opensearcheval[dev]
```

### Docker Installation (Recommended)

```bash
# Clone the repository
git clone https://github.com/llamasearchai/OpenSearchEval.git
cd OpenSearchEval

# Start with Docker Compose
docker-compose up -d

# Access the API at http://localhost:8000
# Access the UI at http://localhost:5000
```

### Basic Usage

```python
import opensearcheval as ose

# Initialize experiment manager
experiments = ose.ExperimentManager()

# Create a new A/B test
experiment = experiments.create_experiment(
    name="New Ranking Algorithm",
    description="Testing improved relevance scoring",
    metrics=["mean_reciprocal_rank", "click_through_rate", "satisfaction_score"]
)

# Evaluate search results
results = [
    {"doc_id": "doc1", "title": "Python Tutorial", "score": 0.95},
    {"doc_id": "doc2", "title": "Machine Learning Guide", "score": 0.87},
]

# Calculate metrics
mrr = ose.mean_reciprocal_rank(
    query="python tutorial",
    results=results,
    relevance_judgments={"doc1": 2, "doc2": 1}
)

print(f"Mean Reciprocal Rank: {mrr:.3f}")
```

### API Usage

```python
import httpx

# Start the API server
# opensearcheval-api --host 0.0.0.0 --port 8000

# Evaluate search results via API
async with httpx.AsyncClient() as client:
    response = await client.post(
        "http://localhost:8000/api/v1/evaluate",
        json={
            "id": "eval_001",
            "query": "python tutorial",
            "results": results,
            "relevance_judgments": {"doc1": 2, "doc2": 1}
        }
    )
    
    metrics = response.json()["metrics"]
    print(f"API Response: {metrics}")
```

### Command Line Interface

```bash
# Evaluate search results from file
opensearcheval evaluate --input-file search_data.json --output-file results.json

# Create an experiment
opensearcheval experiment create \
    --name "Improved Ranking" \
    --metrics "mrr,ndcg_at_10,ctr" \
    --description "Testing new ranking algorithm"

# Generate embeddings
opensearcheval embedding generate \
    --input-file documents.json \
    --output-file embeddings.json \
    --model text-embedding-ada-002

# Run A/B test analysis
opensearcheval ab-test analyze \
    --control-data control.json \
    --treatment-data treatment.json \
    --confidence-level 0.95
```

## Architecture

### Agent-Based Processing

```python
# Initialize agent manager
agent_manager = ose.AgentManager()

# Create specialized agents
search_agent = ose.SearchEvaluationAgent(
    name="search_evaluator",
    metrics=[ose.mean_reciprocal_rank, ose.ndcg_at_k],
    config={"batch_size": 100}
)

ab_test_agent = ose.ABTestAgent(
    name="ab_tester",
    statistical_tests=[ose.t_test, ose.mann_whitney_u_test],
    config={"confidence_level": 0.95}
)

# Register and start agents
agent_manager.register_agent(search_agent)
agent_manager.register_agent(ab_test_agent)
await agent_manager.start_all()
```

### MLX Integration (Apple Silicon)

```python
# Use MLX for accelerated ML operations
from opensearcheval.ml import SearchRankingModel, ClickThroughRatePredictor

# Initialize MLX-powered ranking model
ranking_model = SearchRankingModel(
    embedding_dim=768,
    hidden_dim=256,
    use_mlx=True
)

# Train CTR prediction model
ctr_model = ClickThroughRatePredictor(
    feature_dim=20,
    hidden_dims=[64, 32]
)

# Train the model
trained_model = train_ctr_model(
    training_data=training_examples,
    epochs=50,
    batch_size=64
)
```

## Available Metrics

### Relevance Metrics
- **Mean Reciprocal Rank (MRR)**: Average of reciprocal ranks
- **NDCG@K**: Normalized Discounted Cumulative Gain
- **Precision@K**: Precision at various cutoff points
- **Recall@K**: Recall at various cutoff points
- **F1-Score**: Harmonic mean of precision and recall

### User Behavior Metrics
- **Click-Through Rate (CTR)**: Percentage of results clicked
- **Time to First Click**: Average time before first interaction
- **Dwell Time**: Time spent on clicked results
- **Abandonment Rate**: Percentage of searches without clicks
- **Satisfaction Score**: Composite user satisfaction metric

### Advanced Metrics
- **Reciprocal Rank Fusion**: Combines multiple result sets
- **Diversity Score**: Measures result diversity
- **Novelty Score**: Measures result novelty
- **Coverage**: Measures catalog coverage

## Configuration

### Environment Variables

```bash
# Application
APP_NAME=OpenSearchEval
ENVIRONMENT=production
DEBUG=false

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Database
DB_TYPE=postgresql
DB_URL=postgresql://user:password@localhost/opensearcheval

# LLM Configuration
LLM_MODEL=gpt-4-turbo
LLM_API_KEY=your-openai-api-key
LLM_TEMPERATURE=0.1

# MLX Configuration
USE_MLX=true
MLX_MODEL_PATH=./models/mlx_model

# Caching
REDIS_URL=redis://localhost:6379/0
ENABLE_CACHING=true
CACHE_TTL=3600

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090
```

### Configuration File

```python
from opensearcheval.core.config import get_settings

settings = get_settings()

# Access configuration
print(f"API Host: {settings.API_HOST}")
print(f"Database URL: {settings.database_url}")
print(f"Using MLX: {settings.USE_MLX}")
```

## API Documentation

### REST Endpoints

- `GET /health` - Health check
- `POST /api/v1/evaluate` - Evaluate search results
- `POST /api/v1/analyze-ab-test` - Analyze A/B test results
- `POST /api/v1/llm-judge` - LLM-based evaluation
- `GET /api/v1/experiments` - List experiments
- `POST /api/v1/experiments` - Create experiment
- `GET /api/v1/experiments/{id}` - Get experiment details
- `POST /api/v1/experiments/{id}/start` - Start experiment
- `POST /api/v1/experiments/{id}/stop` - Stop experiment

### WebSocket Support

```python
# Real-time metrics streaming
import websockets

async def metrics_stream():
    uri = "ws://localhost:8000/ws/metrics"
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            metrics = json.loads(message)
            print(f"Real-time metrics: {metrics}")
```

## Data Connectors

### Supported Data Sources

- **Databases**: PostgreSQL, MySQL, SQLite, MongoDB
- **Big Data**: Apache Spark, Databricks, Snowflake
- **Search Engines**: Elasticsearch, OpenSearch, Solr
- **Cloud Storage**: AWS S3, Google Cloud Storage, Azure Blob
- **APIs**: REST APIs, GraphQL endpoints

### Custom Connectors

```python
from opensearcheval.data.connectors import BaseConnector

class CustomConnector(BaseConnector):
    def connect(self):
        # Implement connection logic
        pass
    
    def fetch_data(self, query):
        # Implement data fetching
        pass
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=opensearcheval --cov-report=html

# Run specific test categories
pytest tests/test_metrics.py -v
pytest tests/test_agents.py -v
pytest tests/test_api.py -v

# Run performance tests
pytest tests/performance/ -v
```

### Test Data Generation

```python
from opensearcheval.testing import generate_test_data

# Generate synthetic search data
test_data = generate_test_data(
    num_queries=1000,
    num_results_per_query=50,
    relevance_distribution=[0.6, 0.3, 0.1]  # irrelevant, relevant, highly relevant
)
```

## Deployment

### Production Deployment

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  opensearcheval-api:
    image: opensearcheval:latest
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
      - DB_URL=postgresql://user:password@db/opensearcheval
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
  
  opensearcheval-ui:
    image: opensearcheval-ui:latest
    ports:
      - "5000:5000"
    depends_on:
      - opensearcheval-api
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_DB=opensearcheval
      - POSTGRES_USER=opensearcheval
      - POSTGRES_PASSWORD=secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Kubernetes Deployment

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opensearcheval-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opensearcheval-api
  template:
    metadata:
      labels:
        app: opensearcheval-api
    spec:
      containers:
      - name: api
        image: opensearcheval:latest
        ports:
        - containerPort: 8000
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DB_URL
          valueFrom:
            secretKeyRef:
              name: opensearcheval-secrets
              key: database-url
```

## Monitoring and Observability

### Metrics Collection

```python
from opensearcheval.monitoring import MetricsCollector

collector = MetricsCollector()

# Custom metrics
collector.counter("search_evaluations_total").inc()
collector.histogram("evaluation_duration_seconds").observe(0.5)
collector.gauge("active_experiments").set(5)
```

### Grafana Dashboard

Pre-built Grafana dashboards available at `/grafana/dashboards/`

### Alerting

```python
from opensearcheval.monitoring import AlertManager

alert_manager = AlertManager()

# Configure alerts
alert_manager.add_alert(
    name="high_error_rate",
    condition="error_rate > 0.05",
    notification_channels=["slack", "email"]
)
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone the repository
git clone https://github.com/llamasearchai/OpenSearchEval.git
cd OpenSearchEval

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e .[dev]

# Install pre-commit hooks
pre-commit install

# Run tests
pytest

# Format code
black opensearcheval/
isort opensearcheval/

# Type checking
mypy opensearcheval/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Documentation**: [https://opensearcheval.readthedocs.io/](https://opensearcheval.readthedocs.io/)
- **Issues**: [GitHub Issues](https://github.com/llamasearchai/OpenSearchEval/issues)
- **Discussions**: [GitHub Discussions](https://github.com/llamasearchai/OpenSearchEval/discussions)
- **Email**: nikjois@llamasearch.ai

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

## Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) and [MLX](https://ml-explore.github.io/mlx/)
- Inspired by modern search evaluation best practices
- Special thanks to the open-source community

---

<div align="center">
  <p>Made with love by <a href="https://github.com/nikjois">Nik Jois</a></p>
  <p>Star this project if you find it useful!</p>
</div>