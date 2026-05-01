# Blog & Lebenslauf Update Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Translate and expand `content/lebanslauf.md` to match the new English CV (`~/Downloads/CV/cv_wk_24.tex`); publish 5 German blog posts about the user's 2026 portfolio repos (mytapo, wippestoolen, tcbw-website, tcbw-getraenkebuchung, mai-tasting); generate consistent cover images via OpenAI `gpt-image-1`.

**Architecture:** Hugo static site (PaperMod theme). Each post lives in `content/posts/<slug>/index.md` with a co-located `cover.webp`. A standalone Python script `scripts/generate_covers.py` (PEP 723 inline deps, runnable with `uv run`) reads `OPENAI_API_KEY` from `.env`, calls `gpt-image-1`, and writes WebP covers per slug. All commits batched at the end of the workflow per spec.

**Tech Stack:** Hugo 0.146.0+, Python 3.13 (uv), OpenAI SDK, Pillow, python-dotenv. Cloudflare Pages hosting (no infra changes in scope).

**Spec:** `docs/superpowers/specs/2026-05-01-blog-cv-update-design.md`

---

## File Structure

**Create:**
- `content/posts/wippestoolen/index.md`
- `content/posts/tcbw-website/index.md`
- `content/posts/tcbw-getraenkebuchung/index.md`
- `content/posts/mai-tasting/index.md`
- `scripts/generate_covers.py`
- `scripts/test_generate_covers.py` (small unit test for non-API logic)
- `content/posts/Tapo/cover.webp` (regenerated)
- `content/posts/wippestoolen/cover.webp`
- `content/posts/tcbw-website/cover.webp`
- `content/posts/tcbw-getraenkebuchung/cover.webp`
- `content/posts/mai-tasting/cover.webp`

**Modify:**
- `content/lebanslauf.md` (full replacement of body; preserve frontmatter keys)
- `content/posts/Tapo/index.md` (full replacement of body; preserve directory; new frontmatter date 2026-03-27)
- `doc/tasks/context_session_01.md` (progress log)

**Touch (verify, no changes):**
- `.gitignore` — must already contain `.env` (verified during brainstorming)
- `hugo.toml` — must not need changes; verify build still passes

---

## Conventions used throughout

**Post frontmatter template (TOML)** — every new post uses this exact shape:

```toml
+++
date = '<YYYY-MM-DD>T<HH:MM>:00+02:00'
draft = false
title = '<Titel mit optionalem Emoji>'
cover.image = "cover.webp"
cover.alt = "<alt>"
cover.caption = "<caption>"
cover.relative = true
tags = ["<Tag1>", "<Tag2>", "<Tag3>"]
+++
```

**Date assignments** (all Fridays, all in the past):

| Slug | Date |
|------|------|
| `posts/Tapo/` | `2026-03-27T10:00:00+02:00` |
| `posts/wippestoolen/` | `2026-04-03T10:00:00+02:00` |
| `posts/tcbw-website/` | `2026-04-10T10:00:00+02:00` |
| `posts/tcbw-getraenkebuchung/` | `2026-04-17T10:00:00+02:00` |
| `posts/mai-tasting/` | `2026-04-24T10:00:00+02:00` |

**Word target per post:** 600–1000 Wörter. Mostly the upper end for technical posts (mytapo, mai-tasting), lower end for narrative (tcbw-website).

**Privacy discipline (private repos):** No code snippets, no internal endpoint paths, no internal table/column names, no domain names not already public. Only public references allowed: `maitasting.app`, `tc-bw-attendorn.de`, `wippestoolen.vercel.app`.

**No commits until Task 10.** Each per-content task ends with verification, not commit.

---

## Task 1: Update Lebenslauf

**Files:**
- Modify: `/Users/woerenkaemper/PycharmProjects/faffis-blog/content/lebanslauf.md` (full body replacement)
- Reference (read-only): `/Users/woerenkaemper/Downloads/CV/cv_wk_24.tex`, `/Users/woerenkaemper/Downloads/CV/linkedin_about_de.md`

- [ ] **Step 1: Read source TEX and current Lebenslauf**

```bash
# Use Read tool on:
# /Users/woerenkaemper/Downloads/CV/cv_wk_24.tex
# /Users/woerenkaemper/PycharmProjects/faffis-blog/content/lebanslauf.md
# /Users/woerenkaemper/Downloads/CV/linkedin_about_de.md
```

- [ ] **Step 2: Compose new body following the section list from the spec**

