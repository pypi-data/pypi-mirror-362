#!/usr/bin/env python3
"""
Data Processor Agent - Analyzes and processes data
Supports both A2A protocol and Agent Lobby collaboration
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any, List
import json
import time
import statistics

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.sdk.agent_lobbi_sdk import AgentLobbySDK

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataProcessorAgent:
    """Data Processor Agent with A2A and Agent Lobby capabilities"""
    
    def __init__(self):
        self.agent_id = "data_processor_001"
        self.name = "Data Analysis Processor"
        self.capabilities = ["data_analysis", "statistics", "filtering", "transformation", "trend_analysis"]
        self.processing_history = []
        
    async def analyze_data(self, data: List[float], analysis_type: str = "basic") -> Dict[str, Any]:
        """Analyze numerical data"""
        try:
            start_time = time.time()
            
            if not data:
                raise ValueError("No data provided for analysis")
            
            result = {
                "data_points": len(data),
                "min": min(data),
                "max": max(data),
                "mean": statistics.mean(data),
                "median": statistics.median(data)
            }
            
            if analysis_type == "detailed":
                if len(data) > 1:
                    result.update({
                        "std_dev": statistics.stdev(data),
                        "variance": statistics.variance(data),
                        "range": max(data) - min(data)
                    })
                
                # Trend analysis
                if len(data) >= 3:
                    trend = "stable"
                    if data[-1] > data[0]:
                        trend = "increasing"
                    elif data[-1] < data[0]:
                        trend = "decreasing"
                    result["trend"] = trend
            
            processing_time = time.time() - start_time
            
            # Store in history
            analysis_record = {
                "data": data,
                "analysis_type": analysis_type,
                "result": result,
                "processing_time": processing_time,
                "timestamp": time.time()
            }
            self.processing_history.append(analysis_record)
            
            logger.info(f"✅ Analyzed {len(data)} data points ({analysis_type}) in {processing_time:.4f}s")
            
            return {
                "analysis": result,
                "processing_time": processing_time,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Data analysis failed: {e}")
            return {
                "error": str(e),
                "status": "error"
            }
    
    async def filter_data(self, data: List[float], filter_type: str, threshold: float = None) -> Dict[str, Any]:
        """Filter data based on criteria"""
        try:
            if filter_type == "above_threshold" and threshold is not None:
                filtered = [x for x in data if x > threshold]
            elif filter_type == "below_threshold" and threshold is not None:
                filtered = [x for x in data if x < threshold]
            elif filter_type == "outliers":
                mean = statistics.mean(data)
                std_dev = statistics.stdev(data) if len(data) > 1 else 0
                filtered = [x for x in data if abs(x - mean) <= 2 * std_dev]
            else:
                raise ValueError(f"Unknown filter type: {filter_type}")
            
            return {
                "original_count": len(data),
                "filtered_count": len(filtered),
                "filtered_data": filtered,
                "filter_type": filter_type,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Data filtering failed: {e}")
            return {"error": str(e), "status": "error"}
    
    async def handle_a2a_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle A2A protocol tasks"""
        logger.info(f"📡 A2A Task received: {task_data}")
        
        try:
            task_type = task_data.get("task_type", "analyze")
            data = task_data.get("data", [])
            
            if task_type == "analyze":
                analysis_type = task_data.get("analysis_type", "basic")
                result = await self.analyze_data(data, analysis_type)
            elif task_type == "filter":
                filter_type = task_data.get("filter_type", "outliers")
                threshold = task_data.get("threshold")
                result = await self.filter_data(data, filter_type, threshold)
            else:
                raise ValueError(f"Unknown task type: {task_type}")
            
            return {
                "task_id": task_data.get("id", "unknown"),
                "result": result,
                "status": "completed",
                "agent_id": self.agent_id,
                "protocol": "A2A-v1.0"
            }
            
        except Exception as e:
            logger.error(f"❌ A2A task failed: {e}")
            return {
                "task_id": task_data.get("id", "unknown"),
                "error": str(e),
                "status": "failed",
                "agent_id": self.agent_id,
                "protocol": "A2A-v1.0"
            }
    
    async def handle_lobby_collaboration(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Handle Agent Lobby collaboration requests"""
        logger.info(f"🏛️ Lobby collaboration: {message}")
        
        try:
            msg_type = message.get("type", "analyze")
            
            if msg_type == "analyze":
                return await self.analyze_data(
                    message.get("data", []),
                    message.get("analysis_type", "basic")
                )
            elif msg_type == "filter":
                return await self.filter_data(
                    message.get("data", []),
                    message.get("filter_type", "outliers"),
                    message.get("threshold")
                )
            elif msg_type == "get_insights":
                return self.get_processing_insights()
            else:
                raise ValueError(f"Unknown collaboration message type: {msg_type}")
                
        except Exception as e:
            logger.error(f"❌ Lobby collaboration failed: {e}")
            return {"error": str(e), "status": "error"}
    
    def get_processing_insights(self) -> Dict[str, Any]:
        """Get insights from processing history"""
        if not self.processing_history:
            return {"message": "No data processed yet"}
        
        processing_times = [p["processing_time"] for p in self.processing_history]
        data_sizes = [len(p["data"]) for p in self.processing_history]
        
        return {
            "total_analyses": len(self.processing_history),
            "average_processing_time": sum(processing_times) / len(processing_times),
            "largest_dataset": max(data_sizes),
            "smallest_dataset": min(data_sizes),
            "efficiency_trend": "improving" if len(processing_times) > 1 and processing_times[-1] < processing_times[0] else "stable"
        }

async def main():
    """Main function to run Data Processor Agent"""
    logger.info("📊 Starting Data Processor Agent...")
    
    processor = DataProcessorAgent()
    
    try:
        # Initialize Agent Lobby SDK with A2A support
        sdk = AgentLobbySDK(
            agent_id=processor.agent_id,
            name=processor.name,
            agent_type="data_processor",
            capabilities=processor.capabilities,
            enable_a2a=True,
            task_handler=processor.handle_lobby_collaboration
        )
        
        # Set A2A task handler
        if sdk.a2a_handler:
            sdk.a2a_handler.task_handler = processor.handle_a2a_task
        
        # Register with Agent Lobby
        await sdk.register()
        logger.info("✅ Data Processor Agent registered with Agent Lobby")
        
        # Generate A2A agent card
        if sdk.a2a_handler:
            a2a_card = sdk.generate_a2a_card()
            logger.info(f"📇 A2A Agent Card: {json.dumps(a2a_card, indent=2)}")
        
        # Start metrics collection
        if sdk.metrics_system:
            sdk.metrics_system.start()
            logger.info("📊 Metrics collection started")
        
        # Run test data analysis
        logger.info("🧪 Running initial test analysis...")
        test_datasets = [
            ([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "basic"),
            ([15, 23, 8, 42, 16, 34, 29, 12], "detailed"),
            ([100, 200, 150, 300, 250, 180], "detailed")
        ]
        
        for data, analysis_type in test_datasets:
            result = await processor.analyze_data(data, analysis_type)
            await asyncio.sleep(0.1)
        
        # Show insights
        insights = processor.get_processing_insights()
        logger.info(f"🔍 Processing Insights: {json.dumps(insights, indent=2)}")
        
        # Keep agent running
        logger.info("🟢 Data Processor Agent ready for tasks...")
        logger.info("📡 A2A endpoint: http://localhost:8080/a2a/task")
        logger.info("🏛️ Agent Lobby: Connected and ready for collaboration")
        
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Data Processor Agent shutting down...")
    except Exception as e:
        logger.error(f"❌ Data Processor Agent error: {e}")
    finally:
        if 'sdk' in locals():
            if sdk.metrics_system:
                sdk.metrics_system.stop()
            await sdk.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 