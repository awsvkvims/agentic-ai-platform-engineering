# Architecture Overview

<div class="mermaid">
flowchart TD
    A[User Input] --> B[CLI: first_ai_call.py]
    B --> C[Router: route_request]
    C -->|Kanban terms| D[Tool: explain_kanban_metrics]
    C -->|Platform terms| E[Tool: explain_platform_engineering]
    C -->|PI dependency terms| F[Tool: explain_pi_planning_dependencies]
    C -->|No tool match| G[Model Client: ask_model]
    G --> H[OpenAI API]
    D --> I[Response]
    E --> I
    F --> I
    H --> I
    I --> J[Console Output]
    I --> K[interactions.log]
</div>

## Purpose

This project explores small, understandable patterns for building agentic AI systems for Agile delivery, DevOps enablement, and platform engineering workflows.

The current implementation is intentionally simple:
- a command-line interface accepts user input
- a router decides how to handle the request
- the system either calls a local tool or the language model
- the response is shown to the user and logged

## Current Architecture

The current flow is:

1. The user enters a prompt in the command line
2. The CLI passes that input to the router
3. The router checks whether the request matches a known tool path
4. If a tool matches, the tool returns a deterministic response
5. If no tool matches, the model client sends the prompt to the OpenAI API
6. The chosen response is displayed and saved to the log

## Components

### CLI
**File:** `first_ai_call.py`

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
