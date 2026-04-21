# n8n v2.14.2: Loop Node (Formerly Split in Batches)

## 1. Purpose
The `Loop` node has officially replaced the `Split in Batches` node. It is designed to iterate over arrays or lists of items, passing them sequentially or in small groups (batches) to downstream nodes.

## 2. Core Parameters
- **`mode`** (Options): Defines how items are grouped.
   - `passEach`: Passes items 1 by 1.
   - `passInBatches`: Passes predefined N items per batch.
- **`batchSize`** (Number): Only visible when `mode` is `passInBatches`. Determines the chunk size.

## 3. Node Outputs
The Loop node operates essentially as a router with TWO specific output branches:
1. **Loop Output (Branch 1):** Items passed into the loop for execution.
2. **Done Output (Branch 2):** Triggers only when all items have been processed by the loop.

## 4. Architectural Rules & Anti-Patterns
- **Hallucination Warning:** AI often outputs `SplitInBatches` as the node type. This is WRONG in v2.x architecture context. AI must use the `Loop` node.
- **Routing Structure:** A loop MUST return back to itself. The last node in the processing branch must link back to the input of the `Loop` node to trigger the next batch. If this loopback is missing, execution will stall after batch 1.
- **Data Retention:** By default, data from inside the loop is NOT preserved automatically at the "Done" output unless aggregated (e.g. using an `Item Lists` or `Code` node before closing the loop). In v2.x, the Loop node does not automatically accumulate processed items from branch 1 to branch 2.

## 5. Typical Scenarios
- Scraping an array of URLs without hitting rate limits. Uses `Loop` -> `HTTP Request` -> `Wait` -> back to `Loop`.
