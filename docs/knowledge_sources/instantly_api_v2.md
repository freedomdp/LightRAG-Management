# Instantly API Documentation Summary (v2)

This documentation provides the essential details for integrating with Instantly.ai for campaign and lead management.

## 1. API Authentication
- **Base URL:** `https://api.instantly.ai/v2`
- **Authentication Method:** Bearer Token
- **Headers:**
  - `Authorization: Bearer {{YOUR_API_KEY}}`
  - `Content-Type: application/json`

## 2. Campaign Management
### List Campaigns
Get a list of all campaigns in your workspace.
- **Endpoint:** `GET /api/v2/campaigns`
- **Description:** Returns an array of campaign objects containing `id`, `name`, `status`, etc.

### Other Campaign Endpoints
- `POST /api/v2/campaigns`: Create a new campaign.
- `GET /api/v2/campaigns/{id}`: Get details of a specific campaign.
- `PATCH /api/v2/campaigns/{id}`: Update a campaign.

## 3. Lead Management
### Add Leads to Campaign (Bulk)
Add multiple leads to a specific campaign or list.
- **Endpoint:** `POST /api/v2/leads/add`
- **Description:** Used to import leads into a campaign.
- **Payload Example:**
  ```json
  {
    "campaign_id": "YOUR_CAMPAIGN_ID",
    "skip_if_in_any_campaign": true,
    "leads": [
      {
        "email": "lead@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "company_name": "Example Corp",
        "personalization": "Custom intro here"
      }
    ]
  }
  ```

### Other Lead Endpoints
- `POST /api/v2/leads`: Create a single lead.
- `POST /api/v2/leads/list`: List leads with filters.
- `POST /api/v2/leads/move`: Move leads between campaigns.

## 4. Webhooks
Instantly can send real-time notifications to your system via webhooks.

### Available Webhook Events
| Event Type | Description |
| :--- | :--- |
| `email_sent` | An email was successfully sent. |
| `email_opened` | A lead opened an email. |
| `reply_received` | A reply was received from a lead. |
| `auto_reply_received` | An auto-reply was detected. |
| `link_clicked` | A lead clicked a tracked link. |
| `email_bounced` | An email failed to deliver. |
| `lead_unsubscribed` | A lead opted out of future emails. |
| `account_error` | An issue occurred with the sending account. |
| `campaign_completed` | All leads in a campaign have been processed. |
| `lead_interested` | Lead status changed to "Interested". |
| `lead_not_interested` | Lead status changed to "Not Interested". |
| `lead_neutral` | Lead status changed to "Neutral". |

---
*Extracted from Instantly Developer Documentation (v2) on April 13, 2026.*
