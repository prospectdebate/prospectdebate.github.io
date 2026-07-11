# Prospect Parliamentary Debate

Website for the parliamentary debate team at Prospect High School (Saratoga, CA).
Live at **https://prospectdebate.github.io**.

Static site — plain HTML, one shared stylesheet, one shared script. No build
step, no framework, no dependencies. It's hosted with GitHub Pages straight from
the repo root on the `main` branch.

## Pages

| File            | Purpose                                                              |
| --------------- | ------------------------------------------------------------------- |
| `index.html`    | Landing page. Visual-first hero with the shard-assembly centerpiece. |
| `about.html`    | "The Program" — what parliamentary debate is and how a round works. |
| `calendar.html` | "The Calendar" — this season's tournaments, filterable, with editable per-tournament notes saved to the browser. |
| `record.html`   | **Shelved / unlinked.** Team history & results. Kept on disk but not linked from any nav; can be brought back later. |
| `history.html`  | Legacy redirect stub → currently points at `record.html`.           |

## Structure

```
index.html, about.html, calendar.html   Live pages
record.html                             Shelved (unlinked)
history.html                            Redirect stub
assets/
  site.css                              All styles (design tokens + every section)
  site.js                               All behavior (feature-detected per page)
  video/                                Scroll-scrubbed hero animation + source
    panther-shards.mp4                    Seek-optimized 4-second web render
    panther-shards.blend                  Reproducible Blender scene
    panther-*-preview.png                 Animation review frames
  images/                               Web-optimized images used by the site
    panther-hero.jpg                      Previous hero source image
    gold-fracture.jpg, chamber.jpg        Section backgrounds
    team/                                 Team photos (about.html gallery)
  references/                           Original AI reference images (not shipped to pages)
copy/
  brand-kit.md                          Brand guidelines: colors, type, voice, logo
images/                                 Original (non-optimized) source images + favicon (panther.png)
tools/render_panther.py                 Procedural Blender render script
```

> **Image paths:** `assets/site.css` references images relative to the `assets/`
> folder (e.g. `url("images/panther-hero.jpg")` resolves to
> `assets/images/panther-hero.jpg`). The top-level `images/` folder holds the
> original source files and the favicon.

## Design

- **Palette:** noir + gold. Defined as CSS custom properties at the top of
  `assets/site.css` (`--ink`, `--navy`, `--gold`, `--bone`, etc.).
- **Type:** Big Shoulders Display (headings), Inter (body), Space Mono (labels),
  loaded from Google Fonts.
- **Logo:** faceted gold panther. A small gold pentagon (CSS `clip-path`) stands
  in for the mark in the nav.
- Full brand rationale lives in [`copy/brand-kit.md`](copy/brand-kit.md).

### The connected assembly hero

The landing hero uses a four-second Blender render whose time is tied directly
to hero scroll progress. A single 724-node, 1,371-edge lattice contracts without
changing topology: dispersed constellation → panther wireframe → closing
faceted shell → solid gold panther. There is no completed panther underneath the
animation. The H.264 file is encoded with every frame as a keyframe so forward
and reverse seeking remain responsive. Reduced-motion mode skips the scroll
runway and uses the completed-frame poster.

The authored scene is stored in `assets/video/panther-shards.blend`; its
procedural source is `tools/render_panther.py`.

### Other behavior (`assets/site.js`)

Everything is guarded by element checks, so the single script is safe to include
on every page:

- Dynamic copyright year, scrolled-nav state, mobile hamburger menu.
- Scroll-scrubbed hero video + the corner "prep clock" that counts 20:00 → 00:00 with scroll.
- Word-by-word statement reveal (used where a `#statement` element exists).
- `IntersectionObserver` fade-up for `.reveal` elements.
- Calendar: search + month/location filters, and `contenteditable` notes
  persisted to `localStorage` (`prospect-calendar-notes`).

## Developing locally

No tooling required. Serve the folder over HTTP (relative asset paths won't work
from `file://` in every browser):

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Edit the HTML/CSS/JS directly and refresh.

## Deploying

GitHub Pages serves the repo root on `main`. Merging to `main` publishes to the
live site — a branch push alone does not. There is no build step.

## TODO / follow-ups

- Replace the placeholder Join email `prospectparli@gmail.com` with the real
  contact address (appears in the Join CTAs on all three pages).
- Decide `history.html`'s target now that `record.html` is shelved (repoint to
  the homepage, or leave until The Record returns).
- Fill in real voice/content once the MVP shell is locked (current copy is
  intentionally minimal placeholder).
