# n8n v2.14.2: Item Lists and Error Trigger

## 1. Item Lists Node Overview
In v2.14.2, array manipulation without coding is done via the `Item Lists` node. It replaces legacy manipulations scattered across other tools.
- **`operation`**:
  - `aggregateItems`: Takes 100 individual JSON items moving through a workflow and collapses them into a single item containing an array. Extremely useful before sending 1 single Email instead of 100 emails, or bulk saving into Google Sheets.
  - `splitOutItems`: The reverse. Takes 1 JSON item that has a large array field (e.g., `$json.data.products`) and blows it out into 100 individual downstream n8n items.
  - `sort`: Orders items intuitively.
  - `limit`: Slices the first N items.
  - `concatenate`: Joins fields.

## 2. Error Trigger Node Overview
A robust system MUST have an `Error Trigger` workflow.
- **Purpose**: Instead of stopping silently, you create a dedicated workflow starting exclusively with the `Error Trigger` node. 
- **Configuration**: Inside the main workflow settings (top right), assign the "Error Workflow" to point to your new error workflow.
- **Output**: The `Error Trigger` provides `$json.execution.id`, `$json.workflow.id`, and most importantly `$json.execution.error.message`.
- **Alerting Integration**: Link the `Error Trigger` output to a `Telegram` node (sendMessage) containing an HTML formatted alert:
  `<b>Workflow failed!</b> %0A ID: {{ $json.execution.id }} %0A Error: {{ $json.execution.error.message }}`

## 3. Anti-Patterns (Item Lists)
- **Hallucination Warning:** AI often tries to use `$json.map()` heavily inside `Set` nodes or tries to write 50 lines of JS in a `Code` node just to aggregate items. N8N v2.14.2 explicitly recommends using the `Item Lists` > `Aggregate Items` node for zero-code, high-performance aggregation.
- In `SplitOutItems`, make sure the "Field to Split Out" only references the property name (e.g. `products`), NOT an expression syntax `{{ $json.products }}` unless parameterized.
