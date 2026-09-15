# Portfolio-Sektion & Vereins-Seite — 2026-09-15

## Goal

Extend the Hugo blog at `faffi.cloud` with two new, related surfaces:

1. **`/projekte/`** — a project index over 11 private (non-employer) projects, each with its
   own detail page. Serves both the club audience and the professional audience the CV
   already points at.
2. **`/fuer-vereine/`** — a content page aimed at club board members (Vereinsvorstände),
   written in their language, embedding the five club projects as references.

The blog posts under `content/posts/` stay exactly as they are. The project pages are short
summaries that link to the long-form post where one exists.

## Constraints

- **Language**: German for all site content. English for code, comments, and frontmatter keys
  where they are technical; German for frontmatter keys that appear as content (`tagline`).
- **No employer work.** Nothing related to Krombacher appears anywhere in the portfolio.
  Explicitly excluded: `kpl`, `kpl-agentic-meoton`, `kpl-gopt`, `kpl-rca-multi-line`,
  `kpl-spendenaktion`, `customer_lifetime_value`, `receipt_entity_recognition`,
  `malzsilo-chargenverteilung`, `ki-umfrage-dashboard` (internal employee survey),
  `obsidian-automations` (reports over the KPL repo), `Leadgen_Krombacher`.
- **No commercial framing.** The user is employed full-time; a side business would raise
  secondary-employment questions. Therefore: no prices, no "Honorar", no "Rechnung", no
  "Leistungen", no "Angebot", no contact form. The page describes what is possible and asks
  the maintenance question without attaching a number to it. Consequence: the site keeps its
  private character and an Impressum under § 5 DDG is not triggered.
