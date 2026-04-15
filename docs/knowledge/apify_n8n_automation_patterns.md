# Apify & n8n: Automation Patterns & Integration

This document covers the strategies for integrating Apify Actors into n8n workflows for high-performance data pipelines.

## 1. Installation & Setup
- **Package**: Search for `@apify/n8n-nodes-apify` in n8n community nodes.
- **Authentication**: Create an **API Key** in the Apify Console under *Settings > Integrations*.
- **Endpoint**: Ensure you use `https://api.apify.com/v2` for the API URL.

## 2. Core Automation Patterns

### Pattern A: The "Direct Trigger" (Sync)
*Best for fast tasks (single page scrape).*
1. **n8n Node**: Use `Run Actor` or `Run Task`.
2. **Waiting**: Enable "Wait for Finish".
3. **Data**: The node outputs the Dataset items directly into the next n8n node.

### Pattern B: The "Webhook Bridge" (Async)
*Best for heavy tasks (mass YouTube/G-Maps scraping).*
1. **n8n Node**: Trigger Actor WITHOUT waiting.
2. **Apify Webhook**: In the Apify Task settings, add a Webhook link pointing to an **n8n Webhook Node**.
3. **Event**: Set the event to `RUN.SUCCEEDED`.
4. **Resumption**: Once the Actor finishes (even hours later), it triggers the n8n Webhook to continue the pipeline.

## 3. Advanced Node Operations
- **Get Dataset Items**: Use this to pull results from a previous run or a fixed Dataset ID.
- **Run Task**: Prefer this over "Run Actor" to keep your configurations (parameters, limits) centralized in the Apify UI.
- **AI Tooling**: The Apify node can act as a Tool for the **AI Agent node** in n8n, allowing the agent to "Google the web" or "Analyze a site" autonomously.

## 4. Error Handling
- **Retry Logic**: Configure n8n "On Error" settings to retry Apify tasks if they fail due to concurrency limits.
- **Timeout Management**: For browser-heavy tasks, ensure the Actor timeout (in Apify) is longer than the expected run time.

---
*Created as part of the Agency-Base Intelligence Core.*
