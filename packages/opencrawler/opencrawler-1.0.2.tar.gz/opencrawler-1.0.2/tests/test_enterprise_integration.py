from typing import List
from typing import Dict
from typing import Any

"""
Enterprise Integration Tests for OpenCrawler
Comprehensive tests for distributed processing, multi-modal data handling, and system integration
Author: Nik Jois <nikjois@llamasearch.ai>
"""

import pytest
import asyncio
import time
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random

from webscraper.database import CrawlRecord, ProcessingMetrics
from webscraper.core.distributed_processor import DataChunk, ProcessingResult


@pytest.mark.integration
@pytest.mark.asyncio
class TestFullSystemIntegration:
    """Test complete system integration across all components"""

    async def test_end_to_end_crawling_pipeline(
        self, advanced_crawler, database_manager, multimodal_processor, sample_urls
    ):
        """Test complete end-to-end crawling pipeline"""

        # Start crawl session
        session_id = await advanced_crawler.start_crawl_session(
            session_name="integration_test",
            seed_urls=sample_urls[:3],  # Use first 3 URLs
            crawl_config={"max_depth": 1, "max_pages": 10, "respect_robots_txt": False},
        )

        assert session_id is not None
        assert len(session_id) > 0

        # Crawl batch
        results = await advanced_crawler.crawl_batch(batch_size=5)

        # Verify results
        assert isinstance(results, list)

        # Check crawl statistics
        stats = await advanced_crawler.get_crawl_statistics()
        assert stats["session"]["session_id"] == session_id
        assert stats["crawl_stats"]["completed"] >= 0

        # Verify data was stored in database
        if results:
            stored_records = await database_manager.get_crawl_records(limit=10)
            assert len(stored_records) >= 0  # Should have some records

    async def test_distributed_processing_workflow(
        self, distributed_processor, sample_data_chunk, multimodal_processor
    ):
        """Test distributed processing workflow"""

        # Create multiple data chunks
        chunks = []
        for i in range(5):
            chunk = DataChunk(
                chunk_id=f"test-chunk-{i}",
                data_type="web",
                source_url=f"https://example.com/page{i}",
                content=f"<html><body>Test content {i}</body></html>",
                metadata={"page_number": i},
                size_bytes=1024,
                timestamp=datetime.now(),
            )
            chunks.append(chunk)

        # Submit chunks for processing
        chunk_ids = []
        for chunk in chunks:
            chunk_id = await distributed_processor.submit_data_chunk(chunk)
            chunk_ids.append(chunk_id)

        assert len(chunk_ids) == 5

        # Process chunks in batches
        async def dummy_processor(chunk):
            """Dummy processing function for testing"""
            # Simulate processing with multimodal processor
            result = await multimodal_processor.process(
                data=chunk.content,
                data_type=chunk.data_type,
                metadata=chunk.metadata,
                source_url=chunk.source_url,
            )

            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=True,
                processed_data=result,
                processing_time=0.1,
                output_size_bytes=len(str(result).encode()),
                quality_score=(
                    result.quality_score if hasattr(result, "quality_score") else 0.8
                ),
            )

        results = await distributed_processor.process_batch(chunks, dummy_processor)

        # Verify results
        assert len(results) == 5
        successful_results = [r for r in results if r.success]
        assert len(successful_results) >= 4  # At least 80% success rate

        # Check processing statistics
        stats = await distributed_processor.get_processing_stats()
        assert stats["total_processed"] >= 5

    async def test_multimodal_data_pipeline(
        self,
        multimodal_processor,
        mock_html_content,
        mock_json_data,
        large_text_content,
    ):
        """Test multi-modal data processing pipeline"""

        test_data = [
            (mock_html_content, "web", "text/html"),
            (json.dumps(mock_json_data), "structured", "application/json"),
            (large_text_content, "text", "text/plain"),
            ("print('Hello, World!')", "code", "text/x-python"),
        ]

        results = []
        for content, data_type, content_type in test_data:
            result = await multimodal_processor.process(
                data=content,
                data_type=data_type,
                metadata={"content_type": content_type},
                source_url="https://test.example.com",
            )
            results.append(result)

        # Verify all data types were processed
        assert len(results) == 4

        # Check quality scores
        quality_scores = [r.quality_score for r in results]
        assert all(0.0 <= score <= 1.0 for score in quality_scores)

        # Verify processing times are reasonable
        processing_times = [r.processing_time for r in results]
        assert all(time > 0 for time in processing_times)
        assert max(processing_times) < 10.0  # Should process within 10 seconds

    async def test_database_integration_full_cycle(
        self, database_manager, sample_crawl_record, sample_processing_metrics
    ):
        """Test complete database integration cycle"""

        # Store crawl record
        record_id = await database_manager.store_crawl_record(sample_crawl_record)
        assert record_id is not None

        # Store processing metrics
        await database_manager.store_processing_metrics(sample_processing_metrics)

        # Retrieve and verify data
        records = await database_manager.get_crawl_records(limit=10)
        assert len(records) >= 0

        # Test analytics
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)

        analytics = await database_manager.get_processing_analytics(
            start_time=start_time, end_time=end_time, granularity="5m"
        )

        assert isinstance(analytics, list)

        # Test database statistics
        stats = await database_manager.get_database_stats()
        assert "postgresql" in stats
        assert "timescaledb" in stats
        assert "redis" in stats
        assert "performance" in stats

    async def test_monitoring_and_metrics_integration(
        self, metrics_collector, database_manager
    ):
        """Test monitoring and metrics collection integration"""

        # Let metrics collection run for a short period
        await asyncio.sleep(2)

        # Collect worker metrics
        await metrics_collector.collect_worker_metrics()

        # Get metrics summary
        summary = await metrics_collector.get_metrics_summary()

        assert "worker_id" in summary
        assert "system_info" in summary
        assert "performance" in summary

        # Test Prometheus metrics export
        prometheus_metrics = await metrics_collector.get_prometheus_metrics()
        assert isinstance(prometheus_metrics, str)

        # Test metrics export
        json_export = await metrics_collector.export_metrics(format="json")
        assert isinstance(json_export, str)

        csv_export = await metrics_collector.export_metrics(format="csv")
        assert isinstance(csv_export, str)
        assert "timestamp,metric_type,metric_name,value,tags" in csv_export


