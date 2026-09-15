+++
title = "mAI Whisky & mAI Wine"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Zwei iOS-Apps im App Store auf einem gemeinsamen Backend"
gruppe = "produkte"
status = "appstore"
zeitraum = "2026"
weight = 10
stack = ["FastAPI", "React Native", "Expo", "Postgres", "Railway"]
live_url = "https://maitasting.app"
repo_url = ""
post_url = "/posts/mai-tasting/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Flaschendetail mit Aromen-Radar in der mAI-Whisky-App"
+++

## Problem

Die Whisky-Sammlung wuchs, und die Verkostungsnotizen standen in einem Notizbuch, in
dem sie mit der Zeit verblassen — und mit ihnen der Geschmack im Kopf. Dazu der
Klassiker: Irgendwann weiß man nicht mehr, welche Flaschen schon zu Hause stehen, und
holt die dritte aus derselben Region.

## Lösung

Foto vom Etikett, ein Vision-Modell erkennt die Flasche und legt sie mit Marke, Region
und Jahrgang in der Sammlung ab. Aus freien Notizen wird ein Geschmacksprofil, das als
Radar-Chart über Achsen wie rauchig, süß, fruchtig und würzig liegt. Bei einer
Verkostung bewerten Gäste über eine Web-Seite mit, ohne etwas installieren zu müssen.
Hinter beiden Apps — mAI Whisky und mAI Wine — steht ein einziges Backend. Der
App-Code liegt in einem Monorepo mit einem geteilten Workspace für UI-Komponenten und
API-Client; rund achtzig Prozent der Oberfläche sind ohnehin dieselben, der Rest ist
whisky- oder weinspezifisch.

## Ergebnis

Beide Apps sind im App Store, die Landing-Seite liegt unter maitasting.app, das Backend
läuft auf Railway in einer EU-Region. Eine Backend-Änderung wird an genau einer Stelle
nachgezogen, und beide Apps ziehen gleichzeitig mit — Drift zwischen den Frontends gibt
es damit nicht.
