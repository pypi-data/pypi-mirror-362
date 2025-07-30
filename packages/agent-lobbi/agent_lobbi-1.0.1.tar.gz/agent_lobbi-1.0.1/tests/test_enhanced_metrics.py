#!/usr/bin/env python3
"""
Test suite for Agent Lobby Enhanced Metrics System
Validates all metrics collection, analytics, and monitoring capabilities
"""

import asyncio
import pytest
import time
from datetime import datetime
from unittest.mock import Mock, AsyncMock, patch

# Try importing the enhanced metrics system
try:
    from src.core.agent_metrics_enhanced import (
        EnhancedMetricsSystem,
        MetricsCollector,
        A2AMetricsTracker,
        UserExperienceTracker,
        BusinessIntelligenceTracker,
        AlertManager,
        MetricType,
        AlertLevel
    )
    from src.sdk.agent_lobbi_sdk import AgentLobbySDK
except ImportError as e:
    print(f"❌ Import error: {e}")
    pytest.skip("Enhanced metrics system not available", allow_module_level=True)

class TestEnhancedMetricsSystem:
    """Test the complete enhanced metrics system"""
    
    @pytest.fixture
    def metrics_system(self):
        """Create a metrics system for testing"""
        return EnhancedMetricsSystem()
        
    @pytest.fixture
    def metrics_collector(self):
        """Create a metrics collector for testing"""
        return MetricsCollector()
        
    def test_metrics_system_initialization(self, metrics_system):
        """Test metrics system initialization"""
        assert metrics_system.collector is not None
        assert metrics_system.a2a_tracker is not None
        assert metrics_system.ux_tracker is not None
        assert metrics_system.bi_tracker is not None
        assert metrics_system.alert_manager is not None
        
    def test_metrics_collector_basic_operations(self, metrics_collector):
        """Test basic metrics collection operations"""
        # Test metric recording
        metrics_collector.record_metric("test_metric", 100.0, tags={"test": "value"})
        
        # Test metrics retrieval
        metrics = metrics_collector.get_real_time_metrics()
        assert isinstance(metrics, dict)
        
    def test_a2a_metrics_tracking(self, metrics_system):
        """Test A2A-specific metrics tracking"""
        tracker = metrics_system.a2a_tracker
        
        # Test task start tracking
        tracker.track_task_start("test_task", "test_agent", "test_type")
        assert "test_task" in tracker.active_tasks
        
        # Test task completion tracking
        tracker.track_task_completion("test_task", "completed", 1024)
        assert "test_task" not in tracker.active_tasks
        assert len(tracker.completed_tasks) == 1
        
    def test_user_experience_tracking(self, metrics_system):
        """Test user experience metrics tracking"""
        tracker = metrics_system.ux_tracker
        
        # Test session tracking
        tracker.track_user_session_start("user123", "session456")
        assert "session456" in tracker.user_sessions
        
        # Test interaction tracking
        tracker.track_user_interaction("session456", "click", 250.0)
        
        # Test satisfaction scoring
        score = tracker.calculate_satisfaction_score("session456", 0.95, 1000.0)
        assert 0.0 <= score <= 1.0
        
    def test_business_intelligence_tracking(self, metrics_system):
        """Test business intelligence metrics"""
        tracker = metrics_system.bi_tracker
        
        # Test cost tracking
        tracker.track_cost_per_interaction("user_action", 0.05)
        assert tracker.cost_tracking["user_action"] == 0.05
        
        # Test revenue tracking
        tracker.track_revenue_generation("user123", 10.0)
        assert tracker.revenue_tracking["user123"] == 10.0
        
        # Test ROI calculation
        roi = tracker.calculate_roi("24h")
        assert isinstance(roi, float)
        
    def test_alert_manager(self, metrics_system):
        """Test alert management system"""
        alert_manager = metrics_system.alert_manager
        
        # Add alert rule
        alert_manager.add_alert_rule("test_metric", 100.0, AlertLevel.WARNING, "gt")
        assert len(alert_manager.alert_rules) == 5  # 4 default + 1 added
        
        # Test alert checking
        test_metrics = {
            "test_metric": {"last": 150.0}
        }
        alerts = alert_manager.check_alerts(test_metrics)
        assert len(alerts) == 1
        assert alerts[0]["level"] == AlertLevel.WARNING
        
    def test_dashboard_data_generation(self, metrics_system):
        """Test dashboard data generation"""
        # Generate some test data
        metrics_system.collector.record_metric("test_response_time", 100.0)
        metrics_system.collector.record_metric("test_success_rate", 0.95)
        
        # Get dashboard data
        dashboard_data = metrics_system.get_dashboard_data()
        
        # Validate structure
        assert "timestamp" in dashboard_data
        assert "metrics" in dashboard_data
        assert "alerts" in dashboard_data
        assert "system_health" in dashboard_data
        assert "performance_summary" in dashboard_data
        assert "user_experience_summary" in dashboard_data
        assert "business_summary" in dashboard_data
        
    def test_system_health_calculation(self, metrics_system):
        """Test system health calculation"""
        # Mock metrics
        test_metrics = {
            "a2a_task_success_rate": {"avg": 0.95},
            "a2a_task_duration": {"avg": 2000.0}
        }
        
        health = metrics_system._calculate_system_health(test_metrics)
        assert health in ["Excellent", "Good", "Fair", "Poor"]

