# Context Session 01 - Faffis Blog Setup

## Project Goal
Maintain and develop the personal Hugo-based tech blog at https://faffi.cloud/, covering AI/ML, cloud deployment, Docker, home automation, and data science topics.

## Current Status
- **Phase**: maintenance
- **Last Updated**: 2026-04-30
- **Blockers**: None

## Tasks
- [ ] Define current session goal

## Progress Log
### 2026-04-30
- Session initialized
- Reviewed project structure: Hugo + PaperMod theme, deployed to Cloudflare Pages
- Existing content: 7 post categories (NAS, NarrAItive, Tapo, claude_code, deployment, docker_volumes, fabric)
- No open uncommitted changes except local `.idea/` folder
- No CLAUDE.md exists in project yet
- Awaiting task definition from user

### 2026-05-01
- Task 1 (Update Lebenslauf) — replaced body of `content/lebanslauf.md` with 2026 content
  - Translated/merged from `cv_wk_24.tex` and `linkedin_about_de.md`
  - Updated frontmatter `date` to `2026-05-01T10:00:00+02:00` (preserved all other keys)
  - New sections: "Personal Projects" (5 entries) and "Talks & Publications" (INWT podcast)
  - Removed: Praktika & Studentenjobs, Soft/Hard Skills, Zivildienst, Gymnasium, old Diplomarbeit/Praktikum entries
  - Renamed: "Interessen" → "Off the Clock"
  - Verification: `hugo --quiet` exits 1 due to pre-existing PaperMod RSS template bug
    (`themes/PaperMod/layouts/_default/rss.xml:10` — `site.Author.email` deprecated in newer Hugo).
    Confirmed bug exists on unmodified `main` (same error before my edit).
    With `disableKinds=["RSS"]` and `--buildFuture`, build is clean and `/tmp/hugo-build-cv/lebanslauf/index.html`
    renders correctly (~29 KB, all sections present). `--buildFuture` is required because the date is
    intentionally in the future (2026-05-01 vs today 2026-04-30); Cloudflare Pages will publish on/after that date.

## Open Questions
- What is the focus of this session? (new post, theme adjustment, deployment, refactor, ...)

### 2026-05-01 (Task 2)
- Replaced `content/posts/Tapo/index.md` with technical deep-dive on the public MyTapo repo
  - Frontmatter: TOML, date `2026-03-27T10:00:00+02:00`, new title with event-detection focus, `cover.image = "cover.webp"`
  - 7 sections: Hook, Architektur-Überblick (with ASCII diagram), Event-Detection (with state-machine snippet + threshold table from `appliance_profiles.json`), AWTRIX-Pixel-Clock (HTTP `POST /api/notify` snippet), Solar-Integration (snippet from `solar_energy_generated.py`), Lessons Learned (KLAP timeouts, polling rate, Synology platform), Fazit
  - Word count: 927 (target 600–1000)
  - Code snippets, thresholds, services and ports verified against `event_detector.py`, `awtrix_client.py`, `solar_energy_generated.py`, `EVENT_DETECTION.md`, `docker-compose.synology.yml`
  - No keys/secrets/IPs from `.env.template` included
- Deleted orphan cover `content/posts/Tapo/blog_tapo_energy.webp`
  - New `cover.webp` to be generated in Task 8
- Verification: same pre-existing PaperMod RSS bug as Task 1 (`themes/PaperMod/layouts/_default/rss.xml:10` — `site.Author` deprecated). With `--disableKinds RSS --buildFuture` the build is clean and `/tmp/hugo-build-task2/posts/Tapo/index.html` renders (~34 KB)

### 2026-05-01 (Task 3)
- Created `content/posts/wippestoolen/index.md` (Wippestoolen post, German, 771 words — within 600-800 target)
  - Frontmatter: TOML, date `2026-04-03T10:00:00+02:00`, cover.webp ref, tags Wippestoolen/FastAPI/Postgres/Sharing-Economy/Plattform
  - 7 sections in spec order: Hook (no heading) → Konzept → High-Level-Architektur (with ASCII boxes diagram) → Trust-System → Booking-Flow → Status & Roadmap → Fazit
  - Privacy discipline respected: no code snippets, no internal endpoint paths, no internal table/column/class names, no JWT-claim shapes. Only public references: `https://wippestoolen.vercel.app` and high-level architecture (FastAPI, Postgres, Redis, S3 abstracted, Vercel, Railway, JWT, Email-Verification)
  - Architecture description abstracted from public README/CLAUDE.md only; nothing from `Instructions.md` (private) leaked
  - "siehe auch" link to `/posts/Tapo/` per spec
