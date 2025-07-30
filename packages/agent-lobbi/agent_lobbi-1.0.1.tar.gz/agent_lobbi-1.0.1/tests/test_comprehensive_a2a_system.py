#!/usr/bin/env python3
"""
COMPREHENSIVE A2A API SYSTEM TESTING SUITE
==========================================
Robust unit tests, integration tests, and stress tests for the 
Enhanced A2A API Bridge and Agent Lobby integration.
"""

import asyncio
import json
import pytest
import time
import random
import httpx
import websockets
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any
import logging
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.lobby import Lobby
from api.enhanced_a2a_api_bridge import EnhancedA2AAPIBridge
import uvicorn

# Configure test logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ComprehensiveA2ATestSuite:
    """Comprehensive testing suite for the A2A API system"""
    
    def __init__(self):
        self.lobby = None
        self.a2a_bridge = None
        self.lobby_task = None
        self.bridge_task = None
        self.test_results = {
            "unit_tests": {},
            "integration_tests": {},
            "stress_tests": {},
            "performance_metrics": {}
        }
        
        # Test configuration
        self.lobby_url = "http://localhost:8080"
        self.bridge_url = "http://localhost:8090"
        self.ws_url = "ws://localhost:8081"
        
    async def setup_test_environment(self):
        """Setup the test environment with lobby and A2A bridge"""
        logger.info("🔧 Setting up test environment...")
        
        try:
            # Initialize lobby
            self.lobby = Lobby(host="localhost", http_port=8080, ws_port=8081)
            self.lobby_task = asyncio.create_task(self.lobby.start())
            await asyncio.sleep(2)  # Give lobby time to start
            
            # Initialize A2A bridge
            self.a2a_bridge = EnhancedA2AAPIBridge(
                lobby_instance=self.lobby,
                lobby_host="localhost",
                lobby_http_port=8080,
                lobby_ws_port=8081
            )
            
            # Start A2A bridge
            config = uvicorn.Config(
                self.a2a_bridge.app,
                host="localhost",
                port=8090,
                log_level="error",  # Reduce noise during tests
                access_log=False
            )
            
            server = uvicorn.Server(config)
            self.bridge_task = asyncio.create_task(server.serve())
            await asyncio.sleep(2)  # Give bridge time to start
            
            logger.info("✅ Test environment setup complete")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to setup test environment: {e}")
            return False
    
    async def teardown_test_environment(self):
        """Teardown test environment"""
        logger.info("🧹 Tearing down test environment...")
        
        # Stop bridge
        if self.bridge_task and not self.bridge_task.done():
            self.bridge_task.cancel()
            try:
                await self.bridge_task
            except asyncio.CancelledError:
                pass
        
        # Stop lobby
        if self.lobby_task and not self.lobby_task.done():
            self.lobby_task.cancel()
            try:
                await self.lobby_task
            except asyncio.CancelledError:
                pass
        
        if self.lobby:
            await self.lobby.shutdown()
            
        logger.info("✅ Test environment teardown complete")

    # ================================
    # UNIT TESTS
    # ================================
    
    async def test_unit_lobby_initialization(self):
        """Unit test: Lobby initialization"""
        test_name = "lobby_initialization"
        logger.info(f"🧪 Unit Test: {test_name}")
        
        try:
            # Test lobby attributes
            assert self.lobby is not None, "Lobby should be initialized"
            assert hasattr(self.lobby, 'agents'), "Lobby should have agents dict"
            assert hasattr(self.lobby, 'live_agent_connections'), "Lobby should have connection tracking"
            assert hasattr(self.lobby, 'collaboration_engine'), "Lobby should have collaboration engine"
            
            self.test_results["unit_tests"][test_name] = {"status": "PASS", "details": "All assertions passed"}
            logger.info(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results["unit_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_unit_a2a_bridge_initialization(self):
        """Unit test: A2A Bridge initialization"""
        test_name = "a2a_bridge_initialization"
        logger.info(f"🧪 Unit Test: {test_name}")
        
        try:
            # Test bridge attributes
            assert self.a2a_bridge is not None, "A2A Bridge should be initialized"
            assert self.a2a_bridge.lobby_instance == self.lobby, "Bridge should reference lobby"
            assert hasattr(self.a2a_bridge, 'metrics'), "Bridge should have metrics"
            assert hasattr(self.a2a_bridge, 'app'), "Bridge should have FastAPI app"
            
            self.test_results["unit_tests"][test_name] = {"status": "PASS", "details": "All assertions passed"}
            logger.info(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results["unit_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_unit_agent_registration(self):
        """Unit test: Agent registration functionality"""
        test_name = "agent_registration"
        logger.info(f"🧪 Unit Test: {test_name}")
        
        try:
            # Test agent registration
            agent_data = {
                "agent_id": "test_unit_agent",
                "name": "Test Unit Agent",
                "agent_type": "test",
                "capabilities": ["testing", "unit_testing"]
            }
            
            result = await self.lobby.register_agent(agent_data)
            
            assert result["status"] == "success", f"Registration should succeed: {result}"
            assert "test_unit_agent" in self.lobby.agents, "Agent should be in lobby.agents"
            
            # Verify agent data
            stored_agent = self.lobby.agents["test_unit_agent"]
            assert stored_agent["name"] == "Test Unit Agent", "Agent name should match"
            assert "testing" in stored_agent["capabilities"], "Agent capabilities should match"
            
            self.test_results["unit_tests"][test_name] = {"status": "PASS", "details": "Agent registration successful"}
            logger.info(f"✅ {test_name}: PASS")
            
        except Exception as e:
            self.test_results["unit_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")

    # ================================
    # INTEGRATION TESTS
    # ================================
    
    async def test_integration_a2a_discovery(self):
        """Integration test: A2A discovery endpoint"""
        test_name = "a2a_discovery"
        logger.info(f"🔗 Integration Test: {test_name}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Test A2A discovery endpoint
                response = await client.get(f"{self.bridge_url}/.well-known/agent.json")
                
                assert response.status_code == 200, f"Discovery should return 200: {response.status_code}"
                
                data = response.json()
                assert "name" in data, "Discovery should include name"
                assert "capabilities" in data, "Discovery should include capabilities"
                assert "endpoints" in data, "Discovery should include endpoints"
                assert data["capabilities"]["bridge_mode"] is True, "Should indicate bridge mode"
                
                self.test_results["integration_tests"][test_name] = {
                    "status": "PASS", 
                    "response_time": response.elapsed.total_seconds(),
                    "data": data
                }
                logger.info(f"✅ {test_name}: PASS")
                
        except Exception as e:
            self.test_results["integration_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_integration_a2a_status(self):
        """Integration test: A2A status endpoint"""
        test_name = "a2a_status"
        logger.info(f"🔗 Integration Test: {test_name}")
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.bridge_url}/api/a2a/status")
                
                assert response.status_code == 200, f"Status should return 200: {response.status_code}"
                
                data = response.json()
                assert data["status"] == "operational", "Should be operational"
                assert data["protocol"] == "A2A", "Should indicate A2A protocol"
                assert "agent_count" in data, "Should include agent count"
                assert "capabilities" in data, "Should include capabilities list"
                
                self.test_results["integration_tests"][test_name] = {
                    "status": "PASS",
                    "response_time": response.elapsed.total_seconds(),
                    "agent_count": data["agent_count"]
                }
                logger.info(f"✅ {test_name}: PASS")
                
        except Exception as e:
            self.test_results["integration_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_integration_agent_registration_via_api(self):
        """Integration test: Agent registration via HTTP API"""
        test_name = "agent_registration_api"
        logger.info(f"🔗 Integration Test: {test_name}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Register test agent via lobby HTTP API
                agent_data = {
                    "agent_id": "test_integration_agent",
                    "name": "Test Integration Agent",
                    "agent_type": "integration_test",
                    "capabilities": ["data_analysis", "integration_testing"]
                }
                
                response = await client.post(f"{self.lobby_url}/api/agents/register", json=agent_data)
                
                assert response.status_code == 200, f"Registration should return 200: {response.status_code}"
                
                data = response.json()
                assert data["status"] == "success", f"Registration should succeed: {data}"
                
                # Verify agent appears in discovery
                discovery_response = await client.get(f"{self.bridge_url}/api/a2a/discover")
                discovery_data = discovery_response.json()
                
                agent_found = False
                for agent in discovery_data["agents"]:
                    if agent["agent_id"] == "test_integration_agent":
                        agent_found = True
                        assert "data_analysis" in agent["capabilities"], "Agent capabilities should be discoverable"
                        break
                
                assert agent_found, "Registered agent should appear in A2A discovery"
                
                self.test_results["integration_tests"][test_name] = {
                    "status": "PASS",
                    "agent_registered": True,
                    "discoverable_via_a2a": True
                }
                logger.info(f"✅ {test_name}: PASS")
                
        except Exception as e:
            self.test_results["integration_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_integration_a2a_task_delegation(self):
        """Integration test: A2A task delegation"""
        test_name = "a2a_task_delegation"
        logger.info(f"🔗 Integration Test: {test_name}")
        
        try:
            async with httpx.AsyncClient() as client:
                # Ensure we have a test agent registered
                agent_data = {
                    "agent_id": "test_delegation_agent",
                    "name": "Test Delegation Agent",
                    "agent_type": "delegation_test",
                    "capabilities": ["task_processing", "delegation_testing"]
                }
                
                await client.post(f"{self.lobby_url}/api/agents/register", json=agent_data)
                
                # Test A2A task delegation
                task_data = {
                    "title": "Test A2A Task",
                    "description": "Integration test task for A2A delegation",
                    "required_capabilities": ["task_processing"],
                    "input": {"test_data": "integration_test"},
                    "sender_id": "integration_test_client"
                }
                
                response = await client.post(f"{self.bridge_url}/api/a2a/delegate", json=task_data)
                
                assert response.status_code == 200, f"Delegation should return 200: {response.status_code}"
                
                data = response.json()
                assert data["success"] is True, f"Delegation should succeed: {data}"
                assert "task_id" in data, "Should return task_id"
                assert "workflow_id" in data, "Should return workflow_id"
                
                self.test_results["integration_tests"][test_name] = {
                    "status": "PASS",
                    "task_id": data.get("task_id"),
                    "workflow_id": data.get("workflow_id"),
                    "response_time": response.elapsed.total_seconds()
                }
                logger.info(f"✅ {test_name}: PASS")
                
        except Exception as e:
            self.test_results["integration_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")

    # ================================
    # STRESS TESTS
    # ================================
    
    async def test_stress_concurrent_registrations(self):
        """Stress test: Concurrent agent registrations"""
        test_name = "concurrent_registrations"
        logger.info(f"🏋️ Stress Test: {test_name}")
        
        try:
            start_time = time.time()
            concurrent_agents = 50
            success_count = 0
            error_count = 0
            
            async with httpx.AsyncClient() as client:
                # Create concurrent registration tasks
                tasks = []
                for i in range(concurrent_agents):
                    agent_data = {
                        "agent_id": f"stress_agent_{i}",
                        "name": f"Stress Test Agent {i}",
                        "agent_type": "stress_test",
                        "capabilities": [f"capability_{i % 5}", "stress_testing"]
                    }
                    
                    task = client.post(f"{self.lobby_url}/api/agents/register", json=agent_data)
                    tasks.append(task)
                
                # Execute all registrations concurrently
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                for response in responses:
                    if isinstance(response, Exception):
                        error_count += 1
                    elif hasattr(response, 'status_code') and response.status_code == 200:
                        success_count += 1
                    else:
                        error_count += 1
            
            end_time = time.time()
            total_time = end_time - start_time
            
            success_rate = (success_count / concurrent_agents) * 100
            
            self.test_results["stress_tests"][test_name] = {
                "status": "PASS" if success_rate >= 90 else "PARTIAL",
                "concurrent_requests": concurrent_agents,
                "success_count": success_count,
                "error_count": error_count,
                "success_rate": success_rate,
                "total_time": total_time,
                "requests_per_second": concurrent_agents / total_time
            }
            
            logger.info(f"✅ {test_name}: {success_rate:.1f}% success rate ({success_count}/{concurrent_agents})")
            
        except Exception as e:
            self.test_results["stress_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_stress_rapid_a2a_requests(self):
        """Stress test: Rapid A2A discovery and status requests"""
        test_name = "rapid_a2a_requests"
        logger.info(f"🏋️ Stress Test: {test_name}")
        
        try:
            total_requests = 200
            success_count = 0
            error_count = 0
            response_times = []
            
            async with httpx.AsyncClient() as client:
                for i in range(total_requests):
                    start = time.time()
                    
                    try:
                        # Alternate between discovery and status requests
                        if i % 2 == 0:
                            response = await client.get(f"{self.bridge_url}/.well-known/agent.json")
                        else:
                            response = await client.get(f"{self.bridge_url}/api/a2a/status")
                        
                        end = time.time()
                        response_time = end - start
                        response_times.append(response_time)
                        
                        if response.status_code == 200:
                            success_count += 1
                        else:
                            error_count += 1
                            
                    except Exception:
                        error_count += 1
                        end = time.time()
                        response_times.append(end - start)
            
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
            success_rate = (success_count / total_requests) * 100
            
            self.test_results["stress_tests"][test_name] = {
                "status": "PASS" if success_rate >= 95 else "PARTIAL",
                "total_requests": total_requests,
                "success_count": success_count,
                "error_count": error_count,
                "success_rate": success_rate,
                "avg_response_time": avg_response_time,
                "max_response_time": max_response_time,
                "min_response_time": min_response_time,
                "performance_target": "< 100ms avg",
                "performance_met": avg_response_time < 0.1
            }
            
            logger.info(f"✅ {test_name}: {success_rate:.1f}% success, {avg_response_time*1000:.1f}ms avg")
            
        except Exception as e:
            self.test_results["stress_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")
    
    async def test_stress_concurrent_delegations(self):
        """Stress test: Concurrent A2A task delegations"""
        test_name = "concurrent_delegations"
        logger.info(f"🏋️ Stress Test: {test_name}")
        
        try:
            # Register multiple agents for delegation targets
            async with httpx.AsyncClient() as client:
                for i in range(10):
                    agent_data = {
                        "agent_id": f"delegation_target_{i}",
                        "name": f"Delegation Target {i}",
                        "agent_type": "delegation_target",
                        "capabilities": ["data_processing", "task_execution"]
                    }
                    await client.post(f"{self.lobby_url}/api/agents/register", json=agent_data)
                
                # Now test concurrent delegations
                concurrent_delegations = 30
                success_count = 0
                error_count = 0
                delegation_times = []
                
                tasks = []
                for i in range(concurrent_delegations):
                    task_data = {
                        "title": f"Stress Test Task {i}",
                        "description": f"Concurrent delegation stress test task {i}",
                        "required_capabilities": ["data_processing"],
                        "input": {"task_number": i, "stress_test": True},
                        "sender_id": f"stress_client_{i}"
                    }
                    
                    start = time.time()
                    task = client.post(f"{self.bridge_url}/api/a2a/delegate", json=task_data)
                    tasks.append((task, start))
                
                # Execute all delegations concurrently
                results = await asyncio.gather(*[task for task, _ in tasks], return_exceptions=True)
                
                for i, result in enumerate(results):
                    end_time = time.time()
                    delegation_time = end_time - tasks[i][1]
                    delegation_times.append(delegation_time)
                    
                    if isinstance(result, Exception):
                        error_count += 1
                    elif hasattr(result, 'status_code') and result.status_code == 200:
                        try:
                            data = result.json()
                            if data.get("success"):
                                success_count += 1
                            else:
                                error_count += 1
                        except:
                            error_count += 1
                    else:
                        error_count += 1
                
                success_rate = (success_count / concurrent_delegations) * 100
                avg_delegation_time = sum(delegation_times) / len(delegation_times)
                
                self.test_results["stress_tests"][test_name] = {
                    "status": "PASS" if success_rate >= 80 else "PARTIAL",
                    "concurrent_delegations": concurrent_delegations,
                    "success_count": success_count,
                    "error_count": error_count,
                    "success_rate": success_rate,
                    "avg_delegation_time": avg_delegation_time,
                    "max_delegation_time": max(delegation_times),
                    "min_delegation_time": min(delegation_times)
                }
                
                logger.info(f"✅ {test_name}: {success_rate:.1f}% success, {avg_delegation_time*1000:.1f}ms avg")
                
        except Exception as e:
            self.test_results["stress_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")

    # ================================
    # EDGE CASE TESTS
    # ================================
    
    async def test_edge_invalid_requests(self):
        """Edge case test: Invalid request handling"""
        test_name = "invalid_requests"
        logger.info(f"🧩 Edge Case Test: {test_name}")
        
        try:
            async with httpx.AsyncClient() as client:
                edge_cases = []
                
                # Test invalid JSON
                try:
                    response = await client.post(f"{self.bridge_url}/api/a2a/delegate", 
                                               content="invalid json")
                    edge_cases.append(("invalid_json", response.status_code == 422))
                except:
                    edge_cases.append(("invalid_json", True))
                
                # Test missing required fields
                response = await client.post(f"{self.bridge_url}/api/a2a/delegate", json={})
                edge_cases.append(("missing_fields", response.status_code == 422))
                
                # Test invalid endpoint
                response = await client.get(f"{self.bridge_url}/api/nonexistent")
                edge_cases.append(("invalid_endpoint", response.status_code == 404))
                
                # Test malformed agent registration
                response = await client.post(f"{self.lobby_url}/api/agents/register", 
                                           json={"invalid": "data"})
                edge_cases.append(("malformed_registration", response.status_code in [400, 422]))
                
                passed_cases = sum(1 for _, passed in edge_cases if passed)
                total_cases = len(edge_cases)
                
                self.test_results["integration_tests"][test_name] = {
                    "status": "PASS" if passed_cases == total_cases else "PARTIAL",
                    "test_cases": edge_cases,
                    "passed": passed_cases,
                    "total": total_cases,
                    "success_rate": (passed_cases / total_cases) * 100
                }
                
                logger.info(f"✅ {test_name}: {passed_cases}/{total_cases} edge cases handled correctly")
                
        except Exception as e:
            self.test_results["integration_tests"][test_name] = {"status": "FAIL", "error": str(e)}
            logger.error(f"❌ {test_name}: FAIL - {e}")

    # ================================
    # TEST RUNNER
    # ================================
    
    async def run_all_tests(self):
        """Run the complete test suite"""
        logger.info("🚀 Starting Comprehensive A2A API Test Suite...")
        
        start_time = time.time()
        
        # Setup environment
        if not await self.setup_test_environment():
            logger.error("❌ Failed to setup test environment")
            return False
        
        try:
            # Run unit tests
            logger.info("\n📋 Running Unit Tests...")
            await self.test_unit_lobby_initialization()
            await self.test_unit_a2a_bridge_initialization()
            await self.test_unit_agent_registration()
            
            # Run integration tests
            logger.info("\n🔗 Running Integration Tests...")
            await self.test_integration_a2a_discovery()
            await self.test_integration_a2a_status()
            await self.test_integration_agent_registration_via_api()
            await self.test_integration_a2a_task_delegation()
            await self.test_edge_invalid_requests()
            
            # Run stress tests
            logger.info("\n🏋️ Running Stress Tests...")
            await self.test_stress_concurrent_registrations()
            await self.test_stress_rapid_a2a_requests()
            await self.test_stress_concurrent_delegations()
            
            # Generate test report
            end_time = time.time()
            total_time = end_time - start_time
            
            self.test_results["performance_metrics"] = {
                "total_test_time": total_time,
                "test_completion_time": datetime.now(timezone.utc).isoformat()
            }
            
            self.generate_test_report()
            return True
            
        finally:
            await self.teardown_test_environment()
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        logger.info("\n" + "="*80)
        logger.info("🎯 COMPREHENSIVE A2A API TEST RESULTS")
        logger.info("="*80)
        
        # Unit Tests Summary
        unit_tests = self.test_results["unit_tests"]
        unit_passed = sum(1 for test in unit_tests.values() if test["status"] == "PASS")
        unit_total = len(unit_tests)
        
        logger.info(f"\n📋 UNIT TESTS: {unit_passed}/{unit_total} PASSED")
        for test_name, result in unit_tests.items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            logger.info(f"   {status_icon} {test_name}: {result['status']}")
        
        # Integration Tests Summary
        integration_tests = self.test_results["integration_tests"]
        integration_passed = sum(1 for test in integration_tests.values() if test["status"] == "PASS")
        integration_total = len(integration_tests)
        
        logger.info(f"\n🔗 INTEGRATION TESTS: {integration_passed}/{integration_total} PASSED")
        for test_name, result in integration_tests.items():
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            logger.info(f"   {status_icon} {test_name}: {result['status']}")
            if "response_time" in result:
                logger.info(f"      ⏱️ Response time: {result['response_time']*1000:.1f}ms")
        
        # Stress Tests Summary
        stress_tests = self.test_results["stress_tests"]
        stress_passed = sum(1 for test in stress_tests.values() if test["status"] in ["PASS", "PARTIAL"])
        stress_total = len(stress_tests)
        
        logger.info(f"\n🏋️ STRESS TESTS: {stress_passed}/{stress_total} PASSED")
        for test_name, result in stress_tests.items():
            status_icon = "✅" if result["status"] == "PASS" else "⚠️" if result["status"] == "PARTIAL" else "❌"
            logger.info(f"   {status_icon} {test_name}: {result['status']}")
            if "success_rate" in result:
                logger.info(f"      📊 Success rate: {result['success_rate']:.1f}%")
            if "avg_response_time" in result:
                logger.info(f"      ⏱️ Avg response: {result['avg_response_time']*1000:.1f}ms")
        
        # Overall Summary
        total_passed = unit_passed + integration_passed + stress_passed
        total_tests = unit_total + integration_total + stress_total
        overall_success_rate = (total_passed / total_tests) * 100
        
        logger.info(f"\n🎯 OVERALL RESULTS:")
        logger.info(f"   📊 Success Rate: {overall_success_rate:.1f}% ({total_passed}/{total_tests})")
        logger.info(f"   ⏱️ Total Test Time: {self.test_results['performance_metrics']['total_test_time']:.2f}s")
        
        # Performance Highlights
        logger.info(f"\n⚡ PERFORMANCE HIGHLIGHTS:")
        
        # A2A Discovery Performance
        if "a2a_discovery" in integration_tests:
            discovery_time = integration_tests["a2a_discovery"].get("response_time", 0)
            logger.info(f"   🔍 A2A Discovery: {discovery_time*1000:.1f}ms")
        
        # Stress Test Performance
        if "rapid_a2a_requests" in stress_tests:
            rapid_test = stress_tests["rapid_a2a_requests"]
            avg_time = rapid_test.get("avg_response_time", 0)
            logger.info(f"   🏋️ Rapid Requests: {avg_time*1000:.1f}ms avg (200 requests)")
        
        if "concurrent_registrations" in stress_tests:
            concurrent_test = stress_tests["concurrent_registrations"]
            rps = concurrent_test.get("requests_per_second", 0)
            logger.info(f"   🚀 Concurrent Registrations: {rps:.1f} requests/second")
        
        # Quality Assessment
        logger.info(f"\n🏆 QUALITY ASSESSMENT:")
        if overall_success_rate >= 95:
            logger.info("   🌟 EXCELLENT: System demonstrates exceptional reliability")
        elif overall_success_rate >= 85:
            logger.info("   ✅ GOOD: System shows strong performance with minor issues")
        elif overall_success_rate >= 70:
            logger.info("   ⚠️ ACCEPTABLE: System functional but needs improvement")
        else:
            logger.info("   ❌ POOR: System requires significant fixes")
        
        logger.info("="*80)
        
        # Save detailed results to file
        self.save_test_results()
    
    def save_test_results(self):
        """Save detailed test results to file"""
        try:
            results_file = Path("test_results_comprehensive_a2a.json")
            with open(results_file, 'w') as f:
                json.dump(self.test_results, f, indent=2, default=str)
            logger.info(f"💾 Detailed test results saved to: {results_file}")
        except Exception as e:
            logger.error(f"Failed to save test results: {e}")

# ================================
# MAIN TEST EXECUTION
# ================================

async def main():
    """Main test execution function"""
    test_suite = ComprehensiveA2ATestSuite()
    
    logger.info("🧪 Comprehensive A2A API Testing Suite")
    logger.info("   Testing: Enhanced A2A API Bridge + Agent Lobby Integration")
    logger.info("   Coverage: Unit Tests, Integration Tests, Stress Tests")
    logger.info("   Target: Production-ready robustness validation\n")
    
    success = await test_suite.run_all_tests()
    
    if success:
        logger.info("\n✅ Test suite completed successfully")
        return 0
    else:
        logger.error("\n❌ Test suite failed")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 