Sections in this exact order:
1. Header block (Name, role, contact) — keep current style with markdown line breaks (`\`)
2. **Über mich** — fresh German prose blending current Über-mich tone with the LinkedIn-About honesty (Familie, "lieber rough POC heute Abend als Hype-Framework morgen", Allergie gegen Konsens-Theater)
3. **Tools, Technologien & Fähigkeiten** — emoji-bulleted list mirroring current style; updated with: Python, SQL, TypeScript, Swift, C++; FastAPI, SQLAlchemy, React Native, SwiftUI, Hugo; AWS (S3, ECR, ECS, Sagemaker, Bedrock, Timestream), Railway, Cloudflare Pages; Databricks (Unity Catalog, Delta Lake, PySpark, Workflows); IaC (OpenTofu, Serverless Framework); MLflow, Huggingface; OpenAI, Anthropic, Bedrock, Groq, Ollama, Deepeval; Claude Code (Skills, Hooks, MCP, Sub-Agents)
4. **Berufserfahrung** — chronological reverse:
   - Seit 2026: Senior Full Stack Data Scientist @ Krombacher KSA (Promotion 01/2026; agentische Workflows als Multiplikator; AWS + Databricks ML/GenAI)
   - 2022 – 2025: Data Scientist @ Krombacher KSA (Klippa-Replacement-PoC mit AWS Textract + Bedrock Claude 3.5 Sonnet, Deepeval — −80 % Kosten, +16 % Detection Quality; Databricks Unity Catalog/Delta Lake; OpenTofu IaC)
   - 2020 – 2022: Data Scientist @ Bosch Rexroth, Big Data and Simulation
   - 2016 – 2020: Promotionsstudent @ Bosch Rexroth, CoC Strömungs- und Strukturmechanik
   - 2012 – 2016: Entwicklungsingenieur @ Bosch Rexroth, Ventilentwicklung
5. **Personal Projects** (NEW) — five entries:
   - 2026 — mAI Tasting (Whisky & Wine) — FastAPI, React Native, OpenAI GPT-4o, Railway → link `/posts/mai-tasting/` und `https://maitasting.app`
   - 2026 — Drink-Booking iPad App — Swift, SwiftUI, SwiftData, CloudKit → link `/posts/tcbw-getraenkebuchung/`
   - 2026 — TC Blau-Weiß Website — Hugo, DecapCMS, Cloudflare Pages → link `/posts/tcbw-website/` und `https://tc-bw-attendorn.de`
   - 2024 – heute — MyTapo Energy Monitoring — Python, InfluxDB, Grafana, Docker → link `/posts/Tapo/`
   - 2024 — AI Picture Book — GPT-4, DALL-E 3, ElevenLabs → link `/posts/NarrAItive/`
6. **Talks & Publications** (NEW) — INWT Data Science Deep Dive #88 (02/2026) → link `https://www.podbean.com/ew/pb-apyrq-1a577b8`, "Anomalie-Erkennung im Loyalty-Programm bei Krombacher" — Trust-Score-Modellierung mit Isolation Forest, Feature Engineering, tägliche Update-Infrastruktur auf Databricks
7. **Ausbildung** — only:
   - 2016 – 2020: Promotion in Simulationsmethoden @ Bosch Rexroth
   - 2006 – 2012: Computational Engineering Science @ RWTH Aachen (Schwerpunkt Verbrennung & Strömungsmechanik; Diplomarbeit 1.3; Abschlussnote 1.9)
8. **Sprachen** — Deutsch (Muttersprache); Englisch (Fließend); Spanisch (Grundkenntnisse); Französisch (Grundkenntnisse)
9. **Off the Clock** — Bundesliga (BVB); Tennis (TC Blau-Weiß Attendorn); Kochen für Freunde; Krombacher field-testing; eSports

**Removed sections** (do not include): Praktika & Studentenjobs, Soft Skills, Hard Skills, "Interessen" header (replaced by "Off the Clock").

**Frontmatter to preserve:** keep keys `title`, `draft`, `menu`, `weight`, `tags`, `birth_date_daughter`, `birth_date_son`. **Update** `date` to `2026-05-01T10:00:00+02:00`.

- [ ] **Step 3: Write the new body via Edit/Write tool**

Use `Write` tool (full file replacement is cleaner than many Edits here). Path: `content/lebanslauf.md`. Keep the `+++` frontmatter at top with updated `date`.

- [ ] **Step 4: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-cv
```
Expected: exits 0, no warnings about `lebanslauf.md`.

- [ ] **Step 5: Update context session log**

Append to `doc/tasks/context_session_01.md`:
```markdown
### 2026-05-01
- Lebenslauf updated with new TEX content (Senior promotion 01/2026, Personal Projects, Podcast)
```

---

## Task 2: mytapo Post (replaces existing Tapo post)

**Files:**
- Modify: `content/posts/Tapo/index.md` (full body replacement; keep file path)
- Reference: GitHub repo `ElGarno/MyTapo` (public)

- [ ] **Step 1: Inspect repo for facts**

```bash
gh api repos/ElGarno/MyTapo/contents/EVENT_DETECTION.md --jq '.content' | base64 -d > /tmp/mytapo_event_detection.md
gh api repos/ElGarno/MyTapo/contents/README.md --jq '.content' | base64 -d > /tmp/mytapo_readme.md
gh api repos/ElGarno/MyTapo/contents/event_detector.py --jq '.content' | base64 -d > /tmp/mytapo_event_detector.py
gh api repos/ElGarno/MyTapo/contents/awtrix_client.py --jq '.content' | base64 -d > /tmp/mytapo_awtrix.py
gh api repos/ElGarno/MyTapo/contents/docker-compose.synology.yml --jq '.content' | base64 -d > /tmp/mytapo_compose.yml
```

Read those files (Read tool) and extract:
- Schwellwert/Hysterese-Werte für Event-Detection
- Geräteliste (Espresso, Waschmaschine, Trockner, Solar, ...)
- AWTRIX-Endpunkt-URL und Payload-Struktur
- Service-Topologie aus docker-compose

- [ ] **Step 2: Write post body**

Frontmatter:
```toml
+++
date = '2026-03-27T10:00:00+02:00'
draft = false
title = '⚡ MyTapo: Event-Detection statt Energiemonitoring'
cover.image = "cover.webp"
cover.alt = "MyTapo Event-Detection Pipeline"
cover.caption = "Von Stromverbrauch zu Geräte-Events"
cover.relative = true
tags = ["Tapo", "Energiemonitoring", "InfluxDB", "Grafana", "AWTRIX", "Docker", "Synology"]
+++
```

Body sections (in order):
1. **Hook** (~100 Wörter) — warum Monitoring allein zu wenig ist; Schritt von "wir messen Strom" zu "wir wissen, wann die Waschmaschine fertig ist"
2. **Architektur-Überblick** (~150 Wörter) — P110 → Python-Collector (uv-Skript) → InfluxDB → Grafana + AWTRIX-Pixel-Clock + Pushover; alle Services in Docker auf Synology NAS; ASCII-Diagramm oder Mermaid-Block (nutze Mermaid wenn vom Theme unterstützt, sonst Code-Fence-Diagramm)
3. **Event-Detection-Logik** (~250 Wörter) — Schwellwert mit Hysterese, 5-Minuten-Cooldown nach Start, Geräte-Klassifikation aus Verbrauchs-Fingerprint, Beispiel-Snippet aus dem öffentlichen Repo (z.B. Klassifikations-Funktion oder Threshold-Konstanten)
4. **AWTRIX-Pixel-Clock-Integration** (~150 Wörter) — was AWTRIX ist; HTTP-API-Aufruf-Beispiel; live-Anzeige aktueller Verbräuche/Events
5. **Solar-Integration & Spar-Logik** (~100 Wörter) — wie Solar-Daten gegen Verbrauch verrechnet werden; Optimierungs-Hinweise (Waschen wenn Sonne)
6. **Lessons Learned** (~100 Wörter) — TP-Link-Auth-Quirks (klartextübertragen, Sessions), Rate-Limits, Synology-Quirks
7. **Fazit + siehe-auch-Block** (~50 Wörter) — Verlinkung NarrAItive/Tapo-Stack-Posts

Code-Snippets erlaubt (Repo public). Quellen-Link: `https://github.com/ElGarno/MyTapo`.

- [ ] **Step 3: Replace existing index.md**

Use `Write` tool on `content/posts/Tapo/index.md`. Old `blog_tapo_energy.webp` reference removed (cover.webp will be generated by script). Existing webp file not removed yet — Task 8 will overwrite it via `cover.webp` (different filename — old one becomes orphan; remove in Step 4 below).

- [ ] **Step 4: Remove orphan cover image**

```bash
rm /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/Tapo/blog_tapo_energy.webp
```

- [ ] **Step 5: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-tapo
```
Expected: exits 0. Note: cover.webp doesn't exist yet — Hugo may warn about missing image; that's fine, ignore for now.

---

## Task 3: wippestoolen Post

**Files:**
- Create: `content/posts/wippestoolen/index.md`
- Reference: GitHub repo `ElGarno/Wippestoolen` (private — no code snippets in post)

- [ ] **Step 1: Inspect repo for high-level facts**

```bash
gh api repos/ElGarno/Wippestoolen/contents/README.md --jq '.content' | base64 -d > /tmp/wippe_readme.md
gh api repos/ElGarno/Wippestoolen/contents/CLAUDE.md --jq '.content' | base64 -d > /tmp/wippe_claude.md 2>/dev/null || true
gh api repos/ElGarno/Wippestoolen/contents/docs --jq '.[].name' 2>&1 || true
gh api repos/ElGarno/Wippestoolen/contents/docker-compose.yml --jq '.content' | base64 -d > /tmp/wippe_compose.yml
```

Extract: feature list, architectural layers (FastAPI, Postgres, Redis, S3), deployment (Railway/Vercel/landing). Public references allowed: `wippestoolen.vercel.app`. **No** internal endpoint paths or table/column names.

- [ ] **Step 2: Write post body**

```bash
mkdir -p /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/wippestoolen
```

Frontmatter:
```toml
+++
date = '2026-04-03T10:00:00+02:00'
draft = false
title = '🔧 Wippestoolen: Werkzeug-Sharing für die Nachbarschaft'
cover.image = "cover.webp"
cover.alt = "Wippestoolen Tool-Sharing-Plattform"
cover.caption = "Nachbarschaftshilfe als Plattform"
cover.relative = true
tags = ["Wippestoolen", "FastAPI", "Postgres", "Sharing-Economy", "Plattform"]
+++
```

Body sections:
1. **Hook** (~100 Wörter) — warum Werkzeuge die meiste Zeit ungenutzt im Keller liegen; Sharing-Ansatz für die Straße
2. **Konzept** (~150 Wörter) — was die Plattform macht: Tool-Listings, Bookings, Trust-Scores, Map-Suche
3. **High-Level-Architektur** (~200 Wörter) — Beschreibung **ohne** internen Code:
   - Backend: FastAPI + SQLAlchemy + Postgres + Redis (Caching) + S3 (Bilder)
   - Frontend (Vercel) + Mobile + Landing
   - Auth: JWT mit Email-Verifizierung
   - Deployment: Railway (Backend) + Vercel (Frontend)
   - ASCII/Mermaid-Block mit groben Boxen (Browser → Vercel → Railway-API → Postgres/Redis/S3)
4. **Trust-System** (~150 Wörter) — wie Mutual Reviews & Ratings funktionieren; warum es entscheidend für Sharing-Economy ist
5. **Booking-Flow** (~150 Wörter) — Status-Maschine: request → approve → in-use → returned → reviewed; Edge-Cases (Storno, No-Show)
6. **Status & Roadmap** (~100 Wörter) — wo's gerade steht (privat, in Entwicklung), nächste Schritte
7. **Fazit** (~50 Wörter)

Quellen-Link: `https://wippestoolen.vercel.app` (Landing).

- [ ] **Step 3: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-wippe
```
Expected: exits 0.

---

## Task 4: tcbw-website Post

**Files:**
- Create: `content/posts/tcbw-website/index.md`
- Reference: GitHub repo `ElGarno/tcbw-homepage` (public)

- [ ] **Step 1: Inspect repo**

```bash
gh api repos/ElGarno/tcbw-homepage/contents/README.md --jq '.content' | base64 -d > /tmp/tcbw_readme.md
gh api repos/ElGarno/tcbw-homepage/contents/CLAUDE.md --jq '.content' | base64 -d > /tmp/tcbw_claude.md 2>/dev/null || true
gh api repos/ElGarno/tcbw-homepage/contents/hugo.toml --jq '.content' | base64 -d > /tmp/tcbw_hugo.toml
gh api repos/ElGarno/tcbw-homepage/contents/static/admin --jq '.[].name' 2>&1 || true
```

Extract: tech stack, architecture rationale (security/performance/cost/maintenance), DecapCMS integration approach, deployment.

- [ ] **Step 2: Write post body**

```bash
mkdir -p /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/tcbw-website
```

Frontmatter:
```toml
+++
date = '2026-04-10T10:00:00+02:00'
draft = false
title = '🎾 Vereinswebsite neu gedacht: Hugo + DecapCMS für TC Blau-Weiß Attendorn'
cover.image = "cover.webp"
cover.alt = "TC Blau-Weiß Attendorn Website-Migration"
cover.caption = "Von WordPress zu Static + Headless CMS"
cover.relative = true
tags = ["Hugo", "DecapCMS", "Cloudflare Pages", "Vereinswebsite", "Migration", "Static Site"]
+++
```

Body sections:
1. **Hook** (~150 Wörter) — die alte WordPress-Seite: langsam, zu wartungsintensiv, Plugin-Hölle, Sicherheits-Updates; Vorstand will editieren ohne Tech-Help
2. **Anforderungen** (~150 Wörter) — Liste: nicht-technische Editoren, schnelle Ladezeiten, kein Server-Wartung, kein Hosting-Budget, Branding (Vereinsfarben Blau/Weiß), responsive
3. **Warum Hugo + DecapCMS + Cloudflare Pages** (~250 Wörter) — Trade-off-Analyse:
   - Hugo: schneller Build, Markdown-first, lokale Vorschau
   - DecapCMS: Git-basiert, läuft im Browser, GitHub-OAuth-Login
   - Cloudflare Pages: gratis, globales CDN, automatisches HTTPS, Git-trigger-Builds
   - Snippet aus `hugo.toml` oder `static/admin/config.yml` als Beispiel (Repo ist public — Snippets ok)
4. **Migration in Schritten** (~150 Wörter) — Inhalt aus WP exportiert, Vorlagen neu in Hugo gebaut, DecapCMS-Collections konfiguriert, DNS umgezogen
5. **Vergleichstabelle** alt vs. neu — Performance, Kosten/Monat, Wartungsaufwand, Sicherheits-Patch-Verantwortung
6. **Lessons Learned** (~100 Wörter) — was tricky war (DecapCMS-Auth, Bilder-Workflow), was super lief
7. **Fazit + Verlinkung** — `https://tc-bw-attendorn.de` und `https://github.com/ElGarno/tcbw-homepage`

- [ ] **Step 3: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-tcbw
```
Expected: exits 0.

---

## Task 5: tcbw-getraenkebuchung Post

**Files:**
- Create: `content/posts/tcbw-getraenkebuchung/index.md`
- Reference: GitHub repo `ElGarno/tcbw-getraenkebuchung` (private — no code snippets)

- [ ] **Step 1: Inspect repo for high-level facts**

```bash
gh api repos/ElGarno/tcbw-getraenkebuchung/contents/README.md --jq '.content' | base64 -d > /tmp/getraenke_readme.md 2>/dev/null || true
gh api repos/ElGarno/tcbw-getraenkebuchung/contents/CLAUDE.md --jq '.content' | base64 -d > /tmp/getraenke_claude.md 2>/dev/null || true
```

Extract: feature list, architectural choices (SwiftUI, SwiftData, CloudKit, NFC, Keychain), kiosk strategy. **No** code snippets, **no** internal entity/property names.

- [ ] **Step 2: Write post body**

```bash
mkdir -p /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/tcbw-getraenkebuchung
```

Frontmatter:
```toml
+++
date = '2026-04-17T10:00:00+02:00'
draft = false
title = '📲 Getränkebuchung im Tennisclub: SwiftUI-Kiosk-App auf dem iPad'
cover.image = "cover.webp"
cover.alt = "iPad Kiosk-App auf Theke"
cover.caption = "Strichliste war gestern"
cover.relative = true
tags = ["SwiftUI", "SwiftData", "CloudKit", "NFC", "iPad", "Kiosk", "Vereins-IT"]
+++
```

Body sections:
1. **Hook** (~100 Wörter) — analoge Strichliste an der Theke; verschwundene Striche, falsche Namen, niemand kassiert
2. **Anforderungen** (~150 Wörter) — Kiosk-Modus, Multi-iPad-Sync, offline-fähig, Admin-Panel (Vorstand), Export für Kassenwart, NFC-Login per Vereinsausweis
3. **Architektur** (~250 Wörter) — High-Level **ohne** Code:
   - SwiftUI als UI-Framework
   - SwiftData als lokale Persistenz mit CloudKit-Sync (offline-first)
   - CloudKit-Container koordiniert Multi-iPad-State
   - NFC-Reader nutzt Core NFC für Vereinsausweis-Tap
   - Master-PIN in iOS Keychain (Fallback wenn Karte vergessen)
   - Kiosk-Lockdown via Guided Access (iOS-Bordmittel, kein MDM)
4. **Datenmodell-Skizze** (~100 Wörter) — abstrahiert: Mitglied, Buchung, Getränk; "konzeptionell, nicht das echte Schema"
5. **Lessons Learned** (~150 Wörter) — CloudKit-Sync-Quirks (Eventual Consistency, Conflict Resolution), NFC-UX-Findings (wie haptisches Feedback wirkt), Guided-Access-Fallstricke
6. **Fazit & Verlinkung** — Verein-Kontext (`https://tc-bw-attendorn.de`)

- [ ] **Step 3: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-getraenke
```
Expected: exits 0.

---

## Task 6: mai-tasting Post

**Files:**
- Create: `content/posts/mai-tasting/index.md`
- Reference: GitHub repo `ElGarno/whisky-api` (private — no code snippets)

- [ ] **Step 1: Inspect repo for high-level facts**

```bash
gh api repos/ElGarno/whisky-api/contents/README.md --jq '.content' | base64 -d > /tmp/whisky_readme.md 2>/dev/null || true
gh api repos/ElGarno/whisky-api/contents/CLAUDE.md --jq '.content' | base64 -d > /tmp/whisky_claude.md 2>/dev/null || true
gh api repos/ElGarno/whisky-api/contents/ --jq '.[].name' 2>&1 || true
```

Extract: monorepo layout (npm workspaces), AI-endpoint categories, tech (FastAPI, Railway, GPT-4o vision, JWT). Public references: `maitasting.app`, "App Store mAI Whisky" (live), "mAI Wine Beta". **No** internal endpoint paths or schema.

- [ ] **Step 2: Write post body**

```bash
mkdir -p /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/mai-tasting
```

Frontmatter:
```toml
+++
date = '2026-04-24T10:00:00+02:00'
draft = false
title = '🥃 mAI Tasting: Zwei iOS-Apps auf einem GPT-4o-Backend'
cover.image = "cover.webp"
cover.alt = "mAI Whisky und mAI Wine Architektur"
cover.caption = "Ein Backend, zwei Apps, viele AI-Endpoints"
cover.relative = true
tags = ["FastAPI", "React Native", "GPT-4o", "Vision", "iOS", "Monorepo", "Railway"]
+++
```

Body sections:
1. **Hook** (~100 Wörter) — wie aus einer Whisky-Sammlung der Idee-Funke wurde; warum die Wein-App das gleiche Backend bekam
2. **App-Store-Status** (~80 Wörter) — mAI Whisky live (App Store), mAI Wine in Beta; Verlinkung `https://maitasting.app`
3. **Architektur-Überblick** (~250 Wörter) — High-Level:
   - FastAPI auf Railway EU
   - React Native (Expo) Apps für iOS
   - Monorepo mit npm workspaces, geteilte TypeScript-Komponenten
   - GPT-4o (Vision) als AI-Backbone
   - JWT-Auth, Universal Links via AASA
   - Mermaid-/ASCII-Diagramm: User → App → API → GPT-4o + DB
4. **AI-Endpoints kategorisiert** (~200 Wörter) — Beschreibung der 12+ Endpoints, gruppiert in:
   - Recognition (Flaschen-/Etiketten-Erkennung aus Foto)
   - Tasting (Verkostungs-Reihenfolge, Aromen-Fingerprint)
   - Profiling (gewichtetes User-Aroma-Profil aus Bewertungen)
   - Collection-Health (Sammlungs-Diversität, blinde Flecken)
   - Keine konkreten Endpunkt-Paths
5. **Monorepo-Struktur** (~150 Wörter) — warum npm workspaces; geteilter Frontend-Code zwischen Apps; Vorteile für UI-Konsistenz
6. **Freemium-Tier-Logik** (~80 Wörter) — Konzept: free, paid; was paywalled ist und warum
7. **EAS-Build-Pipeline** (~80 Wörter) — wie Builds laufen, wie Apps zum App Store kommen
8. **Lessons Learned** (~100 Wörter) — was tricky war (Vision-Latenz, AASA-Setup, Universal Links), was super lief
9. **Fazit + Roadmap** — Ausblick mAI Wine Public Launch

Privat-Repo-Disziplin: keine echten Routen, Tabellen, Spaltennamen, Variablen-Namen. Nur Architektur-Pattern und konzeptionelle Beschreibung.

- [ ] **Step 3: Verify Hugo builds**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --quiet --destination /tmp/hugo-build-tasting
```
Expected: exits 0.

---

## Task 7: Cover Image Generator Script

**Files:**
- Create: `scripts/generate_covers.py`
- Create: `scripts/test_generate_covers.py`

**Design notes:** PEP 723 inline dependencies (`uv run scripts/generate_covers.py`). No `pyproject.toml` needed. Logic split: pure functions (prompt assembly, PNG→WebP conversion) are tested; OpenAI call is wrapped in a thin adapter and exercised by the integration run in Task 8.

- [ ] **Step 1: Create `scripts/` dir**

```bash
mkdir -p /Users/woerenkaemper/PycharmProjects/faffis-blog/scripts
```

- [ ] **Step 2: Write the failing test**

`scripts/test_generate_covers.py`:

```python
"""Tests for generate_covers — pure functions only (no network calls)."""

from io import BytesIO
from pathlib import Path

import pytest
from PIL import Image

from generate_covers import (
    SLUG_PROMPTS,
    STYLE_PREFIX,
    build_prompt,
    png_bytes_to_webp,
)


def test_build_prompt_combines_prefix_and_topic() -> None:
    prompt = build_prompt("Tapo")
    assert STYLE_PREFIX in prompt
    assert SLUG_PROMPTS["Tapo"] in prompt


def test_build_prompt_unknown_slug_raises() -> None:
    with pytest.raises(KeyError):
        build_prompt("unknown-slug")


def test_png_bytes_to_webp_writes_valid_webp(tmp_path: Path) -> None:
    img = Image.new("RGB", (1024, 1024), color=(0, 0, 255))
    buf = BytesIO()
    img.save(buf, format="PNG")
    png_bytes = buf.getvalue()

    target = tmp_path / "cover.webp"
    png_bytes_to_webp(png_bytes, target)

    assert target.exists()
    with Image.open(target) as out:
        assert out.format == "WEBP"
        assert out.size == (1024, 1024)
```

- [ ] **Step 3: Run test to verify it fails**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog/scripts
uv run --with pytest --with pillow --with python-dotenv --with openai pytest test_generate_covers.py -v
```
Expected: FAIL — `generate_covers` module not found.

- [ ] **Step 4: Implement the script**

`scripts/generate_covers.py`:

```python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "openai>=1.55",
#     "python-dotenv>=1.0",
#     "Pillow>=10.4",
# ]
# ///
"""Generate cover images for blog posts via OpenAI gpt-image-1.

Usage:
    uv run scripts/generate_covers.py                 # all slugs, skip existing
    uv run scripts/generate_covers.py --slug mytapo   # single slug
    uv run scripts/generate_covers.py --force         # overwrite existing
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
from io import BytesIO
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = REPO_ROOT / "content" / "posts"

STYLE_PREFIX = (
    "Minimalist tech illustration, flat design, soft gradients, "
    "muted color palette (deep blue, warm orange, soft white), "
    "no text, no logos, no people, abstract geometric shapes "
    "representing the topic, suitable as blog post cover."
)

SLUG_PROMPTS: dict[str, str] = {
    "Tapo": (
        "smart plug device with energy waveforms and time-series chart elements"
    ),
    "wippestoolen": (
        "neighborhood houses connected by tool icons (hammer, drill, ladder), "
        "trust-network feel"
    ),
    "tcbw-website": (
        "tennis court silhouette merging into a clean static-site grid, "
        "blue and white"
    ),
    "tcbw-getraenkebuchung": (
        "iPad on a bar counter with abstract drink list and NFC waves"
    ),
    "mai-tasting": (
        "whisky and wine bottle silhouettes with AI/vision overlay, "
        "abstract neural patterns"
    ),
}

COST_PER_IMAGE_USD = 0.04


def build_prompt(slug: str) -> str:
    """Combine style prefix with slug-specific topic."""
    return f"{STYLE_PREFIX} Topic: {SLUG_PROMPTS[slug]}"


def png_bytes_to_webp(png_bytes: bytes, target: Path) -> None:
    """Convert PNG bytes to WebP file at target path."""
    target.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(png_bytes)) as img:
        img.save(target, format="WEBP", quality=85, method=6)


def generate_image(client: OpenAI, slug: str) -> bytes:
    """Call gpt-image-1, return PNG bytes."""
    prompt = build_prompt(slug)
    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024",
        n=1,
    )
    b64 = response.data[0].b64_json
    return base64.b64decode(b64)


def cover_path(slug: str) -> Path:
    return POSTS_DIR / slug / "cover.webp"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--slug",
        choices=sorted(SLUG_PROMPTS.keys()),
        help="Generate only this slug (default: all)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing cover.webp",
    )
    args = parser.parse_args()

    load_dotenv(REPO_ROOT / ".env")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not set (.env or env var)", file=sys.stderr)
        return 1

    client = OpenAI(api_key=api_key)
    slugs = [args.slug] if args.slug else list(SLUG_PROMPTS.keys())
    generated = 0

    for slug in slugs:
        target = cover_path(slug)
        if target.exists() and not args.force:
            print(f"[skip] {slug}: {target.relative_to(REPO_ROOT)} exists")
            continue
        print(f"[gen ] {slug}: calling gpt-image-1 ...")
        png = generate_image(client, slug)
        png_bytes_to_webp(png, target)
        generated += 1
        print(f"[ok  ] {slug}: wrote {target.relative_to(REPO_ROOT)}")

    cost = generated * COST_PER_IMAGE_USD
    print(f"\nDone. Generated {generated} image(s). Estimated cost: ${cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run tests**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog/scripts
uv run --with pytest --with pillow --with python-dotenv --with openai pytest test_generate_covers.py -v
```
Expected: 3 tests PASS.

- [ ] **Step 6: Smoke-test help output (no API call)**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
uv run scripts/generate_covers.py --help
```
Expected: argparse help message; exits 0; no OpenAI call.

---

## Task 8: Generate Cover Images

**Files:**
- Create: `content/posts/Tapo/cover.webp`
- Create: `content/posts/wippestoolen/cover.webp`
- Create: `content/posts/tcbw-website/cover.webp`
- Create: `content/posts/tcbw-getraenkebuchung/cover.webp`
- Create: `content/posts/mai-tasting/cover.webp`

- [ ] **Step 1: Verify .env has OPENAI_API_KEY**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
grep -q '^OPENAI_API_KEY=' .env && echo "OK key present" || echo "MISSING key"
```
Expected: `OK key present`.

- [ ] **Step 2: Run for one slug first, sanity-check**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
uv run scripts/generate_covers.py --slug Tapo
```
Expected: writes `content/posts/Tapo/cover.webp`; exit 0; cost report ~$0.04.

- [ ] **Step 3: Inspect first image visually**

```bash
open /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/Tapo/cover.webp
```

If style is off (wrong color, contains text, photorealistic when minimalist requested) — adjust `STYLE_PREFIX` or slug prompt in `generate_covers.py`, then re-run with `--force --slug Tapo` until satisfied.

- [ ] **Step 4: Generate remaining 4 covers**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
uv run scripts/generate_covers.py
```
Expected: skips Tapo (already exists), generates 4 new ones; cost ~$0.16; exit 0.

- [ ] **Step 5: Spot-check the others**

```bash
ls -la /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/*/cover.webp
open /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/wippestoolen/cover.webp
open /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/tcbw-website/cover.webp
open /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/tcbw-getraenkebuchung/cover.webp
open /Users/woerenkaemper/PycharmProjects/faffis-blog/content/posts/mai-tasting/cover.webp
```

If any individual cover is off, regenerate that one only:
```bash
uv run scripts/generate_covers.py --force --slug <slug>
```

---

## Task 9: Local Hugo Build & Visual Check

- [ ] **Step 1: Full build with strict mode**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo --gc --minify
```
Expected: exits 0; no warnings about missing images, broken shortcodes, or template errors. Output in `public/`.

- [ ] **Step 2: Start dev server**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
hugo server --buildDrafts=false --buildFuture=false
```

In another terminal/window: open `http://localhost:1313` and verify:
- Lebenslauf page loads, all 9 sections render correctly
- 5 new posts appear on the listing page in correct date order (newest first: mai-tasting, getraenke, tcbw-website, wippestoolen, Tapo)
- Each post's cover image displays
- Click into each post: title, frontmatter, body all render; no broken Markdown

Stop server with Ctrl+C.

- [ ] **Step 3: Optional broken-link check** (if `htmltest` or similar is installed)

```bash
which htmltest && htmltest public/ || echo "htmltest not installed — skip"
```
Non-blocking; manual check is fine.

---

## Task 10: Commit Sequence

**Files affected (whole batch):**
- `content/lebanslauf.md` (modified)
- `content/posts/Tapo/index.md` (modified)
- `content/posts/Tapo/blog_tapo_energy.webp` (deleted)
- `content/posts/Tapo/cover.webp` (created)
- `content/posts/wippestoolen/index.md` (created) + cover
- `content/posts/tcbw-website/index.md` (created) + cover
- `content/posts/tcbw-getraenkebuchung/index.md` (created) + cover
- `content/posts/mai-tasting/index.md` (created) + cover
- `scripts/generate_covers.py` (created)
- `scripts/test_generate_covers.py` (created)
- `docs/superpowers/specs/2026-05-01-blog-cv-update-design.md` (created)
- `docs/superpowers/plans/2026-05-01-blog-cv-update.md` (created — this file)
- `doc/tasks/context_session_01.md` (modified)
- `.gitignore` (modified — already done)

- [ ] **Step 1: Verify clean state**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git status
```

- [ ] **Step 2: Commit 1 — design + plan**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add docs/superpowers/specs/2026-05-01-blog-cv-update-design.md docs/superpowers/plans/2026-05-01-blog-cv-update.md
git commit -m "$(cat <<'EOF'
docs: add brainstorming spec and plan for blog and CV update

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 3: Commit 2 — gitignore (if dirty)**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
if ! git diff --quiet .gitignore; then
  git add .gitignore
  git commit -m "$(cat <<'EOF'
chore: ignore .env in repo root

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
fi
```

- [ ] **Step 4: Commit 3 — Lebenslauf**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/lebanslauf.md
git commit -m "$(cat <<'EOF'
feat(cv): translate and expand Lebenslauf with 2026 senior promotion and personal projects

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 5: Commit 4 — mytapo post**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/Tapo/index.md content/posts/Tapo/blog_tapo_energy.webp
git commit -m "$(cat <<'EOF'
feat(blog): add mytapo deep-dive post (replaces previous Tapo post)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Commit 5 — wippestoolen post**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/wippestoolen/index.md
git commit -m "$(cat <<'EOF'
feat(blog): add wippestoolen tool-sharing platform post

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 7: Commit 6 — tcbw-website post**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/tcbw-website/index.md
git commit -m "$(cat <<'EOF'
feat(blog): add TC Blau-Weiss website migration post

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 8: Commit 7 — getraenkebuchung post**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/tcbw-getraenkebuchung/index.md
git commit -m "$(cat <<'EOF'
feat(blog): add TCBW drinks-booking iPad app post

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 9: Commit 8 — mai-tasting post**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/mai-tasting/index.md
git commit -m "$(cat <<'EOF'
feat(blog): add mAI Tasting backend architecture post

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 10: Commit 9 — generator script**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add scripts/generate_covers.py scripts/test_generate_covers.py
git commit -m "$(cat <<'EOF'
chore(blog): add cover image generator script

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 11: Commit 10 — cover images**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add content/posts/Tapo/cover.webp content/posts/wippestoolen/cover.webp content/posts/tcbw-website/cover.webp content/posts/tcbw-getraenkebuchung/cover.webp content/posts/mai-tasting/cover.webp
git commit -m "$(cat <<'EOF'
feat(blog): add cover images for 5 new posts

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 12: Commit 11 — context session**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git add doc/tasks/context_session_01.md
git commit -m "$(cat <<'EOF'
docs(session): update context session with blog and CV update progress

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 13: Verify clean working tree**

```bash
cd /Users/woerenkaemper/PycharmProjects/faffis-blog
git status
git log --oneline -15
```
Expected: working tree clean; 11 new commits visible.

- [ ] **Step 14: Stop and request user "go" before push**

Do **not** push. Ask the user explicitly:
> "Alle Commits lokal. Soll ich `git push origin main` ausführen? (Das löst den Cloudflare-Pages-Build aus.)"

Only push after explicit "yes/go" from the user.

---

## Definition of Done

- [ ] `content/lebanslauf.md` translated and expanded per Task 1
- [ ] All 5 posts in `content/posts/` with correct frontmatter and dates in the past
- [ ] All 5 posts have `cover.webp` from generator
- [ ] `hugo --gc --minify` builds without errors or warnings
- [ ] `hugo server` opened locally; each post visually verified
- [ ] `scripts/generate_covers.py` committed without secrets
- [ ] All commits batched per Task 10 sequence
- [ ] No push to `origin/main` without explicit user approval
- [ ] `doc/tasks/context_session_01.md` updated with final state
