# Focus: Core Agentic Patterns & Workflow Chaining

## Overview
Based on Anthropic's research into effective agent design, this document formalizes the patterns required to move from "Prompt Engineering" to "Agent Engineering". High performance is achieved by trading off LLM flexibility for structured workflow patterns.

---

## 1. The Fallacy of the "One-Shot" Agent
Traditional agents often try to solve complex problems in a single loop. This leads to high variance and low reliability. High-fidelity agents instead use **structured patterns** to decompose the cognitive load.

## 2. Fundamental Patterns

### A. Prompt Chaining
- **Strategy**: Break a task into a fixed sequence of sub-tasks. The output of one step is the input for the next.
- **When to use**: When the task has distinct stages (e.g., Code Design -> Implementation -> Lint Fix -> Documentation).
- **Core Benefit**: Each step has a simplified context, reducing the chance of "Lost in the Middle".

### B. Routing
- **Strategy**: Use an initial "Router" agent to classify the task and send it to a specialized sub-workflow.
- **When to use**: When handling diverse requests (e.g., separating "Bug Fix" from "Feature Request" or "Research").
- **Core Benefit**: Allows for highly tuned system prompts for specific sub-tasks.

### C. Parallelization
- **Strategy**: Run multiple LLM instances in parallel to explore different solutions or handle independent sub-tasks.
- **Types**:
  - **Sectioning**: Parallel processing of different file parts.
  - **Voting**: Multiple candidates for the same solution, followed by a "Judge" selection.
- **Core Benefit**: Speeds up execution and increases reliability through redundancy.

## 3. The Evaluator-Optimizer Loop
This is the most critical pattern for "Subjectivity" (F8).
1. **Generator**: Produces a candidate solution.
2. **Evaluator (Judge)**: Checks the solution against specific criteria (Project Standards, Performance, Style).
3. **Feedback**: If the Judge fails the candidate, it provides a "Refusal with Rationale".
4. **Optimization**: The Generator refines the solution based on the critique.

## 4. Architectural Boundaries
Pattern-based focus requires the agent to "defend" its architecture:
- **State Isolation**: A Worker agent should not be able to global state unless explicitly granted by the Orchestrator.
- **Strict Interfaces**: Tools should pass structured data (JSON) rather than free text whenever possible.

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **Chain Visibility**: Antigravity MUST document the current step of the chain in the `task.md` (e.g., `[ ] Step 2/4: Implementation`).
2. **Judge Mandatory**: For any change affecting more than 3 files, a "Judge" phase is required before finalization. The agent must simulate an internal critique.
3. **Parallel Discovery**: If unsure about an implementation, use the `scratch/` directory to generate 2 alternative approaches and compare them in the implementation plan.
4. **No Premature Exit**: Never mark a task as done if the "Optimizer" loop hasn't run at least once for complex logic.
5. **Standard Compliance**: Every generated pattern MUST include a link back to this manual to ensure consistency.

---
*Reference: Anthropic - Building Effective Agents (2024).*
