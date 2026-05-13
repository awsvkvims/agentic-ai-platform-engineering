# Agentic AI for Platform Engineering

A working agent system that applies AI reasoning to real DevOps 
and platform engineering workflows -- built to explore how 
agentic AI can reduce manual toil for delivery, infrastructure, 
and platform teams.

Built with LangGraph, Python, and OpenAI. Transparent by design:
every decision shows the selected tool, confidence level, and 
reasoning path.

github.com/awsvkvims/agentic-ai-platform-engineering

---

## What This Demonstrates

This is not a chatbot or a tutorial. It is a working agent 
system with deterministic tool execution, observable reasoning, 
and a domain-specific tool registry covering the workflows 
platform and DevOps teams deal with every day.

Specifically it demonstrates:

- Agentic system design using LangGraph orchestration
- Tool selection via structured LLM reasoning (tool + confidence 
  + explanation)
- Deterministic tool execution decoupled from LLM responses
- Two-pass response synthesis (generation + refinement)
- Observable decision paths logged per interaction
- Domain tools covering Agile delivery, DevOps, IaC, and 
  platform engineering

---

## Agent Capabilities

The agent can reason about and analyze:

| Domain | Capability |
|---|---|
| Agile & SAFe Delivery | Backlog risk detection, PI planning dependencies, Kanban flow metrics |
| DevOps | CI/CD pipeline risk review, infrastructure PR summarization |
| Infrastructure as Code | Terraform configuration risk analysis, security and best practice review |
| Platform Engineering | Internal developer platform (IDP) guidance, Backstage workflow patterns |
| FinOps & Governance | Foundation for compliance and cloud governance agents (roadmap) |

---

## How the Agent Works

Every request follows this reasoning path:

```text
User Input
  -> CLI
  -> LangGraph Agent
  -> Tool Selector LLM  (returns JSON: tool + reason + confidence)
  -> Router
      -> Tool Registry  (if high confidence tool match)
      -> Fallback Model (if no strong match)
  -> Tool Execution     (deterministic Python function)
  -> Synthesis LLM      (first pass)
  -> Refinement LLM     (second pass)
  -> Final Response + Interaction Log

Each interaction logs: selected tool, confidence, reasoning, 
tool output, and final response -- making the agent's decisions 
fully auditable.

```

---

## Why This Architecture

Three design principles drove every decision:

**Transparent reasoning.** The agent explains why it selected 
a tool and how confident it is. Black-box AI responses are not 
acceptable in platform engineering contexts.

**Deterministic tool execution.** Domain knowledge lives in 
Python functions, not LLM prompts. This makes tools testable, 
predictable, and independently improvable.

**Simple extensibility.** Adding a new capability means adding 
a tool to the registry and a sample input. The LangGraph 
workflowdoes not change.

---

## Quickstart

```code
    python3.13 -m venv venv
    source venv/bin/activate
    pip install openai python-dotenv pytest langgraph langchain-core
```
Create a .env file:

```code
    OPENAI_API_KEY=your_api_key_here
```

Run the CLI:

```code
    python -m scripts.agent_cli
```

Run the evaluation suite:

```code
    python -m scripts.eval_prompts
```

---

## CLI Commands

    analyze backlog      -- detect delivery risk in backlog items
    analyze terraform    -- review IaC for security and best practice risks
    analyze pipeline     -- review CI/CD pipeline for delivery risks
    analyze pr           -- summarize infrastructure pull request changes
    list tools           -- show available tools
    show tool descriptions

---

## Repository Structure

    src/ai/        agent orchestration, LangGraph graph, prompt loading
    src/tools/     deterministic domain tools
    scripts/       CLI and evaluation entry points
    samples/       sample backlog, Terraform, pipeline, and PR inputs
    prompts/       tool selector and synthesis prompts (separate from code)
    tests/         automated tests
    logs/          interaction logs
    docs/          architecture detail

---

## Roadmap

| Increment | Theme | Status |
|---|---|---|
| 1 | Foundational agent architecture and tool system | Done |
| 2 | Model-driven tool selection, response synthesis, backlog analysis | Done |
| 3 | LangGraph orchestration, Terraform, CI/CD, and PR tools | Done |
| 4 | Platform engineering assistants, IDP and Backstage workflows | In Progress |
| 5 | Compliance and FinOps governance agents | Planned |

---

## Context

Platform engineering teams already orchestrate complex systems 
-- infrastructure provisioning, CI/CD pipelines, developer 
onboarding, governance, and delivery workflows.

This project explores how agentic AI can augment those systems 
with context-aware reasoning -- reducing manual toil, improving 
visibility, and accelerating engineering decisions.

The goal is assistive intelligence, not autonomous action. 
Agents should be transparent, controllable, and safe.

---

## Discussion

If you are designing an Agentic AI roadmap for a platform 
engineering or DevOps organization, collaboration and 
discussion are welcome.
