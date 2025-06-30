+++
date = '2025-06-01T11:30:12+02:00'
draft = false
title = '🚀 YouTube-Videos automatisch ins Obsidian Vault übernehmen – mit Fabric & ZSH'
cover.image = "blog_yt_obsidian.webp" 
cover.alt = "convert YouTube videos to Obsidian notes" 
cover.caption = "YouTube-Videos automatisch in Obsidian Vault übernehmen" 
cover.relative = true
+++


Du nutzt Obsidian als persönlichen Wissensspeicher und möchtest YouTube-Inhalte automatisch als strukturierte und übersetzte Notizen speichern – mit nur einem Terminal-Befehl? Dann ist dieses Setup genau das Richtige für dich.

In dieser Anleitung zeige ich dir, wie du das Open-Source-Tool [Fabric](https://github.com/danielmiessler/fabric) nutzt, um Inhalte aus YouTube-Videos zu extrahieren, ins Deutsche zu übersetzen und direkt als Markdown-Datei in deinem Obsidian Vault zu speichern. Das Ganze basiert auf einem Alias in `.zshrc`, funktioniert aber auch mit jeder anderen Shell.

---

## Warum YouTube-Videos in Obsidian?
YouTube ist eine riesige Wissensquelle, aber oft fehlt die Zeit, um Videos anzusehen oder die wichtigsten Informationen herauszufiltern. Zudem können die Videos direkt "durchsuchbar" gemacht werden, indem sie in Markdown-Dateien umgewandelt werden. So kommen die passenden Inhalte manchmal auch zufällig bei der Suche nach einem bestimmten Thema zum Vorschein.
**Das Beste: Die in markdown umgewandelten Videos lassen sich mit den aktuellen LLMs (Large Language Models) schnell analysieren, zusammenfassen oder vergleichen.**

Mit diesem Setup kannst du:
- Videos automatisch zusammenfassen
- Inhalte ins Deutsche übersetzen
- Ergebnisse direkt in deinem Obsidian Vault speichern

---

## 🧵 Was ist Fabric?

[Fabric](https://github.com/danielmiessler/fabric) ist ein leistungsstarkes Tool zur KI-gestützten Textanalyse. Es verwendet sogenannte "Patterns", um Inhalte aus verschiedenen Quellen zu extrahieren, zu transformieren und zusammenzufassen. Die Patterns sind wie Vorlagen (vordefinierte Prompts), die dir helfen, spezifische Informationen aus Texten zu extrahieren und zu verarbeiten.  Sie sind komplett in Markdown geschrieben und können leicht angepasst oder komplett neu erstellt werden.
Mit Fabric muss sich also nicht selbst um das perfekte Prompting gekümmert werden. Dieser Teil wird einem durch Fabric abgenommen.

---

## 🛠️ Installation

### 🔄 Mit cURL (macOS, ARM64)

```bash
curl -L https://github.com/danielmiessler/fabric/releases/latest/download/fabric-darwin-arm64 > fabric
chmod +x fabric
./fabric --version
```

💡 **Tipp**: Du kannst Fabric auch über `brew` installieren. Siehe [offizielle Dokumentation](https://github.com/danielmiessler/fabric).

---

### ⚙️ Mit Go (empfohlen für neueste Version)

Stelle sicher, dass [Go installiert ist](https://go.dev/doc/install), und führe dann aus:

```bash
go install github.com/danielmiessler/fabric@latest
```

Füge deiner Shell-Konfiguration (`.zshrc`, `.bashrc`, etc.) Folgendes hinzu:

```bash
export GOROOT=$(brew --prefix go)/libexec
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$HOME/.local/bin:$PATH
```

Dann einmalig ausführen:

```bash
fabric --setup
```

Das initialisiert die Fabric-Verzeichnisse und Konfigurationsdateien.

Hier können sowhl die API-Schlüssel für OpenAI, DeepL und andere Dienste hinterlegt werden, die Fabric nutzt. Des Weiteren muss für die Extraktion aus YouTube-Videos der YouTube-API-Schlüssel hinterlegt werden. 
Dieser lässt sich über die Google Cloud Console generieren.
Dazu musst du ein Projekt erstellen, die YouTube Data API aktivieren und einen API-Schlüssel generieren. 
⚠️ **Achtung**: Seit 06/25 muss neben dem API-Schlüssel für YouTube auch yt-dlp installiert sein, um die Videos herunterladen zu können. Hier die [Info](https://github.com/danielmiessler/fabric#:~:text=June%2011%2C%202025,%2D%2Dmetadata%20flag).

---

## 📁 Eigene Patterns

Die Pattern-Dateien findest du hier:

```bash
~/.config/fabric/patterns/
```

In meinem Repository befindet sich der Ordner `additional_patterns` mit **meinen eigenen Patterns**, darunter:

- `extract_wisdom_shortened`
- `translate_to_german`

Bitte kopiere diese in deinen lokalen Fabric-Ordner.

---

## ⚡ YouTube-Kürzel im Terminal

Füge folgende Funktion zu deiner `~/.zshrc` (oder deiner Shell) hinzu:

```bash
yt() {
    local youtube_url="$1"
    local file_title="$2"
    local obsidian_path="pfad_zu_deinem_obsidian/Fabric"
    local file_path="${obsidian_path}/${file_title}.md"
    fabric -y "$youtube_url" --pattern extract_wisdom_shortened | fabric -o "$file_path" --pattern translate_to_german
}
```

🧠 Was passiert hier?

1. Du gibst eine YouTube-URL und einen Dateinamen an.
2. Fabric fasst das Video zusammen mit `extract_wisdom_shortened`.
3. Die Zusammenfassung wird ins Deutsche übersetzt.
4. Das Ergebnis wird als `.md`-Datei in deinem Obsidian-Vault gespeichert.

---

### 📌 Beispielbefehl

```bash
yt "https://www.youtube.com/watch?v=ZTFaYvZdVGs" "Digitale_Profis_2025_04_03_Jellypod"
```

Ergebnis: Eine deutsche Zusammenfassung des Videos als Markdown-Datei im Ordner `Fabric` deines Obsidian Vaults.

---

## 🔁 Fabric aktuell halten

Um Fabric zu aktualisieren, einfach denselben Befehl erneut ausführen:

```bash
go install github.com/danielmiessler/fabric@latest
```

---

## 🧠 Fazit

Dieses Setup automatisiert deinen persönlichen Wissensworkflow: Es extrahiert Inhalte aus Videos, übersetzt sie und speichert sie direkt in deinem digitalen Gehirn (Obsidian). Ideal für alle, die effizient lernen und Inhalte systematisch erfassen möchten.

🔗 [GitHub Repository](https://github.com/ElGarno/fabricAI_setup_obsidian)
