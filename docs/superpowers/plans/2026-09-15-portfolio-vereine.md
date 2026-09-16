# Portfolio-Sektion & Vereins-Seite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a project portfolio at `/projekte/` (11 projects, card index plus detail pages) and a club-facing page at `/fuer-vereine/` to the Hugo blog at faffi.cloud.

**Architecture:** A new Hugo content section `content/projekte/` with one page bundle per project. Four new templates under `layouts/` render a card grid and detail pages; a shortcode re-uses the same card partial to embed one project group inside any page. All styling is appended to the existing `assets/css/extended/custom.css` using PaperMod's CSS custom properties, so dark mode needs no second rule set. Cover images are real screenshots wherever they can be captured, processed by a new uv inline script.

**Tech Stack:** Hugo 0.146.0 (extended), PaperMod (git submodule, read-only), TOML frontmatter, plain CSS, Python 3.13 uv inline scripts with Pillow, Playwright MCP for captures, Xcode 26.6 iPad simulator.

**Spec:** `docs/superpowers/specs/2026-09-15-portfolio-vereine-design.md`

## Global Constraints

- **Hugo version:** Cloudflare Pages pins `HUGO_VERSION=0.146.0`. Nothing may require a newer version.
- **Do not touch:** `themes/PaperMod/**` (git submodule), `layouts/_default/list.html`, `layouts/_default/single.html`, `hugo.toml`, any file under `content/posts/`.
- **Language:** all site-visible content in German. Template variables, CSS class names, Python identifiers and code comments in English.
- **No employer content.** Nothing Krombacher-related appears anywhere. Excluded repos: `kpl`, `kpl-agentic-meoton`, `kpl-gopt`, `kpl-rca-multi-line`, `kpl-spendenaktion`, `customer_lifetime_value`, `receipt_entity_recognition`, `malzsilo-chargenverteilung`, `ki-umfrage-dashboard`, `obsidian-automations`, `Leadgen_Krombacher`.
- **No commercial framing.** Forbidden words anywhere in new content: „Angebot", „Leistungen", „Honorar", „Rechnung", „Preis", „Paket", „Kunde", „beauftragen". No prices, no contact form. The user is employed full-time and a side business would raise secondary-employment questions.
- **Repo links.** `repo_url` is set only for these public repos: `tcbw-homepage`, `tcbw-social-tools`, `NarrAItive`, `MyTapo`, `predict_power_consumption`. Left empty for: `kinderbasar-biekhofen`, `medenspiel-planner`, `tcbw-getraenkebuchung`, `whisky-api`, `Wippestoolen`, `doko-stats`.
- **Privacy when capturing screenshots.** Basar: public pages only, never `/orga/teilnehmer`, `/orga/abrechnung` or `/orga/warteliste` against production. Medenspiel-Planner: seeded test data only, never a real squad list. doko-stats: the dashboard names the user's Doppelkopf group — every player name must be absent or replaced before capturing, and no name appears in the page text either.
- **Commits require explicit approval.** The user's CLAUDE.md forbids unrequested commits. Every commit step below is conditional: stage the files, show `git status` and the proposed message, and only run `git commit` once the user says yes in this session.
- **One deviation from the spec:** the spec lists four new template files; this plan creates five. The status pill was pulled out into `layouts/partials/project-badge.html` because both the card partial and the detail template render it, and duplicating the label mapping in two files is how the two drift apart.
- **Hugo binary.** The machine's `hugo` is 0.166.0, which breaks PaperMod's `rss.xml`; production uses 0.146.0. A pinned 0.146.0 binary lives in the session scratchpad and every build must use it: `export HUGO_BIN=<scratchpad>/hugo146/hugo`. `scripts/check_projekte.sh` honours `${HUGO_BIN:-hugo}`, so it still works unmodified on CI.
- **Counting occurrences in built HTML.** Minified HTML is one single line, so `grep -c` always reports `1`. Count with `grep -o '<needle>' <file> | wc -l`. `grep -q` for mere existence is fine.
- **The check script always builds minified**, so the rendered HTML has unquoted attributes (`class=project-grid`, not `class="project-grid"`). Grep needles must never include `class="`.
- **Verification command used throughout:** `"$HUGO_BIN" --gc --minify` from the repo root must finish with zero errors and zero warnings.

---

### Task 1: Section scaffolding, templates, CSS, first project page

Delivers a rendering `/projekte/` index with one real card and one real detail page. Everything later only adds data.

**Files:**
- Create: `layouts/partials/project-badge.html`
- Create: `layouts/partials/project-card.html`
- Create: `layouts/projekte/list.html`
- Create: `layouts/projekte/single.html`
- Create: `content/projekte/_index.md`
- Create: `content/projekte/kinderbasar/index.md`
- Modify: `assets/css/extended/custom.css` (append only, do not edit existing rules)

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `partial "project-badge.html" <status string>` — renders one status pill. Accepts `"live"`, `"appstore"`, `"wip"`.
  - `partial "project-card.html" <page>` — renders one `<article class="project-card">`. Takes a Hugo Page as context, reads `.Title`, `.Params.tagline`, `.Params.status`, `.Params.zeitraum`, `.Params.stack`, and the page resource named by `.Param "cover.image"`.
  - The frontmatter key set every later project page must use: `title`, `date`, `draft`, `tagline`, `gruppe`, `status`, `zeitraum`, `weight`, `stack`, `live_url`, `repo_url`, `post_url`, `cover.image`, `cover.relative`, `cover.alt`.
  - CSS classes available to later tasks: `.project-grid`, `.project-group`, `.project-group-title`, `.project-card`, `.project-card-cover`, `.project-card-body`, `.project-card-title`, `.project-card-tagline`, `.project-card-meta`, `.project-badge`, `.project-stack`, `.project-zeitraum`, `.project-cover`, `.project-meta`, `.project-links`, `.project-link`, `.project-gallery`.

- [ ] **Step 1: Write the failing verification**

Create the check script `scripts/check_projekte.sh` (it is used by every later task too):

```bash
#!/usr/bin/env bash
# Build the site and assert the portfolio pages rendered as expected.
set -euo pipefail
cd "$(dirname "$0")/.."

"${HUGO_BIN:-hugo}" --gc --minify --quiet

fail=0
check() {  # check <file> <needle> <description>
  if grep -q -- "$2" "$1" 2>/dev/null; then
    echo "ok   $3"
  else
    echo "FAIL $3  (missing '$2' in $1)"
    fail=1
  fi
}

check public/projekte/index.html 'class=project-grid'          'index renders a card grid'
check public/projekte/index.html 'Vereine &amp; Gemeinwohl'    'index renders the Vereine group heading'
check public/projekte/index.html 'Kinderbasar Biekhofen'       'index lists Kinderbasar'
check public/projekte/kinderbasar/index.html 'project-links'   'detail page renders the link bar'
check public/index.html '>Projekte<'                           'Projekte appears in the main menu'

exit $fail
```

Make it executable: `chmod +x scripts/check_projekte.sh`

- [ ] **Step 2: Run it to verify it fails**

Run: `./scripts/check_projekte.sh`
Expected: several `FAIL` lines, exit code 1 — `public/projekte/` does not exist yet.

- [ ] **Step 3: Create `layouts/partials/project-badge.html`**

```go-html-template
{{- /* Renders one status pill. Context: the status string. */ -}}
{{- $labels := dict "live" "Live im Einsatz" "appstore" "Im App Store" "wip" "In Arbeit" -}}
{{- with . -}}
<span class="project-badge project-badge--{{ . }}">{{ index $labels . | default . }}</span>
{{- end -}}
```

- [ ] **Step 4: Create `layouts/partials/project-card.html`**

```go-html-template
{{- /* Renders one project card. Context: a project Page. */ -}}
{{- $p := . -}}
{{- $coverName := $p.Param "cover.image" | default "cover.webp" -}}
{{- $cover := $p.Resources.GetMatch $coverName -}}
<article class="project-card">
  <a class="project-card-link" href="{{ $p.RelPermalink }}">
    {{- with $cover }}
    <img class="project-card-cover" src="{{ .RelPermalink }}"
         alt="{{ $p.Param "cover.alt" | default $p.Title }}" loading="lazy">
    {{- else }}
    <div class="project-card-cover project-card-cover--empty" aria-hidden="true"></div>
    {{- end }}
    <div class="project-card-body">
      <h3 class="project-card-title">{{ $p.Title }}</h3>
      {{- with $p.Params.tagline }}
      <p class="project-card-tagline">{{ . }}</p>
      {{- end }}
      <div class="project-card-meta">
        {{- partial "project-badge.html" $p.Params.status }}
        {{- with $p.Params.zeitraum }}<span class="project-zeitraum">{{ . }}</span>{{ end }}
      </div>
      {{- with $p.Params.stack }}
      <ul class="project-stack">{{ range . }}<li>{{ . }}</li>{{ end }}</ul>
      {{- end }}
    </div>
  </a>
</article>
```

