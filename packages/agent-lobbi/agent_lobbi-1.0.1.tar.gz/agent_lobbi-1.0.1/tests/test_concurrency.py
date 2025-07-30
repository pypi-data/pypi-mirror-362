import asyncio
import logging
import os
import sys
import httpx
from pathlib import Path
import random

# Ensure src is in path
sys.path.append(str(Path(__file__).resolve().parent.parent / 'src'))

from core.lobby import Lobby
from sdk.agent_lobbi_sdk import AgentLobbySDK

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(name)s - %(message)s')
logger = logging.getLogger("ConcurrencyTest")

# --- Test Configuration ---
HTTP_PORT = 8128
WS_PORT = 8129
LOBBY_API_URL = f"http://localhost:{HTTP_PORT}"
NUM_AGENTS = 50  # Number of concurrent agents to simulate
AGENT_CAPABILITIES = ["text-generation", "data-analysis", "file-io"]

# --- Dummy Agent ---
async def run_concurrent_agent(agent_num: int):
    """A dummy agent that registers and connects, then waits."""
    agent_id = f"concurrent_agent_{agent_num}"
    try:
        sdk = AgentLobbySDK(
            lobby_host="localhost",
            lobby_port=HTTP_PORT,
            ws_port=WS_PORT,
            enable_security=False,
            db_path_prefix=f"test_concurrency_{agent_id}" # Prevent DB contention
        )

        # **FIX: Use the correct method to register and connect.**
        await sdk.register_agent(
            agent_id=agent_id,
            name=agent_id,
            agent_type="ConcurrentTester",
            capabilities=[random.choice(AGENT_CAPABILITIES)]
        )
        
        logger.info(f"✅ Agent {agent_id} connected successfully.")
        
        # Keep the agent alive to maintain the connection
        await asyncio.sleep(30) 
        
    except Exception as e:
        logger.error(f"❌ Agent {agent_id} failed to connect: {e}", exc_info=True)
        return False
    finally:
        # Cleanup DB files for this agent
        for f in Path.cwd().glob(f"test_concurrency_{agent_id}_*.db*"):
            try:
                os.remove(f)
            except OSError:
                pass # Ignore cleanup errors
    return True


async def main():
    """
    Test case to verify concurrent agent connections.
    """
    # 1. Start the Lobby
    lobby = Lobby(http_port=HTTP_PORT, ws_port=WS_PORT)
    lobby_task = asyncio.create_task(lobby.start())
    await asyncio.sleep(2) # Give lobby time to start

    try:
        logger.info(f"--- Starting {NUM_AGENTS} concurrent agents ---")
        
        # 2. Launch all agents concurrently
        agent_tasks = [run_concurrent_agent(i) for i in range(NUM_AGENTS)]
        results = await asyncio.gather(*agent_tasks)
        
        # 3. Verify results
        successful_agents = sum(1 for r in results if r is True)
        logger.info(f"--- Test complete: {successful_agents} / {NUM_AGENTS} agents connected successfully. ---")
        
        registered_count = len(lobby.agents)
        live_connection_count = len(lobby.live_agent_connections)

        logger.info(f"Lobby state: {registered_count} agents registered, {live_connection_count} live connections.")

        assert successful_agents == NUM_AGENTS, f"Expected {NUM_AGENTS} successful connections, but got {successful_agents}."
        assert registered_count == NUM_AGENTS, f"Lobby should have {NUM_AGENTS} registered, but has {registered_count}."
        assert live_connection_count == NUM_AGENTS, f"Lobby should have {NUM_AGENTS} live connections, but has {live_connection_count}."

        logger.info(f"✅ TEST PASSED: Successfully handled {NUM_AGENTS} concurrent connections.")

    except Exception as e:
        logger.error(f"TEST: An unexpected error occurred: {e}", exc_info=True)
        assert False, "Test failed due to an unexpected exception."
    finally:
        # 4. Cleanup
        await lobby.stop()
        lobby_task.cancel()
        try:
            await lobby_task
        except asyncio.CancelledError:
            pass
        logger.info("TEST: Lobby shut down.")

if __name__ == "__main__":
    # Increase the default asyncio debug level for this test
    os.environ['PYTHONASYNCIODEBUG'] = '1'
    asyncio.run(main()) 