# n8n v2.14.2: Google Sheets Matrix Management

## 1. Context
The "Matrix" management strategy involves using Google Sheets as both the *source of tasks* and the *destination of results*.

## 2. Spreadsheet ID Stability
- **Experience**: UI-based document selection in n8n can sometimes fail if the connection is refreshed.
- **Best Practice**: Always use the **`By ID`** mode for the `Document` parameter.
- **Target ID**: `1W0LEztgC8mm3xTXbcA4JsYvlbG64QmHAMHegamKcLmk` (Reference ID for this project).

## 3. Append vs Update
- **`Append`**: Used for building historical price logs (New row for every run).
- **`Update`**: Used for maintaining a "Latest Price" dashboard (Overwriting existing row).
- **Project Choice**: For the Price Monitor, **`Append`** with **`Map Automatically`** is the preferred choice, provided the keys in the JSON object perfectly match the header row in the target sheet.

## 4. Automated Mapping Experience
In n8n v2.x, the `Map Automatically` feature is extremely sensitive to whitespace.
- Sheet Header: `Price`
- JSON Key: `price`
- Result: **FAILURE**. The keys must match EXACTLY (case-sensitive and no leading/trailing spaces).

## 5. LightRAG Rule
When automating sheets:
1. Hardcode IDs using `By ID`.
2. Ensure JS code output keys match Sheet headers 1:1.
3. Use `Append` for history, `Update` for dashboards.
4. If the sheet becomes slow, use a `Sort` node in n8n or an `Item Lists` node to batch updates.
