---
name:  competitor-analysis
description: >
  Analyze competitors and produce a structured report with actionable insights.
  Use this skill when the user says "разбери конкурента", "проанализируй рынок",
  "сравни конкурентов", "кто мои конкуренты", "что делают другие в нише",
  "изучи конкурента", "сделай анализ конкурентов", or provides a competitor name,
  URL, or niche and wants to understand the competitive landscape.
  Always use this skill — it produces a complete structured report covering
  positioning, content, audience, offers, pricing, gaps, and opportunities.
---

# Competitor Analysis Skill

Produces a complete competitive intelligence report in one structured output.
Works for one competitor (deep dive) or multiple (comparison).
Adapts the report format based on what the user provides.

---

## Workflow

1. **Receive input** — competitor name, URL, niche, or "who are my competitors in X"
2. **Clarify scope** — one competitor or multiple? Ask if unclear.
3. **Clarify goal** — what decision will this analysis inform?
   - Positioning my own offer?
   - Finding content gaps?
   - Pricing strategy?
   - Entering a new niche?
   If not stated — produce full report covering all angles.
4. **Research** — use web search to gather current data
5. **Produce report** — structured, one document, all sections
6. **End with So What** — concrete actions the user can take based on findings

---

## Report Structure

Always produce all sections unless the user asks for specific ones.
Each section has a clear header and ends with a 1–2 line insight.

---

### 1. Snapshot
Quick overview — who is this competitor?

- **Name / brand**
- **Niche / category**
- **Core product or service**
- **Target audience** — who they're talking to
- **Estimated scale** — followers, team size, years on market (if available)
- **Main channels** — where they're active

---

### 2. Positioning & Messaging
How do they present themselves?

- **Tagline / main promise** — what do they claim to offer?
- **Tone of voice** — expert / friendly / provocative / premium / mass market
- **Key differentiator** — what makes them "different" in their own words
- **Who they're targeting** — beginner / pro / B2B / B2C / age / geography
- **What pain they address**

*Insight: what positioning angle are they owning?*

---

### 3. Offer & Pricing
What are they selling and for how much?

- **Products / services list** — what's available
- **Price points** — free / entry / mid / premium tiers
- **Bonuses, guarantees, trial offers**
- **Sales mechanism** — direct / funnel / community / consultative

*Insight: where is the price gap or underserved tier?*

---

### 4. Content & Distribution
How do they attract and retain audience?

- **Content formats** — posts, videos, podcasts, carousels, newsletters
- **Posting frequency** — how often per platform
- **Top-performing content** — themes that get most engagement (if visible)
- **SEO / keywords** — what topics they rank for (if relevant)
- **Hook patterns** — how they open content

*Insight: what content angle are they NOT covering?*

---

### 5. Audience & Community
Who follows them and how engaged are they?

- **Audience size per channel**
- **Engagement quality** — comments, saves, shares vs. just likes
- **Community format** — Telegram, Discord, closed group, none
- **Audience sentiment** — what people say in comments (praise / complaints)

*Insight: what does the audience want that they're not getting?*

---

### 6. Strengths & Weaknesses
Honest assessment.

**Strengths:**
- What they do better than most
- Where they have clear competitive advantage

**Weaknesses:**
- Where they're weak, slow, or inconsistent
- Common complaints from their audience
- Gaps in content, offer, or service

---

### 7. Opportunities for You
Based on the analysis — where can YOU win?

- **Positioning gap** — angle they're not owning
- **Content gap** — topics or formats they're ignoring
- **Audience gap** — segment they're underserving
- **Offer gap** — price point or format that's missing
- **Channel gap** — platform where they're weak or absent

---

### 8. So What — Action List
3–5 concrete next steps based on this analysis.

Format:
```
→ [Action] because [finding from analysis]
```

Example:
```
→ Create beginner-focused content because competitor talks only to advanced users
→ Add a low-ticket entry offer at $49 because their cheapest is $300
→ Start a Telegram community because they have no community layer
```

---

## Research Sources

Use web search to find:
- Competitor's website, landing pages, about page
- Social media profiles (Instagram, YouTube, Telegram, LinkedIn)
- Pricing pages or course platforms (Gumroad, Teachable, GetCourse, Boosty)
- Reviews and comments (Google, App Store, social media comments)
- SEO tools data if available (search volume, keywords)

If data is unavailable — mark it as "not found / unclear" rather than guessing.

---

## Output Format

Single structured report with:
- All 8 sections with headers
- Each section ends with an *Insight* line
- Action list at the end
- Copy button for the full report

For multiple competitors — produce one section at a time per competitor,
then a final comparison table: who wins on each dimension.

---

## Comparison Table (multiple competitors)

| Dimension | Competitor A | Competitor B | Competitor C |
|-----------|-------------|-------------|-------------|
| Positioning | | | |
| Price range | | | |
| Content strength | | | |
| Audience size | | | |
| Community | | | |
| Main weakness | | | |
| Your opportunity | | | |

---

## Example Prompts That Trigger This Skill

- "Разбери @alice.merash как конкурента"
- "Проанализируй рынок онлайн-школ по Claude"
- "Кто мои конкуренты если я продаю AI-курсы для маркетологов?"
- "Сравни Skillbox и Нетологию по контент-стратегии"
- "Что делает [бренд] лучше меня и где я могу выиграть?"

<!-- INDEX_V2: 21.04.2026 -->
