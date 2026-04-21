# n8n v2.14.2: HTTP Request Node

## 1. Purpose
The core mechanism for calling external APIs, executing webhook payloads, and performing web scraping.

## 2. Core Parameters
- **`method`** (Options): GET, POST, PUT, DELETE, PATCH, HEAD.
- **`url`** (String): The endpoint URL.
- **`authentication`** (Options): `none`, `predefinedCredentialType`, `genericCredentialType`.
- **`sendHeaders`** (Boolean): Toggle to open header key/value inputs.
- **`sendBody`** (Boolean): Toggle to send data. When active, reveals `bodyParameters` or `specifyBody` (json/raw string choices).
- **`sendQuery`** (Boolean): Toggle for query string parameters.

## 3. Important Options (Under 'options')
n8n v2.14.2 requires specific configuration to avoid failures that were implicitly handled in v0.x:
- **`responseFormat`**: By default, it expects JSON. If hitting an HTML page or downloading a file, this MUST be explicitly set to `string` or `file`. If you expect HTML and the format is set to `json`, the node will throw an error immediately.
- **`ignoreResponseCode`**: If true, HTTP statuses like 404 or 500 will NOT throw a workflow exception, instead returning the error code within the JSON `$json.statusCode`. Crucial for robust scraping architectures.
- **`proxy`**: Enables routing traffic through proxies. It uses standard `http://ip:port` format.

## 4. Modern Body Payload Handling
- Instead of using complex `Set` node JSON structures to build HTTP bodies, v2.x encourages using the `specifyBody` parameter combined with `json` format directly inside the HTTP Request node to paste JSON payloads populated with expressions (e.g., `{{ $json.field }}`).

## 5. Anti-Patterns
- Missing `responseFormat` when fetching HTML.
- Passing nested strings in Query parameters instead of proper URL encoding. n8n v2 handles URL encoding for standard query parameters automatically; do not double-encode them.
