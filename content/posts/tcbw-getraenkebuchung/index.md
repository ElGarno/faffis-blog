+++
date = '2026-04-17T10:00:00+02:00'
draft = false
title = '📲 Getränkebuchung im Tennisclub: SwiftUI-Kiosk-App auf dem iPad'
cover.image = "cover.webp"
cover.alt = "iPad Kiosk-App auf der Vereinstheke"
cover.caption = "Strichliste war gestern"
cover.relative = true
tags = ["SwiftUI", "SwiftData", "CloudKit", "NFC", "iPad", "Kiosk", "Vereins-IT"]
+++

An der Theke im Vereinsheim hängt seit gefühlt immer eine Strichliste. Eine A4-Seite, ein Kugelschreiber an einer Schnur, und neben jedem Namen eine Reihe von Strichen: Bier, Wasser, Apfelschorle. Das funktioniert in der Theorie. In der Praxis ist das Ergebnis am Monatsende für den Kassenwart oft mehr Rätselraten als Buchhaltung. Die Frage war: Geht das digitaler, ohne dass an der Theke ein zweiter Bildschirm im Weg steht? Ein iPad steht eh schon dort. Kein PC, kein Drucker, kein Kassensystem.

## Anforderungen

Die Erwartungen an eine digitale Lösung waren klar und sehr alltagsnah:

- **Schnell buchen.** Mitglied tappt seinen Vereinsausweis aufs iPad, sieht den eigenen Kontostand und bucht ein Getränk in zwei bis drei Taps. Mehr Schritte, und es geht zurück zur Strichliste.
- **Multi-iPad.** Vorne an der Theke und im Sommer auf der Terrasse soll parallel gebucht werden, beide Geräte synchron.
- **Offline-fähig.** Das WLAN im Vereinshaus ist nicht jeden Tag stabil. Buchungen müssen lokal funktionieren und später synchronisieren.
- **Admin-Panel.** Vorstand und Kassenwart sehen Mitgliederliste und Kontostände, können korrigieren und das Getränke-Sortiment pflegen.
- **Master-PIN-Fallback.** Karte vergessen, Karte kaputt, Karte noch nicht ausgegeben — es muss einen Notausgang geben.
- **Export.** CSV oder PDF für die Abrechnung am Monatsende.
- **Kiosk-Modus.** Niemand kommt versehentlich auf den Home-Screen oder in eine andere App.

## Architektur

High-Level, ohne Code:

- **SwiftUI** als UI-Framework. Schnelle Iteration, declarative Views, Live-Vorschau in Xcode — perfekt für eine App, die oft an der Theke selbst getestet werden muss.
- **SwiftData** als lokale Persistenz. Apples neueres Framework über Core Data, mit decorator-basierter Schema-Definition. Ideal für offline-first: Buchungen werden immer zuerst lokal geschrieben, der Sync läuft im Hintergrund.
- **CloudKit** als Sync-Layer. Die App nutzt einen privaten CloudKit-Container, der die Daten zwischen den iPads des Vereins synchronisiert. Seit iOS 17 hat SwiftData eine native CloudKit-Bridge — keine eigene Sync-Logik nötig.
- **Core NFC** für die Vereinsausweise. Moderne Mitgliedsausweise tragen einen NFC-Chip; das iPad liest die ID und matcht gegen die lokale Mitgliederliste. Kein Login-Bildschirm, kein Passwort.
- **iOS Keychain** für den Master-PIN. Biometrisch geschützt, lokal pro Gerät, kein Cloud-Sync — der PIN soll genau dort bleiben, wo er gebraucht wird.
- **Guided Access** als Kiosk-Lockdown. iOS-Bordmittel, kein MDM, kein laufendes Lizenz-Tail. Einmal aktiviert, kommt niemand ohne Master-PIN aus der App raus.

Konzeptionell sieht das so aus:

```
   ┌──────────┐         ┌──────────┐
   │ iPad     │         │ iPad     │
   │ Theke    │         │ Terrasse │
   └────┬─────┘         └────┬─────┘
        │                    │
        └────────┬───────────┘
                 │
        ┌────────▼─────────┐
        │ CloudKit         │
        │ (private)        │
        └────────┬─────────┘
                 │
          ┌──────▼──────┐
          │ Admin-iPad  │
          │ (optional)  │
          └─────────────┘
```

## Datenmodell-Skizze

Konzeptionell, nicht das echte Schema. Drei Hauptkonzepte reichen, um den Use Case abzudecken:

- **Mitglied.** Name, NFC-Token (die ID, die der Ausweis liefert), optional ein laufender Kontostand.
- **Getränk.** Bezeichnung, Preis, optional eine Sortiment-Reihenfolge für die Anzeige im Auswahl-Grid.
- **Buchung.** Verknüpfung Mitglied + Getränk + Zeitstempel, plus optionales Storno-Flag für Korrekturen.

Mehr braucht es zunächst nicht. Aggregationen wie Monatssummen oder Top-Getränke ergeben sich aus den Buchungen on the fly. Erweiterungen wie Saisonpässe oder Mengenrabatte sind absichtlich noch nicht im Datenmodell — Stichwort YAGNI.

## Status

Die App läuft auf dem iPad an der Vereinstheke und wird von den Mitgliedern aktiv genutzt — die Resonanz ist durchweg positiv.

## Fazit

Eine schlanke iPad-App, die genau eine Sache gut machen muss, ist ein dankbarer Anwendungsfall für SwiftUI + SwiftData + CloudKit. Das Repo ist privat (Vereinsdaten, Mitgliederbezug), daher kein öffentlicher Link. Wer den Hintergrund zur Vereins-IT-Landschaft mag: siehe den Post zur [Vereinswebsite-Migration](/posts/tcbw-website/) — gleiches Toolkit-Denken, anderer Layer.