- [ ] **Step 5: Create `layouts/projekte/list.html`**

```go-html-template
{{- define "main" }}
<header class="page-header">
  <h1>{{ .Title }}</h1>
</header>

{{- with .Content }}
<div class="post-content">{{ . }}</div>
{{- end }}

{{- $groups := slice
      (dict "key" "vereine"  "title" "Vereine & Gemeinwohl")
      (dict "key" "produkte" "title" "Eigene Produkte")
      (dict "key" "daten"    "title" "Daten & Zuhause") }}

{{- range $g := $groups }}
  {{- $pages := sort (where $.RegularPages "Params.gruppe" $g.key) "Weight" }}
  {{- with $pages }}
<section class="project-group">
  <h2 class="project-group-title">{{ $g.title }}</h2>
  <div class="project-grid">
    {{- range . }}{{ partial "project-card.html" . }}{{ end }}
  </div>
</section>
  {{- end }}
{{- end }}

{{- end }}
```

- [ ] **Step 6: Create `layouts/projekte/single.html`**

```go-html-template
{{- define "main" }}
{{- $coverName := .Param "cover.image" | default "cover.webp" }}
{{- $cover := .Resources.GetMatch $coverName }}
{{- $coverAlt := .Param "cover.alt" | default .Title }}
<article class="post-single project-single">
  <header class="post-header">
    {{ partial "breadcrumbs.html" . }}
    <h1 class="post-title">{{ .Title }}</h1>
    {{- with .Params.tagline }}
    <div class="post-description">{{ . }}</div>
    {{- end }}
    <div class="project-meta">
      {{- partial "project-badge.html" .Params.status }}
      {{- with .Params.zeitraum }}<span class="project-zeitraum">{{ . }}</span>{{ end }}
      {{- with .Params.stack }}
      <ul class="project-stack">{{ range . }}<li>{{ . }}</li>{{ end }}</ul>
      {{- end }}
    </div>
  </header>

  {{- with $cover }}
  <img class="project-cover" src="{{ .RelPermalink }}" alt="{{ $coverAlt }}" loading="lazy">
  {{- end }}

  <div class="post-content">{{ .Content }}</div>

  {{- with .Resources.Match "shot-*.webp" }}
  <div class="project-gallery">
    {{- range . }}<img src="{{ .RelPermalink }}" alt="" loading="lazy">{{ end }}
  </div>
  {{- end }}

  <div class="project-links">
    {{- with .Params.live_url }}
    <a class="project-link" href="{{ . }}" rel="noopener noreferrer" target="_blank">Live ansehen</a>
    {{- end }}
    {{- with .Params.repo_url }}
    <a class="project-link" href="{{ . }}" rel="noopener noreferrer" target="_blank">Quellcode</a>
    {{- end }}
    {{- with .Params.post_url }}
    <a class="project-link" href="{{ . | relURL }}">Ausführlicher Blogpost</a>
    {{- end }}
  </div>
</article>
{{- end }}
```

- [ ] **Step 7: Append the CSS to `assets/css/extended/custom.css`**

```css

/* === Portfolio: Projektkarten und Projektseiten === */

.project-group {
    margin: 2.5rem 0;
}

.project-group-title {
    font-size: 1.4rem;
    margin-bottom: 1rem;
}

.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 1.5rem;
}

@media (max-width: 480px) {
    .project-grid {
        grid-template-columns: 1fr;
    }
}

.project-card {
    background: var(--entry);
    border: 1px solid var(--border);
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.15s ease;
}

.project-card:hover {
    transform: translateY(-2px);
}

.project-card-link {
    display: block;
    color: inherit;
    text-decoration: none;
    box-shadow: none;
}

.project-card-cover {
    width: 100%;
    aspect-ratio: 16 / 9;
    object-fit: cover;
    display: block;
}

.project-card-cover--empty {
    background: var(--code-bg);
}

.project-card-body {
    padding: 1rem;
}

.project-card-title {
    margin: 0 0 0.35rem;
    font-size: 1.1rem;
}

.project-card-tagline {
    margin: 0 0 0.75rem;
    color: var(--secondary);
    font-size: 0.9rem;
    line-height: 1.4;
}

.project-card-meta,
.project-meta {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.5rem;
}

.project-badge {
    display: inline-block;
    padding: 0.15rem 0.6rem;
    border-radius: 999px;
    font-size: 0.75rem;
    font-weight: 600;
    border: 1px solid var(--border);
    color: var(--primary);
    background: var(--code-bg);
}

.project-badge--live {
    border-color: #3f8f5f;
    color: #3f8f5f;
}

.project-badge--appstore {
    border-color: #3a6ea5;
    color: #3a6ea5;
}

.project-badge--wip {
    border-color: #b07d2b;
    color: #b07d2b;
}

.project-zeitraum {
    font-size: 0.8rem;
    color: var(--secondary);
}

.project-stack {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    list-style: none;
    margin: 0;
    padding: 0;
}

.project-stack li {
    font-size: 0.72rem;
    padding: 0.1rem 0.45rem;
    border-radius: 4px;
    background: var(--code-bg);
    color: var(--secondary);
}

.project-cover {
    width: 100%;
    max-width: 720px;
    height: auto;
    border-radius: 8px;
    margin: 0 auto 2em auto;
    display: block;
}

.project-gallery {
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    scroll-snap-type: x mandatory;
    padding-bottom: 0.75rem;
    margin: 1.5rem 0;
}

.project-gallery img {
    flex: 0 0 auto;
    width: 240px;
    height: auto;
    border-radius: 12px;
    scroll-snap-align: start;
    border: 1px solid var(--border);
}

.project-links {
    display: flex;
    flex-wrap: wrap;
    gap: 0.75rem;
    margin-top: 2rem;
}

.project-link {
    padding: 0.4rem 0.9rem;
    border: 1px solid var(--border);
    border-radius: 6px;
    font-size: 0.85rem;
    text-decoration: none;
    box-shadow: none;
    color: var(--primary);
}

.project-link:hover {
    background: var(--code-bg);
}
```

- [ ] **Step 8: Create `content/projekte/_index.md`**

```markdown
+++
title = "Projekte"
date = 2026-09-15T10:00:00+02:00
draft = false
menu = "main"
weight = 15
+++

Was in den letzten Jahren nebenbei entstanden ist: Software für Vereine aus meiner
Ecke, zwei Apps im App Store und ein paar Dinge, die bei mir zu Hause Daten sammeln.
Fast alles läuft produktiv — bei einem Tennisverein, bei einem Kindergarten oder auf
dem NAS im Keller.

Wenn du im Vorstand eines Vereins sitzt und dich fragst, ob sowas auch bei euch ginge:
[Für Vereine](/fuer-vereine/).
```

- [ ] **Step 9: Create `content/projekte/kinderbasar/index.md`**

```markdown
+++
title = "Kinderbasar Biekhofen"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Anmeldung, Kasse und Abrechnung für einen Kinderflohmarkt mit über hundert Verkäufern"
gruppe = "vereine"
status = "live"
zeitraum = "2026"
weight = 10
stack = ["FastAPI", "Postgres", "HTMX", "Railway"]
live_url = "https://basar.faffi.cloud"
repo_url = ""
post_url = ""
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Anmeldeformular des Kinderbasars Biekhofen"
+++

## Problem

Ein Kinderflohmarkt zugunsten des Kindergartens sieht von außen harmlos aus und ist
organisatorisch ein kleines Unternehmen. Verkäufernummern werden per WhatsApp vergeben
und doppelt vergeben, die Einwilligungserklärung liegt irgendwo auf Papier, am
Verkaufstag läuft die Kasse über einen Taschenrechner, und danach sitzt jemand zwei
Abende lang und rechnet aus, wer wie viel bekommt. Wer einmal dabei war, weiß, dass der
Ärger nicht beim Verkaufen entsteht, sondern hinterher bei der Abrechnung.

## Lösung

Eine Web-App, die den gesamten Ablauf abbildet: Anmeldung samt Einwilligung, wobei die
Verkäufernummer sofort auf dem Bildschirm steht; eine Warteliste, die automatisch
übernimmt, sobald alle Nummern vergeben sind; ein Blatt zum Ausdrucken mit Nummer,
To-do-Liste und Regelwerk; eine Kassenansicht, die auch einen Netzausfall übersteht;
und ein Orga-Bereich mit Warenannahme, Umsatzübersicht, Teilnehmerliste und der
fertigen Abrechnung je Nummer — als PDF für die Verkäufer und als CSV für die
Vereinsbücher. Termine, Gebühren und Prozentsätze stehen in den Einstellungen, damit im
nächsten Jahr niemand Code anfassen muss. Selbst der A5-Flyer mit QR-Code fällt aus dem
System heraus.

## Ergebnis

Läuft unter basar.faffi.cloud auf Railway, abgesichert durch getrennte Codes für Kasse
und Orga. 495 Tests, Migrationen laufen beim Start. Ein Probelauf-Modus legt Testdaten
an und räumt sie wieder weg, damit das Orga-Team den Ablauf vorher einmal durchspielen
kann, ohne etwas kaputtzumachen.
```

