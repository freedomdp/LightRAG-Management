# Focus: Implementation Patterns of Evaluator-Optimizer Loops

## Overview
High-quality engineering requires iterative refinement. Based on the Spring AI framework's implementation of agentic loops, this document formalizes the "Evaluator-Optimizer" cycle for automated coding tasks.

---

## 1. The Feedback Engine
In a standard agentic flow, the generator creates code, and the user provides feedback. In the Spring AI "Best Practice" pattern, the agent provides its own feedback through a structured **Evaluator Node**.

## 2. Cycle Components
1. **The Proposal (Generator)**:
   - Input: User requirements + File context + Patterns.
   - Output: Initial code draft.
2. **The Critique (Evaluator)**:
   - Input: Initial code draft + Evaluation Criteria (e.g., Clean Architecture, SOLID, Performance).
   - Output: A list of "Deficiencies" or "Approval".
3. **The Refinement (Optimizer)**:
   - Input: Initial draft + Deficiencies.
   - Output: Final production code.

## 3. Implementation Patterns

### Pattern A: Self-Correction (Single-Loop)
- The generator is prompted with a "Reflective" instruction: *"Examine your own output for potential race conditions or memory leaks before finishing."*

### Pattern B: Cross-Validation (Multi-Agent/Role)
- One cognitive process (Antigravity-Writer) produces code.
- A second cognitive process (Antigravity-Reviewer) acts as a Senior Architect, rejecting any code that doesn't meet the `project.md` safety standards.

## 4. Measuring Quality
Optimization is meaningless without metrics. The agent must use "Logic Anchors" to measure success:
- **Build Pass**: Does the code compile/build?
- **Schema Alignment**: Does it match the existing database or API schema?
- **Style Consistency**: Does it match the existing typography and naming conventions of the project?

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **Cycle Minimum**: For any change deemed "Critical" (marked in `project.md`), at least TWO refinement cycles are mandatory.
2. **Negative Feedback Tolerance**: The agent must never defend a flawed solution. If an evaluator (user or internal) finds a bug, the agent must treat it as high-priority data for the next jump.
3. **Draft Isolation**: Use the `scratch/` directory for "Pattern A" candidates to avoid polluting the main codebase with intermediary versions.
4. **Logic Traceability**: The critique from the Evaluator stage MUST be readable by the human user in the `thought` block.
5. **Pattern Enforcement**: If a component name ends in `Service` or `Controller`, it must follow the established structure for those types in Spring/Standard projects.

---
*Reference: Spring AI - Engineering Patterns (2024).*
