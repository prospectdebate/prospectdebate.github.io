# Session Handoff — Prospect Debate Website Rebuild

> **UPDATE (latest):** The site was restructured from a single long landing
> page into a **4-page site** at the user's request ("move almost everything to
> its own page; the landing should primarily be visually intriguing"). See the
> "Multi-page architecture" section at the bottom — it supersedes the
> single-page description in sections 2 and 4 below. Shared CSS/JS were
> extracted to `assets/site.css` + `assets/site.js`. All four pages verified
> in-browser. Still uncommitted.

## 1. Main goal

Full visual rebuild of the Prospect Debate (Prospect Parliamentary Debate) team
website — a parliamentary debate club at Prospect High School that is
deliberately "rebuilding" its program and reputation. The ask evolved from an
initial generic "premium headphones brand" template into a real project:

- Build a brand identity for **Prospect Debate / Prospect Parliamentary**
  (slogan: **"All we need is 20 minutes."**)
- Generate reference imagery for that identity (a faceted gold panther mark,
  noir/gold visual language)
- Rebuild `index.html` as a premium, scroll-driven, cinematic single-page site
  using that identity, while preserving all real team content (achievements
  history, 35-tournament calendar, team photos)

The site is a **static GitHub Pages site** (`prospectdebate.github.io`) — no
build step, no framework, root-level HTML files.

## 2. Files / sections built or modified

- **`copy/brand-kit.md`** (new) — full brand kit: name, slogan, positioning,
  audience, personality, color palette, typography, logo direction, product
  description ("the product is the program"), key benefits, visual mood,
  website goal, suggested landing sections, and a hero motion brief. Revised
  once already to drop a "glitch/chromatic-aberration" accent concept in favor
  of clean noir + faceted gold (see failed approaches below).
- **`assets/references/`** (new) — three locked AI-generated reference images:
  - `prospect-hero-reference.png` — clean faceted gold panther, noir background
  - `prospect-material-reference.png` — macro shot of a **fractured gold
    panel** (user explicitly preferred this "broken panel" look over a clean
    material shot — keep it)
  - `prospect-workspace-reference.png` — empty noir debate chamber / lectern
- **`assets/images/`** (new) — web-optimized JPGs converted from the
  references for actual site use: `panther-hero.jpg`, `gold-fracture.jpg`,
  `chamber.jpg`
- **`assets/images/team/`** (new) — resized (max 1600px, q78) JPG versions of
  the existing team photos from `images/` (big_team, full_team, medals,
  pen_prep, peninsula, prep, team, team_bonding, tournament) for the new
  "Room" photo gallery section
- **`index.html`** (fully rewritten) — the entire new site. Old version is
  preserved in git history (commit `78c5e47` and earlier) and also backed up
  at `/private/tmp/claude-501/.../scratchpad/index_original_backup.html`
  (session-scratchpad only, **not** persistent — if this handoff is picked up
  in a new environment, rely on git history instead).
- `calendar.html`, `history.html`, `images/` — **untouched**, still the old
  versions. `calendar.html` currently just redirects to `index.html#calendar`
  (from a prior session) which still works since the new site kept the
  `#calendar` section id.

### New `index.html` structure (all in one file, vanilla JS, no build step)

Sections in order: `#top` (hero) → `#rebuild` (statement/narrative) → `#gain`
(6 benefit cards) → `#format` (how a parli round works + animated speech-order
timing bars) → `#record` (stat tiles + full achievements timeline, ported
verbatim from the old site) → `#calendar` (35-tournament table with
search/month/location filters + localStorage-persisted per-row notes) →
`#room` (photo gallery grid) → `#join` (CTA) → footer.

Key JS behaviors implemented (single IIFE at bottom of `index.html`):
- Scroll-driven hero parallax (background zoom + content fade/translate)
- A fixed "prep clock" widget (bottom-right) that counts down from 20:00 to
  00:00 mapped to total page scroll progress, fading in/out near top/bottom
- Word-by-word lit-up reveal for the `#rebuild` statement text, scroll-tied
  (not IntersectionObserver — computed continuously from scroll position)
- Generic `.reveal` fade-up-on-scroll via `IntersectionObserver` (52 elements
  use this class)
