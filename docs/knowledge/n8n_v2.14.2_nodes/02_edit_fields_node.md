# n8n v2.14.2: Edit Fields Node (Formerly Set Node)

## 1. Purpose
The `Edit Fields` node replaced the legacy `Set` node in n8n v1.x and v2.x. It is used to add, modify, replace, or delete fields from the JSON items passing through the workflow.

## 2. Core Parameters
- **`mode`** (Options): Determines how existing fields are treated.
   - `add`: (Default) Adds new fields to the existing input data.
   - `set`: Replaces the entire input item with only the fields defined in this node.
   - `delete`: Removes referenced fields.
   - `keep`: Keeps ONLY the referenced fields, deleting the rest.

- **`assignments`** (Fixed Collection):
   - Here, users map specific values to new or existing keys.
   - `name`: The JSON path or key name to set (e.g., `price`, `user.id`).
   - `type`: Data type to enforce (`string`, `number`, `boolean`, `array`, `object`).
   - `value`: The value to set (can be an expression `$json.value`).

## 3. Advanced Parameters (Additional Options)
- **`dotNotation`** (Boolean): If enabled, keys with dots (e.g., `user.name`) will create nested JSON objects. If disabled, it creates a flat key literally named `user.name`.

## 4. Anti-Patterns & Common Errors
- **Hallucination Warning:** AI often tries to use the legacy `Set` node with properties like `values: { string: [...] }`. This is strictly **INVALID** in n8n v2.14.2. You must use `Edit Fields` with the `assignments` array.
- **Type Mismatch:** Forcing a string into an assignment typed as `number` will throw a runtime error in v2.x. Always cast properly in expressions.