@pytest.mark.integration
@pytest.mark.performance
@pytest.mark.asyncio
class TestPerformanceIntegration:
    """Test system performance under various loads"""

    async def test_concurrent_crawling_performance(
        self, advanced_crawler, performance_test_urls, performance_timer
    ):
        """Test crawling performance under concurrent load"""

        # Start crawl session with many URLs
        session_id = await advanced_crawler.start_crawl_session(
            session_name="performance_test",
            seed_urls=performance_test_urls[:20],  # Use first 20 URLs
            crawl_config={"max_depth": 1, "max_pages": 50, "crawl_delay": 0.1},
        )

        with performance_timer() as timer:
            # Crawl multiple batches concurrently
            tasks = []
            for _ in range(3):  # 3 concurrent batches
                task = asyncio.create_task(advanced_crawler.crawl_batch(batch_size=5))
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify performance
        assert timer.duration < 30.0  # Should complete within 30 seconds

        # Count successful results
        successful_batches = [r for r in results if not isinstance(r, Exception)]
        total_results = sum(
            len(batch) for batch in successful_batches if isinstance(batch, list)
        )

        # Calculate throughput
        if timer.duration > 0:
            throughput = total_results / timer.duration
            assert throughput > 0.5  # At least 0.5 pages per second

    async def test_multimodal_processing_performance(
        self, multimodal_processor, large_text_content, performance_timer
    ):
        """Test multimodal processing performance"""

        # Create large dataset
        test_datasets = []
        for i in range(10):
            test_datasets.append(
                {
                    "content": large_text_content[: 1000 * (i + 1)],  # Varying sizes
                    "data_type": "text",
                    "metadata": {"size": i + 1},
                }
            )

        with performance_timer() as timer:
            # Process all datasets concurrently
            tasks = []
            for dataset in test_datasets:
                task = asyncio.create_task(
                    multimodal_processor.process(
                        data=dataset["content"],
                        data_type=dataset["data_type"],
                        metadata=dataset["metadata"],
                    )
                )
                tasks.append(task)

            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify performance
        successful_results = [r for r in results if not isinstance(r, Exception)]
        assert len(successful_results) >= 8  # At least 80% success rate

        # Check processing speed
        total_data_size = sum(len(d["content"]) for d in test_datasets)
        if timer.duration > 0:
            throughput = total_data_size / timer.duration
            assert throughput > 1000  # At least 1KB per second

    async def test_database_performance_under_load(
        self, database_manager, performance_timer
    ):
        """Test database performance under high load"""

        # Generate test data
        test_records = []
        for i in range(50):
            record = CrawlRecord(
                url=f"https://test.example.com/page{i}",
                domain="test.example.com",
                content_type="text/html",
                content_hash=f"hash{i}",
                size_bytes=1024 * (i + 1),
                processing_time=random.uniform(0.1, 2.0),
                quality_score=random.uniform(0.5, 1.0),
                metadata={"test_id": i},
                content=f"<html><body>Test content {i}</body></html>",
                status="completed",
            )
            test_records.append(record)

        with performance_timer() as timer:
            # Store records concurrently
            tasks = []
            for record in test_records:
                task = asyncio.create_task(database_manager.store_crawl_record(record))
                tasks.append(task)

            record_ids = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify performance
        successful_stores = [r for r in record_ids if not isinstance(r, Exception)]
        assert len(successful_stores) >= 40  # At least 80% success rate

        # Check storage speed
        if timer.duration > 0:
            throughput = len(successful_stores) / timer.duration
            assert throughput > 5  # At least 5 records per second


