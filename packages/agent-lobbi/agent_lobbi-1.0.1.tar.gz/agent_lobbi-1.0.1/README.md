# 🤖 Agent Lobbi – Universal Agent Interoperability Platform

[![PyPI version](https://badge.fury.io/py/agent-lobbi.svg)](https://badge.fury.io/py/agent-lobbi)
[![Python Support](https://img.shields.io/pypi/pyversions/agent-lobbi.svg)](https://pypi.org/project/agent-lobbi/)
[![License: Commercial](https://img.shields.io/badge/License-Commercial-red.svg)](https://agentlobby.com/license)

**Agent Lobbi** is the all-in-one interoperability layer that lets *any* AI agent, service, or application collaborate seamlessly.  At its core is **A2A+** – our superset of the industry-standard A2A protocol – plus an advanced multi-agent orchestration engine, neuromorphic intelligence, real-time metrics, and enterprise-grade security.

---

## 🚀 Highlights

| Capability | Why It Matters |
|------------|----------------|
| **Universal Interoperability** | Connect Python, JavaScript, REST, gRPC, and cloud functions out-of-the-box. |
| **A2A+ Agent-to-Agent** | Speak fluent A2A while enjoying Lobbi extensions: streaming, auth, capability discovery. |
| **Multi-Agent Orchestration** | Neuromorphic selection, N-to-N collaboration, automatic task decomposition. |
| **Metrics & Observability** | 10 000+ metrics / sec, Prometheus endpoint, Grafana dashboard template included. |
| **Enterprise Security** | Consensus, reputation, encryption, zero-trust by default. |
| **Plug-and-Play SDKs** | Python & JS SDKs, CLI tooling, and ready-to-deploy Docker images. |

---

## 🧩 Installation

```bash
pip install agent-lobbi  # base
# or
pip install agent-lobbi[all]  # dev, docs, monitoring, enterprise extras
```

---

## ⚡ Quick Start – 3 Lines

```python
from agent_lobbi import AgentLobbySDK
sdk = AgentLobbySDK(enable_a2a=True)  # A2A+ on by default
await sdk.register_agent(agent_id="hello_world", capabilities=["greeting"], auto_start_a2a=True)
```
Your agent immediately publishes an A2A+ card at `/.well-known/agent.json` and can accept or delegate tasks.

---

## 🤝 Multi-Agent Example (Async / Python)

```python
import asyncio
from agent_lobbi import AgentLobbySDK

async def main():
    sdk = AgentLobbySDK(enable_a2a=True, enable_metrics=True)

    # Register two simple agents
    await sdk.register_agent("writer", capabilities=["draft"], auto_start_a2a=True)
    await sdk.register_agent("reviewer", capabilities=["edit"], auto_start_a2a=True)

    # Orchestrate a collaboration
    report = await sdk.create_collaboration(
        participants=["writer", "reviewer"],
        purpose="Generate & polish Q3 report",
        shared_workspace=True,
    )
    print("Collaboration ID:", report["collaboration_id"])

asyncio.run(main())
```

---

## 📊 Metrics in One Call

```python
metrics = sdk.get_metrics_dashboard()
print(metrics["performance"]["response_time_ms"], "ms")
```
A Prometheus-ready endpoint is automatically exposed at `/api/metrics`.

---

## 🔐 License

This software is provided under a **Commercial License**.  Contact <sales@agentlobby.com> for details and enterprise terms.

---

## ❤️ A Note From Us

*Made with ❤️ from Agent Lobbi to you — happy collaborating!* 