# Apify Expert Guide: Architecture & Core Concepts

This document provides a technical overview of the Apify platform, designed for scaling web automation in the AI Agency.

## 1. The Actor Model (Serverless Microservices)
**Actors** are the building blocks of Apify. Each Actor is a serverless application (Node.js/Python) packaged in a Docker container.
- **Statelessness**: Actors don't store local state; they use Apify Storage.
- **Portability**: They can run on Apify Cloud or locally using the Apify CLI.
- **Ephemerality**: They spin up for a task and shut down immediately after, saving costs.

## 2. Tasks: The Configuration Layer
A **Task** is a specific configuration of an Actor. 
- *Example*: You take the "Google Maps Scraper" Actor and create a Task named "Dubai_Coffee_Shops" with predefined coordinates and search terms.
- **API Endpoints**: Every Task has its own API endpoint for easy triggering from n8n.

## 3. Storage Systems (The 3 Pillars)
### A. Datasets (Structured Data)
Designed for tabular results (Scraped leads, product lists).
- **Format-Agnostic**: Export results instantly to JSON, CSV, XML, or Excel.
- **Append-Only**: Optimized for high-speed write operations during crawling.

### B. Key-Value Stores (Files & State)
Designed for storing unstructured data.
- **Use Cases**: Screenshots, HTML snapshots of blocked pages, or persisting heavy PDF files.
- **Global Access**: Accessible via a simple URL for external tools.

### C. Request Queues (Crawling State)
The "brain" of a crawler.
- **Deduplication**: Automatically ensures the same URL isn't crawled twice.
- **Persistence**: If an Actor crashes, the Queue remembers where it left off.

## 4. Proxies & Anti-Blocking
Apify provides a sophisticated proxy rotation layer:
- **Residential Proxies**: Best for bypassing strict bot detection (Google, Amazon).
- **Datacenter Proxies**: Cheaper/faster, good for sites without advanced protection.
- **Browser Fingerprinting**: Automatically mimics real browser headers to avoid Cloudflare detection.

---
*Created as part of the Agency-Base Intelligence Core.*
