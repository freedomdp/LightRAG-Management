---
name:  client-brief-extractor
description: >
  Extract a structured client brief from a raw task, message, or conversation.
  Use this skill when the user says "разбери ТЗ", "вытащи бриф", "клиент написал вот это",
  "помоги понять задачу", "что клиент хочет", "составь бриф", "оформи задачу",
  or pastes a raw client message, voice note transcript, or messy task description
  and wants it turned into a clean, structured brief.
  Always use this skill — it extracts goals, audience, deliverables, deadlines,
  budget, risks, and open questions from any raw input.
---

# Client Brief Extractor Skill

Turns messy client input into a clean, structured brief.
Works with any format: WhatsApp message, email, voice note transcript,
Notion task, or a few sentences in chat.

---

## Workflow

1. **Receive raw input** — paste from client, transcript, or description
2. **Extract all available information** — map to brief structure
3. **Mark gaps** — flag anything missing or unclear with ⚠️
4. **Output structured brief** — clean, copy-ready
5. **Generate clarifying questions** — only what's genuinely missing
6. **Optional: suggest next step** — what to do with this brief now

---

## Brief Structure

Extract and fill in every field. If information is absent — write `не указано` and flag with ⚠️.

---

### 1. Project Overview
- **What:** one sentence — what is this project?
- **Why:** what problem does the client want to solve?
- **Context:** any background that matters (brand, previous work, situation)

### 2. Goal & Success Criteria
- **Main goal:** what does "done well" look like for the client?
- **Success metric:** how will they measure it? (views, sales, approval, deadline met)

### 3. Deliverables
Exact list of what needs to be produced:
- Format (video / post / deck / design / text / code / etc.)
- Quantity
- Specifications (length, size, format, platform)

### 4. Target Audience
- Who is this for?
- Age, geography, level (beginner / pro), platform

### 5. Tone & Style
- Brand voice (if mentioned)
- Examples or references provided?
- What to avoid?

### 6. Timeline
- **Deadline:** when is the final delivery due?
- **Milestones:** any intermediate checkpoints?
- **Urgency level:** normal / urgent / flexible

### 7. Budget
- Amount stated? If yes — what's included?
- Payment terms mentioned?
- Mark as ⚠️ if not discussed

### 8. Constraints & Requirements
- Technical requirements
- Must-haves the client explicitly stated
- Hard limits (what NOT to do)

### 9. Risks & Red Flags
Proactively flag potential issues:
- Vague goals that could lead to scope creep
- Missing approval process
- Tight deadline with unclear feedback loops
- No budget discussed
- Conflicting requirements

### 10. Open Questions
List only the questions that are genuinely blocking work.
Prioritize — ask 3–5 max, not 20.

Format:
```
1. [Question] — needed to [clarify deliverable / avoid risk / confirm scope]
```

---

## Output Format

Single structured card with all sections.
Each missing field marked with ⚠️.
Open questions listed at the bottom, ready to copy-paste to the client.

---

## Tone Rules

- Write the brief in neutral, professional language
- Don't editorialize — extract what's there, flag what's missing
- If the client's message is emotional or indirect — translate to clear task language
- Never invent details that weren't in the input

---

## Red Flag Patterns

Automatically flag these as risks if present in the raw input:

| Pattern | Risk |
|---------|------|
| "сделай как у [конкурента]" | No original brief — scope creep likely |
| "быстро", "срочно" без даты | Unclear deadline — pin it down |
| "ну ты сам знаешь что нужно" | No clear deliverable — must clarify |
| "бюджет обсудим потом" | Unpaid work risk |
| "можно будет поправить" | Unlimited revisions implied |
| "сделай красиво" | No success criteria |
| Несколько задач в одном сообщении | Scope too wide — needs splitting |

---

## Example

**Raw client input:**
> "Привет! Нам нужно видео для инсты, что-то про наш новый продукт — крем для лица. Хотим чтобы было модно, молодёжно. Можешь к пятнице? Бюджет пока не знаем, обсудим. Референсы скину потом"

**Extracted Brief:**

**Проект:** Видео для Instagram о новом продукте (крем для лица)

**Цель:** Презентация нового продукта, создание интереса у аудитории

**Дедлайн:** Пятница ⚠️ (какая именно дата — не указано)

**Deliverables:**
- 1 × видео для Instagram ⚠️ (формат не указан: Reels / Stories / пост?)
- Длина: ⚠️ не указана
- Платформа: Instagram

**Аудитория:** Молодёжная ⚠️ (возраст, география — не указаны)

**Тон и стиль:** Модно, молодёжно ⚠️ (референсы обещаны, но не предоставлены)

**Бюджет:** ⚠️ Не обсуждался — риск

**Риски:**
- ⚠️ Бюджет не определён — работа может начаться без договорённости об оплате
- ⚠️ Референсы не предоставлены — стиль не согласован
- ⚠️ Дедлайн размытый ("пятница" — какая?)
- ⚠️ Формат видео не указан

**Вопросы клиенту:**
```
1. Какая конкретная дата пятницы — [число]?
2. Какой формат видео: Reels (вертикальное, до 90 сек) или Stories?
3. Какой бюджет на производство?
4. Когда пришлёшь референсы — до начала работы?
5. Кто утверждает финальный вариант и сколько правок включено?
```

<!-- INDEX_V2: 21.04.2026 -->
