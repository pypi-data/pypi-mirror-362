#!/usr/bin/env python3
"""
Simplified Test for Enhanced Agent Lobby A2A+ Implementation
Tests the core functionality without requiring full lobby system integration
"""

import asyncio
import json
import time
import uuid
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_enhanced_sdk_initialization():
    """Test enhanced SDK initialization"""
    logger.info("🧪 Testing enhanced SDK initialization...")
    
    try:
        from src.sdk.agent_lobbi_sdk import AgentLobbySDK
        
        # Test initialization
        sdk = AgentLobbySDK(
            enable_a2a=True,
            enable_metrics=True,
            enable_security=True
        )
        
        # Verify components are initialized
        assert sdk.enable_a2a is True
        assert sdk.enable_metrics is True
        assert sdk.metrics_system is not None
        assert sdk.a2a_handler is not None
        assert sdk.consensus_system is not None
        
        logger.info("✅ SDK initialization successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ SDK initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_metrics_system():
    """Test metrics system functionality"""
    logger.info("🧪 Testing metrics system...")
    
    try:
        from src.core.agent_metrics_enhanced import EnhancedMetricsSystem
        
        # Create metrics system
        metrics = EnhancedMetricsSystem()
        metrics.start()
        
        # Test metric recording
        start_time = time.time()
        for i in range(100):
            metrics.collector.record_metric(
                f"test_metric_{i % 10}",
                float(i),
                tags={"test": "performance"}
            )
        
        collection_time = time.time() - start_time
        logger.info(f"📊 Recorded 100 metrics in {collection_time:.3f}s")
        
        # Test dashboard data
        dashboard_data = metrics.get_dashboard_data()
        assert "performance_summary" in dashboard_data
        
        # Stop metrics system
        metrics.stop()
        
        logger.info("✅ Metrics system test successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Metrics system test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_a2a_agent_card():
    """Test A2A agent card generation"""
    logger.info("🧪 Testing A2A agent card generation...")
    
    try:
        from src.sdk.agent_lobbi_sdk import AgentLobbySDK
        
        # Create SDK
        sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)
        sdk.agent_id = "test_agent_001"
        
        # Generate agent card
        agent_card = sdk.get_a2a_agent_card()
        
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
        
        # Verify extensions
        extensions = agent_card["extensions"]["agent_lobby"]
        assert "enhanced_features" in extensions
        assert "Neuromorphic agent selection" in extensions["enhanced_features"]
        
        logger.info("✅ A2A agent card generation successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ A2A agent card test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_a2a_task_processing():
    """Test A2A task processing"""
    logger.info("🧪 Testing A2A task processing...")
    
    try:
        from src.sdk.agent_lobbi_sdk import AgentLobbySDK
        
        # Create SDK
        sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)
        sdk.agent_id = "test_agent_002"
        
        # Mock task handler
        async def mock_task_handler(task_data):
            return {
                "result": f"Processed task: {task_data.get('id')}",
                "status": "completed",
                "processing_time": 0.05
            }
        
        sdk.task_handler = mock_task_handler
        
        # Create test task
        task_data = {
            "id": str(uuid.uuid4()),
            "type": "test_task",
            "message": "Test A2A task processing"
        }
        
        # Process task
        result = await sdk.a2a_handler.handle_a2a_task(task_data)
        
        # Verify result
        assert "result" in result
        assert result["status"] == "completed"
        
        logger.info("✅ A2A task processing successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ A2A task processing test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_metrics():
    """Test performance metrics tracking"""
    logger.info("🧪 Testing performance metrics...")
    
    try:
        from src.sdk.agent_lobbi_sdk import AgentLobbySDK
        
        # Create SDK
        sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)
        sdk.agent_id = "test_agent_003"
        
        # Generate some metrics
        if sdk.metrics_system:
            sdk.metrics_system.collector.record_metric(
                "response_time", 25.5, tags={"agent_id": sdk.agent_id}
            )
            sdk.metrics_system.collector.record_metric(
                "success_rate", 0.98, tags={"agent_id": sdk.agent_id}
            )
        
        # Get performance metrics
        performance_metrics = sdk.get_performance_metrics()
        
        # Verify structure
        assert "timestamp" in performance_metrics
        assert "performance" in performance_metrics
        assert "user_experience" in performance_metrics
        assert "business_intelligence" in performance_metrics
        
        logger.info("✅ Performance metrics test successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Performance metrics test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_concurrent_operations():
    """Test concurrent operations"""
    logger.info("🧪 Testing concurrent operations...")
    
    try:
        from src.sdk.agent_lobbi_sdk import AgentLobbySDK
        
        # Create SDK
        sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)
        sdk.agent_id = "test_agent_004"
        
        # Test concurrent metric recording
        def record_metrics(batch_id):
            for i in range(10):
                sdk.metrics_system.collector.record_metric(
                    f"concurrent_metric_{batch_id}_{i}",
                    float(i),
                    tags={"batch": str(batch_id)}
                )
        
        # Run concurrent operations
        import threading
        threads = []
        for i in range(5):
            thread = threading.Thread(target=record_metrics, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for completion
        for thread in threads:
            thread.join()
        
        logger.info("✅ Concurrent operations test successful")
        return True
        
    except Exception as e:
        logger.error(f"❌ Concurrent operations test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def run_all_tests():
    """Run all simplified tests"""
    logger.info("🚀 Starting Enhanced A2A+ Implementation Tests...")
    
    tests = [
        ("SDK Initialization", test_enhanced_sdk_initialization),
        ("Metrics System", test_metrics_system),
        ("A2A Agent Card", test_a2a_agent_card),
        ("A2A Task Processing", test_a2a_task_processing),
        ("Performance Metrics", test_performance_metrics),
        ("Concurrent Operations", test_concurrent_operations)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*60}")
        logger.info(f"Running Test: {test_name}")
        logger.info(f"{'='*60}")
        
        try:
            if asyncio.iscoroutinefunction(test_func):
                success = await test_func()
            else:
                success = test_func()
            
            if success:
                passed += 1
                logger.info(f"✅ {test_name}: PASSED")
            else:
                failed += 1
                logger.error(f"❌ {test_name}: FAILED")
                
        except Exception as e:
            failed += 1
            logger.error(f"❌ {test_name}: ERROR - {e}")
    
    logger.info(f"\n{'='*60}")
    logger.info(f"TEST SUMMARY")
    logger.info(f"{'='*60}")
    logger.info(f"✅ Passed: {passed}")
    logger.info(f"❌ Failed: {failed}")
    logger.info(f"📊 Total:  {passed + failed}")
    
    if failed == 0:
        logger.info("🎉 All tests passed! Implementation is ready.")
        return True
    else:
        logger.error(f"🔧 {failed} tests failed. Please fix issues.")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    
    if success:
        print("\n🎉 Enhanced A2A+ Implementation: READY FOR DEPLOYMENT!")
        print("📦 Next steps: PyPI publishing and website integration")
        sys.exit(0)
    else:
        print("\n❌ Enhanced A2A+ Implementation: NEEDS FIXES")
        print("🔧 Please address the failed tests before proceeding")
        sys.exit(1) 