- **Privacy in screenshots.** Several live systems hold real personal data (children's and
  parents' names on the Basar admin pages, player names in the Medenspiel-Planner, the
  Doppelkopf group's names in doko-stats). Only public pages or test data may be captured.
- **Hosting**: Cloudflare Pages with `HUGO_VERSION=0.146.0`. Nothing may break the build.
- **Theme**: PaperMod is a git submodule and must not be modified. All changes live in
  `layouts/` and `assets/css/extended/`.
- **Scope discipline**: the existing `layouts/_default/list.html` and `single.html` are not
  touched. `hugo.toml` is not touched.

## Section 1 — Content structure

New section `content/projekte/`, one page bundle per project (folder with `index.md` plus its
cover image), mirroring how `content/posts/` is already organised.

```
content/
  projekte/
    _index.md                      -> /projekte/          menu main, weight 15
    kinderbasar/index.md
    tcbw-website/index.md
    medenspiel-planner/index.md
    tcbw-getraenkebuchung/index.md
    tcbw-social-tools/index.md
    mai-tasting/index.md
    narraitive/index.md
    wippestoolen/index.md
    mytapo/index.md
    solar-prediction/index.md
    doko-stats/index.md
  fuer-vereine.md                  -> /fuer-vereine/      menu main, weight 16
```

Menu entries are declared in frontmatter (`menu = "main"`), the way `content/lebanslauf.md`
(weight 20) already does. No `[menu]` block is added to `hugo.toml`.

### Frontmatter schema (TOML)

```toml
+++
title = "Kinderbasar Biekhofen"
date = 2026-10-10T10:00:00+02:00
draft = false
tagline = "Anmeldung, Kasse und Abrechnung für den Kinderflohmarkt"
gruppe = "vereine"          # vereine | produkte | daten
status = "live"             # live | appstore | wip
zeitraum = "2026"
weight = 10                 # ordering within the group, ascending
stack = ["FastAPI", "Postgres", "HTMX"]
live_url = "https://basar.faffi.cloud"
repo_url = "https://github.com/ElGarno/kinderbasar-biekhofen"
post_url = ""               # internal link to the long-form post, empty if none
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Anmeldeformular des Kinderbasars"
+++
```

`repo_url` is only set for repositories that are actually public. Verified 2026-09-15:

- **Public** (link them): `tcbw-homepage`, `tcbw-social-tools`, `NarrAItive`, `MyTapo`,
  `predict_power_consumption`.
- **Private** (leave `repo_url` empty): `kinderbasar-biekhofen`, `medenspiel-planner`,
  `tcbw-getraenkebuchung`, `whisky-api`, `Wippestoolen`. `doko-stats` has no remote at all.

The card omits the link rather than linking to a 404.

### Body text

Three short sections per project — **Problem**, **Lösung**, **Ergebnis** — 150 to 250 words
total. Sourced from the project's README and, where one exists, the existing blog post. No
code snippets, no internal endpoint paths, no table or column names for private repos
(same rule as the 2026-05-01 spec).

### The 11 projects

| Slug | Title | Gruppe | Status | Blog post exists |
|---|---|---|---|---|
| `kinderbasar` | Kinderbasar Biekhofen | vereine | live | no |
| `tcbw-website` | Vereinswebsite TC Blau-Weiß | vereine | live | yes (`/posts/tcbw-website/`) |
| `medenspiel-planner` | Medenspiel-Planner | vereine | live | no |
| `tcbw-getraenkebuchung` | Getränkebuchung am iPad | vereine | live | yes (`/posts/tcbw-getraenkebuchung/`) |
| `tcbw-social-tools` | Social-Media-Grafiken | vereine | live | no |
| `mai-tasting` | mAI Whisky & mAI Wine | produkte | appstore | yes (`/posts/mai-tasting/`) |
| `narraitive` | NarrAItive | produkte | wip | yes (`/posts/narraitive/`) |
| `wippestoolen` | Wippestoolen | produkte | wip | yes (`/posts/wippestoolen/`) |
| `mytapo` | MyTapo Event-Detection | daten | live | yes (`/posts/tapo/`) |
| `solar-prediction` | Solar Power Prediction | daten | live | no |
| `doko-stats` | Doppelkopf-Statistik | daten | live | no |

Group headings on the index: **Vereine & Gemeinwohl**, **Eigene Produkte**,
**Daten & Zuhause** — in that order.

## Section 2 — Layouts

Four new files. PaperMod's `baseof.html` is inherited via `{{ define "main" }}`.

| File | Purpose |
|---|---|
| `layouts/projekte/list.html` | Index page: `_index.md` content as intro, then the three groups, each with an `<h2>` and a card grid |
| `layouts/projekte/single.html` | Project page: cover, title, tagline, meta row (status badge, Zeitraum, stack chips), body, link bar (Live · Repo · Blogpost), optional screenshot gallery |
| `layouts/partials/project-card.html` | One card. Takes a page as context. Used by both the index and the shortcode |
| `layouts/shortcodes/projektkarten.html` | `{{< projektkarten gruppe="vereine" >}}` — renders the cards of one group inside any page |

The existing `layouts/_default/list.html` handles posts and the homepage and is left alone;
Hugo picks `layouts/projekte/list.html` for the section by type. The card markup differs
substantially from the post-card markup (grid vs. horizontal thumbnail row), so sharing a
template would mean adding branches to a file that works today.

**Gallery**: `single.html` renders additional page resources matching `shot-*.webp` (if any)
as a horizontal, scrollable row below the body. This is how the portrait App-Store frames for
`mai-tasting` get shown at full height.

## Section 3 — CSS

Appended to `assets/css/extended/custom.css`. Existing rules are not modified.

| Class | Purpose |
|---|---|
| `.project-grid` | CSS grid, `repeat(auto-fill, minmax(280px, 1fr))`, gap `1.5rem`; single column below 480px |
| `.project-card` | Border in `var(--border)`, radius, hover lift; cover at 16:9 via `aspect-ratio` + `object-fit: cover` |
| `.project-badge` | Status pill; `live` green-ish, `appstore` blue-ish, `wip` amber — all derived from PaperMod variables plus one accent each |
| `.project-stack` | Small tech chips, `var(--secondary)` text on `var(--code-bg)` |
| `.project-links` | Link bar on the detail page |
| `.project-gallery` | Horizontal scroll row for portrait screenshots, `scroll-snap-type: x mandatory` |

All colours come from PaperMod's custom properties (`--theme`, `--entry`, `--primary`,
`--secondary`, `--border`, `--code-bg`) so dark mode works without a second rule set.

## Section 4 — `/fuer-vereine/`

Structure, in order:

1. **Einstieg** — in club language, not tech language: what club organisation actually hangs
   on day to day (Strichliste an der Theke, Doodle-Ketten, eine Website, die keiner anfassen
   will, eine Basar-Anmeldung per WhatsApp).
2. **Was möglich ist** — four to five concrete examples drawn from what already runs,
   each one sentence, each pointing at the corresponding project.
