# launcher/AGENTS.md (Readable Home)

The root [AGENTS.md](../AGENTS.md) applies here too. This file adds the rules of Readable Home, this fork's
restyle of the launcher; [docs/readable-home/README.md](../docs/readable-home/README.md) explains each one.

## Code Review Rules

Flag a change to `launcher/` that breaks any of these:

- **Type:** Inter only, through the `font_*` strings in `res/values/fonts.xml`, never a font file or family
  named in a layout or in code. Text sizes come from `res/values/type.xml` (13, 15, 17, 20 and 22sp); only the
  clock and page titles use a display size. No letter spacing anywhere, and names in sentence case.
- **Spacing:** margins and padding are multiples of 8dp (4dp only inside a control). Corners are concentric:
  an outer radius is the inner radius plus the gap between them.
- **1 GB TVs:** no work on the main thread that grows with the number of apps or pixels (decode, scan, grain):
  move it off the main thread or do it once and cache it. No new views on the focus path, no blur, no
  per-frame allocation, no bitmap larger than it is shown.
- **Behaviour:** anything new is off by default, behind `config.xml` or a theme key. D-pad focus must work
  from every edge, and Back must always lead somewhere.
- **Screenshots:** a visual change needs a screenshot from a real TV, with the Wi-Fi name painted over.
