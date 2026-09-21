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

Elements Chrome paints itself are literals, because this is a dark palette and Chrome decides them. The values below were taken from a real installed-Chrome screenshot of this theme:

| Element | Value | Note |
|---|---|---|
| Google mark on the new tab page | `#E8EAED` | `ntp_logo_alternate` makes Chrome paint the mark in a single light neutral tone derived from the new-tab background; it is not the four-colour brand logo |
| New tab search pill | `#FFFFFF` with dark text `#3C4043` | Chrome renders the search box light on this dark page |
| Plus / mic glyphs in the search pill | `#5F6368` | Chrome's dark-surface tone; the Lens glyph keeps its brand colours |
| Shortcut tiles | `#FFFFFF` (YouTube, Chrome Web Store), `#3C4043` (add shortcut) | The round tiles are rendered by the page, not the theme |
| `Gmail` / `Images` row | `Images` only, `#9AA0A6` | Matches the real new-tab header of the reference install |
| Shortcut labels | `#9AA0A6` | Chrome's standard dark-surface tone |
| Omnibox outline | `#9AA0A6` | Chrome's own outline on the dark toolbar |
| `Customize Chrome` pill | `#202124` / `#A8C7FA` | Rendered by the page, not the theme |
| Window glyphs | `#D9D9DE` | Light glyphs on the indigo frame |

The page backdrop behind `screenshot-2` and the marquee is **`ntp_background` darkened to 35% (`#09090C`)**, not `ntp_background` itself. The dark tone is derived from the theme (so it still feels native) but sits clearly below every swatch — otherwise the `Eclipse Navy` card and the window's own new-tab area would merge into the page. The composer asserts the backdrop never equals a swatch colour.

## Logo

`logo/logo.png` is the single 128px icon a Chrome theme ships, exported from the chosen concept in `store-assets/icon-candidates/` (`logo-06-starry.png`): a star-flecked night sky inside a rounded square, with a glowing eclipse disc at the centre. It lives in its own `logo/` folder so it is easy to find when uploading, and `manifest.json` references only that one file.

## Regenerating

    python3 scripts/generate-logo.py             # re-draws the candidate sheet
    python3 scripts/generate-store-assets.py     # screenshots + promo tiles

The composer renders all four assets in one pass; change the styling in the script and re-run instead of editing a PNG.