- Verification: `hugo --quiet --disableKinds RSS --buildFuture --destination /tmp/hugo-build-task3` exits 0; `/tmp/hugo-build-task3/posts/wippestoolen/index.html` rendered ~26 KB
- `cover.webp` not yet present — to be generated in Task 8

### 2026-05-01 (Task 4)
- Created `content/posts/tcbw-website/index.md` (TC Blau-Weiß Attendorn migration story, German, 688 words — within 600-900 target)
  - Frontmatter: TOML, date `2026-04-10T10:00:00+02:00`, cover.webp ref, tags Hugo/DecapCMS/Cloudflare Pages/Vereinswebsite/Migration/Static Site
  - 7 sections in spec order: Hook (no heading) → Anforderungen → Warum Hugo + DecapCMS + Cloudflare Pages → Migration in Schritten → Vergleichstabelle alt vs. neu → Lessons Learned → Fazit
  - Code snippets are real excerpts from the public `tcbw-homepage` repo: `aktuelles` collection definition from `static/admin/config.yml`, plus `baseURL`/`title`/`[params]` slice from `hugo.toml`. Content sections (`aktuelles`, `mannschaften`, `training`, `termine`, `verein`, `galerie`, `seiten`) named verbatim from README.
  - Vergleichstabelle uses plausible numbers (~10–15 €/Monat for old WP hosting, 0 €/Monat for Cloudflare Free)
  - Cross-link: `/posts/tcbw-getraenkebuchung/` (will be valid after Task 5 + Task 10 commit)
- Verification: `hugo --quiet --disableKinds RSS --buildFuture --destination /tmp/hugo-build-task4` exits 0; `/tmp/hugo-build-task4/posts/tcbw-website/index.html` rendered ~31 KB
- `cover.webp` not yet present — to be generated in Task 8

### 2026-05-01 (Task 5)
- Created `content/posts/tcbw-getraenkebuchung/index.md` (TCBW iPad-Kiosk-App SwiftUI/SwiftData/CloudKit, German, 847 words — within 700-900 target)
  - Frontmatter: TOML, date `2026-04-17T10:00:00+02:00`, cover.webp ref, tags SwiftUI/SwiftData/CloudKit/NFC/iPad/Kiosk/Vereins-IT
  - 7 sections in spec order: Hook (no heading) → Anforderungen → Architektur (with ASCII diagram of two iPads → CloudKit → optional Admin-iPad) → Datenmodell-Skizze → Lessons Learned → Status → Fazit
  - Privacy discipline: NO Swift code snippets, no internal struct/class/property names, no CloudKit zone/record-type names, no UI component names. Only abstracted concepts (Mitglied/Getränk/Buchung) explicitly labelled "Konzeptionell, nicht das echte Schema". Repo (`ElGarno/tcbw-getraenkebuchung`) is private — README/CLAUDE.md only consulted for architecture confirmation, nothing copied.
  - Tech stack mentions stayed at Apple framework names per spec (SwiftUI, SwiftData, CloudKit, Core NFC, iOS Keychain, Guided Access)
  - Cross-link to `/posts/tcbw-website/` per spec; explicitly NOT linking to private repo
- Verification: `hugo --quiet --disableKinds RSS --buildFuture --destination /tmp/hugo-build-task5` exits 0; `/tmp/hugo-build-task5/posts/tcbw-getraenkebuchung/index.html` rendered ~28 KB
- `cover.webp` not yet present — to be generated in Task 8