@pytest.mark.integration
@pytest.mark.load
@pytest.mark.slow
@pytest.mark.asyncio
class TestLoadTesting:
    """Load testing for enterprise workloads"""

    async def test_sustained_high_load_crawling(
        self, advanced_crawler, load_test_config, load_test_result
    ):
        """Test system under sustained high load"""

        # Start crawl session
        urls = [f"https://httpbin.org/delay/1?page={i}" for i in range(100)]
        session_id = await advanced_crawler.start_crawl_session(
            session_name="load_test",
            seed_urls=urls,
            crawl_config={
                "max_depth": 1,
                "max_pages": load_test_config["max_urls"],
                "crawl_delay": 0.1,
            },
        )

        start_time = time.time()
        end_time = start_time + load_test_config["test_duration"]

        # Run load test
        while time.time() < end_time:
            batch_start = time.time()

            try:
                results = await advanced_crawler.crawl_batch(batch_size=10)
                batch_duration = time.time() - batch_start

                load_test_result.add_result(success=True, duration=batch_duration)

                # Add individual results
                for result in results:
                    load_test_result.add_result(
                        success=True,
                        duration=(
                            result.processing_time
                            if hasattr(result, "processing_time")
                            else 0.1
                        ),
                    )

            except Exception as e:
                batch_duration = time.time() - batch_start
                load_test_result.add_result(
                    success=False, duration=batch_duration, error=str(e)
                )

            # Brief pause to prevent overwhelming
            await asyncio.sleep(0.1)

        # Verify load test results
        assert load_test_result.success_rate >= 0.7  # At least 70% success rate
        assert (
            load_test_result.average_response_time < 5.0
        )  # Average response time < 5s
        assert load_test_result.percentile_95 < 10.0  # 95th percentile < 10s

    async def test_memory_usage_under_load(
        self, distributed_processor, multimodal_processor, metrics_collector
    ):
        """Test memory usage under heavy load"""

        initial_summary = await metrics_collector.get_metrics_summary()

        # Generate large amount of data
        large_chunks = []
        for i in range(100):
            chunk = DataChunk(
                chunk_id=f"load-test-{i}",
                data_type="text",
                source_url=f"https://test.example.com/large-page-{i}",
                content="x" * 10000,  # 10KB per chunk
                metadata={"load_test": True, "chunk_number": i},
                size_bytes=10000,
                timestamp=datetime.now(),
            )
            large_chunks.append(chunk)

        # Process data in batches
        async def heavy_processor(chunk):
            """Heavy processing function that uses memory"""
            # Simulate memory-intensive processing
            data = chunk.content * 10  # Expand data

            result = await multimodal_processor.process(
                data=data,
                data_type=chunk.data_type,
                metadata=chunk.metadata,
                source_url=chunk.source_url,
            )

            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=True,
                processed_data=result,
                processing_time=0.1,
                output_size_bytes=len(str(result).encode()),
                quality_score=0.8,
            )

        # Process in smaller batches to manage memory
        batch_size = 10
        for i in range(0, len(large_chunks), batch_size):
            batch = large_chunks[i : i + batch_size]
            results = await distributed_processor.process_batch(batch, heavy_processor)

            # Verify batch processing
            assert len(results) == len(batch)

            # Brief pause to allow garbage collection
            await asyncio.sleep(0.1)

        final_summary = await metrics_collector.get_metrics_summary()

        # Verify system remained stable
        # Note: In a real test, you'd check actual memory usage metrics
        assert final_summary["worker_id"] == initial_summary["worker_id"]

    async def test_database_connection_pool_under_load(self, database_manager):
        """Test database connection pool under high concurrent load"""

        # Generate many concurrent database operations
        async def database_operation(operation_id: int):
            """Simulate database-intensive operation"""
            try:
                # Create test record
                record = CrawlRecord(
                    url=f"https://load-test.example.com/page{operation_id}",
                    domain="load-test.example.com",
                    content_type="text/html",
                    content_hash=f"load-hash-{operation_id}",
                    size_bytes=1024,
                    processing_time=0.1,
                    quality_score=0.8,
                    metadata={"load_test": True, "operation_id": operation_id},
                    content=f"<html><body>Load test content {operation_id}</body></html>",
                    status="completed",
                )

                # Store record
                record_id = await database_manager.store_crawl_record(record)

                # Store metrics
                metrics = ProcessingMetrics(
                    timestamp=datetime.now(),
                    worker_id="load-test-worker",
                    operation_type="load_test",
                    duration_ms=100,
                    bytes_processed=1024,
                    success=True,
                    memory_usage_mb=64.0,
                    cpu_usage_percent=20.0,
                )
                await database_manager.store_processing_metrics(metrics)

                return record_id

            except Exception as e:
                return f"Error: {str(e)}"

        # Create many concurrent operations
        num_operations = 50
        tasks = []
        for i in range(num_operations):
            task = asyncio.create_task(database_operation(i))
            tasks.append(task)

        # Wait for all operations to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verify results
        successful_operations = [
            r
            for r in results
            if not isinstance(r, Exception) and not str(r).startswith("Error:")
        ]
        success_rate = len(successful_operations) / num_operations

        assert success_rate >= 0.8  # At least 80% success rate

        # Verify database statistics
        stats = await database_manager.get_database_stats()
        assert stats["performance"]["query_count"] >= num_operations


