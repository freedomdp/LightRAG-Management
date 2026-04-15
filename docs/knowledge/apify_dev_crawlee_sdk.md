# Apify Developer Guide: Crawlee & Custom SDKs

When off-the-shelf Actors are insufficient, the Apify ecosystem provides powerful frameworks for building custom, highly-scalable scrapers.

## 1. Crawlee (The Open-Source Core)
**Crawlee** is the modular Node.js crawling library that powers the best Actors on Apify. 
- **Auto-Bypass**: Built-in logic to rotate browser fingerprints and manage proxies to stay undetected.
- **Engines**: Choose between `Cheerio` (fast HTML parsing), `Puppeteer`, or `Playwright` (full browser automation).
- **Scalability**: Managed Request Queues allow you to crawl millions of pages without losing state.

## 2. Setting Up a Custom Actor
1. **Initialize**: Use `apify create my-actor` via CLI.
2. **Logic**: Write your crawling logic using Crawlee wrappers (`PlaywrightCrawler`, `PuppeteerCrawler`).
3. **Storage**: Use `Actor.pushData()` to save results to the Dataset.
4. **Environment**: Actors run in Docker; Apify handles the infrastructure and scaling.

## 3. Apify Python SDK
For Python-centric workflows (BeautifulSoup, Scrapy, Selenium):
- **Compatibility**: Integrates seamlessly with `Actor.create_proxy_configuration()` for advanced rotation.
- **Workflow**: 
  - Install: `pip install apify`
  - Pattern: Fetch inputs -> Process -> Store in Dataset.

## 4. Building Reliable Scrapers
- **Headless Mode**: Always use headless mode for production runs to save memory/credits.
- **Concurrency**: Set `maxConcurrency` to match your Actor's memory limits.
- **Wait Strategies**: Use Crawlee's `waitForSelector()` or `waitForNavigation()` to handle data-heavy SPAs (Single Page Apps).

---
*Created as part of the Agency-Base Intelligence Core.*
