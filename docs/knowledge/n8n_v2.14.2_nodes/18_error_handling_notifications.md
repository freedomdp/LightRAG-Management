# n8n v2.14.2: Error Handling & Telegram Alerts

## 1. Importance of Silent Failures
In production price monitoring, a failure in 1 out of 50 items (e.g., a dead URL) should not stop the entire workflow. However, the developer must be notified.

## 2. Integrated Error Handling (The "Try-Catch" Node)
While n8n has an "Error Workflow" setting, project experience suggests using individual node error handling for *known* points of failure:
- **HTTP Request Node**: Under `Options`, set **`Ignore Response Code`** to `true`.
- **Result**: Even if the site returns 404, the node produces an item with status code.
- **Downstream**: Use an `If` or `Switch` node to check if the price was found. If not, proceed to the next item but log the error.

## 3. Telegram Alerting Pattern
Always create a reusable Telegram alert string for critical failures.
Format (HTML):
```html
<b>⚠️ n8n Failure!</b>
<b>Workflow:</b> Price Monitor
<b>Node:</b> {{ $node.name }}
<b>Error:</b> {{ $error.message }}
<b>Time:</b> {{ $now }}
```

## 4. Global Error Workflow
For unhandled exceptions (crashes, memory issues):
1. Create a separate workflow `Global Error Handler`.
2. Add a `Error Trigger` node.
3. Add a `Telegram` node to send a summary to the admin chat.
4. Link this workflow in the **Settings** -> **Error Workflow** of the main project.

## 5. LightRAG Rule
"Prevention is better than notification." Use `Ignore Response Code` on scrapers to allow the loop to finish, but always include a "Notification" branch for when a price is `0` or `null` for more than 2 consecutive runs.
