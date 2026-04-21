# n8n v2.14.2: Scraping Artline.ua Specifics

## 1. Site Characteristics (Artline.ua)
Artline.ua is a sophisticated e-commerce site that requires Javascript rendering to display the final calculated price including discounts or assembly components. Standard HTML scraping (GET) often fails.

## 2. Selector Strategy
- **Price Selector**: Often found in classes related to `price`, `total-price`, or specific ID-based elements.
- **Dynamic Selection**: The project uses a **Matrix** in Google Sheets to store selectors. This allows updating the selector in one place (the Sheet) if the site's CSS changes, without touching the n8n JSON nodes.

## 3. Browserless Settings for Artline
To reliably scrape Artline prices:
- **Wait Condition**: `networkidle2` is mandatory. The page loads many assets (images, scripts) that delay the price rendering.
- **Elements Array**: Pass the selector inside an array in the Browserless `/scrape` body:
  `"elements": [{ "selector": "{{ $json.selector }}" }]`

## 4. Experience: Handling Multiple Result Cards
Sometimes a selector matches multiple hidden elements.
- **JS Validation**: In the `Code` node after scraping, always iterate through the results and pick the first one containing actual digits. Avoid picking up "грн" text as the value.

## 5. LightRAG Rule
When scraping Artline.ua or similar complex stores:
1. Always Use Browserless.
2. Use `networkidle2`.
3. Use `parseInt()` with regex `/[^\d]/g` to extract the numerical value from the `res.text`. 
4. Check if the value is `> 0` to filter out empty/placeholder elements.
