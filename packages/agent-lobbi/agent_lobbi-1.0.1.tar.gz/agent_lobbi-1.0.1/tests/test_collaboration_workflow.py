import asyncio
import logging
import os
import sys
import uuid
import httpx
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from core.lobby import Lobby
from sdk.agent_lobbi_sdk import AgentLobbySDK
from core.collaboration_engine import WorkflowStatus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("WorkflowTest")

HTTP_PORT = 8122
WS_PORT = 8123
LOBBY_API_URL = f"http://localhost:{HTTP_PORT}"

# --- Dummy Agent Setup ---
async def run_dummy_agent(agent_id: str, capabilities: list[str], received_task_event: asyncio.Event):
    """A dummy agent that confirms it received a task."""
    sdk = AgentLobbySDK(
        lobby_host="localhost",
        lobby_port=HTTP_PORT,
        ws_port=WS_PORT,
        enable_security=False,
        db_path_prefix=f"test_{agent_id}"
    )

    async def task_handler(task_data):
        logger.info(f"AGENT {agent_id} received task: {task_data.get('name')}")
        received_task_event.set() # Signal that the task was received
        return {"status": "completed", "result": "I summarized the text!"}

    await sdk.register_agent(
        agent_id=agent_id,
        name=agent_id,
        agent_type="SummarizerAgent",
        capabilities=capabilities,
        task_handler=task_handler,
    )
    logger.info(f"AGENT {agent_id} is running and waiting for tasks.")
    # Keep agent alive
    while True:
        await asyncio.sleep(5)

# --- Test ---
async def main():
    lobby = Lobby(http_port=HTTP_PORT, ws_port=WS_PORT)
    await lobby.start()
    logger.info("TEST: Lobby started.")

    received_task_event = asyncio.Event()

    # 1. Start a capable agent
    agent_task = asyncio.create_task(
        run_dummy_agent("agent_summarizer_1", ["text-summarization"], received_task_event)
    )

    # 2. Wait for the agent to connect
    while len(lobby.live_agent_connections) < 1:
        logger.info("TEST: Waiting for agent to connect...")
        await asyncio.sleep(1)
    
    logger.info("TEST: Agent is connected. Submitting task via API.")

    # 3. Submit a task via the new API endpoint
    task_payload = {
        "name": "Summarize Report",
        "goal": "Summarize the provided quarterly report.",
        "required_capabilities": ["text-summarization"],
        "task_data": {
            "document_url": "http://example.com/report.pdf"
        }
    }

    workflow_id = None
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{LOBBY_API_URL}/api/tasks", json=task_payload, timeout=10)
            response.raise_for_status()
            response_data = response.json()
            workflow_id = response_data.get("workflow_id")
            logger.info(f"TEST: Successfully submitted task. Workflow ID: {workflow_id}")
            assert workflow_id is not None
        except httpx.RequestError as e:
            logger.error(f"TEST: Failed to submit task to API: {e}")
            assert False, "API task submission failed"

    # 4. Wait for the agent to receive the task
    try:
        await asyncio.wait_for(received_task_event.wait(), timeout=10.0)
        logger.info("TEST: Agent successfully received the task.")
    except asyncio.TimeoutError:
        logger.error("TEST: Timed out waiting for agent to receive task.")
        assert False, "Test failed: Agent did not receive the task in time."
    
    # 5. Check workflow status (optional, but good practice)
    await asyncio.sleep(2) # Give time for status to update
    final_status = lobby.collaboration_engine.get_workflow_status(workflow_id)
    logger.info(f"TEST: Final workflow status: {final_status}")

    # The goal is to see the task delivered. A full 'COMPLETED' status
    # might take more work, but this confirms the critical path.
    assert final_status['status'] in [WorkflowStatus.RUNNING.value, WorkflowStatus.COMPLETED.value]

    logger.info("✅ TEST PASSED: Collaboration workflow test completed successfully.")

    # Cleanup
    agent_task.cancel()
    await lobby.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, AssertionError) as e:
        if isinstance(e, AssertionError):
            logger.error(f"❌ TEST FAILED: {e}")
        sys.exit(1) 