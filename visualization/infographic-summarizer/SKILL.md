---
name: infographic-summarizer
description: Convert dense reports into single-page infographics with visual hierarchy, key-stat callouts, and a limited colour palette. Trigger when summarising a long document, briefing report, or survey for a one-page visual.
metadata:
  author: Hossam Magdy Balaha
  version: "1.0"
  theme: visualization
tags: [infographic, summary, design, hierarchy, callouts]
related: [visualization/scientific-poster-designer, visualization/dashboard-builder]
prerequisites: []
outputs: [html, svg, pdf]
difficulty: intermediate
estimated_tokens: 950
permissions:
  read_files: true
  write_files: true
  network: false
  execute_code: true
language: en
---

# Infographic Summarizer

## When To Use
- Compressing a multi-page report into a single-page visual summary.
- Producing a briefing slide for executives or stakeholders.
- Highlighting three to five key statistics from a dataset.
- Building a shareable HTML or PNG infographic for social media.

## Workflow
1. Read the source report and extract the headline message.
2. Pull out three to five key statistics that anchor the message.
3. Choose a layout: title block, key-stat row, and detail columns.
4. Select icons for each section from a consistent icon set.
5. Restrict the colour palette to three or four colours total.
6. Render as HTML/CSS and snapshot via Playwright to PNG or PDF.
7. Review readability at the intended display size and iterate.

## Inputs
- Source document (markdown, HTML, or plain text).
- Optional key statistics already chosen by the author.
- Brand palette and an icon set (for example, an open-licence emoji set).

## Outputs
- A standalone HTML infographic.
- A PNG snapshot rendered by Playwright.
- A print-friendly PDF when requested.

## Key Rules
- Establish visual hierarchy: title, key stats, then details.
- Limit the palette to three or four colours.
- Every section is paired with an icon for fast scanning.
- Key statistics are large numerals with short captions.
- Text is sparse; visuals carry the message.
- One page only; if it overflows, cut content, do not shrink fonts.

## Examples
```python
# Render an HTML infographic to PNG via Playwright.
from playwright.sync_api import sync_playwright

def BuildHtml(title, stats, details):
  # Assemble an HTML string with a strict four-colour palette.
  palette = ["#1f3a5f", "#2e86ab", "#a8d0e6", "#f6c89f"]
  statCards = ""
  for (i, s) in enumerate(stats):
    color = palette[i % len(palette)]
    statCards += (
      f'<div class="stat" style="color:{color}">'
      f'<div class="number">{s["Value"]}</div>'
      f'<div class="label">{s["Label"]}</div></div>'
    )
  html = f"""
  <html><head><style>
    body {{ font-family: 'Noto Sans SC', 'DejaVu Sans', sans-serif; }}
    .title {{ font-size: 56px; font-weight: 800; color: {palette[0]}; }}
    .row {{ display: flex; gap: 24px; }}
    .stat {{ flex: 1; text-align: center; }}
    .number {{ font-size: 72px; font-weight: 900; }}
    .label {{ font-size: 20px; color: #444; }}
  </style></head><body>
    <div class="title">{title}</div>
    <div class="row">{statCards}</div>
    <div class="details">{details}</div>
  </body></html>
  """
  return html

def SnapshotInfographic(htmlPath, pngPath):
  # Headless render at a fixed viewport then snapshot.
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1240, "height": 1754})
    page.goto("file://" + htmlPath)
    page.screenshot(path=pngPath, full_page=True)
    browser.close()
```

## References
- Playwright Python docs: https://playwright.dev/python/
- Canva infographic layouts: https://www.canva.com/infographics/templates/
