# Focus: Autonomous Evals & Logic Validation

## Overview
Confidence in agentic behavior requires "Continuous Integration for Logic". Based on Anthropic's engineering methodology, this document defines how an agent must validate its own reasoning before committing changes to the codebase.

---

## 1. The Validation Bridge
A successful agent doesn't just "execute"; it "verifies". The bridge between an idea and an implementation is the **Eval Phase**.

## 2. Logic Graders (Self-Critique)
Before presenting a final solution, the agent MUST run an internal simulation across three dimensions:
- **Constraint Grader**: Did I follow all `project.md` and `Implementation Plan` constraints?
- **Logic Grader**: Is the proposed solution the most efficient? Are there edge cases I ignored?
- **Standard Grader**: Does this look like "Professional Code" or "AI-generated boilerplate"?

## 3. Architectural Asserts
To prevent regression in "Subjectivity" (F8), the agent uses implicit "Asserts":
- **ID Assert**: Every new interactive element must have a unique ID.
- **Dependency Assert**: No new dependencies allowed without explicit Orchestrator approval.
- **Complexity Assert**: If a function exceeds 50 lines, it must be decomposed.

## 4. The "Red-Teaming" Methodology
When solving high-stakes architectural problems:
1. **Adversary Mode**: A sub-routine within the agent's logic tries to find reasons why the proposed change will break the system.
2. **Mitigation Mode**: The primary logic addresses the adversary's concerns.
3. **Synthesis**: The final code reflects the battle between these two perspectives.

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **Eval Block**: Every implementation plan MUST contain a `Verification Plan` section.
2. **Regret Log**: If a previous solution failed, the agent MUST document the reason in the KI or `STATUS.md` to prevent "Looping Errors".
3. **Self-Correction First**: If a lint error occurs, the agent MUST fix it before asking the user for help. Asking for help on syntax is a breach of protocol.
4. **Logic Transparency**: Use the `thought` block to explain *why* a specific logic grader failed during the reasoning process.
5. **No Blind Commit**: Never push files to Git (if applicable) without running at least one validation command (e.g., `grep` for correctness or `status` check).

---
*Reference: Anthropic Engineering - Demystifying Evals (2024).*