- [ ] **Step 10: Run the verification**

Run: `./scripts/check_projekte.sh`
Expected: all five checks `ok`, exit code 0.

- [ ] **Step 11: Visual check in light and dark mode**

Run `hugo server -D` and open `http://localhost:1313/projekte/`. Confirm with Playwright at 1440px and at 390px width, once with the PaperMod theme toggle in light mode and once in dark: the card has a visible border, the badge reads „Live im Einsatz", the stack chips wrap instead of overflowing, and the empty cover placeholder is a neutral block, not a collapsed zero-height element.

- [ ] **Step 12: Stage and propose the commit**

```bash
git add layouts/partials/project-badge.html layouts/partials/project-card.html \
        layouts/projekte/ content/projekte/ assets/css/extended/custom.css \
        scripts/check_projekte.sh
git status
```

Proposed message — run `git commit` only after the user approves:

```
feat(projekte): add portfolio section with card grid and first project page
```

---

### Task 2: The four remaining club projects

**Files:**
- Create: `content/projekte/tcbw-website/index.md`
- Create: `content/projekte/medenspiel-planner/index.md`
- Create: `content/projekte/tcbw-getraenkebuchung/index.md`
- Create: `content/projekte/tcbw-social-tools/index.md`
- Modify: `scripts/check_projekte.sh`

**Interfaces:**
- Consumes: the frontmatter key set and `partial "project-card.html"` from Task 1.
- Produces: five pages with `gruppe = "vereine"`, weights 10–50, which Task 4's shortcode renders on `/fuer-vereine/`.

- [ ] **Step 1: Extend the verification**

Add these lines to `scripts/check_projekte.sh` above the `exit $fail` line:

```bash
check public/projekte/index.html 'Vereinswebsite TC Blau-Wei'     'index lists the TCBW website'
check public/projekte/index.html 'Medenspiel-Planner'             'index lists the Medenspiel-Planner'
check public/projekte/index.html 'Getr'                           'index lists the drinks app'
check public/projekte/index.html 'Social-Media-Grafiken'          'index lists the social tools'
check public/projekte/tcbw-website/index.html 'posts/tcbw-website' 'TCBW page links its blog post'
```

- [ ] **Step 2: Run it to verify it fails**

Run: `./scripts/check_projekte.sh`
Expected: the five new checks `FAIL`, the Task 1 checks still `ok`.

- [ ] **Step 3: Create `content/projekte/tcbw-website/index.md`**

```markdown
+++
title = "Vereinswebsite TC Blau-Weiß"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Von WordPress zu einer Seite, die der Vorstand selbst pflegt"
gruppe = "vereine"
status = "live"
zeitraum = "2026"
weight = 20
stack = ["Hugo", "DecapCMS", "Cloudflare Pages"]
live_url = "https://tc-bw-attendorn.de"
repo_url = "https://github.com/ElGarno/tcbw-homepage"
post_url = "/posts/tcbw-website/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Startseite des TC Blau-Weiß Attendorn"
+++

## Problem

Die alte Vereinsseite lief auf WordPress: langsam, ständig Plugin-Updates, unklarer
Sicherheitsstatus. Im Vorstand wollte niemand PHP-Versionen und Datenbank-Backups
betreuen, und gleichzeitig mussten nicht-technische Vorstandsmitglieder Aktuelles,
Mannschaften und Termine selbst pflegen können. Dazu die Anforderung, dass das Hosting
nichts kostet und nichts kaputtgeht, wenn ein halbes Jahr niemand hinschaut.

## Lösung

Ein Static-Site-Generator plus ein Headless-CMS, das im Browser läuft: Hugo baut die
Seite, DecapCMS gibt dem Vorstand eine Oberfläche zum Schreiben, und jede Änderung
landet als Commit im Git-Repository. Kein Server, keine Datenbank, kein PHP — und damit
auch keine Angriffsfläche, die jemand patchen müsste. Gehostet auf Cloudflare Pages,
das bei jedem Push neu baut.

## Ergebnis

Läuft unter tc-bw-attendorn.de. Das Hosting kostet nichts, die Seite lädt sofort, und
zwei Leute im Vorstand pflegen die Inhalte ohne Rückfrage. Die Mannschaftsdaten aus dem
Repo werden inzwischen auch von den Social-Tools weiterverwendet.
```

- [ ] **Step 4: Create `content/projekte/medenspiel-planner/index.md`**

```markdown
+++
title = "Medenspiel-Planner"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Aufstellungsvorschlag statt Doodle-Kette für die Medenspiele"
gruppe = "vereine"
status = "live"
zeitraum = "2026"
weight = 30
stack = ["FastAPI", "SQLModel", "HTMX", "Railway"]
live_url = "https://medenspiel.tc-bw-attendorn.de"
repo_url = ""
post_url = ""
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Verfügbarkeitsabfrage im Medenspiel-Planner"
+++

## Problem

Die Aufstellung für ein Medenspiel entsteht traditionell in einer WhatsApp-Gruppe und
einer Doodle-Umfrage: Wer kann am Sonntag? Ein Doodle beantwortet allerdings nur die
halbe Frage. Es sagt, wer Zeit hat, aber nicht, wer spielen darf — denn die Aufstellung
muss der verbindlichen Meldeliste folgen. Der Mannschaftsführer sitzt am Ende trotzdem
da und sortiert von Hand. Und wenn ein Spieltag verlegt wird, fängt alles von vorne an.

## Lösung

Eine kleine Web-App ohne Login: Jeder Spieler bekommt einen Magic Link und trägt pro
Spieltag ein, ob er kann — mobil, mit zwei Klicks. Der Mannschaftsführer bekommt keinen
Umfragebalken, sondern einen fertigen Aufstellungsvorschlag, sortiert nach
Meldelistenposition, inklusive Hinweis auf Lücken und einer Reihenfolge, in der er
telefonieren sollte. Spielplan und Meldeliste werden einmal über die Team-ID aus nuLiga
importiert. Wird ein Spiel verlegt, bleiben die vorhandenen Antworten erhalten und nur
die betroffenen Spieler werden erneut gefragt.

## Ergebnis

Läuft unter medenspiel.tc-bw-attendorn.de auf Railway, ein Container mit einem Volume
für die SQLite-Datei. Spieler brauchen kein Konto und kein Passwort — die häufigste
Hürde bei Vereinssoftware fällt damit weg.
```

- [ ] **Step 5: Create `content/projekte/tcbw-getraenkebuchung/index.md`**

```markdown
+++
title = "Getränkebuchung am iPad"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Die Strichliste an der Vereinstheke als Kiosk-App"
gruppe = "vereine"
status = "live"
zeitraum = "2026"
weight = 40
stack = ["SwiftUI", "SwiftData", "CloudKit", "NFC"]
live_url = ""
repo_url = ""
post_url = "/posts/tcbw-getraenkebuchung/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Kiosk-Ansicht der Getränkebuchung auf dem iPad"
+++

## Problem

An der Theke im Vereinsheim hängt eine A4-Seite mit einem Kugelschreiber an einer
Schnur, daneben Striche für Bier, Wasser und Apfelschorle. In der Theorie funktioniert
das. In der Praxis ist das Ergebnis am Monatsende für den Kassenwart eher Rätselraten
als Buchhaltung: unleserliche Striche, vergessene Namen, Zettel, die feucht geworden
sind.

## Lösung

Eine Kiosk-App für das iPad, das ohnehin schon an der Theke steht. Kein zweiter
Bildschirm, kein PC, kein Drucker, kein Kassensystem. Mitglied auswählen oder per NFC
erkennen, Getränk antippen, fertig. Die Daten liegen lokal in SwiftData und
synchronisieren über CloudKit, sodass der Kassenwart seine Auswertung bekommt, ohne an
der Theke zu stehen.

## Ergebnis

Im Einsatz im Vereinsheim. Die Buchung dauert weniger lang als ein Strich, und am
Monatsende steht eine Summe da statt einer Interpretationsaufgabe.
```

