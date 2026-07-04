# System Architecture

This document describes the overall architecture of the Git Integration Agent.

Rather than focusing on implementation details, this document explains how the system is organized, how each module interacts with the others and why each architectural decision was made.

---

# Architectural Principles

The project was designed around a few core principles.

- Single Responsibility Principle
- Small composable components
- Deterministic execution
- Explicit AI contracts
- Reproducible workflows
- Clear separation between planning and execution
- AI used only where semantic reasoning is required

Every component should have one clear responsibility.

The system intentionally avoids large orchestration classes.

---

# High-Level Architecture

```
                   Git Repository
                          │
                          ▼
                 Repository Analysis
                          │
                          ▼
            Integration Strategy Classifier
                          │
                          ▼
                  Feature Planner
                          │
                          ▼
                  Task Generation
                          │
                          ▼
                 Independent Task Runner
                          │
                          ▼
                 Snapshot Construction
                          │
                          ▼
                  Prompt Generation
                          │
                          ▼
                     Claude CLI
                          │
                          ▼
                Response Normalization
                          │
                          ▼
                 Contract Validation
                          │
                          ▼
                Generated Source Files
                          │
                          ▼
                  Final Consolidation
```

---

# Project Structure

```
.
├── agents/
├── analyzers/
├── classifiers/
├── contracts/
├── core/
├── docs/
├── generators/
├── implementation/
├── prompts/
├── workspace/
└── app.py
```

Each directory represents one logical subsystem.

---

# Module Responsibilities

## agents/

Contains reusable infrastructure components.

Examples:

- Claude CLI integration
- Snapshot builder
- Repository explorer
- Response normalizer
- Prompt helpers

These classes should not contain business orchestration.

---

## analyzers/

Responsible for understanding Git.

Responsibilities include:

- commit analysis
- branch comparison
- file discovery
- repository inspection

This layer knows Git.

It knows nothing about AI.

---

## classifiers/

Responsible for selecting the integration strategy.

Example strategies:

- Merge
- Cherry Pick
- Reimplement
- Manual Integration

The classifier determines which workflow should be followed.

---

## contracts/

Defines every AI communication contract.

Examples:

- AI Contract
- Implementation Contract

The contracts make AI communication deterministic.

---

## core/

Coordinates the application.

Examples:

- Feature Planner
- Configuration Manager
- Task Tracking

The core orchestrates the workflow.

---

## generators/

Produces intermediate artifacts.

Examples:

- Analysis package
- Task plan
- Metadata

Generators never execute AI.

---

## implementation/

Contains the semantic implementation pipeline.

This module is responsible for transforming an integration task into generated source code.

It contains:

- Prompt generation
- Claude execution
- Response parsing
- Workspace management
- Runner
- Executor

This is the heart of the project.

---

## prompts/

Stores prompt templates.

Prompt construction is isolated from execution.

This separation allows prompt evolution without changing application logic.

---

## workspace/

Contains every artifact produced during execution.

Nothing inside the workspace belongs to the source code.

Everything can be regenerated.

---

# Execution Pipeline

The implementation pipeline is composed of multiple independent stages.

```
Task

↓

Snapshot Builder

↓

Prompt Generator

↓

Claude CLI

↓

Response Normalizer

↓

Response Parser

↓

Generated Files

↓

Merger
```

Each stage has a single responsibility.

This greatly simplifies debugging.

---

# Planning vs Execution

One of the most important architectural decisions was separating planning from execution.

Planning answers:

"What should be integrated?"

Execution answers:

"How should it be integrated?"

This separation enables:

- resumable executions
- independent task execution
- deterministic planning
- reproducible implementations

---

# Task-Based Architecture

A feature is never implemented as a single unit.

Instead:

```
Feature

↓

Task 1

Task 2

Task 3

Task N
```

Each task represents an isolated implementation scope.

Advantages:

- smaller prompts
- easier debugging
- resumable execution
- lower AI cost
- reduced semantic conflicts

---

# AI Responsibilities

The AI is intentionally restricted.

The model is responsible only for semantic reasoning.

Everything else is deterministic.

The AI does NOT:

- analyze Git
- plan execution order
- classify strategies
- discover files
- manage workspaces

Those responsibilities remain inside deterministic code.

---

# Design Philosophy

The system follows a simple philosophy:

```
Deterministic software

+

Semantic reasoning

=

Reliable AI-assisted integration
```

The deterministic components define the workflow.

The AI only fills the gap that traditional algorithms cannot solve.

---

# Why Claude?

The project currently integrates with Claude CLI because of its strong performance in:

- code understanding
- long-context reasoning
- semantic refactoring
- architectural consistency

The architecture, however, was intentionally designed so that additional LLM providers can be integrated in the future.

---

# Scalability

The current architecture allows future improvements such as:

- Prompt Budget Management
- Incremental Snapshot Loading
- Parallel Task Execution
- Automatic Retry Pipeline
- Multiple LLM Providers
- Resume Interrupted Execution
- Workspace Recovery
- Validation Pipelines

None of these features require major architectural changes.

---

# Design Decisions

Some important decisions made during development:

- Separate planning from execution.
- Execute one task at a time.
- Preserve deterministic orchestration.
- Use explicit AI contracts.
- Store every execution artifact.
- Preserve implementation history.
- Prefer composition over inheritance.
- Keep modules independent whenever possible.

---

# Next Document

The next document is:

```
workflow.md
```

It explains every execution step performed by the Git Integration Agent from repository analysis to final source code generation.
