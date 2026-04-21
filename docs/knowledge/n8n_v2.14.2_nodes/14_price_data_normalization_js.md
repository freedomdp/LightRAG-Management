# n8n v2.14.2: Price Data Normalization (JS)

## 1. Problem
Scraped text often contains currencies (грн, $, руб), spaces, and non-breaking characters (`&nbsp;`). Google Sheets cannot perform math on these strings.

## 2. Practical JS Solution
Inside a `Code` node, use the following regex-based cleaner:

```javascript
let rawText = " 25 400 грн ";
let cleanPrice = parseInt(rawText.replace(/[^\d]/g, '')); 
// Result: 25400 (Number)
```

## 3. Experience: Aggregating Loop Results
When using a Loop, you need to "pivot" results back from individual items into a single row before updating Google Sheets.

### The "Gatherer" Pattern:
```javascript
// Accessing data from a previous node inside a loop context
const allScrapedItems = $items("Scrape Price");
const results = {};

for (const item of allScrapedItems) {
    const productName = item.json.product;
    const price = item.json.data[0]?.results[0]?.text || "0";
    results[productName] = parseInt(price.replace(/[^\d]/g, '')) || 0;
}
return [{ json: { "Shop": "MyName", ...results } }];
```

## 4. Handling Errors (Optional/Smart)
- **Zero Value Check**: If `parseInt` fails, return `0` or `null`, then use a `Filter` node downstream to only update rows that successfully found a price.
- **Trim()**: Always `.trim()` product names before using them as keys to avoid ` "Product "` != `"Product"` issues in JSON objects.

## 5. LightRAG Rule
Data from the web is "dirty". Never send raw scraped text directly to a database or sheet. Always normalize to `Number` using the regex `/ [^\d] /g` first.
