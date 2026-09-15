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
