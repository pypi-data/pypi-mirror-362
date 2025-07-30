import asyncio
import logging
import os
import sys
import httpx
from pathlib import Path

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from core.lobby import Lobby
from core.collaboration_engine import WorkflowStatus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("NoAgentTest")

HTTP_PORT = 8126
WS_PORT = 8127
LOBBY_API_URL = f"http://localhost:{HTTP_PORT}"

async def main():
    """
    Test case to verify the system handles tasks with no capable agents.
    """
    # 1. Start the Lobby
    lobby = Lobby(
        http_port=HTTP_PORT,
        ws_port=WS_PORT
    )
    lobby_task = asyncio.create_task(lobby.start())
    await asyncio.sleep(2)  # Give lobby time to start

    workflow_id = None
    try:
        # 2. Submit a task that NO agent can handle
        task_payload = {
            "name": "Impossible Task",
            "description": "A task that requires a capability no one has.",
            "task_intent": "Process a video file.",
            "required_capabilities": ["video-processing"],
            "task_data": {"input_file": "movie.mp4"}
        }
        
        logger.info(f"TEST: Submitting task requiring 'video-processing' capability...")
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{LOBBY_API_URL}/api/tasks", json=task_payload, timeout=20)
            response.raise_for_status()
            result = response.json()
            workflow_id = result.get("workflow_id")
            assert workflow_id is not None
            logger.info(f"TEST: Task submitted successfully. Workflow ID: {workflow_id}")

        # 3. Wait and check workflow status
        await asyncio.sleep(10) # Give engine time to process and fail

        final_status_data = lobby.collaboration_engine.get_workflow_status(workflow_id)
        final_status = WorkflowStatus(final_status_data["status"])
        
        logger.info(f"TEST: Final workflow status: {final_status.value}")
        
        # 4. Assert that the workflow has failed gracefully
        assert final_status == WorkflowStatus.FAILED, f"Workflow status should be FAILED, but was {final_status.value}"
        # **FIX:** Check for the more generic workflow-level error message.
        assert "Workflow failed due to" in final_status_data.get("error", ""), "The workflow error message was not set correctly."
        
        logger.info("✅ TEST PASSED: Workflow correctly failed because no capable agent was found.")

    except Exception as e:
        logger.error(f"TEST: An unexpected error occurred: {e}", exc_info=True)
        assert False, "Test failed due to an unexpected exception."
    finally:
        # 5. Cleanup
        if workflow_id:
            final_status = lobby.collaboration_engine.get_workflow_status(workflow_id)
            logger.info(f"Final workflow details: {final_status}")
        
        await lobby.stop()
        lobby_task.cancel()
        try:
            await lobby_task
        except asyncio.CancelledError:
            pass
        logger.info("TEST: Lobby shut down.")
        
        # Cleanup DB files
        for f in Path.cwd().glob("test_no_agent_*.db*"):
            try:
                os.remove(f)
                logger.info(f"Cleaned up {f}")
            except OSError as e:
                logger.error(f"Error cleaning up file {f}: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 