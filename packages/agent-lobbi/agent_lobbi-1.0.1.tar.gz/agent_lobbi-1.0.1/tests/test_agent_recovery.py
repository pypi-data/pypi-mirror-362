import asyncio
import logging
import os
import sys
import httpx
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from core.lobby import Lobby
from sdk.agent_lobbi_sdk import AgentLobbySDK
from core.collaboration_engine import WorkflowStatus, TaskStatus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("RecoveryTest")

HTTP_PORT = 8124
WS_PORT = 8125
LOBBY_API_URL = f"http://localhost:{HTTP_PORT}"

# --- Global State for Test Coordination ---
class TestState:
    def __init__(self):
        self.agent_a_received_task = asyncio.Event()
        self.agent_b_received_task = asyncio.Event()
        self.agent_a_task_id = None
        self.agent_b_task_id = None

# --- Dummy Agent Setup ---
async def run_dummy_agent(agent_id: str, capabilities: list[str], state: TestState):
    """A dummy agent that signals when it receives a task."""
    sdk = AgentLobbySDK(
        lobby_host="localhost",
        lobby_port=HTTP_PORT,
        ws_port=WS_PORT,
        enable_security=False,
        db_path_prefix=f"test_{agent_id}"
    )

    async def task_handler(task_data):
        task_id = task_data.get('task_id')
        logger.info(f"AGENT {agent_id} received task: {task_id}")

        if agent_id == "agent_A":
            state.agent_a_task_id = task_id
            state.agent_a_received_task.set()
            # Agent A will hang forever to simulate a crash/unresponsiveness
            await asyncio.sleep(3600)
        
        if agent_id == "agent_B":
            state.agent_b_task_id = task_id
            state.agent_b_received_task.set()
            return {"status": "completed", "result": "I, agent B, finished the task."}

    await sdk.register_agent(
        agent_id=agent_id,
        name=agent_id,
        agent_type="RecoverableSummarizer",
        capabilities=capabilities,
        task_handler=task_handler,
    )
    logger.info(f"AGENT {agent_id} is running.")
    try:
        while True:
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        logger.info(f"AGENT {agent_id} is shutting down.")

# --- Test ---
async def main():
    lobby = Lobby(http_port=HTTP_PORT, ws_port=WS_PORT)
    await lobby.start()
    logger.info("TEST: Lobby started.")

    state = TestState()
    
    # 1. Start two capable agents
    agent_a_task = asyncio.create_task(run_dummy_agent("agent_A", ["text-summarization"], state))
    agent_b_task = asyncio.create_task(run_dummy_agent("agent_B", ["text-summarization"], state))

    # 2. Wait for both agents to connect
    while len(lobby.live_agent_connections) < 2:
        logger.info(f"TEST: Waiting for agents to connect... {len(lobby.live_agent_connections)}/2")
        await asyncio.sleep(1)
    
    logger.info("TEST: Both agents are connected.")

    # 3. Submit a task
    task_payload = {
        "name": "Critical Summary",
        "goal": "Summarize the critical document.",
        "required_capabilities": ["text-summarization"],
    }
    workflow_id = None
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{LOBBY_API_URL}/api/tasks", json=task_payload, timeout=10)
        response.raise_for_status()
        workflow_id = response.json().get("workflow_id")
        logger.info(f"TEST: Task submitted successfully. Workflow ID: {workflow_id}")

    # 4. Wait for Agent A to receive the task
    try:
        await asyncio.wait_for(state.agent_a_received_task.wait(), timeout=10)
        logger.info(f"TEST: Agent A received task {state.agent_a_task_id}. Simulating crash by cancelling it.")
        agent_a_task.cancel()
    except asyncio.TimeoutError:
        assert False, "Test failed: Agent A never received the initial task."

    # 5. Wait for Agent B to receive the re-assigned task
    try:
        logger.info("TEST: Waiting for task to be re-assigned to Agent B...")
        await asyncio.wait_for(state.agent_b_received_task.wait(), timeout=20.0) # Increased timeout
        logger.info(f"TEST: Agent B received task {state.agent_b_task_id}.")
        logger.info("✅ TEST PASSED: Task was successfully re-assigned to Agent B after Agent A failed.")
    except asyncio.TimeoutError:
        logger.error("TEST: Timed out waiting for Agent B to receive the re-assigned task.")
        # Add more debug info
        if workflow_id:
             final_status = lobby.collaboration_engine.get_workflow_status(workflow_id)
             logger.error(f"Final workflow status: {final_status}")
        assert False, "Test failed: Agent B did not receive the re-assigned task."

    # 6. Final verification
    assert state.agent_a_task_id is not None
    assert state.agent_b_task_id is not None
    assert state.agent_a_task_id == state.agent_b_task_id, "The task ID should be the same for both agents."

    # Cleanup
    agent_b_task.cancel()
    await lobby.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, AssertionError) as e:
        if isinstance(e, AssertionError):
            logger.error(f"❌ TEST FAILED: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        sys.exit(1) 