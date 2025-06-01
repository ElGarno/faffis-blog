+++
title = "Docker Volumes verstehen: Daten sichtbar und sicher speichern"
date = '2025-06-01T11:45:12+02:00'
draft = false
tags = ["docker", "volumes", "synology", "n8n", "tutorial"]
description = "Was Docker Volumes sind, warum sie wichtig sind – und wie du sie so nutzt, dass deine Daten dauerhaft sichtbar und gesichert bleiben."
cover.image = "blog_docker_volumes.webp" 
cover.alt = Volume Storage, Container, Docker, Host" 
cover.caption = "Volume Storage in Docker: Container-Daten dauerhaft sichern" 
cover.relative = true
+++

## Warum Volumes in Docker wichtig sind

Wer Docker nutzt, weiß: Container sind flüchtig. Sobald ein Container gelöscht oder neu erstellt wird, sind alle darin gespeicherten Daten weg – **es sei denn, man nutzt Volumes**.

**Volumes** sind der Mechanismus von Docker, um **Daten persistent** zu speichern – also unabhängig vom Lebenszyklus eines Containers. Doch nicht alle Volumes sind gleich: Man unterscheidet zwischen **Docker-verwalteten Volumes** und sogenannten **Bind Mounts**.

---

## Docker Volume vs. Bind Mount

| Art            | Beschreibung                                                                 | Sichtbar im Dateisystem? |
|----------------|------------------------------------------------------------------------------|---------------------------|
| Docker Volume  | Docker verwaltet Speicherort automatisch unter z. B. `/var/lib/docker/volumes` | ❌ Nur über Docker sichtbar |
| Bind Mount     | Du bindest ein Verzeichnis auf deinem Host in den Container ein               | ✅ Sichtbar im Dateisystem  |

---

## Beispiel: n8n Container mit Bind Mount

Wenn du z. B. den Automatisierungs-Dienst [n8n](https://n8n.io/) nutzt und möchtest, dass deine Workflows **nicht verloren gehen**, solltest du den Datenpfad `/home/node/.n8n` auf deinem NAS sichtbar machen.

```yaml
volumes:
  - /volume1/docker/n8n/data:/home/node/.n8n
```

In diesem Fall werden alle Workflows, Credential-Dateien und Einstellungen in deinem Synology-Ordner gespeichert – **auch wenn du den Container später neu aufsetzt**.

---

## Workflows sichern vor Neuinstallation

Wenn du deinen Container neu aufsetzen möchtest:

### 1. **Workflows exportieren (vorher)**
- Gehe im n8n Webinterface auf:
  **Settings → Import/Export → Export All Workflows**
- Lade die `.json`-Datei herunter und bewahre sie sicher auf.

### 2. **Container löschen & neu erstellen**
- Lösche den alten Container:
  ```bash
  docker compose down
  ```
- (Optional: Volume-Verzeichnis vorher sichern)

### 3. **Compose File mit Bind Mount**
Stelle sicher, dass dein `docker-compose.yml` den richtigen Mount nutzt:
```yaml
volumes:
  - /volume1/docker/n8n/data:/home/node/.n8n
```

### 4. **Container starten**
```bash
docker compose up -d
```

### 5. **Workflows wieder importieren**
- Gehe auf **Settings → Import/Export → Import from File**
- Lade deine gesicherte `.json`-Datei wieder hoch.

---

## Vorteile von Bind Mounts

- 🔎 **Transparenz:** Du kannst die Dateien jederzeit über die Synology File Station einsehen.
- 💾 **Backup:** Du kannst die Daten bequem per rsync, Hyper Backup oder Snapshot sichern.
- 🔁 **Upgrade-sicher:** Neuinstallation oder Updates der Container löschen keine Daten.
- 👨‍💻 **Entwicklung & Debugging:** Du kannst direkt im Dateisystem arbeiten, z. B. Logfiles prüfen.

---

## Fazit

**Docker Volumes** sind essenziell für persistente Daten. Wenn du auf einer Synology NAS arbeitest (oder jedem anderen Host), solltest du **bewusst Bind Mounts** einsetzen, um Daten transparent zu speichern und Backup-fähig zu halten.

Ein kleiner Mehraufwand beim Einrichten – aber große Sicherheit im Betrieb.

---

**Tipp:** Du nutzt z. B. Paperless-ngx oder andere datenintensive Container? Dann gilt dasselbe Prinzip. Lieber einmal sauber mounten, als später wichtige Dokumente verlieren.

---

Wenn du Hilfe beim Anpassen deines Compose-Files brauchst oder deine Container-Daten richtig migrieren möchtest, schreib mir gerne bei linkedIn. Ich helfe dir gerne weiter!
