from typing import Optional
from typing import List
from typing import Dict
from typing import Any

"""
Distributed Worker for OpenCrawler
Handles processing tasks in a distributed environment
Author: Nik Jois <nikjois@llamasearch.ai>
"""

import asyncio
import logging
import json
import time
import os
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
import signal
import psutil
import traceback
from dataclasses import dataclass

# Add the parent directory to the path to import webscraper modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from webscraper.database import DatabaseManager, CrawlRecord, ProcessingMetrics
from webscraper.core.distributed_processor import (
    DistributedDataProcessor,
    DataChunk,
    ProcessingResult,
)
from webscraper.processors.multimodal_processor import MultiModalProcessor
from webscraper.core.advanced_scraper import AdvancedScraper
from webscraper.core.config_manager import ConfigManager
from webscraper.utils.monitoring import MetricsCollector

logger = logging.getLogger(__name__)


@dataclass
class WorkerConfig:
    """Configuration for the distributed worker"""

    worker_id: str
    concurrency: int = 100
    timeout: int = 300
    redis_url: str = "redis://localhost:6379"
    postgres_url: str = "postgresql://localhost:5432/opencrawler"
    timescale_url: str = "postgresql://localhost:5432/opencrawler_timeseries"
    max_memory_mb: int = 4096
    max_cpu_percent: float = 85.0


