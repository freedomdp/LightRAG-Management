# n8n v2.14.2: Code Node (Formerly Function/Function Item)

## 1. Purpose
The `Code` node executes custom JavaScript (or Python, depending on the environment setup) and replaces the legacy v1.x `Function` and `Function Item` nodes.

## 2. Architecture & execution modes
- **`mode`** (Options):
  - `runOnceForAllItems`: Similar to the deprecated `Function` node. It receives an array of ALL items (`$input.all()`). Returns an array of items. Use this to aggregate, sort, or manipulate the array as a whole.
  - `runOnceForEachItem`: Similar to the deprecated `Function Item` node. It executes the script iteratively for every single item currently passing through. Useful for appending specific logic per single item without traditional loop handling.

## 3. Context Variables & API
In v2.x, the internal n8n Node.js context is significantly cleaner:
- **`$input.all()`**: Returns the full array of JSON items received by the node. Structure: `[{ json: {...}, binary: {...} }]`.
- **`$input.item`**: The current item being processed (only available in `runOnceForEachItem` mode).
- **`$json`**: Direct access to the current JSON fields.
- **`return` syntax**:
  - Mode 1 (`runOnceForAllItems`) MUST return an array of objects structured as `[{ json: { ... } }]` or literally return `$input.all()`.
  - Mode 2 (`runOnceForEachItem`) MUST return a single object (e.g., `{ json: { ... } }`).

## 4. Dependencies
Unless specifically requested via the `NODE_FUNCTION_ALLOW_BUILTIN` and `NODE_FUNCTION_ALLOW_EXTERNAL` environment variables in `docker-compose.yml`, Code nodes cannot `require('fs')` or `require('axios')`. Limit Code node logic purely to data parsing, array mapping, or math logic. Note: `luxon` is permitted natively for dates: `const { DateTime } = require('luxon');`.

## 5. Anti-Patterns
- **AI Hallucination:** Generating `Function` or `Function Item` nodes. These do not exist in modern n8n v2 UI. AI must generate `Code` nodes.
- **Returning flat arrays:** Returning `[1, 2, 3]` is an error. You must return `[{json: {value: 1}}, {json: {value: 2}}, {json: {value: 3}}]`.
