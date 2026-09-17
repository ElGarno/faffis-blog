+++
title = "Wippestoolen"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Werkzeug-Sharing für die Nachbarschaft"
gruppe = "produkte"
status = "wip"
zeitraum = "2026"
weight = 30
stack = ["FastAPI", "Postgres", "Railway", "Vercel"]
live_url = "https://wippestoolen.de"
repo_url = ""
post_url = "/posts/wippestoolen/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Startseite von Wippestoolen mit dem Hero-Text „Leihen Sie was Sie brauchen, teilen Sie was Sie haben“"
+++

## Problem

Eine Bohrmaschine wird im Schnitt rund 13 Minuten überhaupt benutzt und steht den Rest
ihres Lebens im Keller. In derselben Straße liegt in jedem zweiten Keller dieselbe
Schlagbohrmaschine, derselbe Akku-Schrauber, derselbe Vertikutierer — und jedes dieser
Geräte kommt ein- oder zweimal im Jahr aus dem Regal.

## Lösung

Eine kleine, lokale Plattform, auf der Nachbarn ihr Werkzeug teilen, ausleihen und
wiederfinden. Inspiriert von Foodsharing, aber für die Stichsäge im Keller. Wer etwas
besitzt, legt es mit Fotos, Verfügbarkeit und ungefährem Standort an; wer etwas
braucht, sucht in einer Kartenansicht nach allem in Lauf-Distanz. Aus einem Treffer
wird eine Buchung mit klarem Statusverlauf, nach der Rückgabe bewerten sich beide
Seiten. Technisch bewusst klassisch geschnitten: ein FastAPI-Service gegen Postgres,
davor ein getrenntes Frontend auf Vercel, das später auch eine Mobile-App bedienen
kann.

## Ergebnis

Die Landing-Seite läuft unter [wippestoolen.de](https://wippestoolen.de), das
Web-Frontend ist in der MVP-Phase, die Mobile-App im Konzept. Das eigentliche Produkt
entsteht Schritt für Schritt nebenbei, Familie und Hauptjob haben Vorrang. Offen ist vor
allem das Henne-Ei-Problem des Vertrauens: Zu Beginn hat niemand eine Reputation.
