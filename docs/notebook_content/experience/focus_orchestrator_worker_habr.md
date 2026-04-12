# Focus: Orchestrator-Worker Architecture & Task Routing

## Overview
This document outlines the methodology for implementing a robust "Orchestrator-Worker" pattern to maintain high cognitive focus in AI agents. Based on expert-level architecture research, this pattern prevents "focus drift" (размытие фокуса) by separating the high-level planning logic from the low-level execution logic.

---

## 1. The Core Problem: Cognitive Wander (Размытие)
In flat agentic architectures, a single agent is responsible for both planning and execution. As the context window fills with tool outputs, logs, and intermediary states, the agent's attention to the original goal degrades. This leads to:
- **Recursive Hallucinations**: The agent starts solving problems it created itself, forgetting the user's intent.
- **Context Bloat**: Irrelevant execution details crowd out the system instructions.
- **Decision Fatigue**: The LLM becomes less precise in choosing the next tool.

## 2. The Solution: Role Bifurcation
To maintain focus, the system must be split into two distinct cognitive layers: **The Orchestrator** and **The Worker**.

### A. The Orchestrator (The Architect)
- **Responsibility**: Decomposition, Routing, and Evaluation.
- **Context**: High-level goal, current progress, and architectural standards.
- **Constraint**: **NEVER** touches implementation details (e.g., writing the actual code lines). It only produces "Sub-tasks" or "Directives".

### B. The Worker (The Craftsman)
- **Responsibility**: Atomic execution of a single Sub-task.
- **Context**: Minimalist. Only the specific Sub-task description and the immediate file/API context required.
- **Constraint**: **NEVER** questions the big picture. If it hits a blocker, it reports back to the Orchestrator instead of making architectural pivots.

## 3. Dynamic Routing Protocol
Routing is the mechanism that keeps the agent focused by "swapping" the active instruction set.

### Phase 1: Planning (Orchestrator Mode)
1. Read the user request.
2. Search the knowledge base (RAG).
3. Create a `task.md` with atomic checkboxes.
4. Stop. Verify the plan with the user.

### Phase 2: Execution (Worker Mode)
1. Pick **one** unchecked task from `task.md`.
2. Clear the "Mental Scratchpad" (discard unrelated past history).
3. Execute the task.
4. Update `task.md` with `[x]`.

### Phase 3: Consolidation (Orchestrator Mode)
1. Review the result.
2. Does it align with the `project.md` standards?
3. Decide the next move.

## 4. Avoiding the "Recursive Loop" Trap
When an agent encounters a bug, the natural tendency is to "stay in the file" and keep patching. To prevent this:
- **Maximum 3 Retry Rule**: If a worker fails more than 3 times to fix a specific bug, it **MUST** escalate to the Orchestrator for a "Strategic Reset".
- **Context Flush**: After escalation, the current chat history for that specific bug is purged to avoid reinforced errors.

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **Strict Separation**: Antigravity must always declare which mode it is in (Planning vs Execution).
2. **Atomic Verification**: No task can be marked `[x]` in `task.md` unless its specific verification plan (defined in the implementation plan) has passed.
3. **No Hidden Work**: Every search or shell command MUST be justified by a specific task in the current plan. No "just checking" without documentation.
4. **Boundary Defense**: If a user request contradicts the `project.md` or `agent_readiness_audit.md` standards, the agent MUST flag this as a "Structural Conflict" before proceeding.
5. **JIT Ingestion**: Before building any significantly complex feature, the agent MUST search for related KIs or documentation. Blind coding is prohibited.

---
*Derived from: Habr Research on AI Agent Architectures & Dynamic Routing.*
