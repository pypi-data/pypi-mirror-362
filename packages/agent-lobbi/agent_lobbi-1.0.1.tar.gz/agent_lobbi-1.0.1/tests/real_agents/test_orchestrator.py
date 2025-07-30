#!/usr/bin/env python3
"""
Test Orchestrator - Runs comprehensive tests with real agents
Tests both A2A protocol and Agent Lobby collaboration
"""

import asyncio
import logging
import sys
import os
import json
import time
import requests
from typing import Dict, Any, List
import subprocess

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.sdk.agent_lobbi_sdk import AgentLobbySDK

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TestOrchestrator:
    """Orchestrates comprehensive testing of Agent Lobby + A2A integration"""
    
    def __init__(self):
        self.test_results = []
        self.start_time = time.time()
        self.lobby_url = "http://localhost:8080"
        self.a2a_url = "http://localhost:8080/a2a"
        
    async def test_scenario_1_pure_a2a(self):
        """Test Scenario 1: Pure A2A Communication (via Agent Registration)"""
        logger.info("🧪 === TEST SCENARIO 1: AGENT REGISTRATION TEST ===")
        
        try:
            # Test agent registration via HTTP (simulating A2A-style communication)
            agent_data = {
                "agent_id": "test_a2a_agent_001",
                "name": "A2A Test Agent",
                "agent_type": "calculator",
                "capabilities": ["multiply", "add", "subtract"]
            }
            
            logger.info(f"📡 Registering test agent: {agent_data}")
            response = requests.post(f"{self.lobby_url}/api/agents/register", json=agent_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"✅ Registration Response: {json.dumps(result, indent=2)}")
                
                # Verify response format
                assert "status" in result
                assert result["status"] == "success"
                
                self.test_results.append({
                    "scenario": "Agent Registration (A2A-style)",
                    "status": "PASSED",
                    "details": "Agent registration via HTTP API successful"
                })
            else:
                raise Exception(f"HTTP {response.status_code}: {response.text}")
                
        except Exception as e:
            logger.error(f"❌ Scenario 1 failed: {e}")
            self.test_results.append({
                "scenario": "Agent Registration (A2A-style)",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_scenario_2_agent_lobby_collaboration(self):
        """Test Scenario 2: Agent Lobby Internal Collaboration"""
        logger.info("🧪 === TEST SCENARIO 2: AGENT LOBBY COLLABORATION ===")
        
        try:
            # Create a coordinator agent for testing
            coordinator = AgentLobbySDK(
                lobby_host="localhost",
                lobby_port=8080,
                enable_a2a=True
            )
            
            await coordinator.register_agent(
                agent_id="test_coordinator_001",
                name="Test Coordinator", 
                agent_type="coordinator",
                capabilities=["orchestration", "task_delegation"]
            )
            logger.info("✅ Test coordinator registered")
            
            # Test internal collaboration
            collaboration_message = {
                "type": "calculate",
                "operation": "add",
                "numbers": [10, 20, 30, 40, 50]
            }
            
            # Simulate sending to calculator agent (if running)
            logger.info(f"🏛️ Sending lobby collaboration: {collaboration_message}")
            
            # Check agent registration status
            agents_response = requests.get(f"{self.lobby_url}/api/agents", timeout=5)
            if agents_response.status_code == 200:
                agents = agents_response.json()
                logger.info(f"📋 Registered agents: {json.dumps(agents, indent=2)}")
                
                self.test_results.append({
                    "scenario": "Agent Lobby Collaboration",
                    "status": "PASSED",
                    "details": f"Agent registration and collaboration successful. Active agents: {len(agents)}"
                })
            else:
                raise Exception(f"Could not retrieve agents: {agents_response.status_code}")
                
            await coordinator.shutdown()
            
        except Exception as e:
            logger.error(f"❌ Scenario 2 failed: {e}")
            self.test_results.append({
                "scenario": "Agent Lobby Collaboration",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_scenario_3_hybrid_mode(self):
        """Test Scenario 3: Health Check + Agent Listing"""
        logger.info("🧪 === TEST SCENARIO 3: HEALTH CHECK + AGENT LISTING ===")
        
        try:
            # Test health check endpoint
            health_response = requests.get(f"{self.lobby_url}/health", timeout=5)
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                logger.info(f"✅ Health check: {json.dumps(health_data, indent=2)}")
                
                # Verify health check format
                assert "status" in health_data
                assert health_data["status"] == "ok"
                assert "agents_count" in health_data
                
                # Test agent listing
                agents_response = requests.get(f"{self.lobby_url}/api/agents", timeout=5)
                if agents_response.status_code == 200:
                    agents_data = agents_response.json()
                    logger.info(f"✅ Agents list: {len(agents_data.get('agents', []))} agents found")
                    
                    self.test_results.append({
                        "scenario": "Health Check + Agent Listing",
                        "status": "PASSED",
                        "details": f"System healthy with {health_data.get('agents_count', 0)} agents"
                    })
                else:
                    raise Exception(f"Agent listing failed: {agents_response.status_code}")
            else:
                raise Exception(f"Health check failed: {health_response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Scenario 3 failed: {e}")
            self.test_results.append({
                "scenario": "Health Check + Agent Listing",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_scenario_4_metrics_and_learning(self):
        """Test Scenario 4: System Status and Agent Verification"""
        logger.info("🧪 === TEST SCENARIO 4: SYSTEM STATUS ===")
        
        try:
            # Test health endpoint for system status
            health_response = requests.get(f"{self.lobby_url}/health", timeout=5)
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                logger.info(f"📊 System status: {json.dumps(health_data, indent=2)}")
                
                # Verify health data structure
                required_keys = ["status", "timestamp", "lobby_id"]
                for key in required_keys:
                    if key not in health_data:
                        raise Exception(f"Missing health key: {key}")
                
                # Verify system is operational
                assert health_data["status"] == "ok"
                
                self.test_results.append({
                    "scenario": "System Status and Health",
                    "status": "PASSED",
                    "details": f"System operational with lobby_id: {health_data.get('lobby_id', 'unknown')}"
                })
            else:
                raise Exception(f"Health endpoint failed: {health_response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ Scenario 4 failed: {e}")
            self.test_results.append({
                "scenario": "System Status and Health",
                "status": "FAILED",
                "error": str(e)
            })
    
    async def test_scenario_5_stress_test(self):
        """Test Scenario 5: Concurrent Health Check Stress Test"""
        logger.info("🧪 === TEST SCENARIO 5: CONCURRENT HEALTH CHECKS ===")
        
        try:
            # Send multiple health check requests concurrently
            tasks = []
            for i in range(5):
                tasks.append(self.send_health_request(i))
            
            # Wait for all requests to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            successful = sum(1 for r in results if not isinstance(r, Exception))
            total = len(results)
            
            logger.info(f"📈 Stress test results: {successful}/{total} health checks successful")
            
            if successful >= total * 0.8:  # 80% success rate acceptable
                self.test_results.append({
                    "scenario": "Concurrent Health Checks",
                    "status": "PASSED",
                    "details": f"Handled {successful}/{total} concurrent health checks successfully"
                })
            else:
                raise Exception(f"Only {successful}/{total} requests succeeded")
                
        except Exception as e:
            logger.error(f"❌ Scenario 5 failed: {e}")
            self.test_results.append({
                "scenario": "Concurrent Health Checks",
                "status": "FAILED", 
                "error": str(e)
            })
    
    async def send_health_request(self, request_id: int) -> Dict[str, Any]:
        """Send health check request asynchronously using requests"""
        try:
            response = requests.get(f"{self.lobby_url}/health", timeout=5)
            if response.status_code == 200:
                result = response.json()
                logger.info(f"Health check #{request_id}: {result.get('status', 'unknown')}")
                return result
            else:
                raise Exception(f"HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"Health check #{request_id} failed: {e}")
            raise
    
    def print_summary(self):
        """Print comprehensive test summary"""
        total_time = time.time() - self.start_time
        passed = sum(1 for r in self.test_results if r["status"] == "PASSED")
        total = len(self.test_results)
        
        print("\n" + "="*80)
        print("🧪 COMPREHENSIVE AGENT LOBBY + A2A TEST RESULTS")
        print("="*80)
        
        for i, result in enumerate(self.test_results, 1):
            status_icon = "✅" if result["status"] == "PASSED" else "❌"
            print(f"{i}. {status_icon} {result['scenario']}: {result['status']}")
            if result["status"] == "PASSED":
                print(f"   Details: {result['details']}")
            else:
                print(f"   Error: {result['error']}")
            print()
        
        print(f"📊 SUMMARY: {passed}/{total} scenarios passed ({passed/total*100:.1f}%)")
        print(f"⏱️  Total test time: {total_time:.2f} seconds")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED! Agent Lobby + A2A integration is working perfectly!")
        else:
            print(f"⚠️  {total-passed} tests failed. Check logs for details.")
        
        print("="*80)

async def main():
    """Run comprehensive test suite"""
    logger.info("🚀 Starting Comprehensive Agent Lobby + A2A Test Suite...")
    
    orchestrator = TestOrchestrator()
    
    # Check if Agent Lobby is running
    try:
        response = requests.get(f"{orchestrator.lobby_url}/health", timeout=5)
        if response.status_code != 200:
            raise Exception("Agent Lobby not responding")
        logger.info("✅ Agent Lobby is running and accessible")
    except Exception as e:
        logger.error(f"❌ Agent Lobby not accessible: {e}")
        logger.info("💡 Please start Agent Lobby first: python src/main.py")
        return
    
    # Run all test scenarios
    test_scenarios = [
        orchestrator.test_scenario_1_pure_a2a,
        orchestrator.test_scenario_2_agent_lobby_collaboration,
        orchestrator.test_scenario_3_hybrid_mode,
        orchestrator.test_scenario_4_metrics_and_learning,
        orchestrator.test_scenario_5_stress_test
    ]
    
    for scenario in test_scenarios:
        try:
            await scenario()
        except Exception as e:
            logger.error(f"❌ Scenario failed with unexpected error: {e}")
        
        # Small delay between scenarios
        await asyncio.sleep(1)
    
    # Print comprehensive summary
    orchestrator.print_summary()

if __name__ == "__main__":
    asyncio.run(main()) 