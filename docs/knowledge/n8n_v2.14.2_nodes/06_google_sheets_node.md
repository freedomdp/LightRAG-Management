# n8n v2.14.2: Google Sheets Node

## 1. Purpose
Reads, writes, deletes, and updates rows in Google Sheets. Crucial for syncing scraped data, storing leads, and maintaining price monitoring records.

## 2. Core Structure & Operations
In n8n v2.x, the Google Sheets node operations are standardized into the following layout:
- **`resource`**: `document`, `sheet`, `row`.
- **`operation`**:
  - For `row`: `append`, `clear`, `delete`, `get`, `getAll`, `update`.
  - For `sheet`: `clear`, `create`, `delete`, `read`.
  - For `document`: `create`.

## 3. Row Appending and Updating
- **`documentId`** (String or Lookup): Selects the spreadsheet. Choose 'By ID' to dynamically pass `$json.id`.
- **`sheetName`** (String): Selects the specific tab.
- **`mappingColumnMode`** (Options): VERY IMPORTANT in v2.x.
  - `autoMapInputData`: Automatically maps JSON keys in the node input directly to column headers in the Google Sheet. Keys MUST exactly match the header rows.
  - `mapEachColumnManually`: Opens an explicit Column -> Value mapping matrix. Ideal when n8n input keys differ from Google Sheet column names.

## 4. Anti-Patterns & Best Practices
- **Header Rows:** Ensure the Google Sheet has a defined header row (row 1). Without it, native mapping fails and throws a runtime exception in `v2.x`.
- **Data Types Handling:** Numeric fields in n8n input will be correctly sent to Google Sheets as numeric cells. However, prepending a value with an apostrophe `'` explicitly forces Google Sheets to treat it as a string (ideal for phone numbers or barcodes).
- **Rate Limiting:** Google Sheets API applies rate limits. If looping over 500+ rows using the `Loop` node, always aggregate items using the `Item Lists` node or run the `Google Sheets` node directly on arrays; n8n automatically handles batch saving to row ranges in bulk. Single row-by-row updates in a loop will throttle your workflow quickly.