## Files Modified
- `content/lebanslauf.md` - rewritten for 2026 update (Senior promotion, Personal Projects, Talks & Publications)
- `content/posts/Tapo/index.md` - replaced with MyTapo event-detection deep-dive (Task 2)
- `content/posts/Tapo/blog_tapo_energy.webp` - DELETED (orphan, replaced by cover.webp in Task 8)
- `content/posts/wippestoolen/index.md` - CREATED (Task 3, Wippestoolen tool-sharing post, no code/secrets from private repo)
- `content/posts/tcbw-website/index.md` - CREATED (Task 4, TCBW Hugo+DecapCMS migration story, real config snippets from public repo)
- `content/posts/tcbw-getraenkebuchung/index.md` - CREATED (Task 5, TCBW iPad-Kiosk-App, no code/identifiers from private repo)
- `content/posts/mai-tasting/index.md` - CREATED (Task 6, mAI Whisky & mAI Wine GPT-4o iOS apps, no code/identifiers from private repo)
- `scripts/generate_covers.py` - CREATED (Task 7, PEP 723 script for OpenAI gpt-image-1 cover generation, PNG->WebP)
- `scripts/test_generate_covers.py` - CREATED (Task 7, pytest tests for build_prompt and png_bytes_to_webp; 3/3 passing)

### 2026-05-01 (Task 6)
- Created `content/posts/mai-tasting/index.md` (mAI Whisky / mAI Wine post, German, 982 words — within 800–1000 target)
  - Frontmatter: TOML, date `2026-04-24T10:00:00+02:00`, cover.webp ref, tags FastAPI/React Native/GPT-4o/Vision/iOS/Monorepo/Railway
  - 9 sections in spec order: Hook (no heading) → App-Store-Status → Architektur-Überblick (with ASCII diagram User → Apps → FastAPI/Railway → Postgres/S3/GPT-4o) → AI-Endpoints kategorisiert (Recognition / Tasting / Profiling / Collection-Health) → Monorepo-Struktur → Freemium-Modell → EAS-Build & App-Store-Story → Lessons Learned → Fazit
  - Privacy discipline respected: NO code snippets (Python/TS/Swift/JSON), no internal route paths (no `/api/v1/...`), no internal class/function/property names, no DB schema or column names, no prompt templates or model parameters, no OpenAI organisation references. Only public references: `https://maitasting.app` and abstracted architecture (FastAPI, React Native Expo, GPT-4o, Railway EU, npm workspaces, JWT, AASA, Universal Links, EAS, AppStoreConnect)
  - AI-endpoint categories described conceptually only — no real route names, only generic Recognition / Tasting / Profiling / Collection-Health labels
  - Architecture confirmed via public README from `gh api` (FastAPI, Postgres, JWT, GPT-4o, 12 endpoints, React Native Expo SDK 54) — nothing copied verbatim
  - Cross-link: `/posts/tcbw-getraenkebuchung/` (second iOS side-project) per spec
- Verification: `hugo --quiet --disableKinds RSS --buildFuture --destination /tmp/hugo-build-task6` exits 0
- `cover.webp` not yet present — to be generated in Task 8

### 2026-05-01 (Task 7)
- Created `scripts/generate_covers.py` — PEP 723 inline-metadata script that calls OpenAI `gpt-image-1` (1024x1024), converts PNG -> WebP via Pillow, writes to `content/posts/<slug>/cover.webp`
  - Uses `python-dotenv` to load `OPENAI_API_KEY` from repo-root `.env`
  - Supports `--slug <name>` (choices restricted to known slugs) and `--force` (overwrite existing)
  - Skips slugs whose `cover.webp` already exists unless `--force` is passed (idempotent reruns)
  - Logs estimated cost at the end (`COST_PER_IMAGE_USD = 0.04` * generated count)
  - `STYLE_PREFIX` and `SLUG_PROMPTS` (Tapo, wippestoolen, tcbw-website, tcbw-getraenkebuchung, mai-tasting) match the plan spec verbatim
- Created `scripts/test_generate_covers.py` — 3 pure-function tests (no network calls):
  - `test_build_prompt_combines_prefix_and_topic` — verifies prompt contains both prefix and topic
  - `test_build_prompt_unknown_slug_raises` — verifies KeyError on unknown slug
  - `test_png_bytes_to_webp_writes_valid_webp` — round-trips a real Pillow-generated PNG to WebP and re-opens it to assert format + size
- TDD: tests written first, ran and failed with `ModuleNotFoundError: No module named 'generate_covers'`; implementation added; tests now 3/3 PASS
- Smoke test `uv run scripts/generate_covers.py --help` exits 0 and prints argparse help with the 5 slug choices and `--force` — no API call made
- No covers actually generated (that's Task 8); no commits (those are batched in Task 10)

## Agent Outputs Referenced
- None yet