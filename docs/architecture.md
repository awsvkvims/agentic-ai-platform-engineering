# Architecture Overview

This document describes the architecture of the agent system implemented in this repository.

The system demonstrates a minimal but practical agent workflow that combines model reasoning with deterministic tool execution.

---

# High Level architecture

``` mermaid

flowchart TD

UserInput["User Input"] --> CLI["CLI Interface"]

CLI --> ToolSelector["Tool Selector LLM"]

ToolSelector --> Decision["JSON Tool Decision"]

Decision --> Router["Router"]

Router --> ToolRegistry["Tool Registry"]

ToolRegistry --> ToolExecution["Tool Execution"]

ToolExecution --> ToolResult["Tool Result"]

Router --> ModelFallback["Direct Model Call"]

ToolResult --> Synthesis["Response Synthesis LLM"]

Synthesis --> FinalResponse["Final Response"]

ModelFallback --> FinalResponse

FinalResponse --> ConsoleOutput["Console Output"]

FinalResponse --> Logs["Interaction Log"]

Decision --> Logs

ToolResult --> Logs

```

---

# Core Components

## CLI

The CLI provides a simple interactive interface where users can enter prompts and commands.

Examples include:

- help
- list tools
- show tool descriptions
- analyze backlog

---

## Tool Selector

The tool selector uses an LLM to determine whether a request should be handled by a tool.

It returns structured JSON containing:

- tool
- reason
- confidence

This allows the system to reason about tool usage rather than relying on hard coded rules.

---

## Router

The router is responsible for executing the selected action.

If a tool is selected with high confidence:

- the router locates the tool in the tool registry
- the tool is executed
- the result is sent to the synthesis prompt

If no tool is selected:

- the request is sent directly to the model.

---

## Tool Registry

The tool registry stores structured definitions of all available tools.

Each tool contains:

- name
- description
- function

This allows the selector to reason about available tools.

---

## Tools

Tools are deterministic Python functions that provide domain specific capabilities.

Examples include:

- Kanban metric explanations
- backlog risk analysis
- backlog analysis using structured backlog data
- platform engineering explanations
- PI planning dependency explanations

Tools allow the agent to access structured knowledge rather than relying only on LLM responses.

---

## Prompt Layer

Prompts are stored separately from code in the prompts directory.

Examples:

- prompts/tool_selector.txt
- prompts/synthesis.txt

This allows prompts to be updated independently of application logic.

---

## Logging and Observability

Each interaction records:

- user input
- selected tool
- confidence level
- reason for selection
- tool output
- final response

This provides transparency into how the agent made decisions.

---

# Future Evolution

The architecture will evolve in later stages of the project.

Planned improvements include:

- LangGraph orchestration replacing the router
- DevOps oriented tools for Terraform and CI/CD analysis
- Platform engineering assistants for developer onboarding
- Governance agents for compliance and FinOps

These changes will extend the current architecture while preserving the same core agent pattern.