- [ ] **Step 6: Create `content/projekte/tcbw-social-tools/index.md`**

```markdown
+++
title = "Social-Media-Grafiken auf Knopfdruck"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Instagram-fertige Ergebnisgrafiken, ohne dass jemand Canva öffnen muss"
gruppe = "vereine"
status = "live"
zeitraum = "2026"
weight = 50
stack = ["TypeScript", "Vite", "Cloudflare Pages", "Cloudflare Access"]
live_url = ""
repo_url = "https://github.com/ElGarno/tcbw-social-tools"
post_url = ""
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Formular zur Erzeugung einer Match-Ergebnis-Grafik"
+++

## Problem

Der Instagram-Kanal eines Vereins lebt von Regelmäßigkeit, und Regelmäßigkeit scheitert
an Aufwand. Nach jedem Medenspiel müsste jemand eine Ergebnisgrafik bauen: Vereinsfarben
treffen, Logo richtig platzieren, Namen korrekt schreiben. Das macht genau eine Person,
und wenn die im Urlaub ist, passiert nichts.

## Lösung

Ein internes Werkzeug mit vier Vorlagen — Match-Ergebnis, Heimspiel-Ankündigung,
Saison-Übersicht und Event. Man füllt ein Formular aus und bekommt eine fertige Grafik
im Vereinsdesign heraus. Die Mannschaftsdaten kommen dabei nicht aus einer zweiten
Pflegequelle, sondern direkt aus dem Repository der Vereinswebsite: Ein Build-Schritt
liest die Mannschaftsseiten aus und erzeugt daraus die Auswahllisten. Was auf der
Website steht, steht damit automatisch auch im Werkzeug.

## Ergebnis

Läuft auf Cloudflare Pages hinter Cloudflare Access mit einer E-Mail-Whitelist, damit
nur das Social-Media-Team herankommt. Aus „jemand müsste mal" ist ein Formular geworden,
das jeder im Team bedienen kann.
```

- [ ] **Step 7: Run the verification**

Run: `./scripts/check_projekte.sh`
Expected: all checks `ok`, exit code 0.

- [ ] **Step 8: Stage and propose the commit**

```bash
git add content/projekte/ scripts/check_projekte.sh
git status
```

Proposed message — commit only after approval:

```
feat(projekte): add the four remaining club project pages
```

---

### Task 3: The six non-club projects

Sources to read before writing: the existing blog posts under `content/posts/mai-tasting/index.md`, `content/posts/NarrAItive/index.md`, `content/posts/wippestoolen/index.md`, `content/posts/Tapo/index.md`, plus `~/PycharmProjects/predict_power_consumption/README.md` and `~/doko-stats/README.md`.

**Files:**
- Create: `content/projekte/mai-tasting/index.md`
- Create: `content/projekte/narraitive/index.md`
- Create: `content/projekte/wippestoolen/index.md`
- Create: `content/projekte/mytapo/index.md`
- Create: `content/projekte/solar-prediction/index.md`
- Create: `content/projekte/doko-stats/index.md`
- Modify: `scripts/check_projekte.sh`

**Interfaces:**
- Consumes: the frontmatter key set from Task 1.
- Produces: the `produkte` and `daten` groups, which make the index render all three group headings.

- [ ] **Step 1: Extend the verification**

Add above `exit $fail`:

```bash
check public/projekte/index.html 'Eigene Produkte'   'index renders the Produkte group heading'
check public/projekte/index.html 'Daten &amp; Zuhause' 'index renders the Daten group heading'
check public/projekte/index.html 'mAI Whisky'        'index lists mAI Tasting'
check public/projekte/index.html 'Doppelkopf'        'index lists doko-stats'
```

Also add a privacy guard, since doko-stats must never name the group:

```bash
for name in fabiani niax paumpey ooongbaaak hassan86 flipflop86; do
  if grep -rqi -- "$name" public/projekte/ 2>/dev/null; then
    echo "FAIL privacy: player name '$name' leaked into the portfolio"
    fail=1
  else
    echo "ok   privacy: '$name' absent"
  fi
done
```

- [ ] **Step 2: Run it to verify it fails**

Run: `./scripts/check_projekte.sh`
Expected: the four content checks `FAIL`, the privacy checks already `ok`.

- [ ] **Step 3: Write the six pages**

Each page follows the exact structure of Task 1 Step 9 — TOML frontmatter with the full key set, then `## Problem`, `## Lösung`, `## Ergebnis`, 150 to 250 words total, written in the voice of the existing blog posts (concrete, first person, no marketing adjectives). Frontmatter values are fixed as follows; the prose is condensed from the sources named above.

| | `mai-tasting` | `narraitive` | `wippestoolen` |
|---|---|---|---|
| `title` | mAI Whisky & mAI Wine | NarrAItive | Wippestoolen |
| `tagline` | Zwei iOS-Apps im App Store auf einem gemeinsamen Backend | KI-generierte Bilderbücher, vorgelesen | Werkzeug-Sharing für die Nachbarschaft |
| `gruppe` | produkte | produkte | produkte |
| `status` | appstore | wip | wip |
| `zeitraum` | 2026 | 2023–2025 | 2026 |
| `weight` | 10 | 20 | 30 |
| `stack` | FastAPI, React Native, Expo, Postgres, Railway | Streamlit, DALL·E 3, ElevenLabs, DuckDB | FastAPI, Postgres, Vercel |
| `live_url` | https://maitasting.app | (leer) | https://wippestoolen.vercel.app |
| `repo_url` | (leer) | https://github.com/ElGarno/NarrAItive | (leer) |
| `post_url` | /posts/mai-tasting/ | /posts/narraitive/ | /posts/wippestoolen/ |

| | `mytapo` | `solar-prediction` | `doko-stats` |
|---|---|---|---|
| `title` | MyTapo Event-Detection | Solar Power Prediction | Doppelkopf-Statistik |
| `tagline` | Aus Stromverbrauch werden Geräte-Events | Wetterprognose als Vorhersage der Solarüberproduktion | 5.600 Partien aus der Stammrunde, ausgewertet |
| `gruppe` | daten | daten | daten |
| `status` | live | live | live |
| `zeitraum` | 2026 | 2025–2026 | 2026 |
| `weight` | 10 | 20 | 30 |
| `stack` | Python, InfluxDB, Grafana, Docker, AWTRIX | Python, scikit-learn, InfluxDB, Open-Meteo, Pushover | Python, DuckDB, Docker, Pushover |
| `live_url` | (leer) | (leer) | (leer) |
| `repo_url` | https://github.com/ElGarno/MyTapo | https://github.com/ElGarno/predict_power_consumption | (leer) |
| `post_url` | /posts/tapo/ | (leer) | (leer) |

Facts each prose section must carry:

