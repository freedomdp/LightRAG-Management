# n8n v2.14.2: Unpivot Matrix Pattern (Google Sheets to Items)

## 1. Problem
Google Sheets are often maintained in a "human-readable" horizontal matrix format where each column is a product and each row is a shop. n8n processing (like scraping) requires a "machine-readable" vertical list of tasks.

## 2. Solution: The Unpivot Code Node
To convert a horizontal row into multiple vertical items, use a `Code` node in **`Run Once for All Items`** mode.

### Implementation Logic:
```javascript
const items = $input.all();
const output = [];

for (const row of items) {
  const shopData = row.json;
  const shop = shopData['Магазин'];
  const selector = shopData['Селектор'];
  
  for (const key in shopData) {
    // Skip metadata columns, process only product URLs
    if (key !== 'Магазин' && key !== 'Селектор' && shopData[key]) {
      output.push({
        json: {
          shop: shop,
          selector: selector,
          product: key,
          url: shopData[key]
        }
      });
    }
  }
}
return output;
```

## 3. Experience Gained
- **Column Filtering**: Always skip metadata columns (`Shop`, `Selector`, `ID`) using explicit checks.
- **Empty Cell Handling**: Check for `shopData[key]` existence before pushing to output to avoid trying to scrape empty URLs.
- **Downstream Linking**: Including `shop` and `selector` in every output item ensures subsequent nodes (like HTTP Request) have all the context they need without looking back to previous nodes.

## 4. LightRAG Rule
When dealing with "Price Monitoring" or "Matrix" tasks, prioritize this Unpivot pattern over manual "If" chains. It allows adding 100 products by just adding 100 columns to the sheet without changing the n8n workflow.
