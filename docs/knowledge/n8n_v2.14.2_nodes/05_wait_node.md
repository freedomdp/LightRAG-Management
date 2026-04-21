# n8n v2.14.2: Wait Node

## 1. Purpose
Used to suspend workflow execution temporarily. This is absolutely critical in scraping and automation architectures to avoid IP bans, simulate human behavior, and handle rate limits (HTTP 429).

## 2. Modes and Parameters
- **`resume`** (Options): Defines wait behavior.
  - `afterTime`: Pauses for a defined timeout (seconds, minutes, hours, days).
  - `onWebhook`: Suspends until a specific webhook endpoint is called (creates an execution-specific URL).

### 2.1 After Time Parameters
- **`waitTime`** (Number): The numerical value.
- **`waitTimeUnit`** (Options): `seconds`, `minutes`, `hours`, etc.

## 3. Advanced Usage: Randomized Wait
A crucial pattern in avoiding bot detection when web scraping is using randomized delays.
In n8n v2.14.2, the Wait node does not have a native "randomize time" toggle out of the box. 
**To randomize wait time:**
Instead of a fixed integer in `waitTime`, switch the parameter to Expression mode and use JavaScript math, for example:
`{{ Math.floor(Math.random() * (10 - 3 + 1)) + 3 }}`
*(This creates a random delay between 3 and 10 of the specified `waitTimeUnit`)*

## 4. Anti-Patterns
- **Using Node.js `setTimeout` in a Code node:** Do NEVER use `setTimeout`, `sleep()`, or generic JS async blocks inside a Code node to implement delays. n8n execution environment expects synchronous data returned or Promises. It wastes executing runner resources. ALWAYS use the native `Wait` node.
- **Large Fixed Delays in Synchronous Webhooks:** If a workflow is triggered by an API call that expects an immediate response, using a `Wait` node for several minutes will cause the calling application to timeout (HTTP 504). Ensure triggers return response immediately if downstream waits are extensive.
