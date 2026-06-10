# Agentic AI for Platform Engineering

Practical agentic AI applied to real platform engineering workflows - Terraform risk
analysis, CI/CD pipeline review, backlog risk detection, and developer platform
guidance.

Built with LangGraph and OpenAI. Designed for engineering organizations moving toward
AI-driven delivery lifecycles (AI-DLC).

---

## Overview

This repository explores how agent-style AI systems can support engineering
organizations with operational delivery workflows.

The focus is on practical, deterministic tool execution guided by LLM reasoning
across:

- Agile and SAFe delivery
- Kanban flow optimization
- DevOps enablement
- Infrastructure as Code (Terraform)
- CI/CD pipeline governance
- Internal developer platforms (IDP / Backstage)
- Cloud governance and compliance

Rather than generic chatbots, the goal is assistive agents that reason about
engineering workflows and interact with structured data.

---

## Agent Architecture

The agent follows a transparent, observable reasoning loop:

```
User Input
    |
    v
CLI Interface
    |
    v
LangGraph Orchestrator
    |
    v
Tool Selector (LLM)
    |
    +--[tool selected, confidence: high]--+--[no strong match]--+
    |                                                            |
    v                                                            v
Tool Registry                                         Direct Model Call
    |                                                            |
    v                                                            |
Tool Execution (deterministic Python)                           |
    |                                                            |
    v                                                            |
Response Synthesis (LLM)                                        |
    |                                                            |
    +-----------------------------+------------------------------+
                                  |
                                  v
                          Final Response
                          Console Output
                          Interaction Log
```

### LangGraph Execution Graph

```
[__start__]
     |
     v
[select_tool]
     |
     +--[use_tool]---> [run_tool] ---> [synthesize] ---> [__end__]
     |
     +--[fallback]---> [fallback_model] ---> [__end__]
```

### Reasoning Loop

```
[reason] --> [act] --> [observe] --> [respond]
```

Each interaction logs the full reasoning path:

- selected tool
- confidence level
- reason for selection
- tool output
- final synthesized response

---

## Current Capabilities

The LangGraph agent can:

- Select tools using an LLM with structured JSON output
- Execute deterministic tools against sample inputs
- Synthesize responses from tool results with a two-pass refinement
- Fall back to direct model response when no tool applies
- Log all interactions with full reasoning transparency

### Available Tools

| Tool                   | Description                                                                 |
| ---------------------- | --------------------------------------------------------------------------- |
| terraform_analyzer     | Detects security and best-practice risks in Terraform configuration         |
| cicd_pipeline_reviewer | Reviews CI/CD pipeline YAML for missing test, security, and rollback stages |
| backlog_risk_detector  | Identifies delivery risks in backlog items                                  |
| backlog_analyzer       | Analyzes structured backlog data for flow and risk patterns                 |
| kanban_metrics         | Explains Kanban flow metrics including lead time and throughput             |
| platform_engineering   | Guides on IDP, golden paths, and developer platform concepts                |
| pi_planning            | Explains PI planning dependencies and ART coordination                      |
| pr_diff_summarizer     | Summarizes infrastructure PR diffs for resource changes and security risks  |

---

## Sample Output

### Terraform Risk Analysis

Input (samples/terraform/sample_terraform.tf):

```hcl
resource "aws_security_group" "web" {
  name = "web-sg"
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_s3_bucket" "app_data" {
  bucket = "my-app-data-bucket"
}

resource "aws_db_instance" "app_db" {
  identifier = "app-db"
  engine     = "postgres"
}
```

Agent output:

```
Source:     tool: terraform_analyzer
Confidence: high
Reason:     User asked to analyze Terraform configuration for risks

Tool selection details:
- terraform_analyzer: matches request to analyze Terraform configuration risks

Terraform analysis detected the following issues:

- Security risk:  security group allows access from 0.0.0.0/0
- Best practice:  S3 bucket versioning not configured
- Security risk:  database storage encryption not enabled
```

### CI/CD Pipeline Review

Input: samples/pipeline/sample_pipeline.yml (GitHub Actions workflow)