- Calendar: live search + month/location dropdown filters (AND logic across
  all three), empty-state message, live count badge; notes are
  `contenteditable` divs saved to `localStorage` under key
  `prospect-calendar-notes` keyed by `data-note-key` per tournament
- Speech-order bars animate their width fill when `.speech-order` enters
  view (reuses `.reveal`/`.in` mechanism)

Brand tokens applied via CSS custom properties (`--ink`, `--navy`, `--blue`,
`--gold`, `--gold-hi`, `--bone`, `--muted`, `--cyan`) and Google Fonts **Big
Shoulders Display** (headings), **Inter** (body), **Space Mono** (mono/labels,
prep clock, speech timings) — all per the brand kit.

**Content preserved from the old site (verbatim, not paraphrased):** the full
achievements timeline (2024–25 back through "~2010" founding era under
Georgiana Hays, including two National Championship appearances, national
POI rankings, TOC appearances, hosted invitationals) and the complete
35-row tournament calendar with real Tabroom links. The old team roster
section was **dropped** — it only had `[Name]` placeholders, no real data —
in favor of the photo-based "Room" section.

## 3. Approaches tried and failed (with reasons)

- **GPT Image 2 via Higgsfield MCP** — failed. Requires a paid ("Basic or
  higher") Higgsfield plan; the account is on the free plan. Confirmed via
  `balance` tool: 10 credits but `subscription_plan_type: "free"` — credits
  alone don't unlock plan-gated models. Rejected up front (no charge).
- **`flux_2` (pro variant) and `recraft_v4_1`** — same plan-gated rejection
  (`403 job_minimum_basic_plan_required`), no charge incurred. Established
  this is a blanket gate on premium image models, not model-specific.
- **`z_image`** — this one **worked** on the free plan (very cheap, ~0.2
  credits/image at 2048×1152) and is what actually generated the three locked
  reference images.
- **muapi.ai (CLI/MCP alternative suggested by user)** — abandoned before
  installing. User pivoted back to Higgsfield once it was confirmed some
  credits/models did work there, making a second tool unnecessary.
- **Cinematic background video (`cinematic_studio_video_v2`, image-to-video)**
  — failed. Cost-preflighted successfully (5s silent = 5 credits, 8s silent =
  8 credits — fits the ~9.4 credit balance), but **actual submission fails at
  execution** (`pending` → `failed`) both times it was tried, unlike the image
  models which reject cleanly up front. This is a free-plan execution gate
  hit *after* job acceptance. Confirmed each failed attempt cost effectively
  nothing (~0.45 credits, likely a preprocessing fee, not a full charge).
  **Conclusion: video generation is not available on the free Higgsfield
  plan**, full stop — no model/param combination got past this. **Decision:
  abandon the generated-video plan entirely; use CSS/JS scroll-driven motion
  on the static hero image instead** (this is what was actually built).
- **"Glitch" / chromatic-aberration accent on the panther mark** — generated,
  then explicitly rejected by the user ("get rid of the glitch seam"). Went
  through a couple of exploratory directions (shard-assembly panther,
  molten-gold edges, blue energy core, clean-no-seam) via `AskUserQuestion`;
  user picked shard-assembly, then later actually preferred the *original*
  hero image without any seam and the *fractured gold panel* macro shot
  (which had been an earlier "material" attempt user liked better than the
  clean macro). Brand kit was edited to formally drop glitch as a "signature"
  element (now: rare, optional accent only) — **this revision is done and
  final**, don't reintroduce it.
- **`BRAND-landing` Claude Code skill** — user uploaded and had it installed
  at `.claude/skills/BRAND-landing/SKILL.md`, then asked to fix its mismatches
  (frontmatter name `product-landing` vs folder name `BRAND-landing`; it
  assumed a `website/` Vite+GSAP+Lenis+ffmpeg stack that doesn't match this
  static-HTML project) — **then reversed course and asked to delete it
  entirely** before any fixes were applied. It has been deleted
  (`.claude/skills/` removed). **Do not reinstall or reference this skill** —
  proceed as a plain static site, no Vite/GSAP/Lenis/ffmpeg pipeline.

## 4. Current state / what's next

**Current state:** `index.html` has been fully rewritten and is functionally
verified in-browser at **both desktop (1280×800) and mobile (375×812)**
viewports via a local `python3 -m http.server` on port 8199:
- Hero, rebuild statement, gain cards, format section, record/timeline, and
  join/footer sections all confirmed rendering correctly (some screenshots
  during verification showed stale/mid-transition frames from the headless
  browser tool, but DOM/computed-style checks confirmed actual state — e.g.
  `.reveal.in` elements had `opacity: 1` even when a screenshot looked dim).
  **Note for future verification passes in this environment:** the preview
  browser tab can silently serve a stale cached copy of the page after an
  edit — `navigate` alone was not enough to pick up CSS changes at one point.
  If a change doesn't seem to be applying, force a cache-busted reload
  (`location.href = location.origin + '/?v=' + Date.now()`) before assuming
  the code is wrong, and prefer `elementFromPoint`/computed-style checks over
  trusting a single screenshot.
- Calendar JS fully tested via direct DOM/event dispatch: search, month
  filter, location filter, combined filtering, empty-state message, and
  localStorage note persistence (save + clear) all work correctly (35 total
  rows, filters produced correct subset counts, e.g. October=6,
  October+Online=1, "stanford" search=1). The test note written during
  verification was cleared from `localStorage` afterward.
- No broken images detected (`document.images` completeness check passed for
  all photos referenced at that point in verification).
- Console had no errors at last check.
- **Mobile viewport check is now complete.** Found and fixed two real issues:
  1. **Hero image crop was too tight on mobile portrait** — a 16:9 image
     under `background-size: cover` on a narrow/tall viewport was zooming
     into just the panther's torso. Fixed with a `@media (max-width: 640px)`
     override on `.hero-bg` using `145% auto` sizing instead of `cover`, so
     the full panther is visible floating in the noir background above the
     headline.
  2. **No mobile navigation** — `.nav-links` was just `display:none` under
     900px with no replacement, so in-page nav links (Rebuild, Gain, Format,
     Record, Calendar, Room) were completely inaccessible on mobile except by
     scrolling. Built a proper hamburger menu: `.nav-burger` button (3-line
     icon that morphs to an X via `aria-expanded`), `#mobileMenu` full-width
     dropdown panel (opaque noir background, large tap-friendly links),
     wired up in the JS IIFE (`burger` click toggle + auto-close on link
     tap). Verified: opens/closes correctly, links navigate and close the
     menu, doesn't regress desktop (burger `display:none` / links `flex` at
     ≥900px, confirmed via computed styles at 1280px width).
  - Also verified on mobile: gain cards collapse to 1 column, format section
    collapses to 1 column with speech-order box stacking below the steps,
    calendar filters stack and the table's horizontal scroll container works
    (tested via direct `scrollLeft` manipulation — `scrollWidth: 760` vs
    `clientWidth: 333`), room photo grid collapses to 2 columns with the
    "big" photo spanning full width, join/footer sections read cleanly.

