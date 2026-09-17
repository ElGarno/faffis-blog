+++
title = "Kinderbasar Biekhofen"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Anmeldung, Kasse und Abrechnung für einen Kinderflohmarkt"
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

Läuft unter [basar.faffi.cloud](https://basar.faffi.cloud) auf Railway, abgesichert
durch getrennte Codes für Kasse und Orga. 495 Tests, Migrationen laufen beim Start. Ein
Probelauf-Modus legt Testdaten an und räumt sie wieder weg, damit das Orga-Team den
Ablauf vorher einmal durchspielen kann, ohne etwas kaputtzumachen.
