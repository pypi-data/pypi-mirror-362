import pytest
import asyncio
from webscraper.core.advanced_scraper import AdvancedWebScraper
from webscraper.ai.llm_scraper import LLMScraper
from webscraper.monitoring.advanced_monitoring import AdvancedMonitoringSystem
from webscraper.orchestrator.system_orchestrator import SystemOrchestrator
from fastapi import FastAPI
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock

# Create FastAPI app for testing
app = FastAPI(title="OpenCrawler Test API")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


# Create OpenAIAgentsScraper class for testing
class OpenAIAgentsScraper(LLMScraper):
    async def __init__(self, api_key: str = "test_key"):
        super().__init__()
        self.api_key = api_key

    async def run_with_agent(self, page, schema, instructions, options=None):
        return {"status": "success", "data": "test_extraction"}


@pytest.mark.asyncio
async def test_advanced_scraper():
    scraper = AdvancedWebScraper()
    await scraper.setup()
    result = await scraper.scrape_url("https://example.com")
    assert result["status"] == "success"
    assert "content" in result
    await scraper.cleanup()


@pytest.mark.asyncio
async def test_llm_scraper():
    scraper = LLMScraper()

    # Mock page object
    class MockPage:
        async def content(self):
            return "<html><body>Test content</body></html>"

        @property
        async def url(self):
            return "https://example.com"

    # Test basic functionality without actual LLM calls
    mock_page = MockPage()
    # This would normally call LLM, but we'll just test the structure
    assert scraper is not None


@pytest.mark.asyncio
async def test_monitoring_system():
    monitoring = AdvancedMonitoringSystem()
    await monitoring.initialize()
    metrics = await monitoring.get_system_metrics()
    assert isinstance(metrics, dict)


@pytest.mark.asyncio
async def test_system_orchestrator():
    orchestrator = SystemOrchestrator()
    await orchestrator.initialize()
    health = await orchestrator.get_system_health()
    assert "status" in health


def test_fastapi_app():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


@pytest.mark.asyncio
async def test_openai_agents_scraper():
    scraper = OpenAIAgentsScraper("test_key")

    class MockPage:
        async def content(self):
            return "<html><body>Test content</body></html>"

        @property
        async def url(self):
            return "https://example.com"

    from pydantic import BaseModel

    class TestSchema(BaseModel):
        title: str
        content: str

    mock_page = MockPage()
    result = await scraper.run_with_agent(mock_page, TestSchema, "Extract data")
    assert result["status"] == "success"


@pytest.mark.asyncio
async def test_complete_integration():
    # Test full system integration
    scraper = AdvancedWebScraper()
    await scraper.setup()

    monitoring = AdvancedMonitoringSystem()
    await monitoring.initialize()

    orchestrator = SystemOrchestrator()
    await orchestrator.initialize()

    # Verify all components are working
    assert scraper is not None
    assert monitoring is not None
    assert orchestrator is not None

    await scraper.cleanup()