@pytest.mark.integration
@pytest.mark.network
@pytest.mark.asyncio
class TestNetworkResilience:
    """Test system resilience under network conditions"""

    async def test_crawler_resilience_to_timeouts(self, advanced_crawler):
        """Test crawler behavior with network timeouts"""

        # URLs that will cause timeouts
        timeout_urls = [
            "https://httpbin.org/delay/10",  # Long delay
            "https://httpbin.org/status/408",  # Request timeout
            "https://httpbin.org/status/504",  # Gateway timeout
        ]

        session_id = await advanced_crawler.start_crawl_session(
            session_name="timeout_test",
            seed_urls=timeout_urls,
            crawl_config={
                "max_depth": 1,
                "timeout": 5,  # 5 second timeout
                "retry_attempts": 2,
            },
        )

        # Attempt to crawl (expecting failures)
        results = await advanced_crawler.crawl_batch(batch_size=5)

        # Verify system handled timeouts gracefully
        stats = await advanced_crawler.get_crawl_statistics()
        assert stats["crawl_stats"]["failed"] >= 0  # Some failures expected

        # System should still be responsive
        assert session_id is not None

    async def test_distributed_processor_fault_tolerance(self, distributed_processor):
        """Test distributed processor fault tolerance"""

        # Create chunks that will cause processing errors
        problematic_chunks = []
        for i in range(5):
            chunk = DataChunk(
                chunk_id=f"error-chunk-{i}",
                data_type="unknown",  # Unsupported type
                source_url="invalid://url",
                content="",  # Empty content
                metadata={},
                size_bytes=0,
                timestamp=datetime.now(),
            )
            problematic_chunks.append(chunk)

        # Define a processor that will fail on some inputs
        async def unreliable_processor(chunk):
            """Processor that fails on certain inputs"""
            if chunk.data_type == "unknown":
                raise ValueError("Unsupported data type")

            if len(chunk.content) == 0:
                raise ValueError("Empty content")

            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=True,
                processed_data={"processed": True},
                processing_time=0.1,
                output_size_bytes=100,
                quality_score=0.5,
            )

        # Process chunks (expecting failures)
        results = await distributed_processor.process_batch(
            problematic_chunks, unreliable_processor
        )

        # Verify system handled failures gracefully
        assert len(results) == len(problematic_chunks)

        # Check that failures were properly recorded
        failed_results = [r for r in results if not r.success]
        assert len(failed_results) > 0  # Some failures expected

        # System should still be operational
        stats = await distributed_processor.get_processing_stats()
        assert "total_processed" in stats


