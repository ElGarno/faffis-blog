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
live_url = ""
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
