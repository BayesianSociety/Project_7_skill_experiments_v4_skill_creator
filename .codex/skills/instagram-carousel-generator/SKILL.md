---
name: instagram-carousel-generator
description: Create a 7-slide Instagram carousel from research, notes, reports, or findings, then turn each slide into a production-ready AI image prompt and generate the final square images. Use this skill whenever the user wants Instagram posts, carousel slides, social-media visuals, or wants to turn research into image-led content, even if they only mention "make visuals" or "turn this into an Instagram post."
compatibility:
  tools:
    - Read
    - Write
  skills:
    - imagegen
---

# Instagram Carousel Generator

Use this skill to transform research into a coherent 7-slide Instagram carousel that is visually consistent, concise, and ready for image generation.

The goal is not just to summarize information. The goal is to create a sequence of slides that works as social content:

- easy to scan,
- visually coherent,
- accurate to the source material,
- strong enough that each slide earns its place.

## When to use this skill

Use this skill when the user wants to:

- turn research, findings, or notes into an Instagram carousel,
- create social-media slides from an article, report, memo, or analysis,
- generate square Instagram visuals with a shared style,
- produce both slide copy and image prompts,
- create final images for a carousel rather than stopping at copy only.

Do not use this skill for long-form articles, slide decks, or generic graphic design requests that are not specifically about an Instagram-style carousel.

## Inputs

Expect one or more of:

- raw research text,
- a summary of findings,
- a file containing notes or research,
- brand or style preferences,
- audience and tone guidance.

If the user gives limited style direction, choose a clean modern visual system that feels Instagram-native and stays consistent across all 7 slides.

## Core rules

1. Stay faithful to the research. Do not invent claims, metrics, or conclusions that are not supported by the input.
2. Write for visual consumption, not report reading. Each slide should feel crisp and legible.
3. Keep the carousel structurally coherent. The slides should tell one story, not feel like 7 unrelated facts.
4. Keep text minimal. The image and headline should do most of the work.
5. Maintain one visual language across all slides unless the user explicitly wants varied styles.

## Workflow

### Step 1: Understand the material

Read the research and extract:

- the main thesis,
- the 5 to 7 most useful supporting points,
- any concrete data worth featuring,
- the intended audience if it can be inferred,
- the tone that best matches the topic.

If the material is too thin to support 7 slides, say so and either:

- recommend a shorter carousel, or
- expand carefully by turning one strong finding into multiple angles without inventing new substance.

### Step 2: Build the 7-slide story arc

Create exactly 7 slides unless the user asks otherwise.

Use a narrative arc like this:

1. Hook
2. Problem or context
3. Key finding
4. Supporting insight
5. Supporting insight
6. Implication or takeaway
7. Closing slide or CTA

Adjust the arc when the content demands it, but keep the sequence intentional.

## Slide format

Draft each slide with:

- `Headline:` maximum 8 words
- `Supporting text:` maximum 20 words
- `Visual suggestion:` one sentence describing what the image should show

The supporting text should be natural, sharp, and non-repetitive. Avoid stuffing every slide with jargon.

## Writing guidance

- Prefer concrete language over abstract phrasing.
- Make each headline distinct.
- Avoid repeating the same sentence pattern on every slide.
- If the research includes numbers, use only the most meaningful ones.
- If the topic is complex, simplify without flattening the truth.

## Step 3: Convert slides into image prompts

For each slide, write one detailed image-generation prompt that includes:

- the subject of the slide,
- the intended composition,
- the mood and tone,
- the color treatment,
- the visual style,
- the requirement for a 1:1 Instagram-friendly composition,
- any text treatment only if text is necessary inside the image.

The prompts should be detailed enough for high-quality image generation while preserving a shared visual identity across the whole carousel.

### Style defaults

Unless the user specifies otherwise, use:

- modern,
- minimal,
- polished,
- editorial,
- Instagram-friendly,
- square 1:1 composition,
- strong focal point,
- clean spacing,
- restrained color palette.

Keep prompts visually specific. "Modern and nice" is too vague to be useful.

LAYOUT RULES - you must stick to this:
- All text must stay within a central safe area with at least 12–15% padding from every edge
- No text touching or approaching the borders
- Avoid placing any important content near the top or bottom edges
- Ensure all text is fully visible and not cropped
- Use a balanced, centered composition with generous margins
- Design as if it will be viewed on mobile with UI overlays (safe area enforced)

TEXT HANDLING:
- Keep typography large but contained within the safe area
- Use line breaks if needed to avoid horizontal overflow
- Do not stretch text across the full width
- Prioritize readability over filling space

CONTRAST RULES - you must stick to this:
- Use high contrast between text and background (minimum WCAG-style contrast, dark-on-light or light-on-dark)
- Main headline text must be clearly legible at a glance
- Do NOT use low-contrast, washed-out, or pastel-on-pastel combinations
- Avoid placing text over busy shapes or gradients unless a solid overlay is added
- If text overlaps graphics, add a dark or light backing layer to maintain readability
- Ensure text opacity is 100% (no faded or transparent text)
- Background and text must have strong separation in brightness and color

VISUAL CLARITY:
- Prioritize readability over aesthetic subtlety
- Use bold, high-contrast typography for key messages
- Ensure accessibility-level contrast (clear even on mobile screens)

## Step 4: Generate the actual images

If the `imagegen` skill is available, use it to create the images after the prompts are drafted.

Generate one image per slide and save them with stable names such as:

- `slide-01.png`
- `slide-02.png`
- `slide-03.png`
- `slide-04.png`
- `slide-05.png`
- `slide-06.png`
- `slide-07.png`

If image generation is unavailable, still provide the finished prompts and say that image generation could not be completed in the current environment.

## Output format

Place all the newly generated pictures in this repo in a top folder called imagegen and subfolder named after the name of the analysed subject.
Present the result in this order:

### Carousel summary

- one short sentence on the overall concept,
- one short sentence on the chosen visual direction.

### Slides

For each of the 7 slides, use this exact structure:

`Slide N`
`Headline: ...`
`Supporting text: ...`
`Visual suggestion: ...`
`Image prompt: ...`

### Assets

List the generated image filenames or planned filenames.

## Quality bar

Before finalizing, check:

- Does slide 1 create curiosity?
- Does each slide add something new?
- Is the language short enough for Instagram?
- Do the visuals feel like one set?
- Would a human designer understand what to make from the prompt?

If the answer to any of these is no, revise before finishing.

## Example

**Input:** Turn a short market-research summary about EV charging growth into an Instagram carousel.

**Output shape:**

- 7 slides with concise copy
- 7 visual suggestions
- 7 detailed image prompts
- generated square images via `imagegen`
