+++
title = "Solar Power Prediction"
date = 2026-09-15T10:00:00+02:00
draft = false
tagline = "Wetterprognose als Vorhersage der Solarüberproduktion"
gruppe = "daten"
status = "live"
zeitraum = "2025–2026"
weight = 20
stack = ["Python", "scikit-learn", "InfluxDB", "Open-Meteo", "Pushover"]
live_url = ""
repo_url = "https://github.com/ElGarno/predict_power_consumption"
post_url = ""
cover.image = "cover.webp"
cover.relative = true
cover.alt = "Stündliche Vorhersage der Solarerzeugung für den Folgetag"
+++

## Problem

Strom sollte dann verbraucht werden, wenn die Anlage ihn liefert. Wann sie liefert, ist
aber keine Messfrage, sondern eine Prognosefrage — und wer morgens entscheidet, ob die
Waschmaschine jetzt oder heute Abend läuft, hat diese Antwort nicht.

## Lösung

Die Wetterprognose kommt stündlich von Open-Meteo aus dem DWD-ICON-Modell. Darauf sitzt
ein RandomForest, trainiert auf historischen Wetter- und Verbrauchsdaten aus der
InfluxDB auf dem NAS. Das Modell sagt den Folgetag stundenweise voraus und markiert die
Fenster, in denen die Erzeugung über dem erwarteten Verbrauch liegt. Erfasst sind dabei
nur die Geräte, die an Messsteckdosen hängen — Heizung, Beleuchtung und alles ohne
Zwischenstecker bleiben außen vor. Die Zahlen beschreiben also nicht den gesamten
Haushalt, sondern den gemessenen Teil davon.

## Ergebnis

Der Dienst läuft dauerhaft in einem Container auf dem NAS, trainiert nach Zeitplan neu
und schickt morgens eine Pushover-Nachricht mit den Stunden, in denen sich Waschmaschine
oder Trockner lohnen. Was vorher ein Blick aus dem Fenster und ein Bauchgefühl war,
steht damit vor dem Frühstück auf dem Handy.
