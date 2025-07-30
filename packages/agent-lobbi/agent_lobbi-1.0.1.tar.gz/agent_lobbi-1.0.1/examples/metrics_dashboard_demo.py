#!/usr/bin/env python3
"""
Agent Lobby Enhanced Metrics Dashboard Demo
Real-time monitoring and analytics for A2A+ agents
"""

import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Any
import logging
from dataclasses import asdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Try to import our SDK
try:
    from src.sdk.agent_lobbi_sdk import AgentLobbySDK
    from src.core.agent_metrics_enhanced import (
        EnhancedMetricsSystem, 
        AlertLevel,
        MetricType
    )
except ImportError:
    print("⚠️  Could not import Agent Lobby SDK. Please ensure the package is installed.")
    print("   This demo will run in simulation mode.")
    import sys
    sys.exit(1)

class MetricsDashboardDemo:
    """
    Interactive demo showcasing Agent Lobby's enhanced metrics capabilities
    """
    
    def __init__(self):
        self.agents = {}
        self.demo_running = False
        self.metrics_data = {}
        
    async def run_demo(self):
        """Run the complete metrics dashboard demo"""
        print("🚀 Agent Lobby Enhanced Metrics Dashboard Demo")
        print("=" * 60)
        
        await self._setup_demo_environment()
        await self._run_interactive_demo()
        await self._cleanup_demo()
        
    async def _setup_demo_environment(self):
        """Set up the demo environment with multiple agents"""
        print("\n📊 Setting up Enhanced Metrics Demo Environment...")
        
        # Create multiple agents with different capabilities
        agent_configs = [
            {
                'agent_id': 'analytics_agent_001',
                'name': 'Analytics Agent',
                'type': 'Analyst',
                'capabilities': ['data_analysis', 'pattern_recognition', 'reporting'],
                'a2a_port': 8091
            },
            {
                'agent_id': 'customer_service_agent_001',
                'name': 'Customer Service Agent',
                'type': 'Support',
                'capabilities': ['customer_support', 'issue_resolution', 'communication'],
                'a2a_port': 8092
            },
            {
                'agent_id': 'sales_agent_001',
                'name': 'Sales Agent',
                'type': 'Sales',
                'capabilities': ['lead_generation', 'sales_conversion', 'customer_engagement'],
                'a2a_port': 8093
            }
        ]
        
        # Initialize agents with metrics enabled
        for config in agent_configs:
            try:
                sdk = AgentLobbySDK(
                    enable_metrics=True,
                    enable_a2a=True,
                    a2a_port=config['a2a_port']
                )
                
                # Register agent
                success = await sdk.register_agent(
                    agent_id=config['agent_id'],
                    name=config['name'],
                    agent_type=config['type'],
                    capabilities=config['capabilities'],
                    auto_start_a2a=True
                )
                
                if success:
                    self.agents[config['agent_id']] = sdk
                    print(f"✅ {config['name']} registered with A2A at port {config['a2a_port']}")
                else:
                    print(f"❌ Failed to register {config['name']}")
                    
            except Exception as e:
                print(f"❌ Error setting up {config['name']}: {e}")
                
        print(f"\n🎯 Demo environment ready with {len(self.agents)} agents")
        
    async def _run_interactive_demo(self):
        """Run the interactive demo with real-time metrics"""
        self.demo_running = True
        
        print("\n🌟 Starting Interactive Metrics Demo...")
        print("   - Real-time performance monitoring")
        print("   - User interaction tracking")
        print("   - Business intelligence analytics")
        print("   - A2A protocol metrics")
        print("   - Advanced alerting system")
        
        # Start demo tasks
        demo_tasks = [
            self._simulate_user_interactions(),
            self._simulate_a2a_communications(),
            self._simulate_business_activities(),
            self._display_real_time_dashboard(),
            self._run_performance_tests()
        ]
        
        try:
            await asyncio.gather(*demo_tasks)
        except KeyboardInterrupt:
            print("\n⏹️  Demo interrupted by user")
            self.demo_running = False
            
    async def _simulate_user_interactions(self):
        """Simulate various user interactions"""
        print("\n👥 Simulating User Interactions...")
        
        user_scenarios = [
            "User asking for sales analytics",
            "Customer support inquiry",
            "Data analysis request",
            "Performance report generation",
            "Customer feedback analysis"
        ]
        
        while self.demo_running:
            try:
                # Pick random agent and scenario
                agent_id = random.choice(list(self.agents.keys()))
                scenario = random.choice(user_scenarios)
                sdk = self.agents[agent_id]
                
                # Track user session
                user_id = f"user_{random.randint(1000, 9999)}"
                session_id = f"session_{int(time.time())}"
                
                sdk.track_user_session(user_id, session_id)
                
                # Simulate interaction
                start_time = time.time()
                await sdk.send_message(scenario, "lobby", "user_request")
                response_time = (time.time() - start_time) * 1000
                
                # Track interaction metrics
                sdk.track_user_interaction(session_id, "request", response_time)
                
                # Track business metrics
                sdk.track_business_metric("cost", random.uniform(0.05, 0.20), {
                    'type': 'user_interaction',
                    'user_id': user_id
                })
                
                await asyncio.sleep(random.uniform(2, 5))
                
            except Exception as e:
                logger.error(f"Error in user interaction simulation: {e}")
                await asyncio.sleep(1)
                
    async def _simulate_a2a_communications(self):
        """Simulate A2A protocol communications between agents"""
        print("\n🔄 Simulating A2A Communications...")
        
        a2a_scenarios = [
            "Cross-agent data sharing",
            "Collaborative task processing",
            "Agent capability discovery",
            "Task delegation workflow",
            "Multi-agent coordination"
        ]
        
        while self.demo_running:
            try:
                # Pick two different agents
                agent_ids = list(self.agents.keys())
                if len(agent_ids) >= 2:
                    agent1_id = random.choice(agent_ids)
                    agent2_id = random.choice([aid for aid in agent_ids if aid != agent1_id])
                    
                    scenario = random.choice(a2a_scenarios)
                    
                    # Simulate A2A task
                    sdk1 = self.agents[agent1_id]
                    sdk2 = self.agents[agent2_id]
                    
                    # Create A2A task
                    task_data = {
                        'id': f"a2a_task_{int(time.time())}",
                        'type': 'collaboration',
                        'message': scenario,
                        'from_agent': agent1_id,
                        'to_agent': agent2_id
                    }
                    
                    # Process task (simulated)
                    if sdk1.a2a_handler:
                        result = await sdk1.a2a_handler.handle_a2a_task(task_data)
                        
                        # Track revenue from successful collaboration
                        if result.get('status') == 'completed':
                            sdk1.track_business_metric("revenue", random.uniform(1.0, 5.0), {
                                'user_id': f"system_{agent1_id}",
                                'type': 'a2a_collaboration'
                            })
                    
                await asyncio.sleep(random.uniform(3, 7))
                
            except Exception as e:
                logger.error(f"Error in A2A communication simulation: {e}")
                await asyncio.sleep(1)
                
    async def _simulate_business_activities(self):
        """Simulate business activities and track metrics"""
        print("\n💼 Simulating Business Activities...")
        
        business_scenarios = [
            "Lead qualification",
            "Customer onboarding",
            "Support ticket resolution",
            "Sales opportunity analysis",
            "Customer retention analysis"
        ]
        
        while self.demo_running:
            try:
                # Pick random agent
                agent_id = random.choice(list(self.agents.keys()))
                scenario = random.choice(business_scenarios)
                sdk = self.agents[agent_id]
                
                # Simulate business activity
                activity_cost = random.uniform(0.10, 2.00)
                activity_revenue = random.uniform(0.50, 10.00)
                
                sdk.track_business_metric("cost", activity_cost, {
                    'type': scenario.lower().replace(' ', '_'),
                    'agent_id': agent_id
                })
                
                if random.random() > 0.3:  # 70% success rate
                    sdk.track_business_metric("revenue", activity_revenue, {
                        'user_id': f"business_{random.randint(1000, 9999)}",
                        'type': scenario.lower().replace(' ', '_')
                    })
                
                await asyncio.sleep(random.uniform(4, 8))
                
            except Exception as e:
                logger.error(f"Error in business activity simulation: {e}")
                await asyncio.sleep(1)
                
    async def _display_real_time_dashboard(self):
        """Display real-time dashboard with metrics"""
        print("\n📊 Real-time Metrics Dashboard Active...")
        
        dashboard_counter = 0
        
        while self.demo_running:
            try:
                dashboard_counter += 1
                
                # Clear screen for dashboard update
                if dashboard_counter % 5 == 0:  # Update every 5 iterations
                    print("\n" + "=" * 80)
                    print(f"📊 AGENT LOBBY METRICS DASHBOARD - Update #{dashboard_counter // 5}")
                    print("=" * 80)
                    
                    # Display metrics for each agent
                    for agent_id, sdk in self.agents.items():
                        try:
                            dashboard_data = sdk.get_metrics_dashboard()
                            performance_data = sdk.get_performance_metrics()
                            alerts = sdk.get_alerts()
                            
                            print(f"\n🤖 Agent: {agent_id}")
                            print(f"   System Health: {dashboard_data.get('system_health', 'Unknown')}")
                            
                            # Performance metrics
                            perf = performance_data.get('performance', {})
                            print(f"   📈 Performance:")
                            print(f"      • Avg Response Time: {perf.get('avg_response_time', 0):.2f}ms")
                            print(f"      • Success Rate: {perf.get('success_rate', 0):.2%}")
                            print(f"      • Throughput: {perf.get('throughput', 0)} req/min")
                            print(f"      • Active Tasks: {perf.get('active_tasks', 0)}")
                            
                            # User experience metrics
                            ux = performance_data.get('user_experience', {})
                            print(f"   👥 User Experience:")
                            print(f"      • Satisfaction Score: {ux.get('satisfaction_score', 0):.2f}/1.0")
                            print(f"      • Interaction Frequency: {ux.get('interaction_frequency', 0)}")
                            
                            # Business intelligence
                            bi = performance_data.get('business_intelligence', {})
                            print(f"   💰 Business Intelligence:")
                            print(f"      • Cost Per Interaction: ${bi.get('cost_per_interaction', 0):.3f}")
                            print(f"      • Revenue Generated: ${bi.get('revenue_generated', 0):.2f}")
                            print(f"      • ROI: {bi.get('roi', 0):.2%}")
                            
                            # A2A metrics
                            a2a = dashboard_data.get('a2a_metrics', {})
                            print(f"   🔄 A2A Protocol:")
                            print(f"      • Server Status: {a2a.get('a2a_server_status', 'Unknown')}")
                            print(f"      • Enhanced Capabilities: {len(a2a.get('enhanced_capabilities', []))}")
                            
                            # Alerts
                            if alerts:
                                print(f"   🚨 Active Alerts: {len(alerts)}")
                                for alert in alerts[:3]:  # Show first 3 alerts
                                    print(f"      • {alert['level'].upper()}: {alert['message']}")
                            else:
                                print(f"   ✅ No Active Alerts")
                            
                        except Exception as e:
                            print(f"   ❌ Error retrieving metrics: {e}")
                    
                    # Overall system summary
                    print(f"\n📋 SYSTEM SUMMARY:")
                    print(f"   • Total Agents: {len(self.agents)}")
                    print(f"   • Demo Runtime: {time.time() - getattr(self, '_demo_start_time', time.time()):.0f}s")
                    print(f"   • Metrics Collection: Active")
                    print(f"   • A2A Protocol: Enabled")
                    print("=" * 80)
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error in dashboard display: {e}")
                await asyncio.sleep(1)
                
    async def _run_performance_tests(self):
        """Run performance tests to generate metrics"""
        print("\n⚡ Running Performance Tests...")
        
        test_counter = 0
        
        while self.demo_running:
            try:
                test_counter += 1
                
                # Run performance test every 10 seconds
                if test_counter % 5 == 0:
                    print(f"\n🧪 Performance Test #{test_counter // 5}")
                    
                    for agent_id, sdk in self.agents.items():
                        # Simulate burst of activities
                        tasks = []
                        for i in range(5):
                            tasks.append(sdk.send_message(
                                f"Performance test message {i}",
                                "lobby",
                                "performance_test"
                            ))
                        
                        # Execute tasks concurrently
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        
                        # Track performance results
                        success_count = sum(1 for r in results if r is True)
                        print(f"   Agent {agent_id}: {success_count}/5 messages successful")
                
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error in performance test: {e}")
                await asyncio.sleep(1)
                
    async def _cleanup_demo(self):
        """Clean up demo environment"""
        print("\n🧹 Cleaning up demo environment...")
        
        # Shutdown all agents
        for agent_id, sdk in self.agents.items():
            try:
                await sdk.shutdown()
                print(f"✅ Agent {agent_id} shut down")
            except Exception as e:
                print(f"❌ Error shutting down {agent_id}: {e}")
                
        self.agents.clear()
        print("✅ Demo cleanup complete")

async def main():
    """Main demo function"""
    demo = MetricsDashboardDemo()
    demo._demo_start_time = time.time()
    
    try:
        await demo.run_demo()
    except KeyboardInterrupt:
        print("\n⏹️  Demo interrupted by user")
    except Exception as e:
        print(f"❌ Demo error: {e}")
    finally:
        await demo._cleanup_demo()

if __name__ == "__main__":
    print("🚀 Agent Lobby Enhanced Metrics Dashboard Demo")
    print("   Press Ctrl+C to stop the demo")
    print("   Starting in 3 seconds...")
    
    for i in range(3, 0, -1):
        print(f"   {i}...")
        time.sleep(1)
    
    print("\n🎬 Demo starting now!")
    asyncio.run(main()) 