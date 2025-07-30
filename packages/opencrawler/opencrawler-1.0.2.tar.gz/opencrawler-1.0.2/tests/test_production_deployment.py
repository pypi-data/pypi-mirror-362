#!/usr/bin/env python3
"""
Comprehensive Test Suite for Production Deployment System
Author: Nik Jois <nikjois@llamasearch.ai>
"""

import asyncio
import pytest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from datetime import datetime, timedelta
import json
import yaml
import os
import sys

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from deployment.production_deployment import (
    ProductionDeploymentSystem,
    DeploymentConfig,
    DeploymentEnvironment,
    DeploymentTarget,
    DeploymentStatus,
    SecurityConfig,
    SecurityLevel,
    MonitoringConfig,
    BackupConfig,
    DeploymentResult
)


class TestProductionDeploymentSystem:
    """Comprehensive test suite for ProductionDeploymentSystem"""

    @pytest.fixture
    async def deployment_system(self):
        """Create a deployment system for testing"""
        system = ProductionDeploymentSystem()
        await system.initialize()
        yield system
        await system.cleanup()

    @pytest.fixture
    def mock_docker_client(self):
        """Mock Docker client"""
        client = Mock()
        client.ping.return_value = True
        client.info.return_value = {"ServerVersion": "20.10.0"}
        client.images.build.return_value = (Mock(id="test-image-id"), [])
        client.containers.run.return_value = Mock(id="test-container-id", status="running")
        client.containers.get.side_effect = Exception("Container not found")
        return client

    @pytest.fixture
    def mock_k8s_client(self):
        """Mock Kubernetes client"""
        client = Mock()
        v1 = Mock()
        v1.get_code.return_value = Mock(git_version="v1.20.0")
        v1.list_namespace.return_value = Mock()
        client.CoreV1Api.return_value = v1
        return client

    @pytest.fixture
    def test_config(self):
        """Test deployment configuration"""
        return DeploymentConfig(
            environment=DeploymentEnvironment.DEVELOPMENT,
            target=DeploymentTarget.DOCKER,
            image_name="test-app",
            image_tag="test",
            replicas=1,
            resources={"cpu": "500m", "memory": "512Mi"},
            environment_variables={"ENV": "test"},
            ports=[{"container": 8000, "host": 8000}],
            health_check={"path": "/health", "interval": 30, "timeout": 10, "retries": 3},
            security=SecurityConfig(level=SecurityLevel.BASIC),
            monitoring=MonitoringConfig(enable_prometheus=True),
            backup=BackupConfig(enable_backups=False)
        )

    @pytest.mark.asyncio
    async def test_initialization(self, deployment_system):
        """Test system initialization"""
        assert deployment_system.deployment_id is not None
        assert deployment_system.project_root is not None
        assert deployment_system.temp_dir is not None
        assert len(deployment_system.deployment_configs) > 0
        assert deployment_system.metrics["deployments_total"] == 0

    @pytest.mark.asyncio
    async def test_docker_initialization(self, deployment_system):
        """Test Docker client initialization"""
        with patch('deployment.production_deployment.docker') as mock_docker:
            mock_docker.from_env.return_value = Mock()
            mock_docker.from_env.return_value.ping.return_value = True
            mock_docker.from_env.return_value.info.return_value = {"ServerVersion": "20.10.0"}
            
            await deployment_system._initialize_docker()
            
            assert deployment_system.docker_client is not None

    @pytest.mark.asyncio
    async def test_kubernetes_initialization(self, deployment_system):
        """Test Kubernetes client initialization"""
        with patch('deployment.production_deployment.config') as mock_config, \
             patch('deployment.production_deployment.client') as mock_client:
            
            mock_config.load_kube_config.return_value = None
            mock_client.ApiClient.return_value = Mock()
            mock_client.CoreV1Api.return_value.get_code.return_value = Mock(git_version="v1.20.0")
            
            await deployment_system._initialize_kubernetes()
            
            assert deployment_system.k8s_client is not None

    @pytest.mark.asyncio
    async def test_security_scan(self, deployment_system, test_config):
        """Test security scanning"""
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.PENDING,
            message="Test deployment",
            start_time=datetime.now()
        )
        
        await deployment_system._security_scan(test_config, result)
        
        assert "security_scan_results" in result.__dict__
        assert result.security_scan_results["vulnerabilities_found"] >= 0
        assert result.security_scan_results["scan_duration"] >= 0

    @pytest.mark.asyncio
    async def test_performance_testing(self, deployment_system, test_config):
        """Test performance testing"""
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.RUNNING,
            message="Test deployment",
            start_time=datetime.now(),
            endpoints=["http://localhost:8000"]
        )
        
        with patch('deployment.production_deployment.aiohttp') as mock_aiohttp:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_aiohttp.ClientSession.return_value.__aenter__.return_value = mock_session
            mock_aiohttp.ClientTimeout.return_value = Mock()
            
            await deployment_system._performance_testing(test_config, result)
            
            assert "performance_metrics" in result.__dict__

    @pytest.mark.asyncio
    async def test_docker_deployment(self, deployment_system, test_config, mock_docker_client):
        """Test Docker deployment"""
        deployment_system.docker_client = mock_docker_client
        
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.BUILDING,
            message="Test deployment",
            start_time=datetime.now()
        )
        
        # Mock container
        container = Mock()
        container.id = "test-container-id"
        container.status = "running"
        container.reload.return_value = None
        container.attrs = {
            'NetworkSettings': {
                'Ports': {
                    '8000/tcp': [{'HostIp': '0.0.0.0', 'HostPort': '8000'}]
                }
            }
        }
        
        mock_docker_client.containers.run.return_value = container
        
        await deployment_system._deploy_docker(test_config, result)
        
        assert result.endpoints
        assert result.metrics["container_id"] == "test-container-id"

    @pytest.mark.asyncio
    async def test_kubernetes_deployment(self, deployment_system, test_config, mock_k8s_client):
        """Test Kubernetes deployment"""
        deployment_system.k8s_client = mock_k8s_client
        
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.BUILDING,
            message="Test deployment",
            start_time=datetime.now()
        )
        
        with patch('deployment.production_deployment.client', mock_k8s_client):
            mock_k8s_client.AppsV1Api.return_value.create_namespaced_deployment.return_value = Mock()
            mock_k8s_client.CoreV1Api.return_value.create_namespaced_service.return_value = Mock()
            mock_k8s_client.AppsV1Api.return_value.read_namespaced_deployment.return_value = Mock(
                status=Mock(ready_replicas=1)
            )
            mock_k8s_client.CoreV1Api.return_value.read_namespaced_service.return_value = Mock(
                status=Mock(load_balancer=Mock(ingress=[Mock(ip="10.0.0.1")])),
                spec=Mock(ports=[Mock(port=80)])
            )
            
            await deployment_system._deploy_kubernetes(test_config, result)

    @pytest.mark.asyncio
    async def test_docker_compose_deployment(self, deployment_system, test_config):
        """Test Docker Compose deployment"""
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.BUILDING,
            message="Test deployment",
            start_time=datetime.now()
        )
        
        with patch('subprocess.run') as mock_run:
            mock_run.return_value = Mock(returncode=0, stdout="Success", stderr="")
            
            await deployment_system._deploy_docker_compose(test_config, result)
            
            assert result.logs

    @pytest.mark.asyncio
    async def test_full_deployment_flow(self, deployment_system, test_config):
        """Test complete deployment flow"""
        with patch.object(deployment_system, '_pre_deployment_checks') as mock_pre_checks, \
             patch.object(deployment_system, '_build_application') as mock_build, \
             patch.object(deployment_system, '_deploy_docker') as mock_deploy, \
             patch.object(deployment_system, '_post_deployment_validation') as mock_post_validation, \
             patch.object(deployment_system, '_security_scan') as mock_security_scan, \
             patch.object(deployment_system, '_performance_testing') as mock_performance:
            
            mock_pre_checks.return_value = None
            mock_build.return_value = None
            mock_deploy.return_value = None
            mock_post_validation.return_value = None
            mock_security_scan.return_value = None
            mock_performance.return_value = None
            
            result = await deployment_system.deploy(DeploymentEnvironment.DEVELOPMENT)
            
            assert result.status == DeploymentStatus.RUNNING
            assert result.duration > 0
            assert deployment_system.metrics["deployments_total"] == 1
            assert deployment_system.metrics["deployments_successful"] == 1

    @pytest.mark.asyncio
    async def test_deployment_failure_handling(self, deployment_system, test_config):
        """Test deployment failure handling"""
        with patch.object(deployment_system, '_pre_deployment_checks') as mock_pre_checks:
            mock_pre_checks.side_effect = Exception("Pre-deployment check failed")
            
            result = await deployment_system.deploy(DeploymentEnvironment.DEVELOPMENT)
            
            assert result.status == DeploymentStatus.FAILED
            assert "Pre-deployment check failed" in result.message
            assert deployment_system.metrics["deployments_failed"] == 1

    @pytest.mark.asyncio
    async def test_rollback_functionality(self, deployment_system):
        """Test rollback functionality"""
        # Create a deployment history entry
        deployment_system.deployment_history.append(
            DeploymentResult(
                deployment_id="test-deployment-1",
                status=DeploymentStatus.RUNNING,
                message="Test deployment",
                start_time=datetime.now()
            )
        )
        
        result = await deployment_system.rollback("test-deployment-1")
        
        assert result.status == DeploymentStatus.RUNNING
        assert "rollback_test-deployment-1" in result.deployment_id

    @pytest.mark.asyncio
    async def test_deployment_status_retrieval(self, deployment_system):
        """Test deployment status retrieval"""
        # Add a deployment to active deployments
        test_deployment = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.RUNNING,
            message="Test deployment",
            start_time=datetime.now()
        )
        deployment_system.active_deployments["test-deployment"] = test_deployment
        
        status = await deployment_system.get_deployment_status("test-deployment")
        
        assert status is not None
        assert status.deployment_id == "test-deployment"
        assert status.status == DeploymentStatus.RUNNING

    @pytest.mark.asyncio
    async def test_deployment_logs_retrieval(self, deployment_system):
        """Test deployment logs retrieval"""
        # Add a deployment with logs
        test_deployment = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.RUNNING,
            message="Test deployment",
            start_time=datetime.now(),
            logs=["Log line 1", "Log line 2"]
        )
        deployment_system.active_deployments["test-deployment"] = test_deployment
        
        logs = await deployment_system.get_deployment_logs("test-deployment")
        
        assert len(logs) == 2
        assert "Log line 1" in logs

    @pytest.mark.asyncio
    async def test_deployment_metrics(self, deployment_system):
        """Test deployment metrics"""
        # Update some metrics
        deployment_system.metrics["deployments_total"] = 10
        deployment_system.metrics["deployments_successful"] = 8
        deployment_system.metrics["deployments_failed"] = 2
        
        metrics = await deployment_system.get_deployment_metrics()
        
        assert metrics["deployments_total"] == 10
        assert metrics["deployments_successful"] == 8
        assert metrics["deployments_failed"] == 2

    @pytest.mark.asyncio
    async def test_security_event_logging(self, deployment_system):
        """Test security event logging"""
        await deployment_system._log_security_event("TEST_EVENT", "Test message", {"key": "value"})
        
        assert len(deployment_system.security_audit_log) > 0
        
        event = deployment_system.security_audit_log[-1]
        assert event["event_type"] == "TEST_EVENT"
        assert event["message"] == "Test message"
        assert event["details"]["key"] == "value"

    @pytest.mark.asyncio
    async def test_dockerfile_generation(self, deployment_system, test_config):
        """Test Dockerfile generation"""
        dockerfile_path = deployment_system.project_root / "Dockerfile"
        
        # Remove existing Dockerfile if it exists
        if dockerfile_path.exists():
            dockerfile_path.unlink()
        
        await deployment_system._generate_dockerfile(test_config)
        
        assert dockerfile_path.exists()
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
            assert "FROM python:3.11-slim" in content
            assert "EXPOSE 8000" in content

    @pytest.mark.asyncio
    async def test_kubernetes_manifest_generation(self, deployment_system, test_config):
        """Test Kubernetes manifest generation"""
        manifests = await deployment_system._generate_kubernetes_manifests(test_config)
        
        assert len(manifests) >= 2  # At least Deployment and Service
        
        deployment_manifest = next(m for m in manifests if m["kind"] == "Deployment")
        service_manifest = next(m for m in manifests if m["kind"] == "Service")
        
        assert deployment_manifest["metadata"]["name"] == test_config.image_name
        assert service_manifest["metadata"]["name"] == f"{test_config.image_name}-service"

    @pytest.mark.asyncio
    async def test_docker_compose_config_generation(self, deployment_system, test_config):
        """Test Docker Compose configuration generation"""
        compose_config = await deployment_system._generate_docker_compose_config(test_config)
        
        assert "version" in compose_config
        assert "services" in compose_config
        assert test_config.image_name in compose_config["services"]
        
        service_config = compose_config["services"][test_config.image_name]
        assert service_config["image"] == f"{test_config.image_name}:{test_config.image_tag}"

    @pytest.mark.asyncio
    async def test_network_connectivity_check(self, deployment_system):
        """Test network connectivity check"""
        with patch('socket.gethostbyname') as mock_dns, \
             patch('deployment.production_deployment.aiohttp') as mock_aiohttp:
            
            mock_dns.return_value = "8.8.8.8"
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_aiohttp.ClientSession.return_value.__aenter__.return_value = mock_session
            mock_aiohttp.ClientTimeout.return_value = Mock()
            
            await deployment_system._check_network_connectivity()
            
            mock_dns.assert_called_once()

    @pytest.mark.asyncio
    async def test_environment_validation(self, deployment_system):
        """Test environment validation"""
        with patch('psutil.virtual_memory') as mock_memory, \
             patch('psutil.disk_usage') as mock_disk:
            
            mock_memory.return_value = Mock(available=2 * 1024 * 1024 * 1024)  # 2GB
            mock_disk.return_value = Mock(free=10 * 1024 * 1024 * 1024)  # 10GB
            
            await deployment_system._validate_deployment_environment()

    @pytest.mark.asyncio
    async def test_health_check_validation(self, deployment_system, test_config):
        """Test health check validation"""
        with patch('deployment.production_deployment.aiohttp') as mock_aiohttp:
            mock_session = AsyncMock()
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_session.get.return_value.__aenter__.return_value = mock_response
            mock_aiohttp.ClientSession.return_value.__aenter__.return_value = mock_session
            mock_aiohttp.ClientTimeout.return_value = Mock()
            
            result = await deployment_system._validate_endpoint_health("http://localhost:8000", test_config)
            
            assert result is True

    @pytest.mark.asyncio
    async def test_cleanup(self, deployment_system):
        """Test system cleanup"""
        temp_dir = deployment_system.temp_dir
        
        await deployment_system.cleanup()
        
        assert not temp_dir.exists()

    def test_configuration_loading(self, deployment_system):
        """Test configuration loading"""
        assert DeploymentEnvironment.DEVELOPMENT in deployment_system.deployment_configs
        assert DeploymentEnvironment.STAGING in deployment_system.deployment_configs
        assert DeploymentEnvironment.PRODUCTION in deployment_system.deployment_configs
        
        dev_config = deployment_system.deployment_configs[DeploymentEnvironment.DEVELOPMENT]
        assert dev_config.target == DeploymentTarget.DOCKER
        assert dev_config.replicas == 1
        
        prod_config = deployment_system.deployment_configs[DeploymentEnvironment.PRODUCTION]
        assert prod_config.target == DeploymentTarget.KUBERNETES
        assert prod_config.replicas == 5

    def test_security_configuration(self, deployment_system):
        """Test security configuration"""
        prod_config = deployment_system.deployment_configs[DeploymentEnvironment.PRODUCTION]
        
        assert prod_config.security.level == SecurityLevel.ENTERPRISE
        assert prod_config.security.enable_tls is True
        assert prod_config.security.enable_rbac is True
        assert prod_config.security.enable_image_scanning is True

    def test_monitoring_configuration(self, deployment_system):
        """Test monitoring configuration"""
        prod_config = deployment_system.deployment_configs[DeploymentEnvironment.PRODUCTION]
        
        assert prod_config.monitoring.enable_prometheus is True
        assert prod_config.monitoring.enable_grafana is True
        assert prod_config.monitoring.enable_alertmanager is True

    def test_backup_configuration(self, deployment_system):
        """Test backup configuration"""
        prod_config = deployment_system.deployment_configs[DeploymentEnvironment.PRODUCTION]
        
        assert prod_config.backup.enable_backups is True
        assert prod_config.backup.retention_days == 90
        assert prod_config.backup.encryption_enabled is True


