import logging
"""
Comprehensive Test Suite for OpenCrawler
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path
import json
from datetime import datetime

from webscraper.core.advanced_scraper import AdvancedWebScraper
from webscraper.stealth.stealth_manager import StealthManager
from webscraper.stealth.antibot_bypass import AntiBotBypass
from webscraper.processors.advanced_output_formatter import AdvancedOutputFormatter

from webscraper.utils.monitoring import AdvancedLogger, ScrapingMetrics


class TestAdvancedWebScraper:
    """Test suite for AdvancedWebScraper"""

    @pytest.fixture
    def scraper(self):
        """Create scraper instance for testing"""
        scraper = AdvancedWebScraper(
            stealth_level="medium",
            use_ai=False,
            javascript_enabled=False,
            max_retries=2,
            timeout=10000,
        )
        return scraper

    @pytest.fixture
    def mock_response(self):
        """Mock HTTP response"""
        return {
            "content": "<html><head><title>Test Page</title></head><body><h1>Test</h1><a href='/link'>Link</a></body></html>",
            "status": 200,
            "url": "https://example.com",
            "headers": {"content-type": "text/html"},
        }

    @pytest.mark.asyncio
    async def test_scraper_initialization(self, scraper):
        """Test scraper initialization"""
        assert scraper.stealth_level == "medium"
        assert scraper.use_ai == False
        assert scraper.javascript_enabled == False
        assert scraper.max_retries == 2
        assert scraper.timeout == 10000

    @pytest.mark.asyncio
    async def test_engine_selection(self, scraper):
        """Test intelligent engine selection"""
        # Test JS patterns
        js_url = "https://example.com/app/dashboard"
        engine = await scraper._select_engine(js_url, None, True)
        assert engine == "playwright"

        # Test high stealth preference
        scraper.stealth_level = "high"
        engine = await scraper._select_engine("https://example.com", None, False)
        assert engine == "cloudscraper"

        # Test simple case
        scraper.stealth_level = "low"
        engine = await scraper._select_engine("https://example.com", None, False)
        assert engine == "requests"

    @pytest.mark.asyncio
    async def test_content_extraction(self, scraper, mock_response):
        """Test content extraction functionality"""
        extracted = await scraper._extract_content(mock_response)

        assert extracted["title"] == "Test Page"
        assert len(extracted["headings"]["h1"]) == 1
        assert extracted["headings"]["h1"][0] == "Test"
        assert len(extracted["links"]) == 1
        assert extracted["links"][0]["text"] == "Link"
        assert extracted["links"][0]["href"] == "https://example.com/link"

    @pytest.mark.asyncio
    async def test_retry_mechanism(self, scraper):
        """Test retry mechanism with failures"""
        with patch.object(scraper, "_scrape_with_requests") as mock_scrape:
            # Simulate failures then success
            mock_scrape.side_effect = [
                Exception("Connection error"),
                Exception("Timeout"),
                {"url": "https://example.com", "status": 200, "content": "Success"},
            ]

            result = await scraper.scrape_url("https://example.com")

            assert mock_scrape.call_count == 3
            assert result["status"] == 200

    @pytest.mark.asyncio
    async def test_session_management(self, scraper):
        """Test session data management"""
        # Scrape URLs
        scraper.session_data["visited_urls"].add("https://example.com/page1")

        # Test duplicate detection
        result = await scraper.scrape_url("https://example.com/page1")
        assert result["status"] == "already_visited"

        # Test failed URL tracking
        scraper.session_data["failed_urls"].add("https://example.com/failed")
        assert "https://example.com/failed" in scraper.session_data["failed_urls"]


class TestStealthManager:
    """Test suite for StealthManager"""

    @pytest.fixture
    def stealth_manager(self):
        """Create StealthManager instance"""
        return StealthManager(level="high")

    def test_stealth_headers_generation(self, stealth_manager):
        """Test stealth header generation"""
        headers = stealth_manager.get_stealth_headers()

        assert "User-Agent" in headers
        assert "Accept" in headers
        assert "Accept-Language" in headers
        assert headers["DNT"] == "1"

    async def test_random_delay_calculation(self, stealth_manager):
        """Test random delay generation"""
        delays = [stealth_manager.get_random_delay() for _ in range(10)]

        # Check delays are within expected range
        assert all(0.5 <= d <= 3.5 for d in delays)
        # Check randomness
        assert len(set(delays)) > 5

    @pytest.mark.asyncio
    async def test_playwright_stealth_application(self, stealth_manager):
        """Test Playwright stealth configuration"""
        mock_context = AsyncMock()

        await stealth_manager.apply_stealth_to_playwright(mock_context)

        # Verify stealth methods were called
        mock_context.set_viewport_size.assert_called()
        mock_context.add_init_script.assert_called()
        mock_context.set_extra_http_headers.assert_called()


class TestAntiBotBypass:
    """Test suite for AntiBotBypass"""

    @pytest.fixture
    async def antibot_bypass(self):
        """Create AntiBotBypass instance"""
        stealth_manager = StealthManager()
        return AntiBotBypass(stealth_manager)

    @pytest.mark.asyncio
    async def test_antibot_detection(self, antibot_bypass):
        """Test anti-bot system detection"""
        mock_page = AsyncMock()

        # Test Cloudflare detection
        mock_page.content.return_value = (
            '<div class="cf-browser-verification">Checking your browser</div>'
        )
        detected = await antibot_bypass._detect_antibot_systems(mock_page)
        assert "cloudflare" in detected

        # Test ReCAPTCHA detection
        mock_page.content.return_value = '<div class="g-recaptcha"></div>'
        detected = await antibot_bypass._detect_antibot_systems(mock_page)
        assert "recaptcha" in detected

    @pytest.mark.asyncio
    async def test_cloudflare_bypass(self, antibot_bypass):
        """Test Cloudflare bypass handling"""
        mock_page = AsyncMock()
        mock_page.query_selector.return_value = None

        result = await antibot_bypass._handle_cloudflare(mock_page)
        assert result == True


class TestOutputFormatter:
    """Test suite for AdvancedOutputFormatter"""

    @pytest.fixture
    def formatter(self):
        """Create formatter instance"""
        return AdvancedOutputFormatter()

    @pytest.fixture
    def sample_data(self):
        """Sample scraped data"""
        return [
            {
                "url": "https://example.com/page1",
                "status": 200,
                "content": "Test content",
                "timestamp": datetime.now().isoformat(),
                "engine": "requests",
                "extracted_data": {
                    "title": "Page 1",
                    "links": [{"text": "Link", "href": "https://example.com/link"}],
                    "images": [],
                },
            },
            {
                "url": "https://example.com/page2",
                "status": "failed",
                "error": "Connection timeout",
                "timestamp": datetime.now().isoformat(),
                "engine": "playwright",
            },
        ]

    def test_json_export(self, formatter, sample_data, tmp_path):
        """Test JSON export functionality"""
        output_file = tmp_path / "test.json"
        formatter.export_to_json(sample_data, output_file)

        assert output_file.exists()

        with open(output_file) as f:
            data = json.load(f)

        assert data["count"] == 2
        assert len(data["data"]) == 2
        assert "metadata" in data

    def test_csv_export(self, formatter, sample_data, tmp_path):
        """Test CSV export functionality"""
        output_file = tmp_path / "test.csv"
        formatter.export_to_csv(sample_data, output_file)

        assert output_file.exists()

        import csv

        with open(output_file) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 2
        assert "url" in rows[0]

    def test_markdown_export(self, formatter, sample_data, tmp_path):
        """Test Markdown export functionality"""
        output_file = tmp_path / "test.md"
        formatter.export_to_markdown(sample_data, output_file)

        assert output_file.exists()

        content = output_file.read_text()
        assert "# Web Scraping Results" in content
        assert "Page 1" in content

    def test_organize_output(self, formatter, sample_data, tmp_path):
        """Test output organization"""
        organized = formatter.organize_output(
            sample_data, base_dir=str(tmp_path), organize_by="domain"
        )

        assert "example.com" in organized
        assert (tmp_path / "example.com").exists()

    def test_statistics_generation(self, formatter, sample_data):
        """Test statistics generation"""
        stats = formatter._generate_statistics(sample_data)

        assert stats["total_urls"] == 2
        assert stats["successful"] == 1
        assert stats["failed"] == 1
        assert stats["success_rate"] == 50.0


class TestMonitoring:
    """Test suite for monitoring components"""

    @pytest.fixture
    def logger(self):
        """Create logger instance"""
        return AdvancedLogger(log_dir="test_logs")

    def test_scraping_metrics(self):
        """Test ScrapingMetrics dataclass"""
        metrics = ScrapingMetrics(
            url="https://example.com",
            status="200",
            response_time=1.5,
            content_size=1024,
            engine="requests",
            timestamp=datetime.now(),
        )

        assert metrics.url == "https://example.com"
        assert metrics.response_time == 1.5
        assert metrics.antibot_detected == False

    def test_logging_events(self, logger):
        """Test logging various events"""
        # Test scraping start
        logger.log_scraping_start("https://example.com", "requests")

        # Test scraping complete
        metrics = ScrapingMetrics(
            url="https://example.com",
            status="200",
            response_time=1.5,
            content_size=1024,
            engine="requests",
            timestamp=datetime.now(),
        )
        logger.log_scraping_complete(metrics)

        # Test error logging
        try:
            raise ValueError("Test error")
        except ValueError as e:
            logger.log_error(e, {"url": "https://example.com"})

        # Test anti-bot logging
        logger.log_antibot_detection("https://example.com", "cloudflare", True)


@pytest.mark.asyncio
async def test_end_to_end_scraping():
    """End-to-end integration test"""
    scraper = AdvancedWebScraper(
        stealth_level="low", javascript_enabled=False, max_retries=1
    )

    try:
        # Mock the requests engine
        with patch.object(scraper.engines["requests"], "fetch") as mock_fetch:
            mock_fetch.return_value = {
                "content": "<html><title>Test</title><body>Content</body></html>",
                "status": 200,
                "url": "https://example.com",
                "headers": {},
            }

            # Setup engines
            scraper.engines["requests"] = Mock()
            scraper.engines["requests"].fetch = mock_fetch

            # Perform scraping
            result = await scraper.scrape_url("https://example.com")

            # Verify results
            assert result["status"] == 200
            assert "extracted_data" in result
            assert result["extracted_data"]["title"] == "Test"

    finally:
        # Cleanup
        await scraper.cleanup()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
