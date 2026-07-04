# Workflow

This document describes the complete execution workflow of the Git Integration Agent.

The workflow is divided into independent phases, allowing planning, execution and validation to evolve independently.

---

# Overview

```
Repository

↓

Analyze

↓

Classify

↓

Plan

↓

Execute Tasks

↓

Merge Generated Files
```

Each phase produces artifacts that are stored inside the workspace.

---

# Phase 1 — Repository Analysis

Command:

```bash
python app.py analyze \
    --repo "<repository>" \
    --from feature \
    --to target
```

Purpose:

- inspect the repository;
- compare both branches;
- identify modified files;
- collect metadata;
- detect potential conflicts.

Output:

```
workspace/

analysis/
```

---

# Phase 2 — Integration Strategy

The analysis package is processed by the integration classifier.

Its responsibility is selecting the safest integration strategy.

Possible strategies include:

- Merge
- Reimplementation
- Cherry Pick
- Manual Integration

The selected strategy determines how the remaining workflow behaves.

---

# Phase 3 — Feature Planning

Command:

```bash
python app.py plan-feature
```

Purpose:

Transform a branch integration into multiple independent implementation tasks.

Instead of implementing an entire feature at once, the planner groups files into logical execution units.

Example:

```
Task 1

Infrastructure

↓

Task 2

Domain

↓

Task 3

Application

↓

Task 4

API

↓

Task 5

Tests
```

Advantages:

- smaller prompts;
- easier debugging;
- resumable execution;
- better AI accuracy.

---

# Phase 4 — Task Execution

Command:

```bash
python app.py run-task
```

Each task executes independently.

Execution pipeline:

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
```

Only files belonging to the selected task are processed.

---

# Phase 5 — Complete Integration

Command:

```bash
python app.py integrate-feature
```

This command executes every planned task sequentially.

Typical execution:

```
Task 1

↓

Task 2

↓

Task 3

↓

Task N
```

After every task succeeds, generated files are consolidated.

---

# Execution Artifacts

Every phase generates reproducible artifacts.

Examples:

- analysis results;
- task plan;
- generated prompts;
- AI responses;
- generated files.

These artifacts simplify debugging and auditing.

---

# Error Handling

If a task fails:

```
Task 4

↓

Failure

↓

Fix

↓

Run Task 4 again
```

Previously completed tasks do not need to be regenerated.

---

# Independent Tasks

Tasks are intentionally isolated.

Benefits:

- easier recovery;
- incremental execution;
- reduced AI context;
- simpler validation.

---

# Workspace Lifecycle

```
Plan

↓

Generate Tasks

↓

Execute Tasks

↓

Generate Files

↓

Review

↓

Merge
```

The workspace represents a complete execution history.

It can be deleted and regenerated at any time.

---

# Design Principles

The workflow follows three principles.

## Deterministic Planning

Planning always produces the same execution order for the same inputs.

---

## Independent Execution

Each task is self-contained.

---

## Reproducible Results

Every execution stores its artifacts, allowing investigation and replay.

---

# Next Document

Continue with:

```
implementation-pipeline.md
```

This document explains the internal implementation pipeline in detail.
