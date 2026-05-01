+++
date = '2026-04-03T10:00:00+02:00'
draft = false
title = '🔧 Wippestoolen: Werkzeug-Sharing für die Nachbarschaft'
cover.image = "cover.webp"
cover.alt = "Wippestoolen Tool-Sharing-Plattform"
cover.caption = "Nachbarschaftshilfe als Plattform"
cover.relative = true
tags = ["Wippestoolen", "FastAPI", "Postgres", "Sharing-Economy", "Plattform"]
+++

Werkzeuge liegen die meiste Zeit ihres Lebens im Keller. Eine Bohrmaschine wird im Schnitt rund 13 Minuten *überhaupt* benutzt — den Rest der Zeit sammelt sie Staub, neben einer Stichsäge, die der Nachbar zwei Häuser weiter ebenfalls einmal im Jahr aus dem Regal holt. In der gleichen Straße steht in jedem zweiten Keller dieselbe Schlagbohrmaschine, derselbe Akku-Schrauber, derselbe Vertikutierer. Das ist absurd. Aus diesem Frust ist die Idee zu **Wippestoolen** entstanden — einer kleinen, lokalen Plattform, auf der Nachbarn ihre Werkzeuge teilen, ausleihen und wiederfinden können. Inspiriert von Foodsharing, aber für die Schmuckkästchen-Säge im Keller. Die Landing-Seite läuft unter [wippestoolen.vercel.app](https://wippestoolen.vercel.app), das eigentliche Produkt entsteht gerade Schritt für Schritt nebenbei.

## Konzept

Wippestoolen ist im Kern ein zweiseitiger Marktplatz auf Nachbarschaftsebene. Wer ein Werkzeug besitzt, legt es als Listing an: ein paar Fotos, kurze Beschreibung, Verfügbarkeit, ungefährer Standort. Wer ein Werkzeug *braucht*, sucht in einer Karten-Ansicht nach allem, was in Lauf-Distanz verfügbar ist — also realistisch zwischen „eben um die Ecke holen" und „auf dem Heimweg vom Bäcker mitnehmen". Aus einem Treffer wird eine Buchung mit klarem Status-Verlauf, nach der Rückgabe bewerten sich beide Seiten gegenseitig. Login geschieht über Email mit verifiziertem Account, das Frontend ist responsive gebaut, sodass dieselbe Oberfläche am Handy in der Garage und am Laptop am Küchentisch funktioniert. Eine native Mobile-App teilt sich später dasselbe Backend.

## High-Level-Architektur

Technisch ist die Plattform bewusst klassisch geschnitten: ein Backend-Service in Python auf Basis von **FastAPI**, das gegen eine **Postgres**-Datenbank über SQLAlchemy spricht. Daneben **Redis** als schneller Cache und Session-Store, **AWS S3** für die Werkzeug-Fotos. Das Frontend ist eine separate Single-Page-App, deployed auf **Vercel** — getrennt von der API, kommuniziert nur über HTTPS-Calls. Die Landing-Seite ist ein eigenes statisches Mini-Projekt, das nur die Idee verkauft. Backend und Datenbank leben auf **Railway** (Managed Postgres). Authentifizierung läuft über **JWT**, der Sign-up zwingt zur Email-Bestätigung, bevor man irgendetwas Schreibendes tun kann. Eine native Mobile-App ist in Vorbereitung; sie wird gegen exakt dieselbe API sprechen wie das Web-Frontend, was den größten Hebel für gleiche Geschäftslogik in beiden Welten gibt.

```
[Browser / Mobile]
       │
       ▼
[Vercel-Frontend / Native App]
       │  HTTPS + JWT
       ▼
[Railway: FastAPI-Service]
       │
   ┌───┼─────────┬───────────┐
   ▼   ▼         ▼           ▼
[Postgres] [Redis]   [S3: Tool-Fotos]
```

Die strikte Trennung zwischen Frontend, Backend und Storage zahlt sich später aus: die Mobile-App fügt sich ohne weitere Schicht ein, und das Frontend lässt sich austauschen, ohne die API anzufassen.

## Trust-System

Sharing-Economy steht und fällt mit Vertrauen. AirBnB hatte es, bevor es funktionierte. eBay hat es jahrzehntelang verfeinert. Wer ein eigenes Werkzeug verleiht, möchte es heil — und mit dem dritten Bohrer noch dran — zurückbekommen. Wer leiht, will keine alte Schrott-Kiste, die unterwegs auseinanderfällt. Beide Seiten haben also ein berechtigtes Interesse an der Reputation der jeweils anderen. Die Lösung: gegenseitige Bewertungen nach jeder abgeschlossenen Transaktion, sichtbare Profile mit aggregiertem Score, und ein schrittweiser Aufbau von Reputations-Kapital über die Zeit. Das klassische Henne-Ei-Problem — niemand hat zu Beginn eine Reputation — ist ehrlich gesagt unangenehm und nicht final gelöst. Die aktuelle Idee: in der Anfangsphase über Nachbarschafts-Identifikation (verifizierte Email auf eine bekannte Domain, optional eine Bestätigung durch einen anderen verifizierten User in der Straße) Vertrauen lokal einfließen lassen. Das macht den ersten Bohrer-Verleih leichter, ohne ein vollständiges KYC-Theater aufzubauen.

## Booking-Flow

Eine Buchung läuft als überschaubare Statusmaschine: **Anfrage** → **Bestätigung** → **Übergabe / im Einsatz** → **Rückgabe** → **gegenseitige Bewertung**. Klingt trivial, sobald aber Realität dazwischenfunkt, wird es interessant. Was passiert, wenn der Borrower nicht zur Übergabe erscheint? Was, wenn die Säge zwei Tage später als verabredet zurückkommt? Was, wenn jemand mitten im Zeitraum stornieren muss, weil das Renovierungs-Wochenende wegen Familienbesuch ausfällt? Und vor allem: was, wenn beide Seiten unterschiedlich erinnern, in welchem Zustand das Werkzeug übergeben wurde? Die aktuelle Position ist klar peer-first: die Plattform schubst Erinnerungen über Notifications, dokumentiert Übergaben mit Foto-Belegen und legt Konflikte transparent in beide Profile, greift aber inhaltlich nicht ein. Eine Schiedsrichter-Rolle wird erst dann sinnvoll, wenn das Volumen es rechtfertigt — und nicht ab Tag eins.

## Status & Roadmap

Stand heute: das Backend-Repo ist privat und wird kontinuierlich ausgebaut, die Landing-Seite ist live, das Web-Frontend in der MVP-Phase, die Mobile-App im Konzept. Das Projekt läuft bewusst nebenbei — Familie und Hauptjob haben Priorität.

## Fazit

Wippestoolen ist der ehrliche Versuch, ein Alltagsproblem mit einer schlanken Plattform zu lösen, statt mit einem WhatsApp-Verteiler. Wer reinschauen mag: [wippestoolen.vercel.app](https://wippestoolen.vercel.app). Im selben „Side-Project nebenbei"-Geist läuft auch das Energiemonitoring auf dem Synology-NAS — dazu mehr in [/posts/Tapo/](/posts/Tapo/).
