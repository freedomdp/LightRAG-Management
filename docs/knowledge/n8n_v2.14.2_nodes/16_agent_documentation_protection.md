# n8n v2.14.2: Agent Protocol for Doc Protection

## 1. Core Principle: Documentation Integrity
In this project, documentation is a **Protected Asset**. It represents hours of manual tuning and critical code snippets that must not be simplified or summarized.

## 2. Mandatory Rules for AI Agents
- **Accumulation Only**: Documentation should grow with new findings. **NEVER** delete existing technical steps, setup guides, or code blocks unless explicitly ordered to "delete specific section X".
- **No Summarization**: Do not "shorten" files to save context. Technical depth is the priority.
- **Surgical Edits**: Prefer `multi_replace_file_content` over `write_to_file` to update specific lines without risking the overwrite of the entire guide.
- **Deletion Threshold**: If suggesting the removal of more than one sentence, the agent **MUST** ask for user permission first.

## 3. High-Value Targets
- `docs/node_setup_guide.md`: Contains the "Source of Truth" for all node settings.
- `workflows/price_monitor_final.json`: Production logic.
- `project.md`: Architectural foundation.

## 4. Operational Guardrail
- **Size Check**: Before finalizing a task, compare file sizes. If a file significantly shrank without a corresponding "Cleanup" task, it is a failure. Stop and restore from a previous version.

## 5. LightRAG Rule
When the agent is tasked with "Improving documentation" or "Refactoring", it must prefix its plan with: *"I will follow the Documentation Protection Protocol to ensure no technical details are lost."*