- **mai-tasting** — Problem: wachsende Whisky-Sammlung, Verkostungsnotizen im Notizbuch verblassen, Überblick über vorhandene Flaschen geht verloren. Lösung: Foto vom Etikett, Vision-Modell erkennt die Flasche; ein Backend bedient zwei Apps (Whisky und Wein) aus einem Monorepo mit geteiltem Paket; Geschmacksprofil als Radar-Chart, Gäste bewerten über eine Web-Seite ohne App. Ergebnis: beide Apps live im App Store, Landing unter maitasting.app, Backend auf Railway.
- **narraitive** — Problem: Berge an Bilderbüchern im Wohnzimmer, immer die gleichen Geschichten. Lösung: Text, Bilder und Vorlesestimme generiert, Bücher in einer DuckDB, Oberfläche in Streamlit. Ergebnis: Prototyp, den die eigenen Kinder tatsächlich benutzt haben; kein Produkt, sondern das Projekt, an dem die Bild- und Sprachgenerierung erstmals zusammenkamen.
- **wippestoolen** — Problem: eine Bohrmaschine wird im Schnitt rund 13 Minuten benutzt und steht den Rest ihres Lebens im Keller, in jedem zweiten Keller derselben Straße dieselbe Maschine. Lösung: lokale Plattform zum Teilen, Ausleihen und Wiederfinden von Werkzeug, inspiriert von Foodsharing. Ergebnis: Landing-Seite live, das eigentliche Produkt entsteht schrittweise.
- **mytapo** — Problem: reines Energiemonitoring zeichnet hübsche Sägezähne und beantwortet keine Alltagsfrage. Lösung: aus dem Verbrauchsstrom werden diskrete Events erkannt — Waschzyklus, TV-Session, Espressobezug — und als strukturierte Datenpunkte in eine eigene InfluxDB-Bucket geschrieben. Ergebnis: läuft im Docker-Container auf dem NAS, Anzeige unter anderem auf einer Ulanzi-AWTRIX-Uhr.
- **solar-prediction** — Problem: Strom sollte dann verbraucht werden, wenn die Anlage ihn liefert, aber „wann liefert sie" ist eine Prognosefrage. Lösung: Wetterprognose von Open-Meteo (DWD-ICON), ein RandomForest auf historischen Verbrauchs- und Wetterdaten, stündliche Vorhersage für den Folgetag. Ergebnis: läuft dauerhaft im Container auf dem NAS und schickt morgens eine Pushover-Nachricht, wann sich Waschmaschine oder Trockner lohnen. Ausdrücklich erwähnen, dass nur die Geräte an Messsteckdosen erfasst sind, nicht der gesamte Haushalt.
- **doko-stats** — Problem: eine Stammrunde spielt jahrelang online und hat am Ende eine Zahlenkolonne, aber keine Antwort auf „wer ist eigentlich gut". Lösung: Scraper mit Cursor-Pagination und Rate-Limit-Behandlung zieht die Partien mitsamt Protokoll in eine DuckDB; Auswertung über Datenbank-Views, daraus ein Single-Page-Dashboard und ein Wochenbericht per Pushover. Ergebnis: rund 5.600 Partien der Runde mit vollständigem Protokoll, Auswertung über zwei Zeiträume. **Keine Spielernamen, keine Spitznamen, keine Rangliste — das Repository ist bewusst privat, weil das Dashboard Mitspieler benennt.**

- [ ] **Step 4: Run the verification**

Run: `./scripts/check_projekte.sh`
Expected: all checks `ok`, including the six privacy guards.

- [ ] **Step 5: Count the cards**

Run: `grep -o 'class=project-card>' public/projekte/index.html | wc -l`
Expected: `11`

Note: `grep -c` counts matching LINES, and minified HTML is a single line — it would report `1`. Always count occurrences with `grep -o ... | wc -l`.

- [ ] **Step 6: Stage and propose the commit**

```bash
git add content/projekte/ scripts/check_projekte.sh
git status
```

Proposed message — commit only after approval:

```
feat(projekte): add product and data project pages
```

---

### Task 4: The `projektkarten` shortcode and `/fuer-vereine/`

**Files:**
- Create: `layouts/shortcodes/projektkarten.html`
- Create: `content/fuer-vereine.md`
- Modify: `scripts/check_projekte.sh`

**Interfaces:**
- Consumes: `partial "project-card.html"` and the `gruppe` frontmatter key from Task 1.
- Produces: `{{< projektkarten gruppe="vereine" >}}` — usable in any content file.

- [ ] **Step 1: Extend the verification**

Add above `exit $fail`:

```bash
check public/fuer-vereine/index.html 'class=project-grid' 'Vereins-Seite embeds the card grid'
check public/fuer-vereine/index.html 'Kinderbasar'          'Vereins-Seite shows the Basar reference'
check public/index.html '>Für Vereine<'                     'Für Vereine appears in the main menu'

# The page must not read as a commercial offer.
for word in Honorar Rechnung Angebot Leistungen Preis beauftragen; do
  if grep -q -- "$word" public/fuer-vereine/index.html 2>/dev/null; then
    echo "FAIL commercial wording: '$word' found on /fuer-vereine/"
    fail=1
  else
    echo "ok   no commercial wording: '$word'"
  fi
done

# Exactly the five club projects, not all eleven.
n=$(grep -o 'class=project-card>' public/fuer-vereine/index.html | wc -l | tr -d ' ')
if [ "$n" = "5" ]; then echo "ok   Vereins-Seite shows 5 cards"; else echo "FAIL expected 5 cards, got $n"; fail=1; fi
```

- [ ] **Step 2: Run it to verify it fails**

Run: `./scripts/check_projekte.sh`
Expected: the `/fuer-vereine/` checks `FAIL` (the file does not exist), the word checks pass vacuously.

- [ ] **Step 3: Create `layouts/shortcodes/projektkarten.html`**

```go-html-template
{{- /* Embeds the cards of one project group. Usage: {{< projektkarten gruppe="vereine" >}} */ -}}
{{- $gruppe := .Get "gruppe" -}}
{{- $projekte := where site.RegularPages "Section" "projekte" -}}
{{- $pages := sort (where $projekte "Params.gruppe" $gruppe) "Weight" -}}
<div class="project-grid">
  {{- range $pages }}{{ partial "project-card.html" . }}{{ end }}
</div>
```

- [ ] **Step 4: Create `content/fuer-vereine.md`**

```markdown
+++
title = "Für Vereine"
date = 2026-09-15T10:00:00+02:00
draft = false
menu = "main"
weight = 16
+++

Vereinsarbeit hängt an erstaunlich vielen Zetteln. An der Strichliste an der Theke, an
der Doodle-Umfrage für den nächsten Spieltag, an der Website, die seit drei Jahren
niemand anfassen möchte, an der Basar-Anmeldung, die über WhatsApp läuft und bei der
irgendwann zwei Leute dieselbe Nummer haben. Das funktioniert alles irgendwie — bis es
das nicht mehr tut, und dann sitzt jemand abends da und sortiert es gerade.

Ich baue sowas. Nicht als Firma, sondern weil ich es kann und weil es Spaß macht, wenn
etwas, das man gebaut hat, tatsächlich in einer Turnhalle oder an einer Theke benutzt
wird.

## Was möglich ist

- **Eine Vereinswebsite, die der Vorstand selbst pflegt.** Ohne WordPress, ohne
  Update-Banner, ohne monatliche Kosten fürs Hosting.
- **Die Theke ohne Strichliste.** Ein iPad, das ohnehin schon dasteht, bucht Getränke
  auf Mitglieder — und der Kassenwart bekommt am Monatsende eine Summe statt einer
  Handschriftprobe.
- **Terminabstimmung, die auch eine Aufstellung vorschlägt.** Nicht nur wer kann,
  sondern wer nach Meldeliste spielen sollte.
- **Eine Basar- oder Event-Anmeldung mit Kasse und Abrechnung.** Von der
  Einwilligungserklärung bis zur fertigen Auszahlung je Verkäufernummer.
- **Grafiken für Instagram auf Knopfdruck.** Formular ausfüllen, fertige Ergebnisgrafik
  im Vereinsdesign herausbekommen.

## Bevor ihr fragt: zwei ehrliche Punkte

**Das Bauen ist nicht das Problem.** Eine Vereinswebsite, eine kleine App für die Theke,
ein Anmeldesystem für den Basar — das entsteht meistens an ein paar Abenden, und ich
mache es gerne.

**Das Problem ist das dritte Jahr.** Ein System, das am Basar-Wochenende die Kasse
führt, muss auch nächstes Jahr noch laufen. Updates, Zertifikate, ein Backup, das man
auch wirklich zurückspielen kann — und jemand, der erreichbar ist, wenn samstags um neun
das iPad nicht mehr bucht. Genau daran sterben die meisten Vereinslösungen: Sie werden
gebaut, sie funktionieren, und dann zieht derjenige weg, der sie gebaut hat.

Deshalb rede ich darüber lieber vorher als hinterher. Was ich baue, gehört dem Verein:
Der Quellcode liegt beim Verein, Domain und Zugänge laufen auf den Verein, nicht auf
mich. Laufende Kosten — eine Domain, bei manchen Sachen ein kleiner Server — zahlt der
Verein direkt an den Anbieter. Und wer sich um den laufenden Betrieb kümmert, klären wir
am Anfang gemeinsam; ich helfe dabei, es so zu bauen, dass man dafür kein Informatiker
sein muss.

Ich baue nichts, aus dem man nicht wieder rauskommt. Beim TC Blau-Weiß habe ich eine
WordPress-Seite abgelöst, die langsam war, ständig Updates wollte und die im Vorstand
niemand mehr anfassen mochte. Seitdem steht da eine Seite, die nichts kostet, nichts
kaputtgeht und die zwei Leute im Vorstand selbst pflegen.

## Was schon läuft

{{< projektkarten gruppe="vereine" >}}

## Kontakt

Wenn euch etwas davon bekannt vorkommt, schreibt mir einfach — am besten mit zwei, drei
Sätzen dazu, woran es bei euch gerade hakt. Ich sage auch ehrlich, wenn ich glaube, dass
ihr für euer Problem gar keine Software braucht.

[faffi@gmx.de](mailto:faffi@gmx.de)
```

