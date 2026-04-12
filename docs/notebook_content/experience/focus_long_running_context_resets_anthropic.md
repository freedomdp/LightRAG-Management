# Focus: Managing Context Window Degradation

## Overview
As task duration increases, the "effective" intelligence of an LLM decreases due to context saturation. This document establishes the methodology for "Cognitive Resets" and "Context Flushing" to maintain focus in long-horizon agentic workflows.

---

## 1. The Entropy of Context
The more actions an agent takes, the more "noise" (command outputs, directory listings, intermediary thoughts) enters the context.
- **Symptom 1**: The agent repeats previous mistakes.
- **Symptom 2**: The agent fails to follow subtle system instructions.
- **Symptom 3**: Latency increases, and coherence drops.

## 2. The "Context Flush" Protocol
When context saturation is detected (typically after 5-10 complex tool interactions), the agent MUST perform a flush.
1. **Fact Distillation**: Extract all critical discovered facts, paths, and logic into a temporary "Fact Snapshot".
2. **History Purge**: Terminate the current session/thread logic (metaphorically).
3. **Re-Initialization**: Start a new reasoning cycle, injecting ONLY the "Fact Snapshot" and the original user goal.

## 3. Cognitive Resets
A reset is triggered not just by token count, but by "Cognitive Fog":
- **Condition**: If the last 3 actions produced no progress toward an unchecked item in `task.md`.
- **Action**: Stop. Clear all terminal outputs. Re-read `project.md` and `Implementation Plan` from scratch. Re-evaluate if the current path is viable.

## 4. State Management (Check-pointing)
To prevent data loss during a reset, the agent must treat the filesystem as its "External Long-term Memory":
- **Artifacts over History**: Any valuable design decision or code snippet MUST be saved to an artifact or a file. Never leave a critical insight only in the chat history.
- **Task.md as Ground Truth**: The `task.md` file is the anchor. If it isn't in `task.md`, it doesn't exist for the agent's future self.

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **Flush Alert**: If the conversation history exceeds 20 turns, the agent MUST explicitly ask the user for a "Context Refresh" or proactively summarize the state to keep the window clean.
2. **Snapshot First**: Before any major code deletion or refactor, a "Safety Snapshot" of the original content must be either backed up or explicitly referenced by git hash.
3. **No Drift**: If the agent catches itself performing a "Sub-task of a Sub-task" without updating the plan, it MUST stop and re-align the `task.md`.
4. **History Pruning**: When using `run_command`, avoid large outputs (e.g., `cat` of 1000 lines). Use `head`, `tail`, or `grep` to keep the context slim.
5. **Session Awareness**: At the start of every turn, double-check the "Current State" metadata. If the active file has changed, reset the focus accordingly.

---
*Reference: Anthropic Engineering - Harnessing Design (2024).*