**Remaining work, roughly in order:**

1. ~~Finish mobile verification~~ — **done**, see above.
2. **Double-check the `#format` and `#record` sections' visual polish** in
   both viewports — these were spot-checked via DOM state but not fully
   eyeballed in clean screenshots due to the stale-frame issue.
3. **Cross-check `calendar.html`** still correctly redirects to
   `index.html#calendar` (should be fine, untouched, and the new site kept
   the same section id, but worth a click-through).
4. **Decide on `history.html`** — it was never touched or referenced by the
   rebuild. The brand kit's suggested section list mentions pulling a
   "Results/Momentum" teaser from `history.html`, but the actual achievements
   timeline was ported directly into `#record` instead, effectively
   superseding it. Confirm with the user whether `history.html` should be
   deleted, redirected (like `calendar.html`), or left standalone.
5. **Team roster section was dropped** (only had placeholder `[Name]` data in
   the old site) — confirm this is acceptable, or ask the user for real
   names/roles to reinstate a leadership section.
6. **Optional/deferred: real cinematic background video.** Explicitly
   deferred, not abandoned forever — if the user upgrades their Higgsfield
   plan later, the original video brief is still in
   `copy/brand-kit.md` (§14, Hero Motion Brief) and could be generated then
   and swapped in behind the current CSS-only hero motion.
7. **Git status:** nothing has been committed this session. `index.html` is
   modified, `assets/` and `copy/` are untracked. **Do not commit without
   explicit user confirmation** per standing instructions — surface a diff
   summary and ask first when the user is ready.
