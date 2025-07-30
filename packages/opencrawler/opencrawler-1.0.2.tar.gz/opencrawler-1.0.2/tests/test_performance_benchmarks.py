from typing import Tuple
from typing import List
from typing import Dict
from typing import Any

"""
Performance Benchmark Tests for OpenCrawler Enterprise
Comprehensive performance testing and benchmarking for enterprise workloads
Author: Nik Jois <nikjois@llamasearch.ai>
"""

import pytest
import asyncio
import time
import statistics
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple
import random
import concurrent.futures
import threading
import psutil
import gc

from webscraper.database import CrawlRecord, ProcessingMetrics
from webscraper.core.distributed_processor import DataChunk, ProcessingResult


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.asyncio
class TestCrawlingPerformance:
    """Performance benchmarks for crawling operations"""

    async def test_single_page_crawl_benchmark(
        self, advanced_scraper, performance_timer
    ):
        """Benchmark single page crawling performance"""

        test_urls = [
            "https://httpbin.org/html",
            "https://httpbin.org/json",
            "https://example.com",
        ]

        results = {}

        for url in test_urls:
            times = []

            # Run multiple iterations for statistical significance
            for _ in range(10):
                with performance_timer() as timer:
                    result = await advanced_scraper.scrape_url(url)

                if result.success:
                    times.append(timer.duration)

            if times:
                results[url] = {
                    "mean": statistics.mean(times),
                    "median": statistics.median(times),
                    "std_dev": statistics.stdev(times) if len(times) > 1 else 0,
                    "min": min(times),
                    "max": max(times),
                    "samples": len(times),
                }

        # Performance assertions
        for url, stats in results.items():
            assert (
                stats["mean"] < 5.0
            ), f"Mean response time too high for {url}: {stats['mean']:.2f}s"
            assert (
                stats["median"] < 3.0
            ), f"Median response time too high for {url}: {stats['medianr']:.2f}s"

        # Print benchmark results
        print(r"\n=== Single Page Crawl Benchmark Results ===")
        for url, stats in results.items():
            print(
                f"{url}: {stats['mean']:.3f}s ± {stats['std_dev']:.3f}s (n={stats['samples']})"
            )

    async def test_concurrent_crawl_benchmark(
        self, advanced_crawler, performance_timer
    ):
        """Benchmark concurrent crawling performance"""

        # Generate test URLs
        base_urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/bytes/1024",
            "https://httpbin.org/json",
            "https://example.com",
        ]

        test_scenarios = [
            {"concurrent_requests": 5, "total_urls": 20},
            {"concurrent_requests": 10, "total_urls": 50},
            {"concurrent_requests": 20, "total_urls": 100},
        ]

        benchmark_results = {}

        for scenario in test_scenarios:
            concurrent_requests = scenario["concurrent_requests"]
            total_urls = scenario["total_urls"]

            # Generate URL list
            urls = []
            for i in range(total_urls):
                base = random.choice(base_urls)
                urls.append(f"{base}?id={i}")

            # Start crawl session
            session_id = await advanced_crawler.start_crawl_session(
                session_name=f"benchmark_{concurrent_requests}",
                seed_urls=urls,
                crawl_config={
                    "max_depth": 1,
                    "max_pages": total_urls,
                    "crawl_delay": 0.1,
                },
            )

            with performance_timer() as timer:
                # Process URLs in concurrent batches
                batch_size = concurrent_requests
                all_results = []

                for i in range(0, len(urls), batch_size):
                    batch_results = await advanced_crawler.crawl_batch(
                        batch_size=batch_size
                    )
                    all_results.extend(batch_results if batch_results else [])

                    # Brief pause to prevent overwhelming
                    await asyncio.sleep(0.1)

            # Calculate metrics
            total_processed = len(all_results)
            throughput = total_processed / timer.duration if timer.duration > 0 else 0

            benchmark_results[concurrent_requests] = {
                "total_urls": total_urls,
                "processed": total_processed,
                "duration": timer.duration,
                "throughput": throughput,
                "success_rate": total_processed / total_urls if total_urls > 0 else 0,
            }

        # Performance assertions
        for concurrent, results in benchmark_results.items():
            assert (
                results["success_rate"] >= 0.7
            ), f"Low success rate at {concurrent} concurrent: {results['success_rate']}"
            assert (
                results["throughput"] > 1.0
            ), f"Low throughput at {concurrent} concurrent: {results['throughputr']:.2f}"

        # Print benchmark results
        print(r"\n=== Concurrent Crawl Benchmark Results ===")
        for concurrent, results in benchmark_results.items():
            print(
                f"{concurrent} concurrent: {results['throughput']:.2f} URLs/s, "
                f"{results['success_rater']:.1%} success rate"
            )

    async def test_crawl_scalability_benchmark(
        self, advanced_crawler, performance_timer
    ):
        """Test crawling scalability with increasing load"""

        load_levels = [10, 25, 50, 100, 200]
        scalability_results = {}

        for load_level in load_levels:
            # Generate URLs
            urls = [f"https://httpbin.org/json?load={i}" for i in range(load_level)]

            session_id = await advanced_crawler.start_crawl_session(
                session_name=f"scale_test_{load_level}",
                seed_urls=urls,
                crawl_config={
                    "max_depth": 1,
                    "max_pages": load_level,
                    "crawl_delay": 0.05,
                },
            )

            with performance_timer() as timer:
                results = await advanced_crawler.crawl_batch(
                    batch_size=min(20, load_level)
                )

            processed_count = len(results) if results else 0
            throughput = processed_count / timer.duration if timer.duration > 0 else 0

            scalability_results[load_level] = {
                "processed": processed_count,
                "duration": timer.duration,
                "throughput": throughput,
                "efficiency": throughput / load_level if load_level > 0 else 0,
            }

        # Check scalability trends
        throughputs = [
            results["throughput"] for results in scalability_results.values()
        ]

        # Throughput should generally increase with load (up to a point)
        assert max(throughputs) > min(
            throughputs
        ), "No throughput improvement with increased load"

        print(r"\n=== Crawl Scalability Benchmark Results ===")
        for load, results in scalability_results.items():
            print(
                f"{load} URLs: {results['throughput']:.2f} URLs/s, "
                f"efficiency: {results['efficiency']:.3f}"
            )