Agent output:

```
Source:     tool: cicd_pipeline_reviewer
Confidence: high
Reason:     User asked to review CI/CD pipeline for delivery risks

CI/CD pipeline review detected the following issues:

- Quality risk:     no test stage detected
- Security risk:    no security scan stage detected
- Reliability risk: deploy stage exists without a rollback step
```

---

## Quickstart

Create and activate a virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```
pip install openai python-dotenv pytest langgraph langchain-core
```

Create a .env file in the project root:

```
OPENAI_API_KEY=your_api_key_here
```

Run the CLI from the project root:

```
PYTHONPATH=. python scripts/agent_cli.py
```

---

## CLI Commands

```
help                      Show available commands and example questions
list tools                List all registered tools
show tool descriptions    Show tool names and descriptions
analyze backlog           Run backlog risk analysis on sample data
analyze terraform         Run Terraform risk analysis on sample configuration
analyze pipeline          Run CI/CD pipeline review on sample pipeline
```

---

## Example Questions

```
What is lead time?
What are signs that a backlog may have delivery risk?
How should I analyze backlog items for delivery risk?
What is an internal developer platform?
Explain PI planning dependencies.
Analyze this Terraform for security and best practice risks.
Review this CI/CD pipeline for delivery risks.
```

---

## Repository Structure

```
agentic-ai-platform-engineering/
  scripts/
    agent_cli.py              CLI entry point
  src/
    ai/
      langgraph_agent.py      LangGraph graph and orchestration
      agent_steps.py          Node implementations: select, run, synthesize
      multi_tool_selector.py  LLM tool selection with structured JSON output
      tool_registry.py        Tool registration and lookup
      client.py               OpenAI client wrapper
      config.py               Model configuration (gpt-4.1-mini)
    tools/
      terraform_analyzer.py   Terraform security and best-practice risk detection
      ci_cd_tools.py          CI/CD pipeline stage review
      agile_tools.py          Backlog risk detection and Kanban flow analysis
      platform_tools.py       IDP and platform engineering guidance
      pr_tools.py             Infrastructure PR diff summarization
  prompts/
    tool_selector.txt         Tool selection system prompt
    synthesis.txt             Response synthesis system prompt
  samples/
    terraform/                Sample Terraform configuration
    pipeline/                 Sample CI/CD pipeline YAML
    backlog/                  Sample backlog data
  docs/
    architecture.md           Detailed architecture and sequence diagrams
  logs/
    interactions.log          Full interaction history with reasoning trace
```

---

## Evaluation

Run a quick evaluation of routing behavior across sample prompts:

```
PYTHONPATH=. python eval_prompts.py
```

Prints for each prompt:

- selected tool
- reasoning
- confidence level
- response

---

## Roadmap

### Increment 1 - Complete

Foundational agent architecture and tool system.

### Increment 2 - Complete

Model-driven tool selection, response synthesis, and backlog analysis.

### Increment 3 - Complete

LangGraph orchestration with DevOps tools for Terraform and CI/CD analysis.

### Increment 4 - Planned

Platform engineering assistants for developer onboarding and IDP workflows
inspired by Backstage service catalog and golden path patterns.

### Increment 5 - Planned

Compliance and FinOps governance agents with human-in-the-loop approval steps
for automated infrastructure changes.

---

## Design Philosophy

Platform teams already orchestrate complex systems: infrastructure provisioning,
CI/CD pipelines, developer onboarding, governance, and delivery workflows.

Agentic AI can augment these systems with context-aware reasoning.

Core principles:

- Transparent reasoning: every decision is logged with tool, confidence, and reason
- Deterministic tools: tool execution is predictable and auditable
- Assistive not autonomous: agents support human decisions, not replace them
- Observable decision paths: the agent shows its work

---

## About

Built as part of applied research into AI-driven delivery lifecycle (AI-DLC) design.
Demonstrates practical agentic AI applied to enterprise platform engineering workflows.

Topics: devops, terraform, ai-agents, platform-engineering, langgraph, agentic-ai,
cicd, developer-platform, idp
