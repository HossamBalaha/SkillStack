---
name: scientific-poster-designer
description: Design A0 scientific posters with IMRAD layout and one-metre readability. Trigger when preparing a conference poster, defence poster, or summary poster for a workshop.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [poster, a0, imrad, conference, readability]
related: [visualization/infographic-summarizer, visualization/multi-panel-figure-composer]
prerequisites: []
outputs: [latex, pdf]
difficulty: advanced
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: false
language: en
---

# Scientific Poster Designer

## When To Use
- Producing a conference poster for A0 print (841x1189 mm).
- Creating a portrait or landscape defence poster.
- Summarising a paper visually for a workshop or hallway display.
- Generating a QR code that links to the manuscript or code repository.
- Adapting an existing poster to a new venue's size requirements.

## Workflow
1. Decide orientation (portrait or landscape) and the A0 dimensions in millimetres.
2. Lay out the IMRAD columns: Intro, Methods, Results, Conclusions.
3. Place title and authors across the top banner.
4. Set body font to a minimum of 24 pt for one-metre readability.
5. Scale the title to roughly 85 pt with a colour-coded band beneath.
6. Insert figures and tables; minimise prose so visuals carry the message.
7. Add a QR code in a fixed corner linking to the paper or code.
8. Export a press-ready PDF/X-1a with embedded fonts and bleed.
9. Print a small-scale proof to catch font and overflow issues early.

## Inputs
- Title, author list, affiliations, and the paper's main figures.
- Section text (Intro, Methods, Results, Conclusions) trimmed to poster length.
- A QR target URL and a colour palette aligned with the institution brand.

## Outputs
- A single A0 PDF (portrait or landscape) ready for print.
- A PNG thumbnail for web promotion.
- A `poster.tex` source file (Beamerposter or TikZ) for future edits.

## Key Rules
- Minimum body font is 24 pt; title is approximately 85 pt.
- IMRAD columns must be readable from one metre away.
- Colour-code each section header consistently.
- QR code must be at least 2 cm square and lead to a stable URL.
- Visuals dominate; prose is supporting and trimmed to essentials.
- Embed all fonts and include bleed in the exported PDF.

## Examples
```python
# Compute A0 dimensions and recommend font sizes.
def PosterSpecs(orientation):
  # A0 dimensions in millimetres per ISO 216.
  widthMm = 841
  heightMm = 1189
  if (orientation == "landscape"):
    widthMm, heightMm = heightMm, widthMm
  # Recommended font sizes for one-metre viewing.
  specs = {
    "Title": 85,
    "Section": 36,
    "Body": 24,
    "Caption": 18
  }
  return {
    "WidthMm": widthMm,
    "HeightMm": heightMm,
    "FontSizes": specs
  }

# Convert millimetres to inches for matplotlib or TikZ scaling.
ONE_MM = 1 / 25.4.
poster = PosterSpecs("portrait")
widthIn = poster["WidthMm"] * ONE_MM
heightIn = poster["HeightMm"] * ONE_MM

# Validate that QR code and section headers meet readability rules.
def ValidatePoster(specs, qrSizeMm):
  # Body text must stay legible from one metre away.
  if (specs["FontSizes"]["Body"] < 24):
    raise ValueError("Body font below 24 pt is not one-metre readable.")
  # QR code must scan reliably from arm's length.
  if (qrSizeMm < 20):
    raise ValueError("QR code smaller than 2 cm may not scan at distance.")
  return True
```

## References
- PosterPresentation templates: https://www.posterpresentations.com/free-poster-templates.html
- SciFig A0 templates: https://scifig.ai/scientific-poster-templates/a0