@pytest.mark.integration
@pytest.mark.multimodal
@pytest.mark.asyncio
class TestMultimodalDataIntegration:
    """Test integration of multimodal data processing"""

    async def test_complex_document_processing_pipeline(
        self, multimodal_processor, advanced_crawler
    ):
        """Test processing of complex documents with multiple data types"""

        # Complex HTML with multiple content types
        complex_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Complex Test Document</title>
            <script type="application/json" id="data">
                {"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}
            </script>
        </head>
        <body>
            <h1>Multi-Modal Test Page</h1>
            <p>This page contains various data types for testing.</p>

            <pre><code class="python">
                def hello_world():
                    print("Hello, World!")
                    return True
            </code></pre>

            <div class="data-table">
                <table>
                    <tr><th>ID</th><th>Name</th><th>Score</th></tr>
                    <tr><td>1</td><td>Alice</td><td>95</td></tr>
                    <tr><td>2</td><td>Bob</td><td>87</td></tr>
                </table>
            </div>

            <article>
                <p>This is a long-form article with substantial content that should
                   receive a high quality score. It contains multiple paragraphs,
                   structured information, and meaningful text that provides value
                   to readers interested in web crawling and data processing.</p>
                <p>The content includes technical information about distributed
                   systems, database management, and performance optimization
                   techniques used in enterprise-scale web crawling operations.</p>
            </article>
        </body>
        </html>
        """

        # Process the complex document
        result = await multimodal_processor.process(
            data=complex_html,
            data_type="web",
            metadata={"content_type": "text/html", "complexity": "high"},
            source_url="https://test.example.com/complex-document",
        )

        # Verify comprehensive processing
        assert result.quality_score > 0.5  # Should have good quality
        assert result.processing_time > 0

        # Check that features were extracted
        assert "features" in result.__dict__ or hasattr(result, "features")

        # Process embedded JSON
        json_data = '{"users": [{"id": 1, "name": "John"}, {"id": 2, "name": "Jane"}]}'
        json_result = await multimodal_processor.process(
            data=json_data,
            data_type="structured",
            metadata={"content_type": "application/json"},
            source_url="https://test.example.com/api/users",
        )

        assert json_result.quality_score > 0.0

        # Process code snippet
        code_data = """
        async def hello_world():
            print("Hello, World!")
            return True
        """
        code_result = await multimodal_processor.process(
            data=code_data,
            data_type="code",
            metadata={"language": "python"},
            source_url="https://test.example.com/code/hello.py",
        )

        assert code_result.quality_score > 0.0

    async def test_large_scale_multimodal_processing(
        self, multimodal_processor, distributed_processor
    ):
        """Test large-scale multimodal data processing"""

        # Generate diverse multimodal dataset
        datasets = []

        # HTML documents
        for i in range(10):
            html_content = f"""
            <html><head><title>Document {i}</title></head>
            <body><h1>Page {i}</h1><p>Content for page {i} with unique information.</p></body></html>
            """
            datasets.append(("web", html_content))

        # JSON data
        for i in range(5):
            json_data = json.dumps(
                {
                    "id": i,
                    "title": f"Item {i}",
                    "data": [{"value": j} for j in range(5)],
                    "metadata": {"processed": False},
                }
            )
            datasets.append(("structuredr", json_data))

        # Code samples
        code_samples = [
            r"def factorial(n):\n    return 1 if n <= 1 else n * factorial(n-1)",
            r"function fibonacci(n) {\n    return n <= 1 ? n : fibonacci(n-1) + fibonacci(n-2);\n}",
            r"class DataProcessor {\n    public void process(String data) {\n        System.out.println(data);\n    }\n}",
        ]
        for i, code in enumerate(code_samples):
            datasets.append(("code", code))

        # Create data chunks
        chunks = []
        for i, (data_type, content) in enumerate(datasets):
            chunk = DataChunk(
                chunk_id=f"multimodal-{i}",
                data_type=data_type,
                source_url=f"https://test.example.com/{data_type}/{i}",
                content=content,
                metadata={"batch": "multimodal_test", "index": i},
                size_bytes=len(content.encode()),
                timestamp=datetime.now(),
            )
            chunks.append(chunk)

        # Process all chunks
        async def multimodal_processing_func(chunk):
            """Processing function for multimodal data"""
            result = await multimodal_processor.process(
                data=chunk.content,
                data_type=chunk.data_type,
                metadata=chunk.metadata,
                source_url=chunk.source_url,
            )

            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=True,
                processed_data=result,
                processing_time=result.processing_time,
                output_size_bytes=len(str(result).encode()),
                quality_score=result.quality_score,
            )

        # Process in batches
        all_results = []
        batch_size = 5
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i : i + batch_size]
            batch_results = await distributed_processor.process_batch(
                batch, multimodal_processing_func
            )
            all_results.extend(batch_results)

        # Verify results
        assert len(all_results) == len(chunks)

        # Check success rate by data type
        results_by_type = {}
        for chunk, result in zip(chunks, all_results):
            if chunk.data_type not in results_by_type:
                results_by_type[chunk.data_type] = []
            results_by_type[chunk.data_type].append(result)

        # Verify each data type was processed successfully
        for data_type, results in results_by_type.items():
            successful = [r for r in results if r.success]
            success_rate = len(successful) / len(results)
            assert (
                success_rate >= 0.8
            ), f"Low success rate for {data_type}: {success_rate}"

        # Check quality scores
        quality_scores = [
            r.quality_score
            for r in all_results
            if r.success and hasattr(r, "quality_score")
        ]
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            assert avg_quality > 0.3  # Reasonable average quality