class DistributedWorker:
    """
    Distributed worker for processing crawling tasks

    Features:
    - Processes tasks from Redis queue
    - Handles multi-modal data processing
    - Stores results in PostgreSQL/TimescaleDB
    - Monitors resource usage
    - Supports graceful shutdown
    """

    def __init__(self, config: WorkerConfig):
        self.config = config
        self.worker_id = config.worker_id
        self.running = False
        self.shutdown_event = asyncio.Event()

        # Initialize components
        self.database_manager = None
        self.distributed_processor = None
        self.multimodal_processor = None
        self.advanced_scraper = None
        self.metrics_collector = None

        # Task tracking
        self.processed_tasks = 0
        self.failed_tasks = 0
        self.total_processing_time = 0.0
        self.start_time = datetime.now()

        # Resource monitoring
        self.process = psutil.Process()
        self.max_memory_usage = 0.0
        self.max_cpu_usage = 0.0

        # Setup signal handlers
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        logger.info(
            f"[WORKER] Received signal {signum}, initiating graceful shutdown..."
        )
        self.shutdown_event.set()

    async def initialize(self):
        """Initialize the worker and its components"""
        logger.info(f"[WORKER] Initializing worker {self.worker_id}...")

        try:
            # Load configuration
            config_manager = ConfigManager()
            app_config = config_manager.get_config()

            # Initialize database manager
            db_config = {
                "postgres": {
                    "host": os.getenv("POSTGRES_HOST", "postgres-service"),
                    "port": int(os.getenv("POSTGRES_PORT", "5432")),
                    "database": os.getenv("POSTGRES_DB", "opencrawler"),
                    "user": os.getenv("POSTGRES_USER", "opencrawler"),
                    "pool_size": 5,
                    "max_overflow": 10,
                },
                "timescaledb": {
                    "host": os.getenv(
                        "TIMESCALEDB_HOST", "postgres-timescaledb-service"
                    ),
                    "port": int(os.getenv("TIMESCALEDB_PORT", "5432")),
                    "database": os.getenv("TIMESCALEDB_DB", "opencrawler_timeseries"),
                    "user": os.getenv("TIMESCALEDB_USER", "opencrawler"),
                    "pool_size": 3,
                    "max_overflow": 5,
                },
                "redis": {
                    "host": os.getenv("REDIS_HOST", "redis-service"),
                    "port": int(os.getenv("REDIS_PORT", "6379")),
                    "db": int(os.getenv("REDIS_DB", "0")),
                    "max_connections": 20,
                },
            }

            self.database_manager = DatabaseManager(db_config)
            await self.database_manager.initialize()

            # Initialize distributed processor
            cluster_config = {
                "worker_count": 1,
                "max_concurrent_tasks": self.config.concurrency,
            }

            storage_config = {"data_path": "/data", "max_file_size": "10GB"}

            processing_config = {"timeout": self.config.timeout, "retry_attempts": 3}

            self.distributed_processor = DistributedDataProcessor(
                cluster_config, storage_config, processing_config
            )
            await self.distributed_processor.initialize()

            # Initialize multimodal processor
            multimodal_config = {
                "use_text_models": True,
                "use_vision_models": True,
                "max_file_size": "1GB",
            }

            self.multimodal_processor = MultiModalProcessor(multimodal_config)

            # Initialize advanced scraper
            scraper_config = app_config.get("scraper", {})
            self.advanced_scraper = AdvancedScraper(scraper_config)

            # Initialize metrics collector
            self.metrics_collector = MetricsCollector(
                database_manager=self.database_manager, worker_id=self.worker_id
            )

            logger.info(f"[WORKER] Worker {self.worker_id} initialized successfully")

        except Exception as e:
            logger.error(f"[WORKER] Failed to initialize worker: {e}")
            raise

    async def start(self):
        """Start the worker"""
        logger.info(f"[WORKER] Starting worker {self.worker_id}...")

        self.running = True

        # Start background tasks
        tasks = [
            asyncio.create_task(self._process_tasks()),
            asyncio.create_task(self._monitor_resources()),
            asyncio.create_task(self._collect_metrics()),
            asyncio.create_task(self._health_check()),
        ]

        try:
            # Wait for shutdown signal
            await self.shutdown_event.wait()

            logger.info(f"[WORKER] Shutdown signal received, stopping worker...")

        except Exception as e:
            logger.error(f"[WORKER] Error in worker main loop: {e}")

        finally:
            self.running = False

            # Cancel all tasks
            for task in tasks:
                task.cancel()

            # Wait for tasks to complete
            await asyncio.gather(*tasks, return_exceptions=True)

            # Cleanup
            await self.shutdown()

    async def _process_tasks(self):
        """Main task processing loop"""
        logger.info(f"[WORKER] Started task processing loop")

        while self.running:
            try:
                # Get task from Redis queue
                task_data = await self.database_manager.redis_client.brpop(
                    "task_queue", timeout=5
                )

                if task_data is None:
                    continue

                # Parse task data
                task_json = task_data[1]
                task_info = json.loads(task_json)

                # Process the task
                await self._process_single_task(task_info)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[WORKER] Error in task processing loop: {e}")
                await asyncio.sleep(5)

    async def _process_single_task(self, task_info: Dict[str, Any]):
        """Process a single task"""
        start_time = time.time()
        task_id = task_info.get("task_id", "unknown")

        try:
            logger.info(f"[WORKER] Processing task {task_id}")

            # Create data chunk
            chunk = DataChunk(
                chunk_id=task_id,
                data_type=task_info.get("data_type", "web"),
                source_url=task_info.get("url", ""),
                content=task_info.get("content", ""),
                metadata=task_info.get("metadata", {}),
                size_bytes=len(str(task_info.get("content", "")).encode("utf-8")),
                timestamp=datetime.now(),
            )

            # Process based on task type
            if task_info.get("task_type") == "crawl":
                result = await self._process_crawl_task(chunk)
            elif task_info.get("task_type") == "multimodal":
                result = await self._process_multimodal_task(chunk)
            else:
                # Default processing
                result = await self.distributed_processor._process_single_chunk(
                    chunk, None
                )

            # Store results
            if result.success:
                await self._store_processing_result(chunk, result)
                self.processed_tasks += 1
                logger.info(f"[WORKER] Task {task_id} completed successfully")
            else:
                self.failed_tasks += 1
                logger.error(f"[WORKER] Task {task_id} failed: {result.error}")

            # Update metrics
            processing_time = time.time() - start_time
            self.total_processing_time += processing_time

            # Store processing metrics
            metrics = ProcessingMetrics(
                timestamp=datetime.now(),
                worker_id=self.worker_id,
                operation_type=task_info.get("task_type", "unknown"),
                duration_ms=int(processing_time * 1000),
                bytes_processed=chunk.size_bytes,
                success=result.success,
                error_type=result.error if not result.success else None,
                memory_usage_mb=self.process.memory_info().rss / 1024 / 1024,
                cpu_usage_percent=self.process.cpu_percent(),
            )

            await self.database_manager.store_processing_metrics(metrics)

        except Exception as e:
            logger.error(f"[WORKER] Error processing task {task_id}: {e}")
            logger.error(traceback.format_exc())
            self.failed_tasks += 1

    async def _process_crawl_task(self, chunk: DataChunk) -> ProcessingResult:
        """Process a crawling task"""
        try:
            # Use advanced scraper to crawl the URL
            result = await self.advanced_scraper.scrape_url(chunk.source_url)

            if result.success:
                # Process the crawled content with multimodal processor
                processed_data = await self.multimodal_processor.process(
                    data=result.content,
                    data_type="web",
                    metadata=result.metadata,
                    source_url=chunk.source_url,
                )

                return ProcessingResult(
                    chunk_id=chunk.chunk_id,
                    success=True,
                    processed_data=processed_data,
                    processing_time=result.processing_time,
                    output_size_bytes=len(str(processed_data).encode("utf-8")),
                    quality_score=processed_data.quality_score,
                )
            else:
                return ProcessingResult(
                    chunk_id=chunk.chunk_id,
                    success=False,
                    processed_data=None,
                    error=result.error,
                )

        except Exception as e:
            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=False,
                processed_data=None,
                error=str(e),
            )

    async def _process_multimodal_task(self, chunk: DataChunk) -> ProcessingResult:
        """Process a multimodal task"""
        try:
            # Process with multimodal processor
            processed_data = await self.multimodal_processor.process(
                data=chunk.content,
                data_type=chunk.data_type,
                metadata=chunk.metadata,
                source_url=chunk.source_url,
            )

            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=True,
                processed_data=processed_data,
                processing_time=processed_data.processing_time,
                output_size_bytes=len(str(processed_data).encode("utf-8")),
                quality_score=processed_data.quality_score,
            )

        except Exception as e:
            return ProcessingResult(
                chunk_id=chunk.chunk_id,
                success=False,
                processed_data=None,
                error=str(e),
            )

    async def _store_processing_result(
        self, chunk: DataChunk, result: ProcessingResult
    ):
        """Store processing result in database"""
        try:
            # Create crawl record
            crawl_record = CrawlRecord(
                url=chunk.source_url,
                domain=(
                    chunk.source_url.split("/")[2]
                    if chunk.source_url.startswith("http")
                    else "unknown"
                ),
                content_type=chunk.data_type,
                content_hash=str(hash(str(result.processed_data))),
                size_bytes=result.output_size_bytes,
                processing_time=result.processing_time,
                quality_score=result.quality_score,
                metadata=chunk.metadata,
                content=str(result.processed_data),
                status="completed",
            )

            # Store in database
            await self.database_manager.store_crawl_record(crawl_record)

        except Exception as e:
            logger.error(f"[WORKER] Failed to store processing result: {e}")

    async def _monitor_resources(self):
        """Monitor resource usage"""
        while self.running:
            try:
                # Get current resource usage
                memory_info = self.process.memory_info()
                memory_mb = memory_info.rss / 1024 / 1024
                cpu_percent = self.process.cpu_percent()

                # Update max usage
                self.max_memory_usage = max(self.max_memory_usage, memory_mb)
                self.max_cpu_usage = max(self.max_cpu_usage, cpu_percent)

                # Check limits
                if memory_mb > self.config.max_memory_mb:
                    logger.warning(
                        f"[WORKER] Memory usage exceeded limit: {memory_mb:.2f}MB > {self.config.max_memory_mb}MB"
                    )

                if cpu_percent > self.config.max_cpu_percent:
                    logger.warning(
                        f"[WORKER] CPU usage exceeded limit: {cpu_percent:.2f}% > {self.config.max_cpu_percent}%"
                    )

                await asyncio.sleep(30)  # Check every 30 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[WORKER] Error monitoring resources: {e}")
                await asyncio.sleep(30)

    async def _collect_metrics(self):
        """Collect and store metrics"""
        while self.running:
            try:
                if self.metrics_collector:
                    await self.metrics_collector.collect_worker_metrics()

                await asyncio.sleep(60)  # Collect every minute

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[WORKER] Error collecting metrics: {e}")
                await asyncio.sleep(60)

    async def _health_check(self):
        """Perform health checks"""
        while self.running:
            try:
                # Check database connectivity
                await self.database_manager.redis_client.ping()

                # Update last heartbeat
                await self.database_manager.cache_set(
                    f"worker:{self.worker_id}:heartbeat",
                    datetime.now().isoformat(),
                    ttl=120,
                )

                await asyncio.sleep(30)  # Health check every 30 seconds

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"[WORKER] Health check failed: {e}")
                await asyncio.sleep(30)

    async def get_worker_stats(self) -> Dict[str, Any]:
        """Get worker statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        return {
            "worker_id": self.worker_id,
            "uptime_seconds": uptime,
            "processed_tasks": self.processed_tasks,
            "failed_tasks": self.failed_tasks,
            "success_rate": (
                self.processed_tasks / (self.processed_tasks + self.failed_tasks)
                if (self.processed_tasks + self.failed_tasks) > 0
                else 0.0
            ),
            "total_processing_time": self.total_processing_time,
            "avg_processing_time": (
                self.total_processing_time / self.processed_tasks
                if self.processed_tasks > 0
                else 0.0
            ),
            "max_memory_usage_mb": self.max_memory_usage,
            "max_cpu_usage_percent": self.max_cpu_usage,
            "current_memory_mb": self.process.memory_info().rss / 1024 / 1024,
            "current_cpu_percent": self.process.cpu_percent(),
        }

    async def shutdown(self):
        """Shutdown the worker"""
        logger.info(f"[WORKER] Shutting down worker {self.worker_id}...")

        try:
            # Close database connections
            if self.database_manager:
                await self.database_manager.close()

            # Close distributed processor
            if self.distributed_processor:
                await self.distributed_processor.shutdown()

            # Final metrics
            final_stats = await self.get_worker_stats()
            logger.info(f"[WORKER] Final stats: {final_stats}")

            logger.info(f"[WORKER] Worker {self.worker_id} shutdown complete")

        except Exception as e:
            logger.error(f"[WORKER] Error during shutdown: {e}")


async def main():
    """Main entry point for the worker"""
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("/data/logs/worker.log"),
        ],
    )

    # Create worker configuration
    config = WorkerConfig(
        worker_id=os.getenv("WORKER_ID", f"worker-{os.getpid()}"),
        concurrency=int(os.getenv("WORKER_CONCURRENCY", "100")),
        timeout=int(os.getenv("PROCESSING_TIMEOUT", "300")),
        redis_url=os.getenv("REDIS_URL", "redis://redis-service:6379"),
        postgres_url=os.getenv(
            "POSTGRES_URL", "postgresql://postgres-service:5432/opencrawler"
        ),
        max_memory_mb=int(os.getenv("MAX_MEMORY_MB", "4096")),
        max_cpu_percent=float(os.getenv("MAX_CPU_PERCENT", "85.0")),
    )

    # Create and start worker
    worker = DistributedWorker(config)

    try:
        await worker.initialize()
        await worker.start()

    except Exception as e:
        logger.error(f"[WORKER] Fatal error: {e}")
        logger.error(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
