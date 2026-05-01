+++
date = '2026-04-24T10:00:00+02:00'
draft = false
title = '🥃 mAI Tasting: Zwei iOS-Apps auf einem GPT-4o-Backend'
cover.image = "cover.webp"
cover.alt = "mAI Whisky und mAI Wine Architektur"
cover.caption = "Ein Backend, zwei Apps, viele AI-Endpoints"
cover.relative = true
tags = ["FastAPI", "React Native", "GPT-4o", "Vision", "iOS", "Monorepo", "Railway"]
+++

Angefangen hat es mit einem ganz analogen Problem: einer wachsenden Whisky-Sammlung und einem Notizbuch, in dem Verkostungs-Notizen mit der Zeit verblassen — und mit ihnen der Geschmack im Kopf. Dazu der Klassiker, dass man irgendwann den Überblick verliert, welche Flaschen schon zuhause stehen. Aus diesem Bedarf wuchs die Idee, GPT-4o-Vision für Etiketten-Erkennung zu nutzen — Foto vom Etikett, Flasche ist im System. Aus dem Whisky-Use-Case wurde **mAI Whisky**, parallel folgte die gleiche Idee für Wein als zweite App: **mAI Wine**. Beide sind heute live im App Store. Landing: [maitasting.app](https://maitasting.app).

## App-Store-Status

**mAI Whisky** und **mAI Wine** sind beide im App Store verfügbar. Erste Freunde und Kollegen testen die Apps aktiv und das Feedback ist sehr positiv. Beide Apps haben einen eigenen visuellen Charakter — eine dunkle, holzige Anmutung für Whisky, eine hellere für Wein — teilen sich aber komplett den Tech-Stack und das Backend. Links findet ihr auf [maitasting.app](https://maitasting.app).

## Architektur-Überblick

Das Setup ist bewusst einfach gehalten: ein Backend, zwei Frontends, ein AI-Provider. Der Server ist eine **FastAPI-Anwendung in Python**, deployed auf **Railway in einer EU-Region**. Die EU-Wahl hat zwei Gründe: DSGVO-Konformität und niedrige Latenz für die bisher größte Nutzergruppe im deutschsprachigen Raum. Als persistente Datenbank dient ein **Postgres**, ebenfalls Railway-managed. Hochgeladene Etiketten-Fotos liegen in einem **S3-kompatiblen Object Storage**, die DB hält nur die Referenzen.

Das Herzstück der AI-Funktionen ist **GPT-4o** als Vision- und Text-Modell. Alle Vision-Tasks laufen über dieses eine Modell — das Backend ist ein **Orchestrierungs-Layer**, der Bilder vorbereitet, Prompts zusammensetzt, Antworten parst und das Ergebnis strukturiert ablegt. Die Apps sprechen niemals direkt mit OpenAI, alle GPT-Calls laufen serverseitig — das schützt API-Keys, ermöglicht Rate-Limiting pro Nutzer und erlaubt einen späteren Provider-Wechsel ohne App-Update.

Auth-seitig kommt ein **JWT-Verfahren** mit Refresh-Token-Flow zum Einsatz, Sign-up via Email. Für geteilte Inhalte nutze ich **Universal Links** via AASA, sodass ein Link je nach installierter App im richtigen Frontend oder im Browser landet.

```
   ┌────────────┐        ┌────────────┐
   │ mAI Whisky │        │  mAI Wine  │
   │  (iOS App) │        │  (iOS App) │
   └─────┬──────┘        └─────┬──────┘
         │   HTTPS / JWT       │
         └──────────┬──────────┘
                    ▼
            ┌───────────────┐
            │   FastAPI     │
            │ (Railway EU)  │
            └───┬───┬───┬───┘
                │   │   │
       ┌────────┘   │   └────────┐
       ▼            ▼            ▼
  ┌─────────┐ ┌──────────┐ ┌──────────┐
  │ Postgres│ │  S3-like │ │ GPT-4o   │
  │         │ │  Storage │ │ (OpenAI) │
  └─────────┘ └──────────┘ └──────────┘
```

## AI-Endpoints kategorisiert

Insgesamt hängen am Backend über zwölf AI-Endpoints, die ich gedanklich in vier Kategorien sortiere:

- **Recognition** — Foto rein, Flasche raus. Das Etikett wird zugeschnitten, eine OCR-ähnliche Layout-Analyse durchgeführt und das Ergebnis gegen eine interne Stammdatenbank gematcht. GPT-4o-Vision liest Marke, Distillerie oder Region, Jahrgang/Alterung, Abfüller. Liegt der Confidence-Score unter der Schwelle, schlägt das Frontend Top-3-Alternativen vor, statt eine falsche Treffer-Annahme zu zementieren.

- **Tasting** — der Nutzer hat eine Sammlung und plant ein Verkostungs-Flight. Das Backend schlägt eine sinnvolle **Reihenfolge** vor (leicht → komplex, regionale Cluster), damit der Gaumen nicht von der ersten torfigen Flasche überfordert ist. Außerdem werden freie Verkostungs-Notizen in einen strukturierten **Aromen-Fingerprint** übersetzt — Achsen wie rauchig, süß, fruchtig, vanillig, floral, würzig.

- **Profiling** — aus den Bewertungen über die Zeit baut das System ein gewichtetes **User-Aroma-Profil**. Welche Geschmacks-Achsen mag der Nutzer überdurchschnittlich? Höhere Bewertungen werden stärker gewichtet als Durchschnittsnoten, damit sich das Profil nicht durch ein einzelnes „okay" verwässert.

- **Collection-Health** — Metriken zur **Sammlungs-Diversität**, blinde Flecken („du hast viel Speyside, aber keinen einzigen Islay") und Empfehlungen für neue Flaschen, die sowohl zum Profil als auch zur Diversifikation passen.

Jede Kategorie umfasst mehrere Routen mit eigenen Eingabe- und Ausgabeformaten; Recognition allein hat mehrere Varianten je nach Bildkontext.

## Monorepo-Struktur

Das Mobile-Repo ist als **npm-Workspaces-Monorepo** organisiert: ein Workspace pro App und ein gemeinsamer Shared-Workspace. Die App-Workspaces sind eigenständige Expo-Projekte für Whisky bzw. Wine, der Shared-Workspace enthält UI-Komponenten und einen typisierten API-Client, den beide Apps konsumieren.

Das Reasoning ist pragmatisch: Rund 80 % des UI-Codes sind domänen-agnostisch — Login, Settings, Foto-Capture, Detail-Listen, Filter, Suche, Auth-Flows. Die übrigen 20 % sind whisky- bzw. wein-spezifisch (Aroma-Achsen, Bewertungs-Skalen, Region-Modelle). Eine geteilte API-Client-Library bedeutet außerdem, dass eine Backend-Änderung an einer einzigen Stelle nachgezogen wird und beide Apps gleichzeitig mitziehen — kein Drift zwischen den Frontends.

## Freemium-Modell

Beide Apps laufen als **Freemium**: Der Free Tier enthält die Basis-Funktionen — Sammlung pflegen, Verkostungen einsehen, Etiketten-Erkennung mit monatlichem Limit. Der Paid Tier hebt das Vision-Limit auf, schaltet Profiling und Collection-Health frei und erlaubt unbegrenzte Tasting-Auswertungen. Die Begründung ist nüchtern kalkulatorisch und nicht investorengetrieben: GPT-4o-Calls sind die mit Abstand größten variablen Kosten. Ein Power-User mit hundert Vision-Calls pro Monat kostet spürbar Geld — die Subscription muss das im Power-Case decken, damit das Projekt sich selbst trägt.

## EAS-Build & App-Store-Story

Für die iOS-Builds nutze ich **Expo Application Services (EAS)**: Builds laufen in der EAS-Cloud, werden mit dem AppStoreConnect-Account signiert und direkt in TestFlight hochgeladen. Lokal brauche ich weder einen Xcode-Build noch einen Mac-Build-Server — ein Linux-Laptop reicht für die komplette Release-Pipeline.

Die AppStoreConnect-Submission ist eine eigene Lernkurve: Screenshots in mehreren iPhone-Größen, ausgefülltes Privacy-Manifest, ein Age-Rating, das Alkohol-Bezug korrekt deklariert, sowie eine Store-Beschreibung, die Apples Review-Richtlinien zu alkoholbezogenen Inhalten respektiert.

## Fazit

Zwei Apps, ein Backend, ein AI-Provider — und eine sehr persönliche Domäne als Auslöser. Beide Apps sind live im App Store, der öffentliche Auftritt liegt unter [maitasting.app](https://maitasting.app). Siehe auch das zweite iOS-Side-Projekt unter [TCBW Getränkebuchung](/posts/tcbw-getraenkebuchung/).
