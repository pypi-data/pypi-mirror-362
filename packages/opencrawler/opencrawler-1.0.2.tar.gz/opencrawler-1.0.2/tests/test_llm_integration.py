from typing import Optional
from typing import List

"""
Comprehensive tests for LLM integration features
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from pathlib import Path
import json
import tempfile
from datetime import datetime
import os

from webscraper.ai.llm_integration import (
    LLMConfig,
    StructuredExtractor,
    LLMAgent,
    DocumentationGenerator,
    WebsiteMonitor,
    ShellAgent,
)
from pydantic import BaseModel, Field
from typing import List, Optional


# Test schemas
class TestArticle(BaseModel):
    title: str
    content: str
    author: Optional[str] = None


class TestProduct(BaseModel):
    name: str
    price: str
    available: bool = True


class TestLLMIntegration:
    """Test suite for LLM integration features"""

    @pytest.fixture
    def llm_config(self):
        """Create test LLM configuration"""
        return LLMConfig(
            provider="openai",
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),  # Use environment variable
            temperature=0.5,
            max_tokens=2048,
        )

    @pytest.fixture
    def mock_openai_client(self):
        """Mock OpenAI client"""
        mock = MagicMock()
        mock.chat.completions.create = AsyncMock()
        return mock

    @pytest.fixture
    def mock_anthropic_client(self):
        """Mock Anthropic client"""
        mock = MagicMock()
        mock.messages.create = AsyncMock()
        return mock

    @pytest.mark.asyncio
    async def test_structured_extractor_openai(self, llm_config, mock_openai_client):
        """Test structured extraction with OpenAI"""
        with patch("openai.AsyncOpenAI", return_value=mock_openai_client):
            extractor = StructuredExtractor(llm_config)

            # Mock response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.tool_calls = [MagicMock()]
            mock_response.choices[0].message.tool_calls[0].function.arguments = (
                json.dumps(
                    {
                        "title": "Test Article",
                        "content": "Test content",
                        "author": "Test Author",
                    }
                )
            )

            mock_openai_client.chat.completions.create.return_value = mock_response

            # Test extraction
            result = await extractor.extract(
                "<h1>Test Article</h1><p>Test content</p>", TestArticle, format="html"
            )

            assert isinstance(result, TestArticle)
            assert result.title == "Test Article"
            assert result.content == "Test content"
            assert result.author == "Test Author"

    @pytest.mark.asyncio
    async def test_structured_extractor_anthropic(self, mock_anthropic_client):
        """Test structured extraction with Anthropic"""
        config = LLMConfig(provider="anthropic", model="claude-3-opus-20240229")

        with patch("anthropic.AsyncAnthropic", return_value=mock_anthropic_client):
            extractor = StructuredExtractor(config)

            # Mock response
            mock_response = MagicMock()
            mock_response.content = [MagicMock()]
            mock_response.content[0].text = json.dumps(
                {"name": "Test Product", "price": "$99.99", "available": True}
            )

            mock_anthropic_client.messages.create.return_value = mock_response

            # Test extraction
            result = await extractor.extract(
                "Product: Test Product - Price: $99.99 - In Stock",
                TestProduct,
                format="text",
            )

            assert isinstance(result, TestProduct)
            assert result.name == "Test Product"
            assert result.price == "$99.99"
            assert result.available == True

    @pytest.mark.asyncio
    async def test_llm_agent_planning(self, llm_config):
        """Test LLM agent planning capabilities"""
        with patch(
            "webscraper.ai.llm_integration.StructuredExtractor"
        ) as mock_extractor_class:
            mock_extractor = MagicMock()
            mock_extractor_class.return_value = mock_extractor

            # Mock planning response
            mock_plan = MagicMock()
            mock_plan.steps = [
                {"action": "crawl", "description": "Crawl the website"},
                {"action": "extract", "description": "Extract data"},
            ]
            mock_extractor.extract = AsyncMock(return_value=mock_plan)

            agent = LLMAgent("TestAgent", llm_config)
            steps = await agent.plan(
                "Extract all products", {"url": "https://example.com"}
            )

            assert len(steps) == 2
            assert steps[0]["action"] == "crawl"
            assert steps[1]["action"] == "extract"

    @pytest.mark.asyncio
    async def test_documentation_generator(self, llm_config):
        """Test documentation generation"""
        with patch("webscraper.ai.llm_integration.StructuredExtractor"):
            doc_gen = DocumentationGenerator(llm_config)

            # Test data
            scraped_data = [
                {
                    "url": "https://example.com/docs/intro",
                    "content": "<h1>Introduction</h1><p>Welcome to docs</p>",
                    "extracted_data": {
                        "title": "Introduction",
                        "content": "Welcome to docs",
                    },
                }
            ]

            # Mock TOC generation
            doc_gen._generate_toc = AsyncMock(return_value="- [Introduction](intro.md)")
            doc_gen._process_page_to_markdown = AsyncMock()

            # Test markdown generation
            with tempfile.TemporaryDirectory() as tmpdir:
                output_path = Path(tmpdir) / "docs"
                result = await doc_gen.generate_markdown_docs(
                    scraped_data, output_path=output_path
                )

                assert output_path.exists()
                assert (output_path / "index.md").exists()

    @pytest.mark.asyncio
    async def test_website_monitor(self, llm_config):
        """Test website monitoring functionality"""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage_path = Path(tmpdir)
            monitor = WebsiteMonitor(llm_config, storage_path=storage_path)

            # Mock scraper
            with patch(
                "webscraper.core.advanced_scraper.AdvancedWebScraper"
            ) as mock_scraper_class:
                mock_scraper = MagicMock()
                mock_scraper_class.return_value = mock_scraper
                mock_scraper.setup = AsyncMock()
                mock_scraper.cleanup = AsyncMock()
                mock_scraper.scrape_url = AsyncMock(
                    return_value={
                        "url": "https://example.com",
                        "content": "Test content",
                        "status": 200,
                    }
                )

                # Mock extractor
                with patch.object(monitor, "extractor") as mock_extractor:
                    mock_snapshot = MagicMock()
                    mock_snapshot.dict.return_value = {
                        "title": "Test Page",
                        "main_content_hash": "abc123",
                        "key_elements": {"price": "$99"},
                        "timestamp": datetime.now().isoformat(),
                    }
                    mock_extractor.extract = AsyncMock(return_value=mock_snapshot)

                    # Setup monitoring
                    config = await monitor.setup_monitoring("https://example.com")

                    assert "monitor_id" in config
                    assert config["url"] == "https://example.com"

                    # Check for changes
                    changes = await monitor.check_for_changes(
                        "https://example.com", config["monitor_id"]
                    )
                    assert changes is None  # No changes on first check

    @pytest.mark.asyncio
    async def test_shell_agent_safe_mode(self, llm_config):
        """Test shell agent with safety checks"""
        shell_agent = ShellAgent(llm_config, safe_mode=True)

        # Mock safety check
        with patch.object(shell_agent, "extractor") as mock_extractor:
            # Test unsafe command
            mock_safety = MagicMock()
            mock_safety.is_safe = False
            mock_safety.reason = "Dangerous command"
            mock_extractor.extract = AsyncMock(return_value=mock_safety)

            result = await shell_agent.execute_command("rm -rf /")

            assert result["status"] == "blocked"
            assert "Dangerous command" in result["reason"]

    @pytest.mark.asyncio
    async def test_shell_agent_datasette_analysis(self, llm_config):
        """Test datasette integration for data analysis"""
        shell_agent = ShellAgent(llm_config)

        test_data = [
            {"url": "https://example.com/1", "title": "Page 1", "views": 100},
            {"url": "https://example.com/2", "title": "Page 2", "views": 200},
        ]

        # Test analysis (without actual datasette)
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                stdout="Total views: 300", stderr="", returncode=0
            )

            result = await shell_agent.analyze_with_datasette(
                test_data, "SELECT SUM(views) as total_views FROM scraped_data"
            )

            assert "query" in result
            assert "SELECT SUM(views)" in result["query"]


class TestEndToEndLLMFeatures:
    """End-to-end tests for LLM features"""

    @pytest.mark.asyncio
    async def test_complete_extraction_pipeline(self):
        """Test complete extraction pipeline"""
        config = LLMConfig(provider="openai", model="gpt-4o")

        with patch("openai.AsyncOpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client

            # Mock extraction response
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message.tool_calls = [MagicMock()]
            mock_response.choices[0].message.tool_calls[0].function.arguments = (
                json.dumps(
                    {
                        "title": "Complete Article",
                        "content": "This is a complete test",
                        "author": "Test Suite",
                    }
                )
            )

            mock_client.chat.completions.create = AsyncMock(return_value=mock_response)

            # Create extractor and extract
            extractor = StructuredExtractor(config)

            html_content = """
            <html>
                <head><title>Complete Article</title></head>
                <body>
                    <h1>Complete Article</h1>
                    <p>By Test Suite</p>
                    <p>This is a complete test</p>
                </body>
            </html>
            """

            result = await extractor.extract(
                html_content,
                TestArticle,
                format="html",
                instructions="Extract the article information",
            )

            assert result.title == "Complete Article"
            assert result.author == "Test Suite"
            assert "complete test" in result.content

    @pytest.mark.asyncio
    async def test_agent_autonomous_execution(self):
        """Test agent autonomous execution"""
        config = LLMConfig(provider="openai", model="gpt-4o")

        # Mock tools
        async def mock_crawl(context):
            return {"status": "success", "pages": 5}

        async def mock_extract(context):
            return {"extracted": 10, "format": "json"}

        with patch(
            "webscraper.ai.llm_integration.StructuredExtractor"
        ) as mock_extractor_class:
            mock_extractor = MagicMock()
            mock_extractor_class.return_value = mock_extractor

            # Mock planning
            mock_plan = MagicMock()
            mock_plan.steps = [
                {"action": "mock_crawl", "description": "Crawl website"},
                {"action": "mock_extract", "description": "Extract data"},
            ]
            mock_extractor.extract = AsyncMock(return_value=mock_plan)

            agent = LLMAgent("AutoAgent", config, tools=[mock_crawl, mock_extract])

            result = await agent.execute(
                "Extract all data from website", {"url": "https://example.com"}
            )

            assert result["steps_completed"] == 2
            assert len(result["results"]) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
