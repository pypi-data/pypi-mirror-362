#!/usr/bin/env python3
"""
A2A-Enhanced Agent Lobby SDK Demo
================================

This demo shows how to use Agent Lobby SDK with built-in A2A protocol support.
Your agents get A2A compatibility with Agent Lobby's enhanced intelligence.
"""

import asyncio
import json
import logging
from typing import Dict, Any
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sdk.agent_lobbi_sdk import AgentLobbySDK

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EnhancedAnalysisAgent:
    """Example agent with A2A compatibility"""
    
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.sdk = AgentLobbySDK(
            lobby_host="localhost",
            lobby_port=8080,
            enable_a2a=True,  # Enable A2A protocol support
            a2a_port=8090     # A2A server port
        )
    
    async def task_handler(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tasks with enhanced analysis"""
        logger.info(f"🤖 Agent {self.agent_id} processing task: {task.get('task_id', 'unknown')}")
        
        input_data = task.get('input_data', {})
        text = input_data.get('text', '')
        
        # Enhanced analysis using Agent Lobby intelligence
        result = {
            "analysis": f"Enhanced analysis of: {text}",
            "word_count": len(text.split()),
            "sentiment": "positive",  # Simplified for demo
            "key_insights": [
                "Agent Lobby provides superior intelligence",
                "A2A compatibility ensures universal access",
                "Enhanced results compared to standard A2A"
            ],
            "processing_method": "Agent Lobby Neuromorphic Intelligence",
            "enhanced_by": "Agent Lobby Platform"
        }
        
        logger.info(f"✅ Agent {self.agent_id} completed analysis with enhanced results")
        return result
    
    async def start(self):
        """Start the agent with A2A support"""
        try:
            # Register agent with Agent Lobby
            result = await self.sdk.register_agent(
                agent_id=self.agent_id,
                name="Enhanced Analysis Agent",
                agent_type="DataAnalyst",
                capabilities=["text_analysis", "sentiment_analysis", "data_insights"],
                task_handler=self.task_handler,
                auto_start_a2a=True  # Automatically start A2A server
            )
            
            logger.info(f"🚀 Agent {self.agent_id} registered and A2A server started!")
            logger.info(f"🔗 A2A Agent Card available at: http://localhost:{self.sdk.a2a_port}/.well-known/agent.json")
            
            # Display A2A capabilities
            agent_card = self.sdk.get_a2a_agent_card()
            logger.info(f"📋 A2A Agent Card: {json.dumps(agent_card, indent=2)}")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to start agent: {e}")
            raise

class A2AClient:
    """Example A2A client that calls Agent Lobby agents"""
    
    def __init__(self):
        self.sdk = AgentLobbySDK(
            lobby_host="localhost",
            lobby_port=8080,
            enable_a2a=True
        )
    
    async def call_agent_lobby_via_a2a(self, agent_url: str, message: str):
        """Call Agent Lobby agent using A2A protocol"""
        try:
            logger.info(f"🔄 Calling Agent Lobby agent via A2A: {agent_url}")
            
            # This uses A2A protocol but gets Agent Lobby's enhanced intelligence
            result = await self.sdk.call_a2a_agent(agent_url, message)
            
            logger.info(f"✅ Received A2A response: {json.dumps(result, indent=2)}")
            return result
            
        except Exception as e:
            logger.error(f"❌ A2A call failed: {e}")
            raise

async def demo_a2a_integration():
    """Demonstrate A2A integration with Agent Lobby"""
    print("=" * 80)
    print("🚀 A2A-Enhanced Agent Lobby SDK Demo")
    print("=" * 80)
    
    # 1. Start Agent Lobby agent with A2A support
    print("\n1️⃣ Starting Agent Lobby agent with A2A support...")
    agent = EnhancedAnalysisAgent("enhanced_analysis_agent_001")
    await agent.start()
    
    # Wait for server to start
    await asyncio.sleep(2)
    
    # 2. Test A2A compatibility
    print("\n2️⃣ Testing A2A protocol compatibility...")
    client = A2AClient()
    
    # Call our Agent Lobby agent using A2A protocol
    agent_url = "http://localhost:8090"
    message = "Analyze the performance of Agent Lobby compared to standard A2A implementations"
    
    result = await client.call_agent_lobby_via_a2a(agent_url, message)
    
    # 3. Show the enhanced results
    print("\n3️⃣ Enhanced Results from Agent Lobby:")
    print("=" * 50)
    
    artifacts = result.get('artifacts', [])
    if artifacts:
        for artifact in artifacts:
            parts = artifact.get('parts', [])
            for part in parts:
                if part.get('type') == 'text':
                    print(f"📊 Analysis Result: {part.get('text', '')}")
    
    metadata = result.get('metadata', {})
    if metadata.get('agent_lobby_enhanced'):
        print(f"⚡ Processing Time: {metadata.get('processing_time', 'N/A')}ms")
        print(f"🤖 Agents Involved: {metadata.get('agents_involved', [])}")
        print(f"🧠 Enhanced by: Agent Lobby Platform")
    
    print("\n4️⃣ Key Advantages:")
    print("✅ Standard A2A compatibility")
    print("✅ Agent Lobby's enhanced intelligence")
    print("✅ Neuromorphic agent selection")
    print("✅ Superior results compared to basic A2A")
    print("✅ No additional integration complexity")
    
    print("\n🎉 Demo completed successfully!")

async def demo_multi_protocol_support():
    """Demonstrate multi-protocol support"""
    print("\n" + "=" * 80)
    print("🔄 Multi-Protocol Support Demo")
    print("=" * 80)
    
    # Create SDK with multiple protocol support
    sdk = AgentLobbySDK(
        lobby_host="localhost",
        lobby_port=8080,
        enable_a2a=True,
        a2a_port=8091
    )
    
    async def multi_protocol_handler(task: Dict[str, Any]) -> Dict[str, Any]:
        """Handler that works with multiple protocols"""
        protocol_info = task.get('input_data', {}).get('original_a2a_message')
        
        if protocol_info:
            return {
                "result": "Processed via A2A protocol with Agent Lobby intelligence",
                "protocol": "A2A",
                "enhanced": True
            }
        else:
            return {
                "result": "Processed via native Agent Lobby protocol",
                "protocol": "Agent Lobby Native",
                "enhanced": True
            }
    
    # Register agent with multi-protocol support
    await sdk.register_agent(
        agent_id="multi_protocol_agent",
        name="Multi-Protocol Agent",
        agent_type="Universal",
        capabilities=["multi_protocol", "universal_compatibility"],
        task_handler=multi_protocol_handler,
        auto_start_a2a=True
    )
    
    print("✅ Multi-protocol agent started!")
    print(f"🔗 A2A endpoint: http://localhost:8091/.well-known/agent.json")
    print("🔗 Agent Lobby native: WebSocket connection active")

async def main():
    """Main demo function"""
    try:
        await demo_a2a_integration()
        await asyncio.sleep(2)
        await demo_multi_protocol_support()
        
        # Keep running to demonstrate server functionality
        print("\n⏳ Servers running... Press Ctrl+C to stop")
        await asyncio.sleep(30)
        
    except KeyboardInterrupt:
        print("\n🛑 Demo stopped by user")
    except Exception as e:
        logger.error(f"Demo error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main()) 