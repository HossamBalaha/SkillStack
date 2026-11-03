---
name: infographic-crafter
description: Craft single-takeaway infographics with deliberate visual hierarchy, a curated icon set, statistics callouts at display size, and a restrained colour palette. Use when the user needs a one-page visual summary of a report, a social-share graphic, or a briefing card for a non-technical audience.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: data-storytelling
tags: [infographic, visual-hierarchy, icons, callouts, single-takeaway]
related: [data-storytelling/metric-translation-writer, data-storytelling/audience-tailor, visualization/infographic-summarizer]
prerequisites: []
outputs: [html, svg, pdf]
difficulty: intermediate
estimated_tokens: 1200
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
last_reviewed: 2026-11-02
verified_against: []
---

# Infographic Crafter

## When To Use

- The user says "summarise this report on one page" or "make me a shareable graphic".
- The audience is non-technical and will not read past the headline numbers.
- A briefing needs to land a single takeaway without scrolling.
- The user wants an SVG or PDF that prints cleanly at A4 and shares on social.
- Trigger keywords: infographic, single takeaway, hierarchy, callout, icon set, palette.

## Workflow

1. Extract the one sentence the reader must remember; that is the single takeaway.
2. Pull three to five key statistics that anchor the takeaway; reject any that do not support it.
3. Choose a layout: title block, key-stat row, and one detail column or icon list.
4. Select icons from a single consistent set; one icon per section, no mixing styles.
5. Restrict the palette to three or four colours: one dark, one accent, one neutral, one alert.
6. Size the key statistic numbers at display size (at least 60 pt) with short captions beneath.
7. Render as HTML/CSS and snapshot to PNG, SVG, or PDF via Playwright or D3-to-SVG.
8. Verify readability at the intended display size; if text shrinks below 14 pt, cut content.
9. Add the source line and the data date at the footer; an unsourced infographic fails.

## Inputs

- A source report or dataset and the headline takeaway.
- Optional preselected key statistics.
- Brand palette or an open-licence icon set (Feather, Material, Phosphor).
- Output format: HTML, SVG, or PDF for print.

## Outputs

- `infographic.html` — standalone HTML, mobile and print friendly.
- `infographic.svg` — vector version for embedding and editing.
- `infographic.pdf` — print-ready PDF when requested.
- `palette.json` — the three or four colours and their roles.
- `takeaway.md` — the single sentence plus the supporting stats.

## Key Rules

- One takeaway per infographic; if there are two, make two infographics.
- Hierarchy is enforced by size first, colour second, weight third.
- Palette is three or four colours total; one is reserved for the alert state.
- Icons come from one set; mixing line and filled icons is forbidden.
- Key statistic numbers are display-sized with captions beneath, never beside.
- Text is sparse; if a reader has to read a paragraph, it is not an infographic.
- The footer names the source and the data date; no exceptions.

## Examples

```python
# Render a single-takeaway infographic to SVG and PDF.
from playwright.sync_api import sync_playwright

PALETTE = {"dark": "#0f3a52", "accent": "#2e86ab",
           "neutral": "#a8d0e6", "alert": "#cf222e"}

def BuildHtml(takeaway, stats, source):
  cards = "".join(
    f'<div class="stat"><div class="num">{s["value"]}</div>'
    f'<div class="cap">{s["caption"]}</div></div>'
    for s in stats
  )
  return f"""
  <html><head><style>
    body {{ font-family: 'Inter', 'DejaVu Sans', sans-serif;
           background: #fff; margin: 0; padding: 48px; }}
    .takeaway {{ font-size: 44px; font-weight: 800; color: {PALETTE["dark"]};
                 max-width: 1000px; }}
    .row {{ display: flex; gap: 32px; margin-top: 40px; }}
    .stat {{ flex: 1; text-align: center; }}
    .num {{ font-size: 84px; font-weight: 900; color: {PALETTE["accent"]}; }}
    .cap {{ font-size: 20px; color: #444; margin-top: 8px; }}
    .footer {{ margin-top: 48px; font-size: 14px; color: #777; }}
  </style></head><body>
    <div class="takeaway">{takeaway}</div>
    <div class="row">{cards}</div>
    <div class="footer">Source: {source}. Rendered {__import__("datetime").date.today()}.</div>
  </body></html>
  """

def Render(htmlPath, pdfPath):
  with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1240, "height": 1754})
    page.goto("file://" + htmlPath)
    page.pdf(path=pdfPath, format="A4", print_background=True)
    b.close()
```
