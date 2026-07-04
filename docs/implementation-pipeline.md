# Implementation Pipeline

This document describes the complete implementation pipeline of the Git Integration Agent.

The implementation pipeline is responsible for transforming an integration task into a set of generated source files while keeping the execution deterministic and reproducible.

---

# Overview

The pipeline is intentionally divided into multiple independent stages.

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

Final Consolidation
```

Each stage has a single responsibility.

---

# Design Goals

The implementation pipeline was designed to satisfy the following requirements:

- deterministic execution
- reproducible outputs
- isolated responsibilities
- resumable execution
- complete execution history
- AI used only where semantic reasoning is required

---

# Pipeline Stages

## 1. Task Selection

Input:

```
Task Plan
```

Example:

```
Task 3

Files

- fileA.cs
- fileB.cs
- fileC.cs
```

The selected task defines the exact implementation scope.

No files outside this scope should be generated.

---

## 2. Snapshot Builder

Responsibility:

Collect every piece of information required for implementation.

Typical inputs include:

- source branch version
- target branch version
- file contents
- metadata

Output:

```
Snapshot
```

The snapshot is deterministic.

Running the same task twice with identical inputs must produce the same snapshot.

---

## 3. Prompt Generator

The Prompt Generator converts the snapshot into an implementation prompt.

The prompt contains:

- implementation instructions
- task scope
- snapshot
- AI contract
- response format

The prompt is stored inside the workspace.

Example:

```
implementation-prompt.md
```

---

## 4. Claude CLI

The generated prompt is submitted to Claude CLI.

Responsibilities:

- semantic reasoning
- conflict resolution
- code reconstruction

Claude is not responsible for:

- planning
- orchestration
- workspace management
- file discovery

Those responsibilities remain deterministic.

---

## 5. Response Normalization

The AI response is normalized before parsing.

Typical responsibilities include:

- extracting the expected response
- removing transport artifacts
- preserving the original response for debugging

The original response should never be discarded.

---

## 6. Response Parser

The parser validates the response.

Typical validations include:

- contract validation
- response structure
- required fields
- generated file list

After validation, every generated file is written to disk.

---

## 7. Generated Files

Generated files are stored separately from the repository.

Example:

```
generated-files/

src/

tests/
```

This guarantees that generated content can be reviewed before replacing any repository file.

---

## 8. Final Consolidation

After every task completes successfully, generated files may be consolidated into a single output directory.

This step should only occur after all required tasks have finished.

---

# Execution Flow

```
Task

↓

Snapshot

↓

Prompt

↓

Claude

↓

Normalized Response

↓

Validated Response

↓

Generated Files

↓

Merge
```

---

# Why Multiple Stages?

Separating the implementation into independent stages provides several benefits.

## Easier debugging

Each stage can be inspected independently.

---

## Better testing

Individual components can be unit tested.

---

## Replaceable components

Each stage may evolve independently.

Examples:

- replace Claude with another provider
- improve the parser
- redesign prompt generation

without affecting the remaining pipeline.

---

## Deterministic orchestration

The orchestration code never depends on AI reasoning.

Only semantic reconstruction is delegated to the language model.

---

# Error Recovery

Failures should stop the pipeline immediately.

Typical flow:

```
Task

↓

Stage

↓

Failure

↓

Correction

↓

Re-execute Task
```

Previously completed tasks remain valid.

---

# Workspace Artifacts

Each execution stores its artifacts.

Examples include:

- snapshots
- prompts
- AI responses
- generated files

This enables complete execution auditing.

---

# Current Pipeline

Current implementation:

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

Consolidation
```

The architecture intentionally keeps every stage independent.

Future improvements should preserve this separation.

---

# Future Improvements

Potential enhancements include:

- Prompt Budget Management
- Incremental Snapshot Loading
- Automatic Retry Pipeline
- Response Quality Metrics
- Parallel Task Execution
- Progress Reporting
- Provider Abstraction
- Execution Resume

These improvements can be implemented without changing the overall architecture.

---

# Design Philosophy

The implementation pipeline follows one fundamental principle:

> Deterministic software should orchestrate the workflow.
>
> Artificial Intelligence should perform only semantic reasoning.

Keeping these responsibilities separate makes the system easier to understand, maintain and evolve.

---

# Next Document

Continue with:

```
commands.md
```

This document describes every command available in the Git Integration Agent command-line interface.
