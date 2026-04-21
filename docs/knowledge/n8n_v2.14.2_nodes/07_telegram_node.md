# n8n v2.14.2: Telegram Node

## 1. Purpose
Used to send messages, photos, documents, and manage groups or channels via Telegram Bots. This is central to architectures like the Aberhol AI bot system or Notification modules.

## 2. Core Structure
- **`resource`**: `chat`, `message`, `callbackQuery`, `file`.
- **`operation`**:
  - For `message`: `sendMessage`, `editMessageText`, `deleteMessage`.
  - For `chat`: `get`, `member`, `leave`, etc.

## 3. Key Parameters (sendMessage)
- **`chatId`** (String): The ID of the recipient user, group, or channel. Can be retrieved from `$json.message.chat.id` in a Telegram Trigger.
- **`text`** (String): The content of the message.
- **`additionalFields`** (Fixed Collection):
   - **`parse_mode`** (Options): `HTML` or `Markdown` or `MarkdownV2`. n8n v2 defaults to no parsing, making rich text display as raw text. Set this to `HTML` explicitly if sending `<b>` or `<a href="...">` tags.
   - **`disable_web_page_preview`** (Boolean): Prevents links in the message from generating massive visual link-preview widgets.
   - **`reply_markup`** (JSON/Fixed Collection): Used for inline keyboards or custom reply keyboards.

## 4. Sending Media
When sending a photo, n8n relies on standard binary file handling:
1. Ensure the binary data is present in the node input (e.g., downloaded via `HTTP Request` into a binary property like `data`).
2. Telegram Node Operation: `photo` -> `send`.
3. Toggle `Use Binary File` to True.
4. Supply the binary property key (e.g., `data`).

## 5. Anti-Patterns
- **Invalid Parse Syntax:** Using `MarkdownV2` in Telegram is incredibly strict. A single unescaped `_` or `-` character will cause the Telegram API to return a 400 Bad Request. For dynamic text (like AI output or scraped titles), it is overwhelmingly safer to use `HTML` parse_mode and escape `<` and `>` appropriately.