8. Kill the background dev server (`python3 -m http.server 8199`, background
   task id `b09fnrrg0`) when no longer needed for verification, or restart it
   if continuing in a fresh session (files are served from the project root).

**To resume:** re-launch the local server (`python3 -m http.server 8199` from
the project root), open `http://127.0.0.1:8199/`, resize to mobile, and pick
up the verification pass at step 1 above.

---

## Multi-page architecture (latest state — supersedes single-page notes above)

The user asked to split the one-page site into multiple pages, keeping the
landing page as a pure visual moment. Chosen structure: **4 grouped pages**.

### Files now
- **`index.html`** — landing: static panther hero with a conventional headline,
  description, and two calls to action + 2 `.portal-card` entry cards (Program /
  Calendar) + shared Join CTA + footer. No canvas, video, shard effect, parallax,
  or ambient hero animation.
- **`about.html`** — "The Program": page-hero + Rebuild statement (word-by-word
  reveal) + What You Gain (6 cards) + The Format (speech-order bars) + The Room
  (6 team photos) + Join CTA + footer.
- **`record.html`** — "The Record": currently shelved from primary navigation,
  but still available directly; page-hero + 4 stat tiles + full achievements
  timeline (8 year-groups, 32 rows, ported verbatim) + Join CTA + footer.
- **`calendar.html`** — "The Calendar": page-hero (with the 35-count) + filters
  + 35-row table + editable localStorage notes + Join CTA + footer. (This
  replaced the old redirect stub.)
- **`history.html`** — now a redirect to `record.html` (was a stale duplicate
  of the achievements; meta-refresh + `location.replace`).
- **`assets/site.css`** — ALL shared styles (extracted from the old inline
  `<style>`), including the simple fixed site navigation, `.page-hero`,
  `.portal-*`, nav `[aria-current]` active state, and `.foot-links`. NOTE:
  background-image URLs in this file are relative to `assets/`, so they read
  `url("images/...")` which resolves to `assets/images/...` — do NOT change
  these to `assets/images/...` or they'll break.
- **`assets/site.js`** — ALL shared JS, refactored with **feature-detection**
  (every block guards on element existence) so the one file works on every
  page: year, accessible mobile menu, statement reveal (about only), `.reveal`
  IntersectionObserver, calendar filters + notes (calendar only).

### Shared partials (hand-duplicated in each HTML, since no build step)
- Nav (with `aria-current="page"` on the active link) + mobile menu
- Join CTA `<section class="join" id="join">` (headline/copy varies slightly
  per page; "Join" nav link points to `#join` on every page)
- Footer with `.foot-links` cross-page nav
- `<script src="assets/site.js">`

### Verified (desktop 1280×720 + mobile 390×844)
- The landing hero and shared navigation render without horizontal overflow.
  The mobile menu opens, closes, updates its accessible label/state, and closes
  on Escape. Active navigation state is correct on Program, Calendar, and the
  directly accessible Record page.
- about: statement + 6 gain cards + 6 room photos present. record: 8 years / 4
  stats / 32 rows. calendar: 35 rows, month filter (Oct→6) + count + notes
  wired. history → redirects to record.
- No browser console errors. The old hero sweep, cursor, scroll cue, parallax,
  global film grain, and floating prep timer have been removed.
- KNOWN TOOL QUIRK persists: the preview browser shows blank/stale frames after
  JS `scrollTo` jumps — trust `elementFromPoint`/computed-style checks and
  fresh-load screenshots over a single mid-page screenshot.

### Still open / next
1. Optional visual polish pass on below-fold sections of each page in clean
   screenshots (blocked only by the stale-frame tool quirk; DOM state is
   correct).
2. Same open questions as before: real leadership/roster section (old one was
   placeholder `[Name]`s, still omitted); real contact email (currently
   `prospectparli@gmail.com` placeholder in every Join CTA mailto — CONFIRM or
   replace).
3. Nothing committed to git yet. `index.html` + `calendar.html` + `history.html`
   modified; `about.html`, `record.html`, `assets/site.css`, `assets/site.js`,
   `assets/`, `copy/` new/untracked. Do not commit without user go-ahead.
4. Background dev server: `python3 -m http.server 8199` (bg task `b09fnrrg0`).