- [ ] **Step 5: Run the verification**

Run: `./scripts/check_projekte.sh`
Expected: every check `ok`, including „5 cards" and all six commercial-wording guards.

- [ ] **Step 6: Check the menu order**

Run `hugo server` and confirm the header reads: Projekte · Für Vereine · Lebenslauf (weights 15, 16, 20). If PaperMod renders them in a different order, the cause is a missing or duplicated `weight` in the frontmatter — fix the frontmatter, never `hugo.toml`.

- [ ] **Step 7: Stage and propose the commit**

```bash
git add layouts/shortcodes/projektkarten.html content/fuer-vereine.md scripts/check_projekte.sh
git status
```

Proposed message — commit only after approval:

```
feat(vereine): add Für-Vereine page with embedded project references
```

---

### Task 5: Screenshot processing script

**Files:**
- Create: `scripts/shot_to_cover.py`
- Create: `scripts/test_shot_to_cover.py`

**Interfaces:**
- Consumes: nothing from earlier tasks.
- Produces:
  - `crop_to_cover(src: Path, target: Path, size: tuple[int, int] = (1200, 675)) -> None` — centre-crops a landscape capture to the target aspect ratio and writes WebP.
  - `compose_phone_cover(sources: list[Path], target: Path, background: tuple[int, int, int], size: tuple[int, int] = (1200, 675)) -> None` — scales portrait frames to fit the canvas height with a margin, lays them out side by side, centred, on a solid background, and writes WebP.
  - `to_gallery_shot(src: Path, target: Path, height: int = 1400) -> None` — scales a portrait frame down to `height` and writes WebP.

- [ ] **Step 1: Write the failing tests**

`scripts/test_shot_to_cover.py`:

```python
"""Tests for shot_to_cover — pure image functions, no network."""

from pathlib import Path

from PIL import Image

from shot_to_cover import compose_phone_cover, crop_to_cover, to_gallery_shot


def _make(path: Path, size: tuple[int, int], color: tuple[int, int, int]) -> Path:
    Image.new("RGB", size, color).save(path, format="PNG")
    return path


def test_crop_to_cover_produces_exact_size(tmp_path: Path) -> None:
    src = _make(tmp_path / "shot.png", (1440, 900), (10, 20, 30))
    target = tmp_path / "cover.webp"

    crop_to_cover(src, target)

    with Image.open(target) as out:
        assert out.format == "WEBP"
        assert out.size == (1200, 675)


def test_crop_to_cover_keeps_top_of_tall_capture(tmp_path: Path) -> None:
    # A full-page capture is much taller than 16:9; the interesting part is the top.
    src = tmp_path / "tall.png"
    img = Image.new("RGB", (1440, 3000), (255, 255, 255))
    for y in range(300):
        for x in range(0, 1440, 40):
            img.putpixel((x, y), (255, 0, 0))
    img.save(src, format="PNG")
    target = tmp_path / "cover.webp"

    crop_to_cover(src, target)

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        assert (255, 0, 0) in {out.getpixel((x, 5)) for x in range(0, 1200, 10)}


def test_compose_phone_cover_lays_out_three_frames(tmp_path: Path) -> None:
    sources = [
        _make(tmp_path / f"p{i}.png", (1290, 2796), (200, 100, 50)) for i in range(3)
    ]
    target = tmp_path / "cover.webp"

    compose_phone_cover(sources, target, background=(245, 240, 232))

    with Image.open(target) as out:
        assert out.size == (1200, 675)
        # The corners stay background; the middle carries a frame.
        assert out.getpixel((2, 2)) == (245, 240, 232)
        assert out.getpixel((600, 337)) != (245, 240, 232)


def test_to_gallery_shot_scales_by_height(tmp_path: Path) -> None:
    src = _make(tmp_path / "p.png", (1290, 2796), (0, 0, 0))
    target = tmp_path / "shot-1.webp"

    to_gallery_shot(src, target, height=1400)

    with Image.open(target) as out:
        assert out.height == 1400
        assert out.width == 645
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `cd scripts && uv run --with pillow --with pytest pytest test_shot_to_cover.py -v`
Expected: collection error, `ModuleNotFoundError: No module named 'shot_to_cover'`.

- [ ] **Step 3: Write `scripts/shot_to_cover.py`**

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "Pillow>=10.4",
# ]
# ///
"""Turn raw screenshots into portfolio cover images.

Usage:
    uv run scripts/shot_to_cover.py crop    shot.png content/projekte/basar/cover.webp
    uv run scripts/shot_to_cover.py phones  content/projekte/mai-tasting/cover.webp \
        --background "#F5F0E8" a.png b.png c.png
    uv run scripts/shot_to_cover.py gallery a.png content/projekte/mai-tasting/shot-1.webp
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image

COVER_SIZE = (1200, 675)
WEBP_QUALITY = 82


def _save(img: Image.Image, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    img.save(target, format="WEBP", quality=WEBP_QUALITY, method=6)


def crop_to_cover(
    src: Path, target: Path, size: tuple[int, int] = COVER_SIZE
) -> None:
    """Scale a landscape capture to the target width, then crop from the top."""
    with Image.open(src) as img:
        rgb = img.convert("RGB")
        scale = size[0] / rgb.width
        scaled = rgb.resize(
            (size[0], max(size[1], round(rgb.height * scale))), Image.LANCZOS
        )
        cover = scaled.crop((0, 0, size[0], size[1]))
    # Saved outside the with-block so src may be the same path as target.
    _save(cover, target)


def compose_phone_cover(
    sources: list[Path],
    target: Path,
    background: tuple[int, int, int],
    size: tuple[int, int] = COVER_SIZE,
) -> None:
    """Lay portrait frames side by side, centred, on a solid background."""
    if not sources:
        raise ValueError("compose_phone_cover needs at least one source")

    margin = round(size[1] * 0.08)
    gap = round(size[0] * 0.02)
    frame_height = size[1] - 2 * margin

    frames = []
    for src in sources:
        with Image.open(src) as img:
            img = img.convert("RGB")
            width = round(img.width * frame_height / img.height)
            frames.append(img.resize((width, frame_height), Image.LANCZOS))

    total = sum(f.width for f in frames) + gap * (len(frames) - 1)
    if total > size[0] - 2 * margin:
        shrink = (size[0] - 2 * margin - gap * (len(frames) - 1)) / sum(
            f.width for f in frames
        )
        frames = [
            f.resize((round(f.width * shrink), round(f.height * shrink)), Image.LANCZOS)
            for f in frames
        ]
        total = sum(f.width for f in frames) + gap * (len(frames) - 1)

    canvas = Image.new("RGB", size, background)
    x = (size[0] - total) // 2
    for frame in frames:
        canvas.paste(frame, (x, (size[1] - frame.height) // 2))
        x += frame.width + gap

    _save(canvas, target)


def to_gallery_shot(src: Path, target: Path, height: int = 1400) -> None:
    """Scale a portrait frame to a fixed height for the detail-page gallery."""
    with Image.open(src) as img:
        img = img.convert("RGB")
        width = round(img.width * height / img.height)
        _save(img.resize((width, height), Image.LANCZOS), target)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="mode", required=True)

    p_crop = sub.add_parser("crop", help="landscape capture -> 16:9 cover")
    p_crop.add_argument("src", type=Path)
    p_crop.add_argument("target", type=Path)

    p_phones = sub.add_parser("phones", help="portrait frames -> 16:9 cover")
    p_phones.add_argument("target", type=Path)
    p_phones.add_argument("sources", type=Path, nargs="+")
    p_phones.add_argument("--background", default="#F5F0E8")

    p_gallery = sub.add_parser("gallery", help="portrait frame -> gallery image")
    p_gallery.add_argument("src", type=Path)
    p_gallery.add_argument("target", type=Path)
    p_gallery.add_argument("--height", type=int, default=1400)

    args = parser.parse_args()

    if args.mode == "crop":
        crop_to_cover(args.src, args.target)
    elif args.mode == "phones":
        compose_phone_cover(
            args.sources, args.target, background=_hex_to_rgb(args.background)
        )
    else:
        to_gallery_shot(args.src, args.target, height=args.height)

    print(f"wrote {args.target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `cd scripts && uv run --with pillow --with pytest pytest test_shot_to_cover.py -v`
Expected: 4 passed.

- [ ] **Step 5: Lint**

Run: `uv run ruff check scripts/shot_to_cover.py scripts/test_shot_to_cover.py`
Expected: `All checks passed!`

- [ ] **Step 6: Stage and propose the commit**

```bash
git add scripts/shot_to_cover.py scripts/test_shot_to_cover.py
git status
```

Proposed message — commit only after approval:

```
feat(scripts): add screenshot-to-cover processing
```

---

### Task 6: Capture the publicly reachable systems

**Files:**
- Create: `content/projekte/kinderbasar/cover.webp`
- Create: `content/projekte/tcbw-website/cover.webp`
- Create: `content/projekte/wippestoolen/cover.webp`

**Interfaces:**
- Consumes: `crop_to_cover` from Task 5; the `cover.image` frontmatter from Tasks 1–3.
- Produces: three real cover images; the `.project-card-cover--empty` placeholder disappears for these three cards.

- [ ] **Step 1: Verify the three targets still answer**

```bash
for url in https://basar.faffi.cloud/anmeldung https://tc-bw-attendorn.de https://wippestoolen.vercel.app; do
  printf "%-45s %s\n" "$url" "$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "$url")"
