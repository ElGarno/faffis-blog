+++
title = "Doppelkopf-Statistik"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "5.600 Partien aus der Stammrunde, ausgewertet"
gruppe = "daten"
status = "live"
zeitraum = "2026"
weight = 30
stack = ["Python", "DuckDB", "Docker", "Pushover"]
live_url = ""
repo_url = ""
post_url = ""
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Verteilung der Spielarten und Übersicht der Spielabende im Doppelkopf-Dashboard"
+++

## Problem

Eine Stammrunde spielt jahrelang online Doppelkopf. Am Ende steht eine lange
Zahlenkolonne auf einem Zettel, und auf die naheliegende Frage — wer spielt eigentlich
gut, und woran liegt das — gibt sie keine Antwort. Die Plattform selbst zeigt jede
Partie einzeln, aber nichts über die Jahre hinweg.

## Lösung

Ein Scraper holt die Partien mitsamt vollständigem Protokoll: Login, Cursor-Pagination,
Wiederaufnahme an der Abbruchstelle und ein Umgang mit dem Rate-Limit, der die Seite
nicht überrennt. Alles landet in einer DuckDB. Die eigentliche Auswertung steckt nicht
in Skripten, sondern in Datenbank-Views, und die rohen Seiten bleiben auf der Platte —
nach jeder Schema-Änderung lässt sich der gesamte Bestand daraus in Minuten neu
einlesen, ohne die Seite noch einmal anzufassen. Daraus entstehen zwei Dinge: ein
Dashboard als einzelne HTML-Datei und ein Wochenbericht, der per Pushover auf dem Handy
landet.

## Ergebnis

Rund 5.600 Partien der Runde liegen mit vollständigem Protokoll vor — Stiche, Karten,
Ansagen und Anfangshände. Ausgewertet wird über zwei Zeiträume, zwischen denen das
Dashboard umschaltet. Das Repository bleibt bewusst privat, weil das Dashboard die
Mitspieler namentlich zeigt; hier steht deshalb nur die Pipeline.
