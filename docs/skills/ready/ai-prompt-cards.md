---
name:  ai-prompt-cards
description: >
  Generate structured AI image/video prompt cards for any character or creative direction.
  Use this skill whenever the user asks to create, write, or format prompts for AI generation tools
  (Midjourney, Kling, Higgsfield, ComfyUI, Veo, Stable Diffusion, DALL-E, etc.).
  Also trigger when the user says "сделай промпт", "напиши карточку", "промпт для", "нужен промпт",
  "придумай сцену", or describes a visual concept they want to generate.
  Always use this skill — even for quick single prompts — to ensure consistent format,
  bilingual output, and identity anchoring.
---

# AI Prompt Cards Skill

Generates professional, ready-to-use prompt cards for AI image and video generation.
Each card is bilingual (EN + RU), includes a character identity anchor block,
anti-artifact language, and a copy button for each section.

---

## Workflow

1. **Get the concept** — theme, mood, setting from the user
2. **Build identity block** — ask for character description or extract from reference image
3. **Clarify aesthetic** — ask about the visual style if not specified:
   > "Какая эстетика? Плёнка / чистый цифровой / студия / другое?"
4. **Write EN prompt** — scene + wardrobe + camera + mood
5. **Translate to RU** — fluent natural Russian, not word-for-word
6. **Append technical tags** — based on chosen aesthetic, photo or video
7. **Output card widget** — with copy buttons per section
8. **Offer iteration** — suggest changing angle, light, outfit, or mood

---

## Card Structure

### 1. Identity Block (anchor)
Always placed at the TOP of the prompt. Keeps the model from drifting the character's appearance.

Format:
```
[NAME], [age range], [ethnicity/skin tone], [hair: color, length, texture],
[eyes: color, shape], [distinctive features if any], [body type if relevant]
```

If the user hasn't provided character details — ask before writing:
> "Опиши персонажа: возраст, внешность, волосы, глаза — или скинь референс."

Never invent character details. Always confirm with the user first.

### 2. Scene / Shot Prompt
Must include:
- **Setting** — location, time of day, atmosphere
- **Action / pose** — what the character is doing
- **Wardrobe** — outfit details
- **Camera** — angle, lens type, shot distance
- **Mood** — emotional tone, color palette

### 3. Technical Tags

Choose based on the aesthetic the user specifies. If not specified — ask.

**Film (плёнка):**
```
shot on 35mm film, Kodak Portra 400, natural grain, soft halation,
no CGI, no AI artifacts, photorealistic, editorial photography
```

**Clean digital / studio (чистый цифровой, цикlorама, студия):**
```
shot on Phase One IQ4, clean sharp image, no grain, no film artifacts,
soft studio lighting, seamless backdrop, no CGI, photorealistic, editorial photography
```

**Cinematic video (кино, видео):**
```
shot on 16mm film, Kodak Vision3 500T, natural film grain, cinematic motion,
no CGI, no slow motion, no fisheye distortion, no vignette, no dust overlay,
photorealistic, handheld feel
```

**Clean digital video:**
```
shot on Sony FX6, clean sharp image, no grain, smooth cinematic motion,
no fisheye distortion, no vignette, no CGI, photorealistic
```

**Face priority — always last line regardless of aesthetic:**
```
IMPORTANT: preserve face identity, sharp facial features, consistent character look
```

---

## Output Format

Widget with clearly separated sections and individual copy buttons:

- **Identity Block** — 📋 copy button
- **Prompt EN** — 📋 copy button
- **Prompt RU** — 📋 copy button
- **Technical Tags** — 📋 copy button

RU version = fluent Russian equivalent, naturally adapted, not literal translation.

---

## Character Management

- First use: ask for description or reference image
- "Тот же персонаж" / "same character" → reuse identity block without asking
- Reference image provided → extract descriptors, propose identity block for confirmation

---

## Tool-Specific Adjustments

| Tool | Adjustments |
|------|-------------|
| **Midjourney** | Add `--ar 4:5` or `--ar 9:16`, `--style raw`, `--v 6.1` |
| **Kling / Higgsfield** | Under 400 chars; strip tech params; emphasize motion |
| **ComfyUI** | Output negative prompt block separately |
| **Veo 3** | Emphasize motion, camera movement, audio cues |
| **DALL-E** | Remove film grain tags; add "ultra detailed, 8k" |

No tool specified → universal version, no tool-specific params.

---

## Anti-Artifact Rules

**Avoid:**
- "beautiful", "perfect", "flawless" → uncanny valley
- "ultra realistic" alone → use "photorealistic editorial"
- "dramatic lighting" alone → specify source: "golden hour side light"

**Avoid in video:**
- slow motion / slo-mo
- fisheye lens
- heavy vignette
- dust / film burn overlays (unless intentional)
- zoom transitions

---

## Example

**Theme:** Street fashion, Tokyo, night

**Identity Block:**
```
Mia, 20–24 y.o., Japanese-Korean appearance, short black bob with blunt fringe,
dark almond-shaped eyes, sharp cheekbones, slim build
```

**Prompt EN:**
```
Mia, 20–24 y.o., Japanese-Korean appearance, short black bob with blunt fringe,
dark almond-shaped eyes, sharp cheekbones, slim build —
walking through a rain-slicked street in Shinjuku at night, wearing an oversized
white trench coat and chunky black boots, neon reflections on wet pavement,
confident stride, slight gaze toward camera.
3/4 angle, 35mm lens, medium full shot. Cool blue and magenta neon tones.
Shot on 35mm film, Kodak Portra 400, natural grain, no CGI, no AI artifacts,
photorealistic, editorial photography.
IMPORTANT: preserve face identity, sharp facial features, consistent character look.
```

**Prompt RU:**
```
Миа, 20–24 года, японско-корейская внешность, короткое чёрное каре с прямой чёлкой,
тёмные миндалевидные глаза, выразительные скулы, стройное телосложение —
идёт по мокрой улице в Синдзюку ночью, в оверсайз белом тренче и грубых чёрных
ботинках, отражения неона в лужах, уверенная походка, лёгкий взгляд в камеру.
Угол 3/4, объектив 35 мм, средний план в полный рост. Холодные сине-пурпурные неоновые тона.
Съёмка на 35-мм плёнку, Kodak Portra 400, натуральное зерно, без CGI, без артефактов,
фотореалистично, эдиториал-фотография.
ВАЖНО: сохранить идентичность лица, чёткие черты, единообразный образ персонажа.
```

<!-- INDEX_V2: 21.04.2026 -->