class TestDeploymentConfig:
    """Test deployment configuration classes"""

    def test_deployment_config_creation(self):
        """Test deployment configuration creation"""
        config = DeploymentConfig(
            environment=DeploymentEnvironment.DEVELOPMENT,
            target=DeploymentTarget.DOCKER,
            image_name="test-app"
        )
        
        assert config.environment == DeploymentEnvironment.DEVELOPMENT
        assert config.target == DeploymentTarget.DOCKER
        assert config.image_name == "test-app"
        assert config.image_tag == "latest"  # Default value

    def test_security_config_creation(self):
        """Test security configuration creation"""
        config = SecurityConfig(
            level=SecurityLevel.HIGH,
            enable_tls=True,
            enable_rbac=True
        )
        
        assert config.level == SecurityLevel.HIGH
        assert config.enable_tls is True
        assert config.enable_rbac is True

    def test_monitoring_config_creation(self):
        """Test monitoring configuration creation"""
        config = MonitoringConfig(
            enable_prometheus=True,
            enable_grafana=True,
            enable_alertmanager=False
        )
        
        assert config.enable_prometheus is True
        assert config.enable_grafana is True
        assert config.enable_alertmanager is False

    def test_backup_config_creation(self):
        """Test backup configuration creation"""
        config = BackupConfig(
            enable_backups=True,
            retention_days=30,
            encryption_enabled=True
        )
        
        assert config.enable_backups is True
        assert config.retention_days == 30
        assert config.encryption_enabled is True


class TestDeploymentResult:
    """Test deployment result class"""

    def test_deployment_result_creation(self):
        """Test deployment result creation"""
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.RUNNING,
            message="Test deployment",
            start_time=datetime.now()
        )
        
        assert result.deployment_id == "test-deployment"
        assert result.status == DeploymentStatus.RUNNING
        assert result.message == "Test deployment"
        assert result.start_time is not None

    def test_deployment_result_with_metrics(self):
        """Test deployment result with metrics"""
        result = DeploymentResult(
            deployment_id="test-deployment",
            status=DeploymentStatus.RUNNING,
            message="Test deployment",
            start_time=datetime.now(),
            metrics={"build_time": 120.5, "image_size": 1024000}
        )
        
        assert result.metrics["build_time"] == 120.5
        assert result.metrics["image_size"] == 1024000


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"]) 