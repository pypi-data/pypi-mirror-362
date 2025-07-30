import asyncio
import logging
import os
import time
import uuid

# Ensure src is in path
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from core.lobby import Lobby
from core.message import Message, MessageType, MessagePriority
from sdk.agent_lobbi_sdk import AgentLobbySDK

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("CollabTest")

HTTP_PORT = 8120
WS_PORT = 8121

async def run_dummy_agent(agent_id: str, capabilities: list[str]):
    """Spin-up an SDK-powered dummy agent that simply echoes tasks."""
    sdk = AgentLobbySDK(
        lobby_host="localhost",
        lobby_port=HTTP_PORT,
        ws_port=WS_PORT,
        enable_security=False,
        db_path_prefix=f"test_{agent_id}"
    )

    async def task_handler(task_data):
        logger.info(f"{agent_id} received task: {task_data}")
        # Simulate work
        await asyncio.sleep(1)
        # Respond in a minimal format the lobby currently understands
        return {"echo": task_data}

    await sdk.register_agent(
        agent_id=agent_id,
        name=agent_id,
        agent_type="DummyAgent",
        capabilities=capabilities,
        task_handler=task_handler,
    )

    # Keep agent alive
    while True:
        await asyncio.sleep(5)

async def main():
    # 1. Start lobby
    lobby = Lobby(http_port=HTTP_PORT, ws_port=WS_PORT)
    await lobby.start()

    logger.info("Lobby started – launching agents…")

    # 2. Launch two dummy agents
    agent_tasks = [
        asyncio.create_task(run_dummy_agent("agent_alpha", ["text-summarization"])),
        asyncio.create_task(run_dummy_agent("agent_beta", ["data-analysis"])),
    ]

    # 3. Wait until both WebSocket connections are active
    while len(lobby.live_agent_connections) < 2:
        logger.info(f"Waiting for agents to connect… {len(lobby.live_agent_connections)}/2 connected")
        await asyncio.sleep(1)

    logger.info("Both agents are online – sending a test task to agent_alpha")

    # 4. Craft test message
    test_message = Message(
        sender_id="test_suite",
        receiver_id="agent_alpha",
        message_type=MessageType.REQUEST,
        payload={
            "task_id": str(uuid.uuid4()),
            "task_name": "Quick Echo",
            "capability_name": "text-summarization",
            "input_data": {"text": "Hello world"},
        },
        priority=MessagePriority.NORMAL,
    )

    await lobby._priority_queues[test_message.priority.value].put(
        (test_message.priority.value, time.time(), test_message.message_id, test_message)
    )

    # 5. Let the system run for a short while so messages round-trip
    await asyncio.sleep(5)

    logger.info("Shutting everything down…")
    for t in agent_tasks:
        t.cancel()
    await lobby.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass 