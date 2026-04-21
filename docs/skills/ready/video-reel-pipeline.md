---
name:  video-reel-pipeline
description: >
  Transform a creative concept into ready-to-generate video prompts for AI video tools
  (Kling, Higgsfield, Veo 3, Runway, Pika, etc.).
  Use this skill when the user says "сделай видео промпт", "промпт для Kling",
  "промпт для Higgsfield", "сними сцену", "сделай Reel", "напиши сцены для видео",
  or describes a video concept, mood, or shot they want to generate.
  Always use this skill for video prompt requests — it handles scene structure,
  motion language, shot-specific limits, and anti-artifact rules automatically.
---

# Video Reel Pipeline Skill

Converts a creative concept into structured, ready-to-paste video prompts.
Output is bilingual (EN + RU), organized by scene, with motion language,
camera direction, and tool-specific formatting built in.

---

## Workflow

1. **Get the concept** — theme, mood, character, setting from the user
2. **Determine scene count** — infer from the request:
   - Single idea / "одна сцена" → 1 prompt
   - "Reel", "ролик", "видео" without further detail → ask: "Сколько сцен? Или сделать 3–5?"
   - Explicit count → generate exactly that many
3. **Clarify tool if needed** — Kling, Higgsfield, Veo 3, or universal
4. **Write scene prompts** — one prompt per scene, EN first
5. **Translate to RU** — fluent Russian equivalent
6. **Output scene cards** — each scene in its own card with copy buttons
7. **Add editing note** — suggest scene order and pacing for CapCut/edit

---

## Prompt Structure (per scene)

Each scene prompt must include all of these elements:

```
[IDENTITY BLOCK] —
[ACTION / MOTION] — what is happening, how the character moves
[SETTING] — location, time of day, atmosphere
[WARDROBE] — outfit details relevant to the scene
[CAMERA] — shot type, angle, movement
[MOOD / LIGHT] — emotional tone, lighting source
[TECHNICAL TAGS]
```

---

## Motion Language

Video prompts need explicit motion. Always describe:
- **Character motion** — walking, turning, reaching, hair movement, etc.
- **Camera motion** — tracking shot, slow push-in, orbit, static, handheld drift
- **Environmental motion** — wind, crowd, traffic, light flicker, etc.

Avoid vague words like "dynamic", "cinematic movement" — be specific:
- ✓ "camera slowly pushes in from medium to close-up"
- ✗ "cinematic dynamic shot"
- ✓ "subject turns toward camera with a slight smile"
- ✗ "beautiful motion"

---

## Technical Tags by Tool

### Universal (no tool specified)
```
photorealistic, no CGI, no AI artifacts, smooth natural motion,
no slow motion, no fisheye distortion, no vignette,
IMPORTANT: preserve face identity, consistent character look
```

### Kling
- Max prompt length: ~400 characters — keep it tight
- No negative prompt field — bake anti-artifact language into the prompt
- Emphasize motion over description
- Add at end: `| 1080p | 16:9` or `| 9:16` for Reels

### Higgsfield (Nano Banana)
- Supports longer prompts — up to ~600 characters
- Motion style is key — describe the feel: "handheld", "tracking", "locked off"
- Works well with style references in prompt: "editorial fashion film"
- Add at end: `photorealistic, editorial, no artifacts`

### Veo 3
- Supports audio cues — add ambient sound description
- Describe camera as a cinematographer would: "35mm handheld, shallow depth"
- Can handle complex multi-element scenes
- Add: `filmed on location, natural sound, no CGI`

### Runway / Pika
- Short prompts work better — under 300 characters
- Focus on single dominant motion
- Avoid complex compositions

---

## Anti-Artifact Rules for Video

**Never use:**
- slow motion / slo-mo (unless explicitly requested)
- fisheye lens / wide-angle distortion
- heavy vignette
- dust / film burn / light leak overlays (unless intentional)
- zoom transitions
- "dramatic", "epic", "stunning" — describe instead

**Always include:**
- explicit camera movement (even "static locked-off shot" counts)
- character motion description
- "no CGI", "no AI artifacts", "photorealistic"
- face identity preservation tag

---

## Output Format

One card per scene. Each card contains:
- Scene number + title
- **Prompt EN** with copy button
- **Prompt RU** with copy button
- Character limit indicator (for tool-specific versions)

After all scenes — a short **editing note**: suggested order, pacing, transition type.

---

## Tool-Specific Prompt Length Limits

| Tool | Max chars | Notes |
|------|-----------|-------|
| Kling | ~400 | Tight — cut description, keep motion |
| Higgsfield | ~600 | More room for style and atmosphere |
| Veo 3 | ~800 | Full cinematographer language |
| Runway | ~300 | One motion, one subject |
| Universal | no limit | Full version, user adapts |

---

## Example — 3-scene Reel (fashion, urban night)

**Scene 1 — Arrival**
```
[CHARACTER], slim build, wearing a black leather jacket and wide-leg trousers —
stepping out of a taxi onto a rain-wet street in Shibuya at night,
looking up at neon signs, slight smile.
Camera: static low-angle shot, eye level rises as she stands.
Neon reflections on wet pavement, ambient city sound.
Photorealistic, no CGI, no slow motion, no fisheye.
IMPORTANT: preserve face identity, consistent character look. | 9:16
```

**Scene 2 — Walk**
```
[CHARACTER], same outfit —
walking confidently through a crowd on a busy crossing,
people blurred in background, she moves in focus.
Camera: tracking shot from front, slight handheld drift, medium shot.
Overcast neon-lit night, cool blue and pink tones.
Photorealistic, no CGI, smooth natural motion, no fisheye.
IMPORTANT: preserve face identity, consistent character look. | 9:16
```

**Scene 3 — Close-up**
```
[CHARACTER] —
stops and turns slightly toward camera, brushes hair back with one hand,
direct confident gaze into lens.
Camera: slow push-in from medium to close-up, locked off then drifts slightly.
Neon bokeh background, warm highlight on face.
Photorealistic, no CGI, no slow motion.
IMPORTANT: preserve face identity, sharp facial features. | 9:16
```

**Editing note:** Cut scene 1 → 2 → 3 on beat. Scene 1: 3–4 sec. Scene 2: 4–5 sec. Scene 3: 3 sec hold on gaze, fade out. Total ~12 sec Reel.

<!-- INDEX_V2: 21.04.2026 -->
