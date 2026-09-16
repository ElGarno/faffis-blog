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
cover.alt = "Illustration eines Tablets mit Getränkesymbol neben Tennisball und -schläger, per Funksymbol mit einem Becher verbunden"
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
