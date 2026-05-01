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

Die alte Vereinswebsite des TC Blau-Weiß Attendorn lief auf WordPress, und sie lief in dem Sinne, dass die Seite irgendwie noch erreichbar war. Sie lud langsam, wollte ständig Plugin-Updates, hatte einen unklaren Sicherheitsstatus, und niemand im Vorstand hatte Lust, sich um PHP-Versionen, Datenbank-Backups und das nächste „Update verfügbar"-Banner zu kümmern. Gleichzeitig sollten zwei Dinge gleichzeitig wahr sein: nicht-technische Vorstandsmitglieder mussten Inhalte selbst pflegen können — Aktuelles, Mannschaften, Termine — **und** das Hosting durfte nichts kosten und nichts kaputtgehen, wenn niemand ein halbes Jahr hinschaut. Die offensichtliche Antwort war ein Static-Site-Generator plus ein Headless-CMS, das im Browser läuft. Konkret: Hugo + DecapCMS auf Cloudflare Pages.

## Anforderungen

Die Wunschliste aus Vereinssicht war pragmatisch und ziemlich klar:

- Vorstand editiert Inhalte ohne Tech-Hilfe, ohne FTP, ohne SSH.
- Bilder hochladen für Galerie und Aktuelles muss in zwei Klicks gehen.
- Schnelle Ladezeiten auch auf dem Handy auf dem Tennisplatz.
- Kein Server, keine PHP-Updates, keine Plugin-Maintenance.
- Hosting-Budget: 0 Euro.
- Vereinsfarben Blau und Weiß, klares Layout.
- Responsive für Smartphone, Tablet, Desktop.

Inhaltlich gibt es sieben editierbare Bereiche, die regelmäßig angefasst werden: `aktuelles` (News-Posts), `mannschaften` (sieben aktive Teams), `training` (Trainer und Zeiten), `termine` (Medenspiele und Events), `verein` (Vorstand, Historie, Mitgliedschaft), `galerie` und die rechtlichen `seiten` (Impressum, Datenschutz). Genau diese Bereiche müssen ohne Markdown-Kenntnisse erreichbar sein.

## Warum Hugo + DecapCMS + Cloudflare Pages

**Hugo** rendert die ganze Seite in unter einer Sekunde, hat eine sehr einfache Markdown-first-Logik und liefert mit `hugo server` eine lokale Live-Vorschau, die Änderungen sofort zeigt. Templates sind reines Go-HTML, keine Build-Pipeline, kein Webpack.

**DecapCMS** ist Git-basiert: Jede Änderung im Admin-UI wird ein Commit auf GitHub. Das heißt: vollständige Versionierung, kein eigenes Datenbank-Backup nötig, und technische Editoren können dieselben Inhalte direkt im Repo bearbeiten. Die Admin-UI ist eine statische Seite unter `/admin/` mit GitHub-OAuth-Login. Die Collection-Definitionen leben in `static/admin/config.yml`:

```yaml
collections:
  - name: "aktuelles"
    label: "Aktuelles"
    folder: "content/aktuelles"
    create: true
    fields:
      - { label: "Titel", name: "title", widget: "string" }
      - { label: "Datum", name: "date", widget: "datetime" }
      - { label: "Beschreibung", name: "description", widget: "text" }
      - { label: "Bild", name: "image", widget: "image", required: false }
      - { label: "Inhalt", name: "body", widget: "markdown" }
```

Damit bekommt der Vorstand für jede News ein Formular mit beschrifteten Feldern: „Titel", „Datum", „Bild" — keine YAML-Frontmatter-Diskussion mehr.

**Cloudflare Pages** liefert das Ganze: Free Tier, globales CDN, automatisches HTTPS und ein Build, der durch jeden `git push` auf `main` getriggert wird. Kein eigener Server, keine Skalierungs-Frage, keine TLS-Renewal-Erinnerung.

Die Hugo-Konfiguration selbst ist bewusst klein gehalten — Vereinsdaten als Site-Params, damit Templates sie zentral lesen können:

```toml
baseURL = "https://tc-bw-attendorn.de/"
languageCode = "de"
title = "Tennisclub Blau-Weiss Attendorn e.V."

[params]
  tagline = "Tennis an der Burg Schnellenberg"
  founded = "1931"
  courtbookingURL = "https://tc-bw-attendorn.courtbooking.de/login?standard=true"
```

## Migration in Schritten

Der Ablauf war linear: zuerst eine **Inhalts-Inventur** (WordPress-Export gezogen, Bilder gesichert, alte Texte sortiert). Dann **Hugo-Templates aufgesetzt**, bewusst ohne Standard-Theme wie PaperMod, weil die Seite ein eigenes, vereinstypisches Layout in Blau/Weiß bekommen sollte; eigene `layouts/` und ein einzelnes `static/css/main.css` reichen dafür. Anschließend **Content-Collections in DecapCMS konfiguriert** für Mannschaften, Aktuelles, Termine, Training, Galerie und die Startseite. **DNS-Umzug** auf Cloudflare lief parallel — die neue Seite wurde unter Subdomain getestet, dann auf den `A`/`CNAME`-Eintrag der Hauptdomain umgeschaltet.

## Vergleichstabelle alt vs. neu

| Aspekt | Alte WordPress-Seite | Neue Static-Lösung |
|---|---|---|
| Ladezeit | mehrere Sekunden | < 1 s (CDN-Edge) |
| Hosting-Kosten | ~10–15 €/Monat | 0 €/Monat (Cloudflare Free) |
| Sicherheits-Patches | manuell, regelmäßig nötig | nicht nötig (kein Server) |
| Editieren | nur Admin-Login mit Passwort | Markdown im Repo **oder** DecapCMS-UI im Browser |
| Backup | Plugin-Backup, manuell | Git-History (jeder Commit ist ein Backup) |

## Fazit

Die neue Seite läuft seit der Umstellung wartungsfrei: [tc-bw-attendorn.de](https://tc-bw-attendorn.de). Quellcode öffentlich auf [github.com/ElGarno/tcbw-homepage](https://github.com/ElGarno/tcbw-homepage). Siehe auch den kommenden Post zur [iPad-Getränkebuchung](/posts/tcbw-getraenkebuchung/) im selben Verein — gleicher Stack-Gedanke, anderer Use Case.
