+++
date = '2026-03-27T10:00:00+02:00'
draft = false
title = '⚡ MyTapo: Event-Detection statt reinem Energiemonitoring'
cover.image = "cover.webp"
cover.alt = "MyTapo Event-Detection Pipeline"
cover.caption = "Von Stromverbrauch zu Geräte-Events"
cover.relative = true
tags = ["Tapo", "Energiemonitoring", "InfluxDB", "Grafana", "AWTRIX", "Docker", "Synology"]
+++

Reines Energiemonitoring ist schnell langweilig. Eine Zeitreihe in Grafana, die hübsche Sägezähne zeichnet, beantwortet noch keine Frage, die mich im Alltag wirklich interessiert: *Ist die Waschmaschine fertig?* *Wie viele Espressi habe ich diese Woche gemacht?* *Lohnt sich der Trockner heute überhaupt, oder läuft die Solaranlage gleich auf Hochtouren?* Aus diesem Frust ist der nächste Schritt im [MyTapo-Repo](https://github.com/ElGarno/MyTapo) entstanden: weg vom rohen Verbrauchsstrom, hin zu diskreten Geräte-Events. Statt nur Watt zu messen, erkennt der Service jetzt Wasch-Zyklen, TV-Sessions und Espresso-Bezüge — und schickt die als strukturierte Datenpunkte in eine eigene InfluxDB-Bucket. Aus „messen" wird „verstehen".

## Architektur-Überblick

Die Pipeline besteht aus mehreren kleinen Diensten, die alle in Docker-Containern auf meinem Synology-NAS laufen. Tapo P110-Plugs liefern alle 15 Sekunden Verbrauchsdaten an einen Python-Collector (`influx_consumption`), der sie in die `power_consumption`-Bucket einer lokalen InfluxDB schreibt. Ein zweiter Service (`event_detector`) liest die Rohdaten, erkennt Geräte-Events anhand konfigurierter Profile und legt sie als eigene Zeitreihe in die `appliance_events`-Bucket. Daneben laufen `solar_energy_monitor`, `washing_machine_alert` und `washing_dryer_alert` als spezialisierte Services. Visualisiert wird in Grafana, Push-Benachrichtigungen gehen über Pushover an mich und meine Frau, und eine Ulanzi AWTRIX-Pixel-Clock im Wohnzimmer zeigt Live-Stats und Tageszusammenfassungen.

```
[Tapo P110]
    │  (HTTPS / KLAP)
    ▼
[influx_consumption] ──▶ InfluxDB: power_consumption
                               │
                               ▼
                       [event_detector] ──▶ InfluxDB: appliance_events
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
          [Grafana]        [AWTRIX]        [Pushover]
```

Alle Services teilen sich das Netzwerk auf dem NAS und konsumieren `.env`-Variablen — keine Magie, keine Cloud, kein Vendor-Lock-in.

## Event-Detection

Das Herz des Systems ist eine simple Zustandsmaschine pro Gerät: `idle → active → cooling_down → idle`. Jedes Gerät hat ein Profil mit Schwellwert-Hysterese (`threshold_on` / `threshold_off`), Mindest- und Maximaldauer sowie einer Cooldown-Zeit, die Doppel-Events nach Lastspitzen verhindert. Die globale `cooling_confirmation_seconds` (default: 30 s) sorgt dafür, dass kurze Stromabfälle — etwa Pausen zwischen Schleudergängen — nicht fälschlich ein Zyklusende auslösen.

Die aktuell konfigurierten Profile aus `config/appliance_profiles.json`:

| Gerät | Event | On | Off | Dauer |
|-------|-------|----|----|-------|
| `kaffe_bar` | espresso | >800 W | <50 W | 20 s – 3 min |
| `television` | tv_session | >30 W | <10 W | 1 min+ |
| `hwr_charger` | ebike_charge | >100 W | <20 W | 5 min+ |
| `bathroom` | hairdryer | >1000 W | <50 W | 30 s – 15 min |
| `kitchen` | airfryer | >1000 W | <100 W | 3 min – 1 h |
| `washing_machine` | wash_cycle | >100 W | <10 W | 10 min – 3 h |
| `washing_dryer` | dry_cycle | >40 W | <10 W | 10 min – 3 h |

Die Kernlogik ist bewusst klein gehalten:

```python
if state.state == "idle":
    if power >= profile["threshold_on"]:
        state.state = "active"
        state.event_start = timestamp
        state.power_readings = [(power, timestamp)]

elif state.state == "active":
    state.power_readings.append((power, timestamp))
    if power < profile["threshold_off"]:
        state.state = "cooling_down"
        state.cooling_start = timestamp

elif state.state == "cooling_down":
    if power >= profile["threshold_off"]:
        # Falscher Alarm — zurück in active
        state.state = "active"
    elif (timestamp - state.cooling_start).total_seconds() >= cooling_confirmation:
        return self._finalize_event(timestamp)
```

Beim Finalisieren wird Spitzen-, Durchschnittsleistung und Energie (`avg_power * duration / 3600`) berechnet und mit Tags wie `hour_of_day` und `day_of_week` in InfluxDB geschrieben — perfekt für Heatmaps. Details und Flux-Query-Beispiele finden sich in [`EVENT_DETECTION.md`](https://github.com/ElGarno/MyTapo/blob/main/EVENT_DETECTION.md).

## AWTRIX-Pixel-Clock-Integration

AWTRIX läuft auf einer Ulanzi Smart Pixel Clock (32×8 LEDs) und stellt eine kleine HTTP-API bereit. Notifications schickt der Service per `POST` an `/api/notify` mit JSON-Payload — Text, LaMetric-Icon-ID, Farbe, Anzeigedauer:

```python
url = f"http://{host}/api/notify"
payload = {
    "text": "Espresso: 45s",
    "icon": "4049",          # Coffee cup
    "color": "#00FF00",
    "duration": 10,
    "sound": "chime",
}
requests.post(url, json=payload, timeout=10)
```

Auf dem Display zeigt sich live die aktuelle Solar-Leistung (`Solar: 1240W`, mit Regenbogen-Effekt ab 1 kW), bei Bedarf eine Fertig-Meldung der Waschmaschine, sowie alle 20 Minuten (xx:05, xx:25, xx:45) eine rotierende Tag/Woche/Monat/Jahr-Zusammenfassung. Damit AWTRIX-Carousel und Notifications nicht kollidieren, vermeidet der Detector aktiv die Minuten 0–2 jedes 10-Minuten-Zyklus und queued Nachrichten in einem `deque`.

## Solar-Integration & Spar-Logik

Die Solaranlage hängt ebenfalls an einem Tapo-Plug. `solar_energy_generated.py` aggregiert die Tageserzeugung, vergleicht sie gegen Jahres-Maximum und -Mittelwert und multipliziert mit einem Strompreis (28 ct/kWh), um eine grobe Ersparnis auszugeben:

```python
solar_today_kwh = df.loc[today_str]["Value"] / 1000
saved_costs_today = compute_costs(solar_today_kwh)  # 0.28 €/kWh
```

Während der Tageslicht-Stunden (6–19 Uhr) blinkt die aktuelle Erzeugung alle 10 Minuten auf der AWTRIX. So sieht man auf einen Blick, ob es sich lohnt, den Trockner *jetzt* anzuwerfen — oder lieber abends, wenn die Wäsche eh schon trocken ist und der Strom günstig ist.

## Lessons Learned

Das KLAP-Protokoll der Tapo-Geräte wirft regelmäßig `SessionTimeout`- oder `403 Forbidden`-Fehler. Im Repo löse ich das mit einem `tapo_connection_pool`, der Sessions proaktiv alle 120 Minuten erneuert (`session_refresh_minutes = 120`) und zusätzlich reaktiv neu authentifiziert, sobald die typischen Auth-Indikatoren `403`, `Forbidden`, `SessionTimeout` oder `Response error` auftauchen. Auf dem Synology-NAS brauchen die Container `platform: linux/amd64` und `network_mode: "bridge"` in der Compose-Datei — sonst gibt es Probleme mit DNS-Auflösung und Architektur-Mismatches.

## Fazit

Der Sprung von „rohem Verbrauch in InfluxDB" zu „strukturierten Geräte-Events" hat das System schlagartig nützlicher gemacht. Statt Watt zu interpretieren, lese ich Sätze wie *„Heute: 3 Espressi, 2.1 h TV, 1 Wasch-Zyklus"* auf der Pixel-Uhr ab. Code und Doku liegen offen unter [github.com/ElGarno/MyTapo](https://github.com/ElGarno/MyTapo). Wer mehr zu Heim-Automatisierung lesen mag, findet einen weiteren Side-Quest unter [/posts/NarrAItive/](/posts/NarrAItive/).
