# n8n v2.14.2: Local Browserless Integration (Docker)

## 1. Context
For stable scraping of SPA (Single Page Applications) or sites with heavy JS (like Artline, Rozetka), standard `HTTP Request` (GET) often returns empty HTML. The project experience confirms that **Local Browserless Chrome** is the superior choice over external APIs.

## 2. Connectivity (Docker-to-Docker)
- **URL**: `http://browserless:3000/scrape`
- **Port**: 3000
- Ensure n8n and browserless share the same Docker network (defined in `docker-compose.yml`).

## 3. Node Configuration (n8n v2.x)
- **Method**: `POST`
- **Body Content Type**: `JSON`
- **Payload Template**:
```json
{
  "url": "{{ $json.url }}",
  "elements": [{ "selector": "{{ $json.selector }}" }],
  "gotoOptions": { "waitUntil": "networkidle2" }
}
```

## 4. Key Lessons
- **`networkidle2`**: This is critical. `load` or `domcontentloaded` triggers too early for many price widgets. `networkidle2` waits until there are no more than 2 network connections for at least 500ms.
- **Selector Precision**: Always pass the selector dynamically from the Google Sheet (`{{ $json.selector }}`) rather than hardcoding. This allows fixing the scraper for a specific shop by just editing a cell in the spreadsheet.

## 5. LightRAG Rule
If a site returns "Access Denied" or empty values via standard `HTTP Request (GET)`, immediately recommend switching to the payload above using the local Browserless service.