class TestSDKMetricsIntegration:
    """Test SDK integration with enhanced metrics"""
    
    @pytest.fixture
    def sdk_with_metrics(self):
        """Create SDK with metrics enabled"""
        return AgentLobbySDK(
            enable_metrics=True,
            enable_a2a=True,
            enable_security=False  # Disable for testing
        )
        
    def test_sdk_metrics_initialization(self, sdk_with_metrics):
        """Test SDK metrics system initialization"""
        assert sdk_with_metrics.enable_metrics is True
        assert sdk_with_metrics.metrics_system is not None
        
    def test_sdk_metrics_dashboard(self, sdk_with_metrics):
        """Test SDK metrics dashboard"""
        dashboard = sdk_with_metrics.get_metrics_dashboard()
        assert "timestamp" in dashboard
        assert "metrics" in dashboard
        assert "a2a_metrics" in dashboard
        
    def test_sdk_performance_metrics(self, sdk_with_metrics):
        """Test SDK performance metrics"""
        metrics = sdk_with_metrics.get_performance_metrics()
        assert "timestamp" in metrics
        assert "performance" in metrics
        assert "user_experience" in metrics
        assert "business_intelligence" in metrics
        
    def test_sdk_user_tracking(self, sdk_with_metrics):
        """Test SDK user tracking capabilities"""
        # Test user session tracking
        sdk_with_metrics.track_user_session("user123", "session456")
        
        # Test user interaction tracking
        sdk_with_metrics.track_user_interaction("session456", "click", 250.0)
        
        # Test business metric tracking
        sdk_with_metrics.track_business_metric("cost", 0.05, {"type": "user_action"})
        sdk_with_metrics.track_business_metric("revenue", 1.0, {"user_id": "user123"})
        
    def test_sdk_alerts(self, sdk_with_metrics):
        """Test SDK alert system"""
        alerts = sdk_with_metrics.get_alerts()
        assert isinstance(alerts, list)
        
    @pytest.mark.asyncio
    async def test_sdk_message_metrics(self, sdk_with_metrics):
        """Test message sending metrics"""
        # Mock WebSocket connection
        sdk_with_metrics.websocket_connection = Mock()
        sdk_with_metrics.websocket_connection.send = AsyncMock()
        sdk_with_metrics.connected = True
        sdk_with_metrics.agent_id = "test_agent"
        sdk_with_metrics.session_id = "test_session"
        
        # Send message and verify metrics tracking
        result = await sdk_with_metrics.send_message("test message", "lobby", "test")
        assert result is True
        
        # Verify metrics were recorded
        metrics = sdk_with_metrics.get_performance_metrics()
        assert metrics is not None

