# Assets

Four English deliverables, all rendered from one headless-Chromium source (`scripts/generate-references.py`):

| File | Size | Content |
|------|------|---------|
| `screenshots/en/screenshot-1-browser.png` | 1280x800 | Full-window mockup of the themed browser |
| `screenshots/en/screenshot-2-introduction.png` | 1280x800 | Theme intro with the 2x2 colour cards |
| `promo/440x280.png` | 440x280 | Brand tile |
| `promo/1400x560.png` | 1400x560 | Marquee with a scaled window preview |

## Calibration

The window mockup is authored in the pixel space of real maximized Chrome (1080x675) and rasterised at a matching device scale factor, so the 1280x800 store shot stays crisp instead of being upscaled. Theme-controlled surfaces (frame, toolbar, active tab, bookmark bar, omnibox, new tab page, text, links) are read from `manifest.json` at render time.

Elements Chrome paints itself are literals, because this is a dark palette and Chrome decides them:

| Element | Value | Note |
|---|---|---|
| Google mark on the new tab page | `#A9C4E8` | `ntp_logo_alternate` makes Chrome paint the mark in a single tint derived from the new-tab background; this is a light blue matching the eclipse-navy page and should be confirmed against a real install |
| New tab search pill | `#303134` | Google's dark search surface, not a theme colour |
| Search placeholder, shortcut labels, Gmail / Images | `#9AA0A6` | Chrome's standard dark-surface tone |
| New tab shortcut circles | `#2F3033` | Rendered by the page, not the theme |
| `Customize Chrome` pill | `#202124` / `#A8C7FA` | Rendered by the page, not the theme |
| Focused omnibox outline | `#8CA0CC` | Chrome's own outline on the dark toolbar |
| Window glyphs | `#D9D9DE` | Light glyphs on the indigo frame |

## Logo

`logo/logo128.png` is exported at 128px from the chosen concept in `store-assets/icon-candidates/` (`logo-06-starry.png`): a star-flecked night sky inside a rounded square, with a glowing eclipse disc at the centre. A Chrome theme ships exactly one icon size, so `manifest.json` references only the 128px file.

## Regenerating

    python3 scripts/generate-logo.py             # re-draws the candidate sheet
    python3 scripts/generate-store-assets.py     # screenshots + promo tiles

The composer renders all four assets in one pass; change the styling in the script and re-run instead of editing a PNG.
