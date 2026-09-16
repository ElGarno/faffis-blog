+++
title = "NarrAItive"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "KI-generierte Bilderbücher, vorgelesen"
gruppe = "produkte"
status = "archiv"
zeitraum = "2023–2025"
weight = 20
stack = ["Streamlit", "DALL·E 3", "ElevenLabs", "DuckDB"]
live_url = ""
repo_url = "https://github.com/ElGarno/NarrAItive"
post_url = "/posts/narraitive/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "NarrAItive-Logo: ein Kind liest ein Bilderbuch, darüber eine Glühbirne, darunter der Schriftzug mit dem Untertitel Digital Children's Picture Book"
+++

## Problem

An einem Sonntag im Jahr 2023 saß ich im Wohnzimmer und staunte über die Berge an
Bilderbüchern für unsere Kinder. Vorgelesen wurden trotzdem immer dieselben drei, und
eine Geschichte, in der das eigene Kind vorkommt, war in keinem der Stapel dabei.

## Lösung

Ein Stichwort genügt — „Emilia reist mit einem Einhorn nach Italien". Das System
erkennt, welche Charaktere unbekannt sind, fragt nach dem Aussehen oder liest es aus
einem hochgeladenen Bild, schreibt die Geschichte in zehn Abschnitten, erzeugt zu jedem
Abschnitt ein Bild und spricht die Kapitel mit einer Stimme ein, die sich auch klonen
lässt. Geschichten, Charaktere und die Pfade zu Bildern und Audiodateien liegen in
einer DuckDB, die Oberfläche ist Streamlit. So lässt sich ein einmal erzeugtes Buch
jederzeit wieder aufschlagen.

## Ergebnis

Ein Prototyp, den unsere Kinder tatsächlich benutzt haben. Kein fertiges Produkt und
auch keins geplant, aber das Projekt, in dem Text-, Bild- und Sprachgenerierung bei mir
zum ersten Mal in einer Anwendung zusammengekommen sind — und damit die Grundlage für
alles, was danach kam.
