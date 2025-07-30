#!/usr/bin/env python3
"""
Updated Simple Mock Lobby Server
Supports the integrated Agent Lobbi SDK with enhanced features
"""

import asyncio
import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Dict, Set, Any
from aiohttp import web, WSMsgType
import websockets
from websockets.exceptions import ConnectionClosedError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EnhancedMockLobby:
    """Enhanced mock lobby server with SDK integration support"""
    
    def __init__(self, http_port: int = 8093, ws_port: int = 8094):
        self.http_port = http_port
        self.ws_port = ws_port
        
        # Agent registry
        self.registered_agents: Dict[str, Dict[str, Any]] = {}
        self.websocket_connections: Dict[str, Any] = {}
        
        # Task and collaboration tracking
        self.completed_tasks: Dict[str, Dict[str, Any]] = {}
        self.collaborations: Dict[str, Dict[str, Any]] = {}
        
        # Security and metrics
        self.agent_metrics: Dict[str, Dict[str, Any]] = {}
        self.data_access_attempts: List[Dict[str, Any]] = []
        
        logger.info(f"Enhanced Mock Lobby initialized - HTTP:{http_port}, WS:{ws_port}")
    
    async def register_agent_handler(self, request):
        """Enhanced agent registration handler"""
        try:
            data = await request.json()
            agent_id = data.get('payload', {}).get('agent_id')
            agent_type = data.get('payload', {}).get('agent_type', 'Unknown')
            capabilities = data.get('payload', {}).get('capabilities', [])
            
            if not agent_id:
                return web.json_response(
                    {"status": "error", "message": "Missing agent_id"},
                    status=400
                )
            
            # Register agent with enhanced info
            registration_data = {
                "agent_id": agent_id,
                "agent_type": agent_type,
                "capabilities": capabilities,
                "registered_at": datetime.now(timezone.utc).isoformat(),
                "status": "active",
                "auth_token": f"token_{uuid.uuid4().hex[:16]}",
                "api_key": f"api_{uuid.uuid4().hex[:16]}",
                "session_id": f"session_{uuid.uuid4().hex[:12]}"
            }
            
            self.registered_agents[agent_id] = registration_data
            
            # Initialize metrics
            self.agent_metrics[agent_id] = {
                "tasks_completed": 0,
                "collaborations_joined": 0,
                "data_accesses": 0,
                "total_points": 0.0,
                "performance_score": 1.0
            }
            
            logger.info(f"Enhanced registration: {agent_id} ({agent_type}) with {len(capabilities)} capabilities")
            
            return web.json_response({
                "status": "success",
                "agent_id": agent_id,
                "auth_token": registration_data["auth_token"],
                "api_key": registration_data["api_key"],
                "session_id": registration_data["session_id"],
                "message": "Agent registered with enhanced features"
            })
            
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return web.json_response(
                {"status": "error", "message": str(e)},
                status=500
            )
    
    async def task_submission_handler(self, request):
        """Handle task submissions for consensus system"""
        try:
            data = await request.json()
            agent_id = data.get('agent_id')
            task_id = data.get('task_id')
            difficulty = data.get('difficulty', 'medium')
            collaborators = data.get('collaborators', [])
            quality_score = data.get('quality_score', 1.0)
            
            if not agent_id or not task_id:
                return web.json_response(
                    {"status": "error", "message": "Missing required fields"},
                    status=400
                )
            
            # Calculate points based on difficulty
            difficulty_multipliers = {
                "trivial": 1.0,
                "easy": 1.5,
                "medium": 2.0,
                "hard": 3.0,
                "expert": 5.0
            }
            
            base_points = 10.0
            difficulty_multiplier = difficulty_multipliers.get(difficulty, 2.0)
            collaboration_bonus = len(collaborators) * 2.0
            
            points_awarded = base_points * difficulty_multiplier * quality_score + collaboration_bonus
            
            # Track task
            task_data = {
                "task_id": task_id,
                "agent_id": agent_id,
                "difficulty": difficulty,
                "collaborators": collaborators,
                "quality_score": quality_score,
                "points_awarded": points_awarded,
                "completed_at": datetime.now(timezone.utc).isoformat()
            }
            
            self.completed_tasks[task_id] = task_data
            
            # Update agent metrics
            if agent_id in self.agent_metrics:
                self.agent_metrics[agent_id]["tasks_completed"] += 1
                self.agent_metrics[agent_id]["total_points"] += points_awarded
                
                # Update collaborators
                for collab_id in collaborators:
                    if collab_id in self.agent_metrics:
                        self.agent_metrics[collab_id]["collaborations_joined"] += 1
                        self.agent_metrics[collab_id]["total_points"] += (points_awarded * 0.3)
            
            logger.info(f"Task submitted: {task_id} by {agent_id}, {points_awarded:.1f} points awarded")
            
            return web.json_response({
                "status": "success",
                "task_id": task_id,
                "points_awarded": points_awarded,
                "message": "Task recorded in consensus system"
            })
            
        except Exception as e:
            logger.error(f"Task submission error: {e}")
            return web.json_response(
                {"status": "error", "message": str(e)},
                status=500
            )
    
    async def data_access_handler(self, request):
        """Handle data access requests for protection layer"""
        try:
            data = await request.json()
            requester_id = data.get('requester_id')
            target_agent = data.get('target_agent')
            data_type = data.get('data_type')
            purpose = data.get('purpose', '')
            
            # Simple access control logic
            access_granted = True
            denial_reason = None
            
            # Block suspicious requests
            suspicious_keywords = ['confidential', 'model_weights', 'training_data', 'proprietary']
            if any(keyword in data_type.lower() or keyword in purpose.lower() 
                   for keyword in suspicious_keywords):
                access_granted = False
                denial_reason = "Suspicious data access pattern detected"
            
            # Track access attempt
            access_attempt = {
                "requester_id": requester_id,
                "target_agent": target_agent,
                "data_type": data_type,
                "purpose": purpose,
                "access_granted": access_granted,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "denial_reason": denial_reason
            }
            
            self.data_access_attempts.append(access_attempt)
            
            # Update metrics
            if requester_id in self.agent_metrics:
                self.agent_metrics[requester_id]["data_accesses"] += 1
            
            logger.info(f"Data access: {requester_id} -> {target_agent}/{data_type}: {'GRANTED' if access_granted else 'DENIED'}")
            
            return web.json_response({
                "status": "success" if access_granted else "denied",
                "access_granted": access_granted,
                "target_agent": target_agent,
                "data_type": data_type,
                "reason": "Access granted" if access_granted else denial_reason,
                "data": {"sample": "data"} if access_granted else None
            })
            
        except Exception as e:
            logger.error(f"Data access error: {e}")
            return web.json_response(
                {"status": "error", "message": str(e)},
                status=500
            )
    
    async def metrics_handler(self, request):
        """Handle agent metrics requests"""
        try:
            agent_id = request.query.get('agent_id')
            
            if agent_id and agent_id in self.agent_metrics:
                metrics = self.agent_metrics[agent_id].copy()
                metrics["agent_id"] = agent_id
                return web.json_response({
                    "status": "success",
                    "metrics": metrics
                })
            else:
                # Return system overview
                total_agents = len(self.registered_agents)
                total_tasks = len(self.completed_tasks)
                total_points = sum(m.get("total_points", 0) for m in self.agent_metrics.values())
                
                return web.json_response({
                    "status": "success",
                    "system_metrics": {
                        "total_agents": total_agents,
                        "total_tasks": total_tasks,
                        "total_points": total_points,
                        "active_collaborations": len(self.collaborations)
                    }
                })
                
        except Exception as e:
            logger.error(f"Metrics error: {e}")
            return web.json_response(
                {"status": "error", "message": str(e)},
                status=500
            )
    
    async def leaderboard_handler(self, request):
        """Handle leaderboard requests"""
        try:
            limit = int(request.query.get('limit', 10))
            
            # Sort agents by total points
            sorted_agents = sorted(
                [(aid, metrics) for aid, metrics in self.agent_metrics.items()],
                key=lambda x: x[1].get("total_points", 0),
                reverse=True
            )
            
            leaderboard = []
            for i, (agent_id, metrics) in enumerate(sorted_agents[:limit]):
                leaderboard.append({
                    "rank": i + 1,
                    "agent_id": agent_id,
                    "total_points": metrics.get("total_points", 0),
                    "tasks_completed": metrics.get("tasks_completed", 0),
                    "collaborations_joined": metrics.get("collaborations_joined", 0)
                })
            
            return web.json_response({
                "status": "success",
                "leaderboard": leaderboard
            })
            
        except Exception as e:
            logger.error(f"Leaderboard error: {e}")
            return web.json_response(
                {"status": "error", "message": str(e)},
                status=500
            )
    
    async def websocket_handler(self, websocket, path):
        """Enhanced WebSocket handler"""
        agent_id = "unknown_agent"
        try:
            logger.info("New WebSocket connection attempt")
            
            async for message in websocket:
                try:
                    data = json.loads(message)
                    msg_type = data.get("type", "unknown")
                    
                    if msg_type == "identify":
                        agent_id = data.get("agent_id", f"agent_{uuid.uuid4().hex[:8]}")
                        self.websocket_connections[agent_id] = websocket
                        logger.info(f"WebSocket identified: {agent_id}")
                        
                        await websocket.send(json.dumps({
                            "type": "identified",
                            "agent_id": agent_id,
                            "status": "connected"
                        }))
                    
                    elif msg_type == "collaboration_request":
                        # Handle collaboration requests
                        collab_id = f"collab_{uuid.uuid4().hex[:8]}"
                        participants = data.get("participants", [])
                        
                        self.collaborations[collab_id] = {
                            "id": collab_id,
                            "participants": participants,
                            "created_by": agent_id,
                            "created_at": datetime.now(timezone.utc).isoformat()
                        }
                        
                        await websocket.send(json.dumps({
                            "type": "collaboration_created",
                            "collaboration_id": collab_id,
                            "participants": participants
                        }))
                        
                        logger.info(f"Collaboration created: {collab_id} by {agent_id}")
                    
                except json.JSONDecodeError:
                    logger.error("Invalid JSON in WebSocket message")
                except Exception as e:
                    logger.error(f"WebSocket message error: {e}")
                    
        except ConnectionClosedError:
            logger.info(f"WebSocket disconnected: {agent_id}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            if agent_id in self.websocket_connections:
                del self.websocket_connections[agent_id]
            logger.info(f"Cleaned up WebSocket for: {agent_id}")
    
    def create_http_app(self):
        """Create HTTP application with all endpoints"""
        app = web.Application()
        
        # Add CORS headers
        async def add_cors_headers(request, handler):
            response = await handler(request)
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
            return response
        
        app.middlewares.append(add_cors_headers)
        
        # Routes
        app.router.add_post('/api/register', self.register_agent_handler)
        app.router.add_post('/api/tasks', self.task_submission_handler)
        app.router.add_post('/api/data_access', self.data_access_handler)
        app.router.add_get('/api/metrics', self.metrics_handler)
        app.router.add_get('/api/leaderboard', self.leaderboard_handler)
        
        # Health check
        async def health_check(request):
            return web.json_response({
                "status": "healthy",
                "agents_registered": len(self.registered_agents),
                "websocket_connections": len(self.websocket_connections),
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
        
        app.router.add_get('/health', health_check)
        
        return app
    
    async def start_servers(self):
        """Start both HTTP and WebSocket servers"""
        logger.info("Starting Enhanced Mock Lobby servers...")
        
        # Start HTTP server
        app = self.create_http_app()
        runner = web.AppRunner(app)
        await runner.setup()
        
        site = web.TCPSite(runner, 'localhost', self.http_port)
        await site.start()
        
        logger.info(f"HTTP server started on http://localhost:{self.http_port}")
        
        # Start WebSocket server
        ws_server = await websockets.serve(
            self.websocket_handler,
            'localhost',
            self.ws_port,
            ping_interval=30,
            ping_timeout=10
        )
        
        logger.info(f"WebSocket server started on ws://localhost:{self.ws_port}")
        
        return runner, ws_server
    
    async def stop_servers(self, runner, ws_server):
        """Stop all servers"""
        logger.info("Stopping Enhanced Mock Lobby servers...")
        
        ws_server.close()
        await ws_server.wait_closed()
        
        await runner.cleanup()
        
        logger.info("All servers stopped")

async def main():
    """Main function to run the enhanced mock lobby"""
    lobby = EnhancedMockLobby(http_port=8093, ws_port=8094)
    
    try:
        runner, ws_server = await lobby.start_servers()
        
        print("Enhanced Mock Lobby running:")
        print(f"  HTTP API: http://localhost:{lobby.http_port}")
        print(f"  WebSocket: ws://localhost:{lobby.ws_port}")
        print("  Endpoints:")
        print("    POST /api/register - Agent registration")
        print("    POST /api/tasks - Task submission")
        print("    POST /api/data_access - Data access requests")
        print("    GET /api/metrics - Agent metrics")
        print("    GET /api/leaderboard - Reputation leaderboard")
        print("    GET /health - Health check")
        print("\\nPress Ctrl+C to stop...")
        
        # Keep running
        while True:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        print("\\nShutting down...")
    except Exception as e:
        logger.error(f"Server error: {e}")
    finally:
        await lobby.stop_servers(runner, ws_server)

if __name__ == "__main__":
    asyncio.run(main()) 