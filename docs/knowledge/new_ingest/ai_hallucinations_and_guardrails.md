# AI Hallucinations: Detection & Guardrails

As an Agentic AI, maintaining factual accuracy and staying within boundaries is critical for professional agency work. This document defines the standards for self-monitoring and error prevention.

## ⚠️ Understanding Hallucinations in SEO

SEO is prone to "creative" hallucinations where an agent might:
1.  **Invent nonexistent hooks**: Suggesting `wp_head_seo` (doesn't exist) instead of `wp_head`.
2.  **Fabricate stats**: Claiming code improves speed by "400%" without data.
3.  **Ambiguous boundaries**: Attempting to fix server-side Nginx config when asked for WP code.

## 🛠️ Hallucination Detection Tools (Market Standards)

1.  **Galileo**: Enterprise-grade observability for LLM inputs and outputs.
2.  **Cleanlab**: Identifies noisy labels and factual drift in training data/retrieval.
3.  **Vectara HHEM**: Hallucination Evaluation Model for RAG systems (calculates a factuality score).
4.  **Giskard**: Open-source framework for scanning vulnerabilities and performance leaks in models.

## 🛡️ Guardrail Strategies for the Agent

To ensure high-quality output, apply these logic patterns:

### 1. Chain-of-Thought (CoT) Verification
Before generating any PHP code, the agent MUST:
- State the Hook name.
- Verify its existence in official documentation.
- Describe the logic in 1 sentence.

### 2. Structured Output (Schema Validation)
- Use JSON schemas for configurations.
- Adhere to strict Markdown checklists for task reporting.
- "Zero-Creativity" mode for technical specifications.

### 3. Self-Correction Cycle
1.  **Generate**: Produce the code/answer.
2.  **Critique**: Check against the "Iron Rules" (project.md) and the "Technical SEO Checklist".
3.  **Refine**: Fix any inaccuracies BEFORE presenting to the user.

### 4. RAG-First Mentality
- If unsure about a WP hook or SEO metric, use `mcp_lightrag_query_knowledge` or `context7` search.
- Do NOT rely on training data for versions > 2024.

## 🚫 The "Stop & Ask" Protocol

The agent MUST stop and ask for clarification if:
- The task requires access to production secrets (`.env` values beyond generic keys).
- The requested change contradicts established `project.md` standards.
- The outcome could lead to a permanent data loss (e.g., bulk database deletion) without a backup.
