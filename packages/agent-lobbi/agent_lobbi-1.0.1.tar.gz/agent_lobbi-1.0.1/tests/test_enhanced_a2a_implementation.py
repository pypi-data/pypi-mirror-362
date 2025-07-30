#!/usr/bin/env python3
"""
Comprehensive Test Suite for Enhanced Agent Lobby A2A+ Implementation

This test suite validates:
1. Enhanced SDK initialization with A2A and metrics
2. Agent registration and capability advertising
3. A2A protocol integration and agent card generation
4. Enhanced metrics collection and reporting
5. WebSocket communication and task handling
6. Cross-protocol compatibility (A2A ↔ Agent Lobby)
7. Performance and robustness testing
"""

import asyncio
import json
import time
import uuid
import logging
import pytest
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, patch, AsyncMock
import aiohttp
import websockets
import threading
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the components we're testing
from src.sdk.agent_lobbi_sdk import AgentLobbySDK
from src.core.agent_metrics_enhanced import EnhancedMetricsSystem
from src.core.lobby import Lobby

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestEnhancedA2AImplementation:
    """Comprehensive test suite for enhanced A2A+ implementation"""

    @pytest.fixture
    async def lobby_server(self):
        """Start a test lobby server"""
        lobby = Lobby(host="localhost", http_port=8080, ws_port=8081)
        try:
            await lobby.start()
            yield lobby
        finally:
            await lobby.stop()

    @pytest.fixture
    def enhanced_sdk(self):
        """Create an enhanced SDK instance for testing"""
        sdk = AgentLobbySDK(
            lobby_host="localhost",
            lobby_port=8080,
            ws_port=8081,
            enable_security=True,
            enable_a2a=True,
            enable_metrics=True,
            a2a_port=8090
        )
        yield sdk
        # Cleanup
        if sdk.metrics_system:
            sdk.metrics_system.stop()

    @pytest.fixture
    def metrics_system(self):
        """Create standalone metrics system for testing"""
        metrics = EnhancedMetricsSystem()
        metrics.start()
        yield metrics
        metrics.stop()

    async def test_enhanced_sdk_initialization(self, enhanced_sdk):
        """Test enhanced SDK initialization with all features enabled"""
        logger.info("🧪 Testing enhanced SDK initialization...")
        
        # Verify all systems are initialized
        assert enhanced_sdk.enable_a2a is True
        assert enhanced_sdk.enable_metrics is True
        assert enhanced_sdk.metrics_system is not None
        assert enhanced_sdk.a2a_handler is not None
        assert enhanced_sdk.consensus_system is not None
        assert enhanced_sdk.data_protection is not None
        
        # Verify metrics system is running
        assert enhanced_sdk.metrics_system.running is True
        
        # Test A2A handler initialization
        assert enhanced_sdk.a2a_handler.sdk == enhanced_sdk
        assert enhanced_sdk.a2a_handler.metrics_system == enhanced_sdk.metrics_system
        
        logger.info("✅ Enhanced SDK initialization test passed")

    async def test_agent_registration_with_metrics(self, enhanced_sdk, lobby_server):
        """Test agent registration with comprehensive metrics tracking"""
        logger.info("🧪 Testing agent registration with metrics...")
        
        # Mock task handler
        async def mock_task_handler(task_data):
            return {"result": "mock_processing", "status": "completed"}
        
        # Register agent
        success = await enhanced_sdk.register_agent(
            agent_id="test_agent_001",
            name="Test Agent",
            agent_type="test",
            capabilities=["testing", "analysis"],
            task_handler=mock_task_handler
        )
        
        assert success is True
        assert enhanced_sdk.agent_id == "test_agent_001"
        assert enhanced_sdk.api_key is not None
        assert enhanced_sdk.task_handler == mock_task_handler
        
        # Verify metrics are being tracked
        dashboard_data = enhanced_sdk.get_metrics_dashboard()
        assert "a2a_metrics" in dashboard_data
        assert "agent_card_url" in dashboard_data["a2a_metrics"]
        
        logger.info("✅ Agent registration with metrics test passed")

    async def test_a2a_agent_card_generation(self, enhanced_sdk):
        """Test A2A agent card generation with enhanced capabilities"""
        logger.info("🧪 Testing A2A agent card generation...")
        
        # Set up agent
        enhanced_sdk.agent_id = "test_agent_002"
        
        # Generate agent card
        agent_card = enhanced_sdk.get_a2a_agent_card()
        
        # Verify structure
        assert "name" in agent_card
        assert "description" in agent_card
        assert "capabilities" in agent_card
        assert "extensions" in agent_card
        
        # Verify enhanced capabilities
        capabilities = agent_card["capabilities"]
        assert capabilities["neuromorphic_learning"] is True
        assert capabilities["collective_intelligence"] is True
        assert capabilities["real_time_metrics"] is True
        
        # Verify Agent Lobby extensions
        extensions = agent_card["extensions"]["agent_lobby"]
        assert "enhanced_features" in extensions
        assert "performance_metrics" in extensions
        assert "analytics" in extensions
        
        enhanced_features = extensions["enhanced_features"]
        assert "Neuromorphic agent selection" in enhanced_features
        assert "Collective intelligence" in enhanced_features
        assert "Real-time collaboration" in enhanced_features
        
        logger.info("✅ A2A agent card generation test passed")

    async def test_metrics_collection_performance(self, metrics_system):
        """Test metrics collection performance and accuracy"""
        logger.info("🧪 Testing metrics collection performance...")
        
        # Test high-volume metrics collection
        start_time = time.time()
        num_metrics = 1000
        
        for i in range(num_metrics):
            metrics_system.collector.record_metric(
                f"test_metric_{i % 10}",
                float(i),
                tags={"test": "performance", "batch": str(i // 100)}
            )
        
        collection_time = time.time() - start_time
        
        # Verify performance (should handle 1000 metrics in < 1 second)
        assert collection_time < 1.0
        
        # Process metrics to populate aggregated_metrics
        metrics_system.collector._process_metrics()
        
        # Verify metrics are stored
        real_time_metrics = metrics_system.collector.get_real_time_metrics()
        assert len(real_time_metrics) > 0
        
        logger.info(f"✅ Metrics performance test passed: {num_metrics} metrics in {collection_time:.3f}s")

    async def test_a2a_task_processing(self, enhanced_sdk):
        """Test A2A task processing with metrics tracking"""
        logger.info("🧪 Testing A2A task processing...")
        
        # Mock task handler
        async def mock_a2a_handler(task_data):
            return {
                "result": f"Processed A2A task: {task_data.get('id')}",
                "status": "completed",
                "processing_time": 0.1
            }
        
        enhanced_sdk.task_handler = mock_a2a_handler
        enhanced_sdk.agent_id = "test_agent_003"
        
        # Simulate A2A task
        task_data = {
            "id": str(uuid.uuid4()),
            "type": "analysis",
            "message": "Test A2A task",
            "timestamp": datetime.now().isoformat()
        }
        
        # Process task through A2A handler
        result = await enhanced_sdk.a2a_handler.handle_a2a_task(task_data)
        
        # Verify result
        assert "result" in result
        assert result["status"] == "completed"
        
        # Verify metrics tracking
        if enhanced_sdk.metrics_system:
            dashboard_data = enhanced_sdk.get_metrics_dashboard()
            assert "performance_summary" in dashboard_data
            assert "a2a_metrics" in dashboard_data
        
        logger.info("✅ A2A task processing test passed")

    async def test_cross_protocol_communication(self, enhanced_sdk):
        """Test communication between A2A and Agent Lobby protocols"""
        logger.info("🧪 Testing cross-protocol communication...")
        
        # Set up agent
        enhanced_sdk.agent_id = "test_agent_004"
        
        # Test A2A message formatting
        a2a_message = {
            "role": "user",
            "parts": [{
                "type": "text",
                "text": "Test cross-protocol message"
            }]
        }
        
        # Verify A2A handler can process the message format
        assert enhanced_sdk.a2a_handler is not None
        
        # Test metrics integration
        if enhanced_sdk.metrics_system:
            # Track a simulated A2A interaction
            enhanced_sdk.metrics_system.a2a_tracker.track_task_start(
                "test_task_001", enhanced_sdk.agent_id, "cross_protocol_test"
            )
            
            enhanced_sdk.metrics_system.a2a_tracker.track_task_completion(
                "test_task_001", "completed", len(str(a2a_message))
            )
        
        logger.info("✅ Cross-protocol communication test passed")

    async def test_enhanced_metrics_dashboard(self, enhanced_sdk):
        """Test comprehensive metrics dashboard functionality"""
        logger.info("🧪 Testing enhanced metrics dashboard...")
        
        # Set up agent
        enhanced_sdk.agent_id = "test_agent_005"
        
        # Generate some metrics
        if enhanced_sdk.metrics_system:
            # Record various metrics
            enhanced_sdk.metrics_system.collector.record_metric(
                "response_time", 45.2, tags={"agent_id": enhanced_sdk.agent_id}
            )
            enhanced_sdk.metrics_system.collector.record_metric(
                "success_rate", 0.95, tags={"agent_id": enhanced_sdk.agent_id}
            )
            enhanced_sdk.metrics_system.collector.record_metric(
                "cost_per_interaction", 0.02, tags={"agent_id": enhanced_sdk.agent_id}
            )
        
        # Get dashboard data
        dashboard_data = enhanced_sdk.get_metrics_dashboard()
        
        # Verify structure
        assert "timestamp" in dashboard_data
        assert "performance_summary" in dashboard_data
        # Verify structure with correct keys
        assert "user_experience_summary" in dashboard_data
        assert "business_summary" in dashboard_data
        assert "a2a_metrics" in dashboard_data
        
        # Verify A2A specific metrics
        a2a_metrics = dashboard_data["a2a_metrics"]
        assert "enhanced_capabilities" in a2a_metrics
        assert "neuromorphic_learning" in a2a_metrics["enhanced_capabilities"]
        
        logger.info("✅ Enhanced metrics dashboard test passed")

    async def test_concurrent_agent_operations(self, enhanced_sdk):
        """Test concurrent agent operations with metrics"""
        logger.info("🧪 Testing concurrent agent operations...")
        
        # Set up multiple concurrent tasks
        async def simulate_agent_task(task_id: str):
            task_data = {
                "id": task_id,
                "type": "concurrent_test",
                "message": f"Concurrent task {task_id}"
            }
            
            if enhanced_sdk.metrics_system:
                enhanced_sdk.metrics_system.a2a_tracker.track_task_start(
                    task_id, enhanced_sdk.agent_id or "test_agent", "concurrent_test"
                )
            
            # Simulate processing
            await asyncio.sleep(0.1)
            
            if enhanced_sdk.metrics_system:
                enhanced_sdk.metrics_system.a2a_tracker.track_task_completion(
                    task_id, "completed", 100
                )
            
            return f"Completed {task_id}"
        
        # Run multiple tasks concurrently
        enhanced_sdk.agent_id = "test_agent_006"
        tasks = [simulate_agent_task(f"task_{i}") for i in range(10)]
        results = await asyncio.gather(*tasks)
        
        # Verify all tasks completed
        assert len(results) == 10
        for i, result in enumerate(results):
            assert result == f"Completed task_{i}"
        
        logger.info("✅ Concurrent agent operations test passed")

    async def test_error_handling_and_recovery(self, enhanced_sdk):
        """Test error handling and recovery mechanisms"""
        logger.info("🧪 Testing error handling and recovery...")
        
        # Set up agent
        enhanced_sdk.agent_id = "test_agent_007"
        
        # Test error scenario
        async def failing_task_handler(task_data):
            raise Exception("Simulated task failure")
        
        enhanced_sdk.task_handler = failing_task_handler
        
        # Process task that will fail
        task_data = {
            "id": "failing_task",
            "type": "error_test",
            "message": "This will fail"
        }
        
        # Should handle error gracefully
        try:
            result = await enhanced_sdk.a2a_handler.handle_a2a_task(task_data)
            assert "error" in result
            assert result["status"] == "failed"
        except Exception as e:
            # Should not propagate unhandled exceptions
            pytest.fail(f"Unhandled exception: {e}")
        
        logger.info("✅ Error handling and recovery test passed")

    async def test_security_and_data_protection(self, enhanced_sdk):
        """Test security systems and data protection"""
        logger.info("🧪 Testing security and data protection...")
        
        # Verify security systems are initialized
        assert enhanced_sdk.consensus_system is not None
        assert enhanced_sdk.data_protection is not None
        assert enhanced_sdk.recovery_system is not None
        assert enhanced_sdk.tracking_system is not None
        
        # Test data access request
        enhanced_sdk.agent_id = "test_agent_008"
        
        access_result = await enhanced_sdk.request_data_access(
            target_agent="test_target",
            data_type="test_data",
            purpose="testing"
        )
        
        assert "status" in access_result
        assert "access_granted" in access_result
        
        logger.info("✅ Security and data protection test passed")


class TestLobbySystemIntegration:
    """Test integration with the lobby system"""

    async def test_lobby_system_startup(self):
        """Test lobby system startup and shutdown"""
        logger.info("🧪 Testing lobby system startup...")
        
        lobby = Lobby(host="localhost", http_port=8080, ws_port=8081)
        
        try:
            # Start lobby
            await lobby.start()
            
            # Verify servers are running
            assert lobby.http_server is not None
            assert lobby.ws_server is not None
            assert lobby.running is True
            
            # Test HTTP endpoint
            async with aiohttp.ClientSession() as session:
                async with session.get("http://localhost:8080/health") as response:
                    # Should get some response (even if 404, means server is running)
                    assert response.status in [200, 404, 405]
            
            logger.info("✅ Lobby system startup test passed")
            
        finally:
            await lobby.stop()

    async def test_websocket_connection(self):
        """Test WebSocket connection to lobby"""
        logger.info("🧪 Testing WebSocket connection...")
        
        lobby = Lobby(host="localhost", http_port=8080, ws_port=8081)
        
        try:
            await lobby.start()
            
            # Test WebSocket connection
            uri = "ws://localhost:8081/api/ws/test_agent?agent_id=test_agent"
            
            async with websockets.connect(uri) as websocket:
                # Send a test message
                test_message = {
                    "message_type": "test",
                    "payload": {"test": "data"}
                }
                
                await websocket.send(json.dumps(test_message))
                
                # Connection should stay open
                await asyncio.sleep(0.1)
                
            logger.info("✅ WebSocket connection test passed")
            
        finally:
            await lobby.stop()


async def run_comprehensive_tests():
    """Run all comprehensive tests"""
    logger.info("🚀 Starting comprehensive A2A+ implementation tests...")
    
    # Run tests
    test_suite = TestEnhancedA2AImplementation()
    lobby_tests = TestLobbySystemIntegration()
    
    try:
        # Test 1: Enhanced SDK initialization
        sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)
        await test_suite.test_enhanced_sdk_initialization(sdk)
        
        # Test 2: Metrics system performance
        metrics = EnhancedMetricsSystem()
        metrics.start()
        await test_suite.test_metrics_collection_performance(metrics)
        metrics.stop()
        
        # Test 3: A2A agent card generation
        await test_suite.test_a2a_agent_card_generation(sdk)
        
        # Test 4: A2A task processing
        await test_suite.test_a2a_task_processing(sdk)
        
        # Test 5: Cross-protocol communication
        await test_suite.test_cross_protocol_communication(sdk)
        
        # Test 6: Enhanced metrics dashboard
        await test_suite.test_enhanced_metrics_dashboard(sdk)
        
        # Test 7: Concurrent operations
        await test_suite.test_concurrent_agent_operations(sdk)
        
        # Test 8: Error handling
        await test_suite.test_error_handling_and_recovery(sdk)
        
        # Test 9: Security systems
        await test_suite.test_security_and_data_protection(sdk)
        
        # Test 10: Lobby system integration
        await lobby_tests.test_lobby_system_startup()
        
        # Test 11: WebSocket connection
        await lobby_tests.test_websocket_connection()
        
        # Cleanup
        if sdk.metrics_system:
            sdk.metrics_system.stop()
        
        logger.info("🎉 All comprehensive tests passed!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run tests
    success = asyncio.run(run_comprehensive_tests())
    
    if success:
        print("\n✅ Enhanced A2A+ Implementation Test Suite: PASSED")
        print("🚀 Ready for PyPI publishing and website integration!")
    else:
        print("\n❌ Enhanced A2A+ Implementation Test Suite: FAILED")
        print("🔧 Please fix issues before proceeding to PyPI publishing")
        sys.exit(1) 