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

Die alte Vereinsseite lief auf WordPress, aber genutzt hat sie kaum noch jemand:
unübersichtlich gewachsen, mit veralteten Inhalten, und sicherheitstechnisch war das
schon lange nicht mehr zu verantworten. Im Vorstand wollte sich niemand um PHP-Versionen
und Plugin-Updates kümmern. Dazu die Anforderung, dass das Hosting nichts kostet und
nichts kaputtgeht, wenn ein halbes Jahr niemand hinschaut.

## Lösung

Ein Static-Site-Generator plus ein Headless-CMS, das im Browser läuft: Hugo baut die
Seite, DecapCMS gibt dem Vorstand eine Oberfläche zum Schreiben, und jede Änderung
landet als Commit im Git-Repository. Kein Server, keine Datenbank, kein PHP — und damit
auch keine Angriffsfläche, die jemand patchen müsste. Gehostet auf Cloudflare Pages,
das bei jedem Push neu baut.

## Ergebnis

Läuft unter tc-bw-attendorn.de, das Hosting kostet nichts. Der laufende Betrieb besteht
vor allem daraus, automatisch erzeugte Pull Requests zu bestätigen: Spielergebnisse
zieht die Seite selbstständig von nuLiga, und eine eingehende Vorstandsmail löst einen
Agenten aus, der sie in Termine, Infos und Sonstiges zerlegt und als Änderungsvorschlag
einarbeitet. Die Mannschaftsdaten aus dem Repo verwenden inzwischen auch die
Social-Tools weiter.
