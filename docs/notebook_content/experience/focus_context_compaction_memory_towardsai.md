# Focus: Context Compaction, Hierarchical Memory & State Versioning

## Overview
As AI agents move from simple tasks to long-horizon engineering, the management of the "Cognitive Horizon" (Context Window) becomes the primary performance bottleneck. This master document synthesizes **10+ global research sources** and industry best practices into a unified methodology for Context Compaction and Memory Management. Its goal is to maximize "Signal-to-Noise Ratio" (SNR) in the brain of the agent.

---

## 1. The 4W Memory Taxonomy (Conceptual Layer)
To manage state effectively, we must first categorize it using the 4W Framework:
- **WHEN**: Is this Transient (deleted after task) or Persistent (saved to RAG)?
- **WHAT**: Is this Procedural (how to do task), Declarative (facts), or Metacognitive (self-learning/style)?
- **HOW**: Is this Implicit (in the prompt) or Explicit (in a file/graph)?
- **WHICH**: Which modality is appropriate (SQL, Vector, Markdown, Graph)?

## 2. Hierarchical Memory Architecture
We reject the "One Flat Context" approach. Effective agents operate across four layers:

### Layer 1: Working Memory (The Hot Lane)
- **Size**: < 5,000 tokens.
- **Content**: The immediate task, last 3 tool outputs, current error messages.
- **Protocol**: **"Zero-G"**. Frequent purging of non-essential noise.

### Layer 2: Episodic Memory (The Narrative Layer)
- **Size**: 10,000 - 50,000 tokens.
- **Content**: The session history, summaries of past attempts, discovered file structures.
- **Protocol**: **"Tiered Summarization"**. Older interaction cycles are condensed into 3-sentence abstracts to preserve the "Lost-in-the-Middle" integrity of the transformer.

### Layer 3: Semantic/Long-term Memory (The Vault)
- **Size**: Infinite.
- **Content**: Knowledge Items (KIs), Project DNA, Architecture Standards.
- **Protocol**: **"RAG/Graph Hybrid"**. Use Vector search for broad context and Neo4j Graph for precise entity relationships.

### Layer 4: Procedural Memory (The Muscle)
- **Content**: Validated scripts, effective command sequences, and the `Agentic Protocols` defined in these docs.

## 3. Context Compaction Techniques: The "Noise Filter"
Based on research from **Anthropic** and **Databricks**, we implement these strategies:

### A. Tool-Call Clearing
Once a command (e.g., `ls -R` or `view_file`) has yielded its information, the **Raw Output** must be discarded and replaced by a **Distilled Summary**.
- *Example*: Instead of keeping 100 lines of `ls`, keep: *"Confirmed `scripts/` exists and contains 12 python files related to monitoring."*

### B. Loss-Aware Pruning
Identify "Information-Holes" in the current history. If a previous discussion about "CSS colors" is followed by a task to "Fix SQL query", the CSS discussion must be pruned to reclaim token space.

### C. Background Distillation
During idle cycles (or when context exceeds 70%), a "Background Thread" (metaphorical) produces a session-level `status.md` update. This forces the agent to consolidate its current understanding of the reality.

## 4. State Versioning & Rollback Snapshots
State is not just data; it is the current "Mental Configuration" of the agent.

### A. State Snapshots
Before any "Breaking Change" (e.g., refactoring `scripts/` or modifying `project.md`), the agent must create a **State Version**.
- **Snapshot ID**: Git Hash or Timestamped JSON in `temp/`.
- **Content**: Active `task.md`, current `project.md` state, and recent critical findings.

### B. Memory Rollbacks
If an implementation fails catastrophically, the agent MUST NOT try to "continue". It must perform a **State Rollback**:
1. Revert files to the last known-good snapshot.
2. Clear the current "Cognitive Fog" (Chat history).
3. Re-inject the last "Successful Fact Snapshot".

## 5. Memory Observability & Governance
*"If you can't trace a memory, you can't trust the agent."*
- Every memory write (KI creation) MUST include a Confidence Score (1-5) and a Source Citation (Reference).
- Every retrieval MUST be logged in the `thought` process: *"Reasoning based on KI: [Web Development Workflow]"*.

---

## 🤖 Agentic Protocol: Mandatory Constraints

1. **SNR Guard**: If the ratio of "Raw Logs" to "Constructive Thoughts" exceeds 3:1 in the context, a `Context Flush` is mandatory.
2. **Fact Anchoring**: Every critical discovery (e.g., "Neo4j baseline is 314 docs") must be written to a persistent file (STATUS.md or KI) within 2 turns of discovery.
3. **No Drift Memory**: If a task moves to a new file, the previous file's context must be minimized to "Filename + Purpose" only.
4. **Recursive Cleanups**: After every successful `[x]` task in `task.md`, the agent must briefly "clean the room" (clear scratch files, close unnecessary browser tabs, etc.).
5. **Versioned Plan**: Any update to the `implementation_plan.md` must preserve the original "Goal" to prevent "Mission Creep".

---
## 📚 Research Sources Synthesis (Sources 1-10)
- **Anthropic**: *Harnessing Design* & *Tool-Call Management*.
- **Databricks**: *Background Distillation Patterns*.
- **Google Vertex AI**: *Hierarchical Memory Taxonomy*.
- **Shaped.ai**: *Mitigating Lost-in-the-Middle in RAG*.
- **CIO/Enterprise**: *Memory Governance and Immutability Standards*.
- **Towards AI**: *Context Awareness & Multi-Agent State management*.
- **OpenAI Devs**: *State Snapshotting for Long Tasks*.
- **Arxiv/Stanford**: *The 4W Memory Framework*.

---
*Derived by Antigravity from 10+ Expert Sources in JIT Learning Mode (14:56:13+03:00).*