class TestA2AMetricsIntegration:
    """Test A2A protocol metrics integration"""
    
    @pytest.fixture
    def a2a_handler(self):
        """Create A2A handler for testing"""
        from src.sdk.agent_lobbi_sdk import A2AProtocolHandler
        
        mock_sdk = Mock()
        mock_sdk.agent_id = "test_agent"
        mock_sdk.a2a_port = 8090
        
        metrics_system = EnhancedMetricsSystem()
        return A2AProtocolHandler(mock_sdk, metrics_system)
        
    @pytest.mark.asyncio
    async def test_a2a_task_handling_metrics(self, a2a_handler):
        """Test A2A task handling with metrics"""
        task_data = {
            "id": "test_task",
            "type": "test_type",
            "message": "test message"
        }
        
        # Handle task and verify metrics
        result = await a2a_handler.handle_a2a_task(task_data)
        assert result is not None
        assert "status" in result
        
    def test_a2a_agent_card_enhancement(self, a2a_handler):
        """Test A2A agent card with metrics capabilities"""
        agent_card = a2a_handler.agent_card
        
        # Verify enhanced capabilities
        assert "real_time_metrics" in agent_card["capabilities"]
        assert "advanced_analytics" in agent_card["capabilities"]
        assert "agent_lobby" in agent_card["extensions"]
        
        # Verify metrics-related extensions
        extensions = agent_card["extensions"]["agent_lobby"]
        assert "analytics" in extensions
        assert extensions["performance_metrics"]["metrics_enabled"] is True

class TestPerformanceAndScaling:
    """Test performance and scaling of metrics system"""
    
    @pytest.fixture
    def high_load_metrics_system(self):
        """Create metrics system configured for high load"""
        return EnhancedMetricsSystem()
        
    def test_high_volume_metrics_collection(self, high_load_metrics_system):
        """Test metrics collection under high load"""
        collector = high_load_metrics_system.collector
        
        # Record many metrics quickly
        start_time = time.time()
        for i in range(1000):
            collector.record_metric(f"test_metric_{i % 10}", float(i), tags={"batch": "test"})
        
        collection_time = time.time() - start_time
        assert collection_time < 1.0  # Should collect 1000 metrics in under 1 second
        
        # Verify metrics were recorded
        metrics = collector.get_real_time_metrics()
        assert len(metrics) > 0
        
    def test_metrics_memory_management(self, high_load_metrics_system):
        """Test memory management in metrics system"""
        collector = high_load_metrics_system.collector
        
        # Record metrics over time to test buffer management
        for i in range(500):
            collector.record_metric("memory_test", float(i))
            
        # Verify buffer is managed properly
        assert len(collector.metrics_buffer) <= 10000  # Should not exceed buffer size
        
    def test_concurrent_metrics_access(self, high_load_metrics_system):
        """Test concurrent access to metrics system"""
        import threading
        
        collector = high_load_metrics_system.collector
        results = []
        
        def record_metrics():
            for i in range(100):
                collector.record_metric("concurrent_test", float(i))
                
        def read_metrics():
            for i in range(10):
                metrics = collector.get_real_time_metrics()
                results.append(len(metrics))
                
        # Start concurrent threads
        threads = []
        for _ in range(5):
            threads.append(threading.Thread(target=record_metrics))
            threads.append(threading.Thread(target=read_metrics))
            
        # Run all threads
        for thread in threads:
            thread.start()
            
        for thread in threads:
            thread.join()
            
        # Verify no errors occurred
        assert len(results) > 0

# Integration test
@pytest.mark.asyncio
async def test_complete_metrics_workflow():
    """Test complete end-to-end metrics workflow"""
    # Create SDK with metrics
    sdk = AgentLobbySDK(
        enable_metrics=True,
        enable_a2a=True,
        enable_security=False
    )
    
    # Start metrics collection
    sdk.metrics_system.start()
    
    try:
        # Simulate user session
        sdk.track_user_session("user123", "session456")
        
        # Simulate interactions
        sdk.track_user_interaction("session456", "click", 250.0)
        sdk.track_user_interaction("session456", "scroll", 100.0)
        
        # Simulate business activities
        sdk.track_business_metric("cost", 0.05, {"type": "user_action"})
        sdk.track_business_metric("revenue", 2.0, {"user_id": "user123"})
        
        # Allow some time for metrics processing
        await asyncio.sleep(0.1)
        
        # Get comprehensive metrics
        dashboard = sdk.get_metrics_dashboard()
        performance = sdk.get_performance_metrics()
        alerts = sdk.get_alerts()
        
        # Verify all components are working
        assert dashboard is not None
        assert performance is not None
        assert isinstance(alerts, list)
        
        # Verify data structure
        assert "timestamp" in dashboard
        assert "metrics" in dashboard
        assert "system_health" in dashboard
        
    finally:
        # Clean up
        sdk.metrics_system.stop()

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
    print("✅ Enhanced Metrics System Tests Complete!") 