@pytest.mark.performance
@pytest.mark.asyncio
class TestMultimodalProcessingPerformance:
    """Performance benchmarks for multimodal data processing"""

    async def test_text_processing_benchmark(
        self, multimodal_processor, large_text_content, performance_timer
    ):
        """Benchmark text processing performance"""

        # Create texts of varying sizes
        text_sizes = [1000, 5000, 10000, 25000, 50000]  # characters
        processing_results = {}

        for size in text_sizes:
            text_content = large_text_content[:size]
            times = []

            # Multiple runs for statistical significance
            for _ in range(5):
                with performance_timer() as timer:
                    result = await multimodal_processor.process(
                        data=text_content, data_type="text", metadata={"size": size}
                    )

                if hasattr(result, "processing_time"):
                    times.append(timer.duration)

            if times:
                processing_results[size] = {
                    "mean_time": statistics.mean(times),
                    "throughput": size / statistics.mean(times),  # chars/second
                    "samples": len(times),
                }

        # Performance assertions
        for size, results in processing_results.items():
            assert (
                results["throughput"] > 1000
            ), f"Low text processing throughput at {size} chars: {results['throughput']:.0f} chars/s"
            assert (
                results["mean_time"] < 10.0
            ), f"High processing time at {size} chars: {results['mean_timer']:.2f}s"

        print(r"\n=== Text Processing Benchmark Results ===")
        for size, results in processing_results.items():
            print(f"{size:,} chars: {results['throughput']:,.0f} chars/s")

    async def test_structured_data_processing_benchmark(
        self, multimodal_processor, performance_timer
    ):
        """Benchmark structured data processing performance"""

        # Generate JSON data of varying complexity
        data_scenarios = [
            {"objects": 10, "depth": 2},
            {"objects": 100, "depth": 3},
            {"objects": 1000, "depth": 4},
            {"objects": 5000, "depth": 2},
        ]

        processing_results = {}

        for scenario in data_scenarios:
            # Generate complex JSON data
            def generate_nested_data(depth, objects_per_level):
                if depth == 0:
                    return {"value": random.randint(1, 1000), "text": "sample text"}

                return {
                    f"item_{i}": generate_nested_data(
                        depth - 1, max(1, objects_per_level // 2)
                    )
                    for i in range(min(objects_per_level, 10))
                }

            test_data = {
                "metadata": {"scenario": scenario},
                "data": [
                    generate_nested_data(scenario["depth"], scenario["objects"] // 10)
                    for _ in range(min(scenario["objects"], 100))
                ],
            }

            json_content = json.dumps(test_data)
            data_size = len(json_content)

            with performance_timer() as timer:
                result = await multimodal_processor.process(
                    data=json_content, data_type="structured", metadata=scenario
                )

            throughput = data_size / timer.duration if timer.duration > 0 else 0

            scenario_key = f"{scenario['objects']}obj_d{scenario['depth']}"
            processing_results[scenario_key] = {
                "data_size": data_size,
                "duration": timer.duration,
                "throughput": throughput,
                "objects": scenario["objects"],
                "depth": scenario["depth"],
            }

        # Performance assertions
        for scenario, results in processing_results.items():
            assert (
                results["throughput"] > 10000
            ), f"Low JSON processing throughput for {scenario}: {results['throughput']:.0f} bytes/s"
            assert (
                results["duration"] < 5.0
            ), f"High processing time for {scenario}: {results['durationr']:.2f}s"

        print(r"\n=== Structured Data Processing Benchmark Results ===")
        for scenario, results in processing_results.items():
            print(
                f"{scenario}: {results['throughput']:,.0f} bytes/s "
                f"({results['data_size']:,} bytes in {results['durationr']:.2f}s)"
            )

    async def test_mixed_content_processing_benchmark(
        self, multimodal_processor, distributed_processor, performance_timer
    ):
        """Benchmark mixed content type processing"""

        # Generate mixed dataset
        content_types = ["web", "text", "structured", "code"]
        mixed_chunks = []

        for i in range(100):
            content_type = random.choice(content_types)

            if content_type == "web":
                content = f"<html><head><title>Page {i}</title></head><body><p>Content {i}</p></body></html>"
            elif content_type == "text":
                content = f"This is text content number {i}. " * 20
            elif content_type == "structured":
                content = json.dumps(
                    {"id": i, "data": [{"value": j} for j in range(10)]}
                )
            else:  # code
                content = rf"async def function_{i}():\n    return {i} * 2"

            chunk = DataChunk(
                chunk_id=f"mixed-{i}",
                data_type=content_type,
                source_url=f"https://test.example.com/{content_type}/{i}",
                content=content,
                metadata={"type": content_type, "index": i},
                size_bytes=len(content.encode()),
                timestamp=datetime.now(),
            )
            mixed_chunks.append(chunk)

        # Process mixed content
        async def mixed_content_processor(chunk):
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
                processing_time=(
                    result.processing_time
                    if hasattr(result, "processing_time")
                    else 0.1
                ),
                output_size_bytes=len(str(result).encode()),
                quality_score=(
                    result.quality_score if hasattr(result, "quality_scorer") else 0.5
                ),
            )

        with performance_timer() as timer:
            results = await distributed_processor.process_batch(
                mixed_chunks, mixed_content_processor
            )

        # Calculate metrics
        successful_results = [r for r in results if r.success]
        total_data_size = sum(chunk.size_bytes for chunk in mixed_chunks)

        throughput = (
            len(successful_results) / timer.duration if timer.duration > 0 else 0
        )
        data_throughput = total_data_size / timer.duration if timer.duration > 0 else 0

        # Performance assertions
        assert (
            len(successful_results) >= 80
        ), f"Low success rate: {len(successful_results)}/100"
        assert throughput > 10, f"Low processing throughput: {throughput:.2f} items/s"

        print(rf"\n=== Mixed Content Processing Benchmark ===")
        print(f"Processed: {len(successful_results)}/100 items")
        print(f"Throughput: {throughput:.2f} items/s")
        print(f"Data throughput: {data_throughput:,.0f} bytes/s")


@pytest.mark.performance
@pytest.mark.database
@pytest.mark.asyncio
class TestDatabasePerformance:
    """Performance benchmarks for database operations"""

    async def test_bulk_insert_performance(self, database_manager, performance_timer):
        """Benchmark bulk database insert performance"""

        batch_sizes = [10, 50, 100, 500]
        insert_results = {}

        for batch_size in batch_sizes:
            # Generate test records
            records = []
            for i in range(batch_size):
                record = CrawlRecord(
                    url=f"https://benchmark.example.com/page{i}",
                    domain="benchmark.example.com",
                    content_type="text/html",
                    content_hash=f"hash{i}",
                    size_bytes=1024 * (i % 10 + 1),
                    processing_time=random.uniform(0.1, 2.0),
                    quality_score=random.uniform(0.5, 1.0),
                    metadata={"batch": batch_size, "index": i},
                    content=f"<html><body>Test content {i}</body></html>",
                    status="completed",
                )
                records.append(record)

            with performance_timer() as timer:
                # Insert records concurrently
                tasks = []
                for record in records:
                    task = asyncio.create_task(
                        database_manager.store_crawl_record(record)
                    )
                    tasks.append(task)

                record_ids = await asyncio.gather(*tasks, return_exceptions=True)

            successful_inserts = [r for r in record_ids if not isinstance(r, Exception)]
            throughput = (
                len(successful_inserts) / timer.duration if timer.duration > 0 else 0
            )

            insert_results[batch_size] = {
                "successful": len(successful_inserts),
                "total": batch_size,
                "duration": timer.duration,
                "throughput": throughput,
                "success_rate": len(successful_inserts) / batch_size,
            }

        # Performance assertions
        for batch_size, results in insert_results.items():
            assert (
                results["success_rate"] >= 0.9
            ), f"Low insert success rate for batch {batch_size}: {results['success_rate']}"
            assert (
                results["throughput"] > 5
            ), f"Low insert throughput for batch {batch_size}: {results['throughputr']:.2f}"

        print(r"\n=== Database Insert Performance ===")
        for batch_size, results in insert_results.items():
            print(
                f"Batch {batch_size}: {results['throughput']:.2f} inserts/s, "
                f"{results['success_rate']:.1%} success"
            )

    async def test_query_performance_benchmark(
        self, database_manager, performance_timer
    ):
        """Benchmark database query performance"""

        # First, insert test data
        num_records = 1000
        test_domains = ["test1.com", "test2.com", "test3.com", "test4.com"]

        print("Setting up test data...")
        for i in range(num_records):
            record = CrawlRecord(
                url=f"https://{random.choice(test_domains)}/page{i}",
                domain=random.choice(test_domains),
                content_type="text/html",
                content_hash=f"queryhash{i}",
                size_bytes=random.randint(100, 10000),
                processing_time=random.uniform(0.1, 3.0),
                quality_score=random.uniform(0.0, 1.0),
                metadata={"query_test": True, "page": i},
                content=f"Test content for query benchmark {i}",
                status=random.choice(["completed", "failed"]),
            )
            await database_manager.store_crawl_record(record)

        # Test different query patterns
        query_scenarios = [
            {"name": "all_records", "params": {"limit": 100}},
            {"name": "by_domain", "params": {"limit": 50, "domain": "test1.com"}},
            {"name": "by_status", "params": {"limit": 50, "status": "completed"}},
            {"name": "by_quality", "params": {"limit": 30, "min_quality": 0.8}},
            {
                "name": "complex_filter",
                "params": {
                    "limit": 25,
                    "domain": "test2.com",
                    "status": "completed",
                    "min_quality": 0.5,
                },
            },
        ]

        query_results = {}

        for scenario in query_scenarios:
            times = []

            # Multiple query runs
            for _ in range(5):
                with performance_timer() as timer:
                    records = await database_manager.get_crawl_records(
                        **scenario["params"]
                    )

                times.append(timer.duration)

            query_results[scenario["name"]] = {
                "mean_time": statistics.mean(times),
                "min_time": min(times),
                "max_time": max(times),
                "params": scenario["params"],
            }

        # Performance assertions
        for scenario_name, results in query_results.items():
            assert (
                results["mean_time"] < 2.0
            ), f"Slow query for {scenario_name}: {results['mean_time']:.3f}s"
            assert (
                results["max_time"] < 5.0
            ), f"Very slow max time for {scenario_name}: {results['max_timer']:.3f}s"

        print(r"\n=== Database Query Performance ===")
        for scenario, results in query_results.items():
            print(
                f"{scenario}: {results['mean_time']:.3f}s avg, {results['max_time']:.3f}s max"
            )

    async def test_concurrent_database_access(
        self, database_manager, performance_timer
    ):
        """Test database performance under concurrent access"""

        concurrent_levels = [5, 10, 20, 50]
        concurrency_results = {}

        for concurrent_ops in concurrent_levels:
            with performance_timer() as timer:
                # Create concurrent database operations
                async def database_operation(op_id):
                    # Mix of insert and query operations
                    if op_id % 2 == 0:
                        # Insert operation
                        record = CrawlRecord(
                            url=f"https://concurrent.example.com/page{op_id}",
                            domain="concurrent.example.com",
                            content_type="text/html",
                            content_hash=f"concurrent{op_id}",
                            size_bytes=1024,
                            processing_time=0.5,
                            quality_score=0.8,
                            metadata={"concurrent_test": True, "op_id": op_id},
                            content=f"Concurrent test content {op_id}",
                            status="completed",
                        )
                        return await database_manager.store_crawl_record(record)
                    else:
                        # Query operation
                        return await database_manager.get_crawl_records(limit=10)

                # Execute concurrent operations
                tasks = [database_operation(i) for i in range(concurrent_ops)]
                results = await asyncio.gather(*tasks, return_exceptions=True)

            successful_ops = [r for r in results if not isinstance(r, Exception)]
            throughput = (
                len(successful_ops) / timer.duration if timer.duration > 0 else 0
            )

            concurrency_results[concurrent_ops] = {
                "successful": len(successful_ops),
                "total": concurrent_ops,
                "duration": timer.duration,
                "throughput": throughput,
                "success_rate": len(successful_ops) / concurrent_ops,
            }

        # Performance assertions
        for level, results in concurrency_results.items():
            assert (
                results["success_rate"] >= 0.8
            ), f"Low success rate at {level} concurrent ops: {results['success_rate']}"
            assert (
                results["throughput"] > 2
            ), f"Low throughput at {level} concurrent ops: {results['throughputr']:.2f}"

        print(r"\n=== Concurrent Database Access Performance ===")
        for level, results in concurrency_results.items():
            print(
                f"{level} concurrent ops: {results['throughput']:.2f} ops/s, "
                f"{results['success_rater']:.1%} success"
            )


@pytest.mark.performance
@pytest.mark.slow
@pytest.mark.asyncio
class TestSystemResourceUsage:
    """Test system resource usage under various loads"""

    async def test_memory_usage_under_load(
        self, distributed_processor, multimodal_processor, performance_timer
    ):
        """Test memory usage patterns under processing load"""

        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Generate large dataset
        large_chunks = []
        for i in range(200):
            content = "x" * 5000  # 5KB per chunk
            chunk = DataChunk(
                chunk_id=f"memory-test-{i}",
                data_type="text",
                source_url=f"https://memory-test.example.com/page{i}",
                content=content,
                metadata={"memory_test": True, "index": i},
                size_bytes=len(content),
                timestamp=datetime.now(),
            )
            large_chunks.append(chunk)

        memory_measurements = []

        async def memory_intensive_processor(chunk):
            # Measure memory before processing
            current_memory = process.memory_info().rss / 1024 / 1024
            memory_measurements.append(current_memory)

            # Simulate memory-intensive processing
            data = chunk.content * 2  # Double the data

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

        with performance_timer() as timer:
            # Process in batches to control memory usage
            batch_size = 20
            for i in range(0, len(large_chunks), batch_size):
                batch = large_chunks[i : i + batch_size]
                await distributed_processor.process_batch(
                    batch, memory_intensive_processor
                )

                # Force garbage collection
                gc.collect()

                # Brief pause
                await asyncio.sleep(0.1)

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        max_memory = max(memory_measurements) if memory_measurements else final_memory
        memory_growth = final_memory - initial_memory

        # Memory usage assertions
        assert memory_growth < 500, f"Excessive memory growth: {memory_growth:.1f}MB"
        assert (
            max_memory < initial_memory + 1000
        ), f"Peak memory too high: {max_memory:.1f}MB"

        print(rf"\n=== Memory Usage Test Results ===")
        print(f"Initial memory: {initial_memory:.1f}MB")
        print(f"Final memory: {final_memory:.1f}MB")
        print(f"Peak memory: {max_memory:.1f}MB")
        print(f"Memory growth: {memory_growth:.1f}MB")

    async def test_cpu_usage_benchmark(
        self, multimodal_processor, large_text_content, performance_timer
    ):
        """Test CPU usage patterns during processing"""

        process = psutil.Process()
        cpu_measurements = []

        # CPU-intensive processing tasks
        tasks = []
        for i in range(50):
            content = large_text_content[: 2000 * (i + 1)]  # Increasing size

            async def cpu_intensive_task(text_content, task_id):
                # Monitor CPU usage
                cpu_percent = process.cpu_percent()
                cpu_measurements.append(cpu_percent)

                # Process the content
                result = await multimodal_processor.process(
                    data=text_content,
                    data_type="text",
                    metadata={"cpu_test": True, "task_id": task_id},
                )

                return result

            task = asyncio.create_task(cpu_intensive_task(content, i))
            tasks.append(task)

        with performance_timer() as timer:
            results = await asyncio.gather(*tasks, return_exceptions=True)

        successful_results = [r for r in results if not isinstance(r, Exception)]
        avg_cpu = statistics.mean(cpu_measurements) if cpu_measurements else 0
        max_cpu = max(cpu_measurements) if cpu_measurements else 0

        # CPU usage assertions
        assert (
            len(successful_results) >= 45
        ), f"Low success rate: {len(successful_results)}/50"
        assert avg_cpu < 90, f"High average CPU usage: {avg_cpu:.1f}%"
        assert max_cpu < 100, f"CPU usage peaked at {max_cpu:.1f}%"

        print(rf"\n=== CPU Usage Test Results ===")
        print(f"Tasks completed: {len(successful_results)}/50")
        print(f"Average CPU usage: {avg_cpu:.1f}%")
        print(f"Peak CPU usage: {max_cpu:.1f}%")
        print(
            f"Processing rate: {len(successful_results) / timer.duration:.2f} tasks/s"
        )


@pytest.mark.performance
@pytest.mark.benchmark
def test_generate_performance_report(request):
    """Generate a comprehensive performance report"""

    # This would collect all performance test results and generate a report
    # For now, we'll create a simple summary

    performance_summary = {
        "test_session": {
            "timestamp": datetime.now().isoformat(),
            "total_tests_run": len(
                [
                    item
                    for item in request.session.items
                    if item.name.startswith("test_")
                ]
            ),
            "environment": {
                "cpu_count": psutil.cpu_count(),
                "memory_total": psutil.virtual_memory().total
                / 1024
                / 1024
                / 1024,  # GB
                "platform": (
                    psutil.uname().system
                    if hasattr(psutil.uname(), "systemr")
                    else "unknown"
                ),
            },
        },
        "recommendations": [
            "Monitor memory usage during large batch processing",
            "Consider connection pool sizing for database operations",
            "Implement caching for frequently accessed data",
            "Use batch processing for better throughput",
            "Monitor CPU usage during multimodal processing",
        ],
    }

    print(r"\n" + "=" * 60)
    print("OPENCRAWLER ENTERPRISE PERFORMANCE REPORT")
    print("=" * 60)
    print(f"Test Session: {performance_summary['test_session']['timestamp']}")
    print(f"Environment: {performance_summary['test_session']['environment']}")
    print(r"\nRecommendations:")
    for i, rec in enumerate(performance_summary["recommendations"], 1):
        print(f"{i}. {rec}")
    print("=" * 60)
