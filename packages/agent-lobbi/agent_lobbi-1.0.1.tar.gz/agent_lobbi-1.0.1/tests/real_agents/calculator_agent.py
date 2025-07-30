#!/usr/bin/env python3
"""
Calculator Agent - Handles mathematical calculations
Supports both A2A protocol and Agent Lobby collaboration
"""

import asyncio
import logging
import sys
import os
from typing import Dict, Any, List
import json
import time

# Add parent directories to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

from src.sdk.agent_lobbi_sdk import AgentLobbySDK

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CalculatorAgent:
    """Calculator Agent with A2A and Agent Lobby capabilities"""
    
    def __init__(self):
        self.agent_id = "calculator_agent_001"
        self.name = "Mathematical Calculator"
        self.capabilities = ["addition", "subtraction", "multiplication", "division", "statistics"]
        self.calculation_history = []
        
    async def calculate(self, operation: str, numbers: List[float]) -> Dict[str, Any]:
        """Perform mathematical calculations"""
        try:
            result = None
            start_time = time.time()
            
            if operation == "add":
                result = sum(numbers)
            elif operation == "subtract":
                result = numbers[0] - sum(numbers[1:])
            elif operation == "multiply":
                result = 1
                for num in numbers:
                    result *= num
            elif operation == "divide":
                result = numbers[0]
                for num in numbers[1:]:
                    if num == 0:
                        raise ValueError("Division by zero")
                    result /= num
            elif operation == "average":
                result = sum(numbers) / len(numbers)
            elif operation == "max":
                result = max(numbers)
            elif operation == "min":
                result = min(numbers)
            else:
                raise ValueError(f"Unknown operation: {operation}")
            
            calculation_time = time.time() - start_time
            
            # Store in history for learning
            calculation_record = {
                "operation": operation,
                "numbers": numbers,
                "result": result,
                "calculation_time": calculation_time,
                "timestamp": time.time()
            }
            self.calculation_history.append(calculation_record)
            
            logger.info(f"✅ Calculated {operation}({numbers}) = {result} in {calculation_time:.4f}s")
            
            return {
                "result": result,
                "operation": operation,
                "numbers": numbers,
                "calculation_time": calculation_time,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"❌ Calculation failed: {e}")
            return {
                "error": str(e),
                "operation": operation,
                "numbers": numbers,
                "status": "error"
            }
    
    async def handle_a2a_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Handle A2A protocol tasks"""
        logger.info(f"📡 A2A Task received: {task_data}")
        
        try:
            # Extract operation and numbers from A2A task
            operation = task_data.get("operation", "add")
            numbers = task_data.get("numbers", [])
            
            if not numbers:
                raise ValueError("No numbers provided for calculation")
            
            # Perform calculation
            calc_result = await self.calculate(operation, numbers)
            
            # Return in A2A format
            return {
                "task_id": task_data.get("id", "unknown"),
                "result": calc_result,
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
            msg_type = message.get("type", "calculate")
            
            if msg_type == "calculate":
                return await self.calculate(
                    message.get("operation", "add"),
                    message.get("numbers", [])
                )
            elif msg_type == "get_statistics":
                return self.get_performance_stats()
            elif msg_type == "get_history":
                return {"history": self.calculation_history[-10:]}  # Last 10 calculations
            else:
                raise ValueError(f"Unknown collaboration message type: {msg_type}")
                
        except Exception as e:
            logger.error(f"❌ Lobby collaboration failed: {e}")
            return {"error": str(e), "status": "error"}
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for learning"""
        if not self.calculation_history:
            return {"message": "No calculations performed yet"}
        
        calc_times = [calc["calculation_time"] for calc in self.calculation_history]
        operations = [calc["operation"] for calc in self.calculation_history]
        
        return {
            "total_calculations": len(self.calculation_history),
            "average_calc_time": sum(calc_times) / len(calc_times),
            "fastest_calc_time": min(calc_times),
            "slowest_calc_time": max(calc_times),
            "operations_performed": list(set(operations)),
            "most_common_operation": max(set(operations), key=operations.count) if operations else None
        }

async def main():
    """Main function to run Calculator Agent"""
    logger.info("🧮 Starting Calculator Agent...")
    
    # Create calculator instance
    calculator = CalculatorAgent()
    
    try:
        # Initialize Agent Lobby SDK with A2A support
        sdk = AgentLobbySDK(
            agent_id=calculator.agent_id,
            name=calculator.name,
            agent_type="calculator",
            capabilities=calculator.capabilities,
            enable_a2a=True,  # Enable A2A protocol support
            task_handler=calculator.handle_lobby_collaboration
        )
        
        # Set A2A task handler
        if sdk.a2a_handler:
            sdk.a2a_handler.task_handler = calculator.handle_a2a_task
        
        # Register with Agent Lobby
        await sdk.register()
        logger.info("✅ Calculator Agent registered with Agent Lobby")
        
        # Generate A2A agent card
        if sdk.a2a_handler:
            a2a_card = sdk.generate_a2a_card()
            logger.info(f"📇 A2A Agent Card: {json.dumps(a2a_card, indent=2)}")
        
        # Start metrics collection
        if sdk.metrics_system:
            sdk.metrics_system.start()
            logger.info("📊 Metrics collection started")
        
        # Run some test calculations to populate history
        logger.info("🧪 Running initial test calculations...")
        test_calculations = [
            ("add", [1, 2, 3, 4, 5]),
            ("multiply", [2, 3, 4]),
            ("average", [10, 20, 30, 40, 50]),
            ("divide", [100, 5, 2])
        ]
        
        for operation, numbers in test_calculations:
            result = await calculator.calculate(operation, numbers)
            await asyncio.sleep(0.1)  # Small delay between calculations
        
        # Show performance stats
        stats = calculator.get_performance_stats()
        logger.info(f"📈 Performance Stats: {json.dumps(stats, indent=2)}")
        
        # Keep agent running
        logger.info("🟢 Calculator Agent ready for tasks...")
        logger.info("📡 A2A endpoint: http://localhost:8080/a2a/task")
        logger.info("🏛️ Agent Lobby: Connected and ready for collaboration")
        
        # Run indefinitely
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("🛑 Calculator Agent shutting down...")
    except Exception as e:
        logger.error(f"❌ Calculator Agent error: {e}")
    finally:
        if 'sdk' in locals():
            if sdk.metrics_system:
                sdk.metrics_system.stop()
            await sdk.disconnect()

if __name__ == "__main__":
    asyncio.run(main()) 