done
```

Expected: `200` three times. If one is not 200, skip that project here and give it a generated cover in Task 9 instead.

- [ ] **Step 2: Capture with Playwright**

For each URL: `browser_resize` to 1440 × 900, `browser_navigate`, wait for the page to settle, dismiss any cookie banner if one appears, then `browser_take_screenshot` (viewport only, not full page) into the scratchpad directory as `basar.png`, `tcbw.png`, `wippestoolen.png`.

**Privacy:** `https://basar.faffi.cloud/anmeldung` is the public registration form and holds no personal data. Do not navigate to any `/orga/*` path.

- [ ] **Step 3: Convert to covers**

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/basar.png"         content/projekte/kinderbasar/cover.webp
uv run scripts/shot_to_cover.py crop "$SCRATCH/tcbw.png"          content/projekte/tcbw-website/cover.webp
uv run scripts/shot_to_cover.py crop "$SCRATCH/wippestoolen.png"  content/projekte/wippestoolen/cover.webp
```

(`$SCRATCH` is the session scratchpad directory.)

- [ ] **Step 4: Verify the images landed and are the right shape**

```bash
uv run --with pillow python -c "
from pathlib import Path
from PIL import Image
for p in Path('content/projekte').glob('*/cover.webp'):
    with Image.open(p) as im:
        print(p, im.format, im.size)
        assert im.format == 'WEBP' and im.size == (1200, 675), p
"
```

Expected: three lines, each `WEBP (1200, 675)`, no assertion error.

- [ ] **Step 5: Rebuild and check**

Run: `./scripts/check_projekte.sh`
Expected: all checks `ok`.

Then: `grep -o 'project-card-cover--empty' public/projekte/index.html | wc -l`
Expected: `8` (eleven cards minus the three now covered).

- [ ] **Step 6: Stage and propose the commit**

```bash
git add content/projekte/*/cover.webp
git status
```

Proposed message — commit only after approval:

```
feat(projekte): add screenshots for the publicly reachable projects
```

---

### Task 7: Capture the locally runnable systems

Each sub-step is independent: if one application will not start within a few minutes, note it, move on, and let Task 9 generate a fallback cover for it. Do not spend time debugging someone else's project.

**Files:**
- Create: `content/projekte/tcbw-social-tools/cover.webp`
- Create: `content/projekte/doko-stats/cover.webp`
- Create: `content/projekte/medenspiel-planner/cover.webp`
- Create: `content/projekte/narraitive/cover.webp`
- Create: `content/projekte/tcbw-getraenkebuchung/cover.webp`

**Interfaces:**
- Consumes: `crop_to_cover` from Task 5.
- Produces: up to five more real covers.

- [ ] **Step 1: Social-Tools**

```bash
cd ~/PycharmProjects/tcbw-social-tools && npm install && npm run dev
```

The sibling repo `~/PycharmProjects/tcbw-homepage` is already checked out, which the prebuild step needs. Capture the form view at 1440 × 900, then:

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/social.png" content/projekte/tcbw-social-tools/cover.webp
```

- [ ] **Step 2: doko-stats**

The prebuilt dashboard is at `~/doko-stats/dashboard.html`. **Before capturing, confirm no player name is visible.** Open it with Playwright via `file:///Users/woerenkaemper/doko-stats/dashboard.html`, and pick a view that shows aggregate charts rather than the per-player ranking. If every view names players, skip this capture — Task 9 generates a cover instead.

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/doko.png" content/projekte/doko-stats/cover.webp
```

- [ ] **Step 3: Medenspiel-Planner**

```bash
cd ~/PycharmProjects/medenspiel-planner && uv sync && uv run uvicorn medenspiel.web.app:app --reload
```

Open `http://localhost:8000/setup/<token>` as described in that repo's README to seed data. **Use the seeded import only — do not capture a view containing a real squad list.** Capture the player availability view, which is the interesting screen.

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/medenspiel.png" content/projekte/medenspiel-planner/cover.webp
```

- [ ] **Step 4: NarrAItive**

```bash
cd ~/PycharmProjects/NarrAItive && uv run streamlit run app.py
```

The local `narrAItive_duckDB.duckdb` holds existing books, so the library view renders without any API key. Capture that view; do not trigger a generation run.

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/narraitive.png" content/projekte/narraitive/cover.webp
```

- [ ] **Step 5: Getränkebuchung in the iPad simulator**

```bash
xcrun simctl boot "iPad Pro 11-inch (M5)"
open -a Simulator
cd ~/PycharmProjects/tcbw-getraenkebuchung
xcodebuild -list                 # read the scheme name from the "Schemes:" block
xcodebuild -scheme "$SCHEME" -destination 'platform=iOS Simulator,name=iPad Pro 11-inch (M5)' build
```

If the build needs a CloudKit entitlement or a signing identity that is not available, stop and use the existing cover instead:

```bash
cp content/posts/tcbw-getraenkebuchung/cover.webp content/projekte/tcbw-getraenkebuchung/cover.webp
```

Otherwise capture the kiosk screen with `xcrun simctl io booted screenshot "$SCRATCH/ipad.png"` and convert:

```bash
uv run scripts/shot_to_cover.py crop "$SCRATCH/ipad.png" content/projekte/tcbw-getraenkebuchung/cover.webp
```

- [ ] **Step 6: Verify every image written so far**

```bash
uv run --with pillow python -c "
from pathlib import Path
from PIL import Image
for p in sorted(Path('content/projekte').glob('*/cover.webp')):
    with Image.open(p) as im:
        assert im.format == 'WEBP' and im.size == (1200, 675), (p, im.size)
        print('ok', p)
"
```

- [ ] **Step 7: Rebuild and report which projects still lack a cover**

```bash
./scripts/check_projekte.sh
for d in content/projekte/*/; do
  [ -f "$d/cover.webp" ] || echo "no cover yet: $d"
done
```

- [ ] **Step 8: Stage and propose the commit**

```bash
git add content/projekte/*/cover.webp
git status
```

Proposed message — commit only after approval:

```
feat(projekte): add screenshots captured from local runs
```

---

### Task 8: mAI Tasting cover and gallery

**Files:**
- Create: `content/projekte/mai-tasting/cover.webp`
- Create: `content/projekte/mai-tasting/shot-1.webp`
- Create: `content/projekte/mai-tasting/shot-2.webp`
- Create: `content/projekte/mai-tasting/shot-3.webp`
- Create: `content/projekte/mai-tasting/shot-4.webp`
- Modify: `scripts/check_projekte.sh`

**Interfaces:**
- Consumes: `compose_phone_cover` and `to_gallery_shot` from Task 5; the `shot-*.webp` gallery block in `layouts/projekte/single.html` from Task 1.
- Produces: the only page that exercises the gallery markup.

Source frames (1290 × 2796, already polished for the App Store):
`~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots/01-sammlung.png`, `02-ki-verkostung.png`, `03-geschmacksprofil.png`, and `~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Wine-Screeenshots/` (note the repo's spelling with three `e`) for one wine frame.

- [ ] **Step 1: Extend the verification**

Add above `exit $fail`:

```bash
check public/projekte/mai-tasting/index.html 'project-gallery' 'mAI Tasting renders the gallery'
```

- [ ] **Step 2: Run it to verify it fails**

Run: `./scripts/check_projekte.sh`
Expected: the new check `FAIL` — no `shot-*.webp` resources exist yet.

- [ ] **Step 3: Confirm the source files and read the background colour**

```bash
ls ~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots/
ls ~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Wine-Screeenshots/
uv run --with pillow python -c "
from PIL import Image
p='/Users/woerenkaemper/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots/01-sammlung.png'
with Image.open(p) as im: print('background pixel:', im.convert('RGB').getpixel((5,5)))
"
```

Use the printed RGB value as the `--background` for the compose step, so the cover matches the frames instead of sitting on an arbitrary colour.

- [ ] **Step 4: Build the cover from three whisky frames**

```bash
S=~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots
uv run scripts/shot_to_cover.py phones content/projekte/mai-tasting/cover.webp \
  --background "#<value from step 3>" \
  "$S/01-sammlung.png" "$S/02-ki-verkostung.png" "$S/03-geschmacksprofil.png"
