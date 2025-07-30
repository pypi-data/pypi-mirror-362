# OpenCrawler

<div align="center">
  <img src="assets/opencrawler-logo.svg" alt="OpenCrawler Logo" width="200" height="200">
  <br>
  <em>AI-Powered Web Intelligence</em>
</div>

[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-1.0.2-blue.svg)](https://pypi.org/project/opencrawler/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**OpenCrawler** is a production-ready, enterprise-grade web scraping and crawling framework with advanced AI integration, comprehensive monitoring, and scalable architecture.

## 🚀 Quick Installation

```bash
# Install from PyPI
pip install opencrawler

# Install with AI capabilities
pip install "opencrawler[ai]"

# Install with all features
pip install "opencrawler[all]"
```

## Features

### Core Capabilities
- **Multi-Engine Support**: Playwright, Selenium, Requests, CloudScraper
- **AI-Powered Extraction**: OpenAI Agents SDK integration for intelligent data extraction
- **Stealth Technology**: Advanced anti-detection and bot bypass capabilities
- **Distributed Processing**: Scalable architecture for high-volume operations
- **Real-time Monitoring**: Comprehensive metrics and health monitoring
- **Enterprise Security**: RBAC, audit trails, and compliance features

### Advanced Features
- **LLM Integration**: Support for OpenAI, Anthropic, and local models
- **Microservice Architecture**: FastAPI-based REST API with auto-documentation
- **Database Support**: PostgreSQL, TimescaleDB, Redis integration
- **Container Ready**: Docker and Kubernetes deployment configurations
- **Performance Optimization**: Intelligent caching, rate limiting, and resource management
- **Error Recovery**: Sophisticated error handling and retry mechanisms

## Quick Start

### Basic Usage

```python
import asyncio
from webscraper.core.advanced_scraper import AdvancedWebScraper

async def main():
    # Initialize scraper
    scraper = AdvancedWebScraper()
    await scraper.setup()
    
    # Scrape a webpage
    result = await scraper.scrape_url("https://example.com")
    print(f"Title: {result.get('title')}")
    print(f"Content length: {len(result.get('content', ''))}")
    
    # Cleanup
    await scraper.cleanup()

asyncio.run(main())
```

### CLI Usage

```bash
# Basic scraping
opencrawler scrape https://example.com

# Advanced scraping with AI
opencrawler scrape https://example.com --ai-extract --model gpt-4

# Start API server
opencrawler api --host 0.0.0.0 --port 8000

# Run system validation
opencrawler-validate --level production
```

## Architecture

OpenCrawler follows a modular, microservice-oriented architecture:

```
OpenCrawler/
├── webscraper/
│   ├── core/           # Core scraping engines
│   ├── ai/             # AI/LLM integration
│   ├── api/            # FastAPI REST API
│   ├── engines/        # Scraping engines (Playwright, Selenium, etc.)
│   ├── processors/     # Data processing pipelines
│   ├── monitoring/     # System monitoring and metrics
│   ├── security/       # Authentication and security
│   ├── utils/          # Utilities and helpers
│   └── orchestrator/   # System orchestration
├── tests/              # Comprehensive test suite
├── deployment/         # Docker and Kubernetes configs
├── docs/               # Documentation
└── examples/           # Usage examples
```

## Configuration

### Environment Variables

```bash
# OpenAI API (optional)
export OPENAI_API_KEY="your-api-key-here"

# Database (optional)
export DATABASE_URL="postgresql://user:pass@localhost/opencrawler"

# Redis (optional)
export REDIS_URL="redis://localhost:6379"

# Test mode
export OPENCRAWLER_TEST_MODE=true
```

### Configuration File

Create a `config.yaml` file:

```yaml
scraper:
  engines: ["playwright", "requests"]
  stealth_level: "medium"
  javascript_enabled: true
  
ai:
  enabled: true
  model: "gpt-4"
  temperature: 0.7
  
database:
  url: "postgresql://localhost/opencrawler"
  pool_size: 10
  
monitoring:
  enabled: true
  metrics_port: 9090
  
security:
  enable_auth: true
  rate_limit: 100
```

## API Reference

### REST API

Start the API server:

```bash
opencrawler-api --port 8000
```

#### Endpoints

- `GET /health` - Health check
- `POST /scrape` - Scrape a single URL
- `POST /crawl` - Crawl multiple URLs
- `GET /metrics` - System metrics
- `GET /docs` - API documentation

#### Example Request

```bash
curl -X POST "http://localhost:8000/scrape" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com", "extract_ai": true}'
```

### Python API

```python
from webscraper.api.complete_api import OpenCrawlerAPI

# Initialize API
api = OpenCrawlerAPI()
await api.initialize()

# Scrape with AI
result = await api.scrape_with_ai(
    url="https://example.com",
    schema={"title": "string", "content": "string"}
)

# Cleanup
await api.cleanup()
```

## Advanced Usage

### AI-Powered Extraction

```python
from webscraper.ai.llm_scraper import LLMScraper

scraper = LLMScraper()
await scraper.initialize()

# Extract structured data
result = await scraper.run(
    url="https://news.example.com",
    schema={
        "title": "string",
        "author": "string", 
        "date": "date",
        "content": "string"
    }
)
```

### Distributed Processing

```python
from webscraper.core.distributed_processor import DistributedProcessor

processor = DistributedProcessor(worker_count=16)
await processor.initialize()

# Process multiple URLs
results = await processor.process_batch([
    "https://example1.com",
    "https://example2.com",
    "https://example3.com"
])
```

### Custom Engines

```python
from webscraper.engines.base_engine import BaseEngine

class CustomEngine(BaseEngine):
    async def fetch(self, url: str, **kwargs) -> dict:
        # Custom implementation
        return {"content": "...", "status": 200}

# Register custom engine
scraper.register_engine("custom", CustomEngine())
```

## Monitoring and Metrics

### Built-in Monitoring

```python
from webscraper.monitoring.advanced_monitoring import AdvancedMonitoringSystem

monitor = AdvancedMonitoringSystem()
await monitor.initialize()

# Get system metrics
metrics = await monitor.get_system_metrics()
print(f"CPU: {metrics['cpu_usage']}%")
print(f"Memory: {metrics['memory_usage']}%")
```

### Prometheus Integration

OpenCrawler exports metrics to Prometheus:

```bash
# Start with monitoring
python master_cli.py api --enable-metrics --metrics-port 9090
```

Metrics available at `http://localhost:9090/metrics`

## Deployment

### Docker

```bash
# Build image
docker build -t opencrawler .

# Run container
docker run -p 8000:8000 opencrawler
```

### Docker Compose

```bash
# Start all services
docker-compose up -d

# Production deployment
docker-compose -f docker-compose.production.yml up -d
```

### Kubernetes

```bash
# Deploy to Kubernetes
kubectl apply -f kubernetes/

# Check deployment
kubectl get pods -l app=opencrawler
```

### Production Deployment

```python
from deployment.production_deployment import ProductionDeploymentSystem

deployment = ProductionDeploymentSystem()
await deployment.initialize()

# Deploy to production
result = await deployment.deploy(
    environment="production",
    config_overrides={"replicas": 5}
)
```

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_complete_system.py

# Run with coverage
pytest --cov=webscraper

# Run in test mode
OPENCRAWLER_TEST_MODE=true pytest
```

### Test Categories

- **Unit Tests**: Core component testing
- **Integration Tests**: Service integration testing
- **Performance Tests**: Load and performance testing
- **Security Tests**: Security validation
- **End-to-End Tests**: Complete workflow testing

### Validation

```bash
# Run comprehensive validation
python webscraper/utils/comprehensive_validator.py --level production

# Check system health
python -c "
from webscraper.orchestrator.system_orchestrator import SystemOrchestrator
import asyncio

async def main():
    orchestrator = SystemOrchestrator()
    await orchestrator.initialize()
    health = await orchestrator.get_system_health()
    print(f'System Status: {health[\"status\"]}')
    await orchestrator.shutdown()

asyncio.run(main())
"
```

## Performance

### Benchmarks

- **Single Page**: ~2-5 seconds per page
- **Concurrent Crawling**: 50-100 pages/minute
- **Memory Usage**: <1GB for typical workloads
- **CPU Usage**: Optimized for multi-core systems

### Optimization

```python
# Enable performance optimizations
scraper = AdvancedWebScraper(
    stealth_level="low",  # Faster but less stealthy
    javascript_enabled=False,  # Skip JS rendering
    cache_enabled=True,  # Enable caching
    concurrent_requests=10  # Increase concurrency
)
```

## Security

### Authentication

```python
from webscraper.security.authentication import AuthManager

auth = AuthManager()
await auth.initialize()

# Create user
user = await auth.create_user("username", "password", ["scraper"])

# Authenticate
token = await auth.authenticate("username", "password")
```

### Rate Limiting

```python
from webscraper.security.rate_limiter import RateLimiter

limiter = RateLimiter(requests_per_minute=60)
await limiter.check_rate_limit(user_id="user123")
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Clone and install
git clone https://github.com/llamasearch/opencrawler.git
cd opencrawler
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install

# Run tests
pytest
```

### Code Style

We use [Black](https://github.com/psf/black) for code formatting:

```bash
# Format code
black webscraper/

# Check formatting
black --check webscraper/
```

## License

OpenCrawler is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- **Documentation**: [docs/](docs/)
- **Examples**: [examples/](examples/)
- **Issues**: [GitHub Issues](https://github.com/llamasearch/opencrawler/issues)
- **Discussions**: [GitHub Discussions](https://github.com/llamasearch/opencrawler/discussions)

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and updates.

## Assets

OpenCrawler includes a complete set of professional logo assets:

### Logo Variants

- **`assets/opencrawler-logo.svg`** - Main logo with full branding (light theme)
- **`assets/opencrawler-logo-dark.svg`** - Dark variant for light backgrounds
- **`assets/opencrawler-icon.svg`** - Icon version for app icons and buttons
- **`assets/favicon.svg`** - Favicon optimized for small sizes

### Design Features

- **Spider/Crawler Theme**: Represents web crawling and data extraction
- **AI/Neural Network Elements**: Symbolizes AI-powered intelligence
- **Modern Gradients**: Professional blue, green, and orange color scheme
- **Scalable Vector Graphics**: Perfect quality at any size
- **Multiple Formats**: SVG for web, can be converted to PNG/ICO as needed

### Usage Guidelines

```html
<!-- Main logo for documentation -->
<img src="assets/opencrawler-logo.svg" alt="OpenCrawler" width="200">

<!-- Dark variant for light backgrounds -->
<img src="assets/opencrawler-logo-dark.svg" alt="OpenCrawler" width="200">

<!-- Icon for buttons/navigation -->
<img src="assets/opencrawler-icon.svg" alt="OpenCrawler" width="32">

<!-- Favicon -->
<link rel="icon" type="image/svg+xml" href="assets/favicon.svg">
```

## Acknowledgments

OpenCrawler is built with these excellent libraries:

- [Playwright](https://playwright.dev/) - Modern web automation
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance API framework
- [OpenAI](https://openai.com/) - AI/LLM integration
- [PostgreSQL](https://www.postgresql.org/) - Database backend
- [Docker](https://www.docker.com/) - Containerization
- [Kubernetes](https://kubernetes.io/) - Container orchestration

---

**Author**: Nik Jois <nikjois@llamasearch.ai>  
**Organization**: LlamaSearch.ai  
**Version**: 1.0.1  
**Status**: Production Ready 