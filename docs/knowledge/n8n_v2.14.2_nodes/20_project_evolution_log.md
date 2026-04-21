# n8n v2.14.2: Project Evolution & Decisions

## 1. History of Scraping Choice
Initially, the project explored external APIs like Apify, Browseract, and Scrape.do.
- **Decision**: Switched to **Local Browserless Chrome**.
- **Reasoning**: Zero cost per request, total control over JS rendering timeouts, and data privacy.

## 2. History of Data Storage
- **Decision**: Standardized on **Google Sheets Matrix**.
- **Reasoning**: Allows non-technical users (the project manager) to add new shops and products without logging into n8n. The "Unpivot" logic (Doc 11) handles the technical translation.

## 3. History of Versioning
- **Decision**: Frozen at **n8n v2.14.2**.
- **Reasoning**: Stability of core nodes and compatibility with local Docker setup. Upgrading to v2.15+ or v3.x is postponed until full regression tests are passed.

## 4. Key Architectural Win: The "Matrix Update"
Instead of "Create Row" which bloats sheets, the project uses **"Update Row" or "Append with Fixed Matrix"** logic. This keeps the Google Sheet compact and allows using it as a live dashboard.

## 5. LightRAG Rule
When the user asks "Why are we doing it this way?", refer to this evolution log. The sequence is: **Cost-Effective Local Tools** -> **Scalable Spreadsheet Management** -> **Stable Fixed Versions.** Avoid suggesting "latest shiny tools" if they break this fundamental philosophy.