```

- [ ] **Step 5: Build the four gallery images**

```bash
S=~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Whisky-Screenshots
W=~/PycharmProjects/whisky-api/uploads/Screenshots/Claude-Design-Wine-Screeenshots
uv run scripts/shot_to_cover.py gallery "$S/01-sammlung.png"       content/projekte/mai-tasting/shot-1.webp
uv run scripts/shot_to_cover.py gallery "$S/02-ki-verkostung.png"  content/projekte/mai-tasting/shot-2.webp
uv run scripts/shot_to_cover.py gallery "$S/03-geschmacksprofil.png" content/projekte/mai-tasting/shot-3.webp
uv run scripts/shot_to_cover.py gallery "$W/$(ls $W | head -1)"    content/projekte/mai-tasting/shot-4.webp
```

- [ ] **Step 6: Run the verification**

Run: `./scripts/check_projekte.sh`
Expected: all checks `ok`, including the gallery check.

- [ ] **Step 7: Look at the result**

Open `http://localhost:1313/projekte/mai-tasting/` at 1440px and at 390px. The gallery must scroll horizontally on the phone rather than squashing the frames, and the card cover on `/projekte/` must show three readable phones, not three slivers.

- [ ] **Step 8: Stage and propose the commit**

```bash
git add content/projekte/mai-tasting/ scripts/check_projekte.sh
git status
```

Proposed message — commit only after approval:

```
feat(projekte): add mAI Tasting App-Store frames as cover and gallery
```

---

### Task 9: Fallback covers and the final pass

**Files:**
- Modify: `scripts/generate_covers.py` (add the missing slugs to `SLUG_PROMPTS`, and let it target `content/projekte/` as well)
- Create: any still-missing `content/projekte/*/cover.webp`
- Modify: `README.md`

**Interfaces:**
- Consumes: everything above.
- Produces: a complete portfolio with no empty cover placeholders.

- [ ] **Step 1: List what is still missing**

```bash
for d in content/projekte/*/; do [ -f "$d/cover.webp" ] || echo "${d#content/projekte/}"; done
```

Expected at minimum: `mytapo/` and `solar-prediction/` (NAS-only, home network required), plus anything Task 7 had to skip.

- [ ] **Step 2: Re-use existing post covers where one exists**

```bash
[ -f content/projekte/mytapo/cover.webp ] || cp content/posts/Tapo/cover.webp content/projekte/mytapo/cover.webp
[ -f content/projekte/narraitive/cover.webp ] || cp content/posts/NarrAItive/NarrAItive_logo.webp content/projekte/narraitive/cover.webp
[ -f content/projekte/wippestoolen/cover.webp ] || cp content/posts/wippestoolen/cover.webp content/projekte/wippestoolen/cover.webp
[ -f content/projekte/tcbw-website/cover.webp ] || cp content/posts/tcbw-website/cover.webp content/projekte/tcbw-website/cover.webp
```

These are not 1200 × 675, so normalise them:

```bash
for f in content/projekte/*/cover.webp; do
  uv run scripts/shot_to_cover.py crop "$f" "$f"
done
```

- [ ] **Step 3: Generate the remaining covers**

In `scripts/generate_covers.py`, add to `SLUG_PROMPTS`:

```python
    "solar-prediction": (
        "solar panels under a forecast sky, a rising prediction curve overlaid, "
        "hourly bars beneath it"
    ),
    "doko-stats": (
        "abstract playing cards fanned out, turning into a bar chart, "
        "no faces, no text, no suits that resemble a real brand"
    ),
```

and add a `--section` flag so the script can write into `content/projekte/<slug>/cover.webp` instead of `content/posts/<slug>/cover.webp`:

```python
def cover_path(slug: str, section: str = "posts") -> Path:
    return REPO_ROOT / "content" / section / slug / "cover.webp"
```

Update the two call sites of `cover_path` in `main()` to pass `args.section`, and add:

```python
    parser.add_argument(
        "--section", default="posts", choices=["posts", "projekte"],
        help="Content section to write covers into",
    )
```

Then run, only for the slugs that still have no cover:

```bash
uv run scripts/generate_covers.py --section projekte --slug solar-prediction
uv run scripts/generate_covers.py --section projekte --slug doko-stats
```

Cost: roughly $0.04 per image.

- [ ] **Step 4: Update the existing cover test**

`scripts/test_generate_covers.py` must still pass with the new signature. Add:

```python
def test_cover_path_targets_the_requested_section() -> None:
    from generate_covers import cover_path

    assert cover_path("doko-stats", "projekte").parts[-3:] == (
        "projekte",
        "doko-stats",
        "cover.webp",
    )
    assert cover_path("Tapo").parts[-3:] == ("posts", "Tapo", "cover.webp")
```

Run: `cd scripts && uv run --with pillow --with pytest --with openai --with python-dotenv pytest -v`
Expected: all tests pass.

- [ ] **Step 5: Confirm every project has a normalised cover**

```bash
uv run --with pillow python -c "
from pathlib import Path
from PIL import Image
dirs = sorted(p for p in Path('content/projekte').iterdir() if p.is_dir())
assert len(dirs) == 11, len(dirs)
for d in dirs:
    f = d / 'cover.webp'
    assert f.exists(), f
    with Image.open(f) as im:
        assert im.size == (1200, 675), (f, im.size)
print('all 11 covers present and normalised')
"
```

- [ ] **Step 6: Full verification pass**

```bash
./scripts/check_projekte.sh
grep -o 'project-card-cover--empty' public/projekte/index.html | wc -l
```

Expected: every check `ok`; the placeholder count is `0`.

- [ ] **Step 7: Check every internal link resolves**

```bash
grep -oh 'href="/[^"]*"' public/projekte/*/index.html public/fuer-vereine/index.html \
  | sed 's/href="//;s/"$//' | sort -u | while read -r p; do
    f="public${p%/}/index.html"
    [ -f "$f" ] || [ -f "public${p}" ] || echo "BROKEN: $p"
  done
```

Expected: no `BROKEN` lines. In particular `/posts/tapo/`, `/posts/narraitive/`, `/posts/mai-tasting/`, `/posts/wippestoolen/`, `/posts/tcbw-website/` and `/posts/tcbw-getraenkebuchung/` must all resolve — Hugo lowercases paths by default, so the `NarrAItive` and `Tapo` folders become `/posts/narraitive/` and `/posts/tapo/`.

- [ ] **Step 8: Visual pass over all three surfaces**

With `hugo server` running, use Playwright to view `/projekte/`, `/projekte/kinderbasar/`, `/projekte/mai-tasting/` and `/fuer-vereine/`, each at 1440px and 390px, and each in light and dark mode — eight to sixteen views. Look for: cards of equal height in a row, no horizontal page scroll at 390px, badge text legible on both backgrounds, gallery scrolling rather than overflowing, menu fitting on one line at 390px.

- [ ] **Step 9: Update the README**

In `README.md`, under the "About" list, add a line documenting the new section:

```markdown
- **Portfolio:** project pages live in `content/projekte/` (one page bundle each, see
  `docs/superpowers/specs/2026-09-15-portfolio-vereine-design.md` for the frontmatter
  schema). `scripts/check_projekte.sh` builds the site and asserts they render.
```

- [ ] **Step 10: Stage and propose the final commit**

```bash
git add content/projekte/ scripts/ README.md
git status
```

Proposed message — commit only after approval:

```
feat(projekte): complete portfolio covers and verification
```

---

## Notes for the executor

- **If a capture is impossible today**, do not block. Generate or re-use a cover, and note in the final report which projects deserve a real screenshot later. Two of them (MyTapo, Solar Prediction) run on the NAS and are only reachable from the home network — that is expected.
- **If `hugo --gc --minify` warns** about anything, treat it as a failure. Cloudflare Pages builds with the same version and a warning today is a broken deploy tomorrow.
- **Never edit** `themes/PaperMod/`. If a template needs a partial that does not exist, write it under `layouts/partials/`.
- **The user reviews before every commit.** Do not run `git commit` unprompted, and never `git push`.
