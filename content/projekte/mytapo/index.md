+++
title = "MyTapo Event-Detection"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Aus Stromverbrauch werden Geräte-Events"
gruppe = "daten"
status = "live"
zeitraum = "2026"
weight = 10
stack = ["Python", "InfluxDB", "Grafana", "Docker", "AWTRIX"]
live_url = ""
repo_url = "https://github.com/ElGarno/MyTapo"
post_url = "/posts/tapo/"
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Grafana-Ansicht der erkannten Geräte-Events"
+++

## Problem

Reines Energiemonitoring ist schnell langweilig. Eine Zeitreihe in Grafana zeichnet
hübsche Sägezähne und beantwortet keine der Fragen, die im Alltag tatsächlich
vorkommen: Ist die Waschmaschine fertig? Wie viele Espressi waren es diese Woche?

## Lösung

Aus dem rohen Verbrauchsstrom werden diskrete Events. Eine Zustandsmaschine pro Gerät —
idle, active, cooling down — erkennt anhand von Schwellwert-Hysterese, Mindest- und
Maximaldauer und einer Cooldown-Zeit, wann ein Waschzyklus, eine TV-Session oder ein
Espressobezug beginnt und wann er endet. Kurze Stromabfälle zwischen zwei
Schleudergängen lösen dabei kein falsches Zyklusende aus. Jedes abgeschlossene Event
geht mit Spitzenleistung, Durchschnitt, Energie und Tags wie Stunde und Wochentag in
eine eigene InfluxDB-Bucket, getrennt von den Rohdaten.

## Ergebnis

Läuft in Docker-Containern auf dem NAS, ohne Cloud und ohne Vendor-Lock-in. Angezeigt
wird in Grafana, per Pushover und auf einer Ulanzi-AWTRIX-Pixeluhr im Wohnzimmer, die
zwischen aktueller Solarleistung und Tageszusammenfassung wechselt. Statt Watt zu
interpretieren, lese ich dort Sätze wie „3 Espressi, 2,1 h TV, 1 Waschzyklus" ab.
