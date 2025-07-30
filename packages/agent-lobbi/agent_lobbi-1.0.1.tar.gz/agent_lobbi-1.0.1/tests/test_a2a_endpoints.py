#!/usr/bin/env python3
"""
A2A Protocol Endpoints Test
==========================
Test the newly added A2A (Agent-to-Agent) protocol endpoints in Agent Lobby.
This demonstrates how external A2A clients can interact with Agent Lobby.
"""

import asyncio
import aiohttp
import json
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class A2AEndpointTester:
    """Test the A2A protocol endpoints in Agent Lobby"""
    
    def __init__(self, lobby_host="localhost", lobby_port=8080):
        self.lobby_host = lobby_host
        self.lobby_port = lobby_port
        self.base_url = f"http://{lobby_host}:{lobby_port}"
        
    async def test_agent_discovery(self):
        """Test A2A agent discovery endpoint (/.well-known/agent.json)"""
        print("\n🔍 Testing A2A Agent Discovery...")
        
        try:
            async with aiohttp.ClientSession() as session:
                # Test the standard A2A discovery endpoint
                async with session.get(f"{self.base_url}/.well-known/agent.json") as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ Agent Discovery successful!")
                        print(f"   Platform: {data.get('name')}")
                        print(f"   Version: {data.get('version')}")
                        print(f"   Capabilities: {len(data.get('capabilities', {}))}")
                        print(f"   Skills: {', '.join(data.get('skills', []))}")
                        print(f"   A2A Endpoints: {len(data.get('endpoints', {}))}")
                        return True
                    else:
                        print(f"❌ Agent Discovery failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Agent Discovery error: {e}")
            return False
    
    async def test_a2a_agent_listing(self):
        """Test A2A agent listing endpoint"""
        print("\n📋 Testing A2A Agent Listing...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/a2a/discover") as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ A2A Agent Listing successful!")
                        print(f"   Total Agents: {data.get('total_count', 0)}")
                        print(f"   Platform: {data.get('lobby_info', {}).get('platform')}")
                        
                        for agent in data.get('agents', [])[:3]:  # Show first 3 agents
                            print(f"   Agent: {agent.get('name')} ({agent.get('status')})")
                            print(f"     Capabilities: {', '.join(agent.get('capabilities', []))}")
                        
                        return True
                    else:
                        print(f"❌ A2A Agent Listing failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ A2A Agent Listing error: {e}")
            return False
    
    async def test_a2a_status(self):
        """Test A2A status endpoint"""
        print("\n📊 Testing A2A Status...")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/a2a/status") as response:
                    if response.status == 200:
                        data = await response.json()
                        print("✅ A2A Status successful!")
                        print(f"   Lobby Status: {data.get('lobby_status')}")
                        print(f"   Platform: {data.get('platform')}")
                        print(f"   Version: {data.get('version')}")
                        print(f"   Agent Count: {data.get('agent_count')}")
                        print(f"   Active Connections: {data.get('active_connections')}")
                        print(f"   Protocols: {', '.join(data.get('protocols_supported', []))}")
                        return True
                    else:
                        print(f"❌ A2A Status failed: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ A2A Status error: {e}")
            return False
    
    async def test_a2a_task_delegation(self):
        """Test A2A task delegation endpoint"""
        print("\n🎯 Testing A2A Task Delegation...")
        
        task_data = {
            "title": "Test A2A Task",
            "description": "This is a test task from A2A protocol",
            "required_capabilities": ["testing", "validation"],
            "sender_id": "a2a_test_client",
            "input": {
                "test_data": "Hello from A2A client",
                "priority": "normal"
            },
            "context": {
                "source": "A2A protocol test",
                "timestamp": datetime.now().isoformat()
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/a2a/delegate",
                    json=task_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        print("✅ A2A Task Delegation successful!")
                        print(f"   Task ID: {data.get('task_id')}")
                        print(f"   Assigned to: {data.get('assigned_to')}")
                        print(f"   Message: {data.get('message')}")
                        return True
                    else:
                        print(f"❌ A2A Task Delegation failed: {response.status}")
                        print(f"   Error: {data.get('message')}")
                        print(f"   Error Code: {data.get('error_code')}")
                        if data.get('required_capabilities'):
                            print(f"   Required: {data.get('required_capabilities')}")
                        return False
                        
        except Exception as e:
            print(f"❌ A2A Task Delegation error: {e}")
            return False
    
    async def test_a2a_communication(self):
        """Test A2A communication endpoint"""
        print("\n💬 Testing A2A Communication...")
        
        message_data = {
            "message": "Hello from A2A client! This is a test communication.",
            "sender_id": "a2a_test_client",
            "type": "greeting",
            "context": {
                "source": "A2A protocol test",
                "test_type": "communication"
            }
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/api/a2a/communicate",
                    json=message_data,
                    headers={"Content-Type": "application/json"}
                ) as response:
                    data = await response.json()
                    
                    if response.status == 200:
                        print("✅ A2A Communication successful!")
                        print(f"   Message: {data.get('message')}")
                        recipients = data.get('recipients', [])
                        if recipients:
                            print(f"   Sent to: {', '.join(recipients)}")
                        return True
                    else:
                        print(f"❌ A2A Communication failed: {response.status}")
                        print(f"   Error: {data.get('message')}")
                        print(f"   Error Code: {data.get('error_code')}")
                        return False
                        
        except Exception as e:
            print(f"❌ A2A Communication error: {e}")
            return False
    
    async def test_specific_agent_info(self):
        """Test getting specific agent information via A2A"""
        print("\n👤 Testing Specific Agent Info...")
        
        try:
            # First get the list of agents
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/api/a2a/discover") as response:
                    if response.status == 200:
                        data = await response.json()
                        agents = data.get('agents', [])
                        
                        if agents:
                            # Test getting info for the first agent
                            test_agent_id = agents[0].get('agent_id')
                            
                            async with session.get(f"{self.base_url}/api/a2a/agents/{test_agent_id}") as agent_response:
                                if agent_response.status == 200:
                                    agent_data = await agent_response.json()
                                    print("✅ Specific Agent Info successful!")
                                    print(f"   Agent ID: {agent_data.get('agent_id')}")
                                    print(f"   Name: {agent_data.get('name')}")
                                    print(f"   Status: {agent_data.get('status')}")
                                    print(f"   Protocols: {', '.join(agent_data.get('protocols', []))}")
                                    return True
                                else:
                                    print(f"❌ Specific Agent Info failed: {agent_response.status}")
                                    return False
                        else:
                            print("⚠️  No agents available to test")
                            return True
                    else:
                        print(f"❌ Could not get agent list: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ Specific Agent Info error: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all A2A endpoint tests"""
        print("🚀 Starting A2A Protocol Endpoint Tests")
        print("========================================")
        
        tests = [
            ("Agent Discovery", self.test_agent_discovery),
            ("A2A Status", self.test_a2a_status),
            ("A2A Agent Listing", self.test_a2a_agent_listing),
            ("Specific Agent Info", self.test_specific_agent_info),
            ("A2A Task Delegation", self.test_a2a_task_delegation),
            ("A2A Communication", self.test_a2a_communication),
        ]
        
        results = []
        
        for test_name, test_func in tests:
            try:
                result = await test_func()
                results.append((test_name, result))
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                results.append((test_name, False))
        
        # Summary
        print("\n📊 Test Results Summary")
        print("======================")
        
        passed = sum(1 for _, result in results if result)
        total = len(results)
        
        for test_name, result in results:
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"{status} {test_name}")
        
        print(f"\n🏆 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All A2A protocol endpoints are working correctly!")
        else:
            print("⚠️  Some A2A endpoints need attention.")
        
        return passed == total

async def main():
    """Main test function"""
    print("Agent Lobby A2A Protocol Endpoint Tester")
    print("========================================")
    
    # Check if lobby is running
    tester = A2AEndpointTester()
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{tester.base_url}/health") as response:
                if response.status != 200:
                    print("❌ Agent Lobby is not running or not accessible")
                    print(f"   Please start the lobby: python src/main.py")
                    return False
                    
        print("✅ Agent Lobby is running, proceeding with A2A tests...\n")
        
        # Run all tests
        success = await tester.run_all_tests()
        return success
        
    except Exception as e:
        print(f"❌ Could not connect to Agent Lobby: {e}")
        print("   Please ensure the lobby is running on localhost:8080")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 