3. **Bevor ihr fragt: zwei ehrliche Punkte** — the text agreed in the brainstorming session:
   building is the easy part and is done gladly; the third year is where club software dies.
   Source code belongs to the club, domain and accounts run on the club, running costs are
   paid directly to the provider, and who maintains it is settled up front. Closing line
   references the WordPress site replaced at TC Blau-Weiß — a site that was slow, wanted
   constant updates, and that nobody on the board wanted to touch. No prices, no invoice.
4. **Referenzen** — `{{< projektkarten gruppe="vereine" >}}`.
5. **Kontakt** — one paragraph plus `faffi@gmx.de`. No form.

## Section 5 — Images

Priority is real screenshots wherever they can be obtained.

| Project | Source | Fallback |
|---|---|---|
| `kinderbasar` | Playwright on `https://basar.faffi.cloud/anmeldung` (public, verified 200). Admin views only via `/orga/testdaten` data, if at all | none needed |
| `tcbw-website` | Playwright on `https://tc-bw-attendorn.de` | existing `posts/tcbw-website/cover.webp` |
| `medenspiel-planner` | Root returns 404 (magic link required) — run locally with seeded test data, capture `localhost` | generated cover |
| `tcbw-getraenkebuchung` | Xcode 26.6 with iPad Pro 11" simulator available — build and capture the kiosk screen | existing `posts/tcbw-getraenkebuchung/cover.webp` |
| `tcbw-social-tools` | `npm run dev` locally (sibling repo `tcbw-homepage` is checked out), capture `localhost` | generated cover |
| `mai-tasting` | Existing App-Store frames in `whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots/` and `…-Wine-…`, 1290×2796 | none needed |
| `narraitive` | Streamlit `app.py` with the local `narrAItive_duckDB.duckdb`, capture `localhost` | existing `NarrAItive_logo.webp` |
| `wippestoolen` | Playwright on `https://wippestoolen.vercel.app` (verified 200) | existing `posts/wippestoolen/cover.webp` |
| `mytapo` | Grafana on the NAS — home network only | existing `posts/Tapo/cover.webp` |
| `solar-prediction` | Dashboard on the NAS — home network only | generated cover |
| `doko-stats` | `~/doko-stats/dashboard.html` locally via `file://` | generated cover |

**Processing.** A new uv inline script `scripts/shot_to_cover.py`, modelled on the existing
`scripts/generate_covers.py`:

- Landscape captures: take at 1440×900, crop to 1200×675, save as WebP quality 82.
- Portrait frames (mai-tasting): compose two or three frames side by side on a 1200×675
  canvas filled with the app's background colour, scaled to fit with a margin — this produces
  the card cover. The originals are additionally copied into the page bundle as
  `shot-1.webp`, `shot-2.webp`, … for the gallery.
- Generated covers reuse `scripts/generate_covers.py` with the existing `STYLE_PREFIX`, so the
  fallback images sit in the same visual family as the post covers.

**Privacy rules when capturing:**

- Basar: public pages only. No `/orga/teilnehmer`, `/orga/abrechnung`, `/orga/warteliste`
  against production data.
- Medenspiel-Planner: seeded test data only, never real squad lists.
- doko-stats: the dashboard shows the regular group's real names — either capture a view
  without names, or replace them before capturing.
- MyTapo / Solar: own household data, unproblematic.

## Section 6 — Sequence and verification

1. Scaffolding: the four layout files, the CSS block, `_index.md`, all 11 project pages with
   text and frontmatter but no images yet.
2. `/fuer-vereine/`.
3. Images, in the order of the table above; fallbacks for anything not reachable today.
4. Optional: a minimal Impressum page, only if the user asks for it.

Each step ends with:

- `hugo --gc --minify` completes without errors or warnings.
- `hugo server` plus a Playwright pass over `/projekte/`, one project page, and
  `/fuer-vereine/` — each in light and dark mode, and at 390px viewport width.
- Internal links (`post_url`) are verified to resolve against `public/` after the build.

Nothing is committed until the user approves it.

## Out of scope

- Any change to existing blog posts, `layouts/_default/*`, or `hugo.toml`.
- English translations of the new pages.
- A contact form, analytics, or a newsletter.
- An Impressum or privacy page unless explicitly requested.
- New blog posts for the projects that lack one — the project page is the summary; a post can
  follow later as its own task.
