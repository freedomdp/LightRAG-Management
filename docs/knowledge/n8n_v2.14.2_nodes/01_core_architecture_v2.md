# n8n v2.14.2 Core Architecture & Node Fundamentals

## 1. Introduction
This document covers the core architecture, data structures, and node standard guidelines in n8n version 2.14.2. Understanding this is critical for preventing hallucinated nodes and parameters in LightRAG when building workflows.

## 2. Core Behavior Changes in v2.x (vs v0.x / v1.x)
- **Node Renaming:** 
  - `Set` is now `Edit Fields`
  - `Split in Batches` is now `Loop`
  - `Function` and `Function Item` are purely `Code`
- **Output Matching (Item Linking):** n8n v2.x relies heavily on automatic item matching. Expressions no longer strictly require `$('NodeName').item.json` in all scenarios; `$json.myField` automatically resolves correctly in mapped scenarios.
- **Node Parameter Validation:** v2.x strictly enforces parameter typing. Invalid string inputs into number fields will instantly fail validation before execution starts.

## 3. Node Types and Execution
- **Triggers:** Start a workflow (e.g., `Webhook`, `Schedule Trigger`, `Telegram Trigger`). Cannot be placed mid-workflow.
- **Regular Nodes:** Process data (e.g., `HTTP Request`, `Loop`, `Code`). Have inputs and outputs.
- **Sub-workflow Nodes:** `Execute Workflow` allows calling other workflows. Parameter passing is strictly typed.

## 4. Parameter Types Reference
All node properties in n8n v2.14.2 adhere to the `INodeProperties` interface:
- **String:** Regular text.
- **Number:** Numeric values (floats or ints). Cannot accept empty strings without expression mode.
- **Boolean:** Switch toggles.
- **Options:** Dropdown selections. Values must match the internal `name` of the option exactly, not the `displayName`.
- **Collection:** Grouped flexible parameters (found often in "Additional Fields" or "Query Parameters").

## 5. LightRAG Rule
When planning an n8n workflow for v2.14.2:
- NEVER hallucinate the `Set` node. Use `Edit Fields`.
- NEVER hallucinate `Split in Batches`. Use `Loop`.
- Only use parameters specifically documented for v2.x nodes.
