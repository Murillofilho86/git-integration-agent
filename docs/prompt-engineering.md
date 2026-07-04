# Prompt Engineering

This document explains how prompts are constructed inside the Git Integration Agent.

Prompt engineering is a fundamental part of the project because it directly affects implementation quality and reproducibility.

---

# Design Goals

The prompt generation process aims to produce prompts that are:

- deterministic
- reproducible
- auditable
- explicit
- independent of repository structure

---

# Prompt Structure

Each prompt is composed of multiple sections.

```
System Instructions

↓

Task Description

↓

Implementation Scope

↓

Snapshot

↓

Expected Output

↓

AI Contract
```

Every section has a specific responsibility.

---

# Snapshot

The snapshot contains the information required for semantic reasoning.

Typical contents include:

- current implementation
- target implementation
- metadata
- task scope

Snapshots intentionally avoid unrelated files.

---

# AI Contract

Every prompt contains an explicit response contract.

The AI must produce a deterministic structure.

The parser relies on this contract to validate the response.

---

# Prompt Design Principles

The project follows several prompt engineering principles.

## Explicit instructions

The model should never infer response format.

Everything must be explicitly described.

---

## Limited scope

Every prompt covers only one task.

Large implementations are divided into smaller execution units.

---

## Deterministic output

The expected response format is always the same.

---

## Complete implementation

Generated files must always be complete.

Partial snippets are never accepted.

---

# Known Challenges

Large prompts may reduce response quality.

Potential mitigations include:

- prompt budget management
- incremental snapshots
- dynamic context loading

These improvements are planned for future versions.

---

# Prompt Evolution

Prompt templates evolve independently from application code.

This separation allows experimentation without modifying the execution pipeline.

---

# Best Practices

- keep instructions explicit
- minimize unrelated context
- avoid ambiguous wording
- validate every AI response
- preserve deterministic execution
