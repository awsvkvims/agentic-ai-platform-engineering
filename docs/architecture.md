# Architecture Overview

``` mermaid
flowchart TD
    A[User Input] --> B[CLI: client_cli.py]
    B --> C[Tool Selector LLM]
    C --> D[JSON Tool Choice + Reason]
    D --> E[Router]
    E --> F[Tool Registry]
    F --> G[Selected Tool]
    G --> H[Tool Result]
    E -->|none| I[Direct Model Call]
    H --> J[Synthesis LLM]
    J --> K[Final Response]
    I --> K
    K --> L[Console Output]
    K --> M[interactions.log]
    H --> M
    D --> M
```

## Purpose

This project explores small, understandable patterns for building agentic AI systems for Agile delivery, DevOps enablement, and platform engineering workflows.

The current implementation is intentionally simple:
- a command-line interface accepts user input
- a router decides how to handle the request
- the system either calls a local tool or the language model
- the response is shown to the user and logged

## Current Architecture

The system now follows a simple agent-style workflow.

1. The user enters a prompt in the CLI.
2. The tool selector (an LLM call) analyzes the request and chooses a tool or returns `none`.
3. The router receives the selected tool name.
4. If a tool is selected:
   - the router finds the tool in the tool registry
   - the tool executes and returns deterministic output
   - the model synthesizes a final answer using the tool result
5. If no tool is selected:
   - the router sends the prompt directly to the model
6. The final response is displayed to the user and logged.

This creates a simple **reason --> act --> observe --> respond** loop.

## Components

### CLI
**File:** `client_cli.py`

This is the entry point for the project. It:
- collects user input
- calls the router
- prints the chosen source and response
- writes the interaction to `interactions.log`

### Router
**File:** `src/ai/router.py`

The router contains the decision logic. It examines the input text and determines whether to:
- call a local tool
- or fall back to the language model

This is the first agent-like behavior in the project.

### Tools
**File:** `src/ai/tools.py`

The tools module contains local deterministic functions for specific domain topics:
- Kanban metrics
- platform engineering
- PI planning dependencies

These tools are useful because they are:
- fast
- predictable
- easy to test

### Model Client
**File:** `src/ai/client.py`

The model client is responsible for communicating with the OpenAI API. It:
- loads the API key from `.env`
- applies the configured model name
- sends prompts to the model
- returns the model response text

### Config
**File:** `src/ai/config.py`

The config module stores settings that may change over time, such as:
- model name
- default system role

This keeps configuration separate from logic.

### Tests
**File:** `tests/test_router.py`

The test file verifies that known requests are routed correctly. This is the beginning of an engineering discipline around reliability and maintainability.

## Design Principles

The current system follows a few simple design principles:

### Separation of concerns
Each module has one clear responsibility:
- CLI for interaction
- router for decision-making
- tools for deterministic knowledge
- client for model access
- config for settings

### Deterministic where possible
If a request can be answered reliably by a local tool, the system uses that path instead of calling the model.

### Model as fallback
The language model is used when the request does not match a known local tool.

### Observability
The system shows which source was used and logs interactions for later review.

## Current Limitations

This project is still intentionally small. Current limitations include:
- routing is keyword-based
- tools are static functions
- there is no memory across interactions
- there is no structured state object
- there is no multi-step workflow or graph orchestration yet

## Next Evolution

A natural next step is to evolve this design toward a more structured agent workflow by adding:
- structured tool metadata
- explicit state handling
- richer routing rules
- multiple decision steps
- graph-based orchestration similar to LangGraph

## Summary

This architecture is a beginner-friendly foundation for learning agentic AI in a practical platform engineering context.

It already demonstrates:
- routing
- tool usage
- model fallback
- configuration
- logging
- basic testing

The goal is to grow this foundation incrementally into a more capable agent workflow system.
