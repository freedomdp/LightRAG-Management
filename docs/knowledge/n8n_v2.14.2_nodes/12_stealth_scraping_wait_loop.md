# n8n v2.14.2: Stealth Scraping (Loop + Wait Pattern)

## 1. Overview
In v2.14.2, the most reliable way to avoid IP bans and "Bot Detected" errors on sites like Artline.ua is the **Recursive Loopback Wait** strategy.

## 2. Practical Configuration
- **Node A: Loop (Split in Batches)** 
  - `Batch Size`: 2 or 3 (Low values mimic human browsing speed).
- **Node B: Scrape Logic (HTTP/Browserless)**
- **Node C: Wait**
  - `Wait Time`: 5-10 Seconds.
  - `Path`: Connect the output of the Wait node BACK to the input of the **Loop** node.

## 3. Critical Experience: The Loopback
In n8n v2.x, if you don't connect the end of your processing branch back to the "Loop" node, the automation will stop after the first 3 items. 
- **Wait node placement**: Always place the Wait node *before* returning to the Loop to ensure the cool-down happens between batches, not just at the start.

## 4. Why this works better than "Execute for each item"
The `Execute for each item` mode in n8n v2.x tries to run everything as fast as the runner allows. By using a manual Loop + Wait, we gain granular control over the "Heartbeat" of the scraper.

## 5. LightRAG Rule
When the user mentions "blocking", "stealth", "ban", or "many items", ALWAYS suggest the `Loop` + `Wait` recursive pattern. Never scrape more than 5 items in a single surge without a delay.
