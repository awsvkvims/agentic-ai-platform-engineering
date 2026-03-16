# Agentic AI for Platform Engineering Lab

Practical experiments exploring how agentic AI can support Agile delivery, DevOps enablement, and modern platform engineering teams.

---

# Overview

This repository explores how agent-style AI systems can assist engineering organizations with real operational workflows.

The focus is on practical scenarios across:

- Agile and SAFe delivery
- Kanban flow optimization
- DevOps enablement
- Infrastructure as Code (Terraform)
- CI/CD automation
- Developer platforms such as Backstage
- Cloud governance, compliance, and FinOps

Rather than building generic chatbots, the goal is to design assistive agents that can reason about engineering workflows and interact with tools and structured data.

Examples explored in this repository include:

- analyzing backlog risk and delivery bottlenecks
- explaining Kanban flow metrics
- guiding developers through platform engineering concepts
- detecting delivery risks in backlog items
- preparing the foundation for DevOps and platform agents

---

# Current Capabilities

The current implementation demonstrates a minimal agent architecture that can:

- select tools using an LLM
- reason about when tools should be used
- execute deterministic tools
- synthesize responses from tool results
- analyze backlog risk using real backlog data
- provide CLI interaction with observable reasoning

Example capabilities include:

- Kanban metric explanations
- backlog risk detection
- backlog analysis using sample backlog data
- platform engineering explanations
- PI planning dependency explanations

The system logs the reasoning path including:

- selected tool
- confidence level
- reasoning explanation
- tool output

This makes the system easier to inspect and debug.

---

# Architecture

A high level overview of the architecture is available in:

docs/architecture.md

The current system follows a simple agent workflow.

User
-> CLI
-> Tool Selector LLM
-> JSON tool decision
-> Router
-> Tool Registry
-> Tool Execution
-> Tool Result
-> Response Synthesis LLM
-> Final Response

The architecture emphasizes:

- transparent reasoning
- deterministic tool execution
- observable decision paths
- simple extensibility

---

# Quickstart

Create and activate a virtual environment

    python3.13 -m venv venv
    source venv/bin/activate

Install dependencies

    pip install openai python-dotenv pytest

Create a .env file in the project root

    OPENAI_API_KEY=your_api_key_here

Run the CLI

    python agent_cli.py

---

# CLI Commands

Inside the CLI you can run the following commands.

- help
- list tools
- show tool descriptions
- analyze backlog

---

# Example Questions

Examples of questions you can ask the agent.

- What is lead time?
- What are signs that a backlog may have delivery risk?
- How should I analyze backlog items for delivery risk?
- What is an internal developer platform?
- Explain PI planning dependencies.

---

# Evaluation Script

You can run a quick evaluation of routing behavior.

    python eval_prompts.py

This runs several prompts and prints:

- selected tool
- reasoning
- confidence level
- response

---

# Repository Goals

This repository serves three purposes.

- **Experimentation**: Exploring agent design patterns applicable to platform engineering and DevOps environments.

- **Reference Implementations**: Providing small working examples of agent workflows that support delivery, infrastructure, and platform operations.

- **Advisory Foundation**: Demonstrating approaches that can help organizations design an Agentic AI roadmap for platform engineering.

---

# Project Roadmap

The repository evolves incrementally.

- **Increment 1**: Foundational agent architecture and tool system.

- **Increment 2**: Model driven tool selection and backlog analysis agents.

- **Increment 3**: LangGraph integration and DevOps oriented agents.

- **Increment 4**: Platform engineering assistants inspired by Backstage workflows.

- **Increment 5**: Compliance and FinOps governance agents.

---

# Why Agentic AI for Platform Engineering

Platform teams already orchestrate complex systems such as:

- infrastructure provisioning
- CI/CD pipelines
- developer onboarding
- governance and compliance
- delivery workflows

Agentic AI can augment these systems by providing context aware reasoning and workflow assistance.

Potential benefits include:

- reducing manual operational work
- improving developer onboarding
- accelerating delivery workflows
- improving governance visibility
- supporting engineering decision making

The goal is assistive intelligence rather than autonomous systems.

Agents should remain transparent, controllable, and safe.

---

# Collaboration

This repository is part of an ongoing exploration into how agentic AI can become a practical capability inside platform engineering teams.

If you are exploring similar ideas or designing an Agentic AI roadmap for your platform organization, collaboration and discussion are welcome.