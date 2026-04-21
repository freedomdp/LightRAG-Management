# n8n v2.14.2: Switch Node

## 1. Purpose
The Switch node redirects the workflow execution flow into different branches based on evaluation rules. It completely replaces the legacy `IF` node for multi-branch logic, though `If` still exists for simple true/false checks.

## 2. Core Structure
- **`mode`** (Options): `rules`.
- **`rules`** (Fixed Collection):
  - Array of rule conditions. Each rule evaluates against your input.
  - **`value1`**: Usually the expression checking `$json.field`
  - **`operation`**: `equal`, `notEqual`, `contains`, `exists`, `isEmpty`, `larger`, `smaller`, `regex`, etc.
  - **`value2`**: The target test value.
- **`fallbackOutput`** (Options): Dictates what happens if NO rules match.
  - `none`: Silently drops the item.
  - `0`, `1`, `2`...: Routes the unmatched item to a specific output index (often used to build a "Default" branch).
  - `extra`: Provides an entirely distinct fallback output branch separated from the standard rule outputs.

## 3. Data Type Evaluation Rules
In v2.x, the Switch node strictly evaluates types:
- A JSON field containing `500` (Number) evaluated with `equal` operation to `"500"` (String) might be rejected depending on the strictness toggle (often hidden in type checking). To be safe, always ensure `$json.price` is cast correctly or use `.toString()` in expressions if comparing string against string.
- `isEmpty` operation is extremely robust in v2.x. It safely captures null, undefined, "", and empty objects `{}`. It is highly recommended over `equal` -> `""` when evaluating scraped web text that might be missing entirely in the HTML payload.

## 4. Output Branches
Every defined rule inside `rules` corresponds logically to an Output index 0, 1, 2, ..., N. When designing logic, make sure the UI wiring perfectly aligns with the target index.

## 5. Anti-Patterns
- Using multiple `If` nodes chained recursively instead of one `Switch` node.
- Comparing floats with strict `equal`. Use `larger` and `smaller` to create bounded ranges for numeric monitoring.
