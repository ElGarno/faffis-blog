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
