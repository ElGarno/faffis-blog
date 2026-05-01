+++
title = "Fabian Wörenkämper - Lebenslauf"
date = 2026-05-01T00:00:00+02:00
draft = false
menu = "main"
weight = 20
tags = ["lebenslauf"]
birth_date_daughter = 2020-07-12T10:00:00+02:00
birth_date_son = 2022-07-05T10:00:00+02:00
+++

---
**Senior Full Stack Data Scientist, Krombacher**\
Wippeskuhlen 53, 57439 Attendorn\
📞 +49 171 274 956 0\
📧 [faffi@gmx.de](mailto:faffi@gmx.de)\
🌐 [LinkedIn](https://www.linkedin.com/in/fabian-woerenkaemper/) · [Facebook](https://www.facebook.com/el.garno)

---

## Über mich

Ehemann, Vater einer 5-jährigen Tochter und eines 3-jährigen Sohnes — mit Abstand der wichtigste Teil meines Lebens. Ansonsten: unverschämt gut gelaunt, allergisch gegen Konsens-Theater und überzeugt, dass die besten Ideen in einer Küche, auf einem Tennisplatz oder bei einem Pils entstehen — nicht in Status-Meetings.

Beruflich übernehme ich End-to-End-Verantwortung für AI-Produkte: von der Cloud-Infrastruktur auf AWS und Databricks über ML- und GenAI-Services bis zu Live-iOS-Apps im App Store. Lieber ein rougher POC heute Abend als ein weiteres Hype-Framework-Review morgen früh. Besonders besessen bin ich gerade von Agentic AI Development mit Claude Code (eigene Skills, Hooks, MCP-Server, Sub-Agents) — individuelle Delivery vervielfachen, ohne Qualität einzubüßen.

---

## Tools, Technologien & Fähigkeiten

- 💻 **Programmiersprachen**: Python, SQL, TypeScript, Swift, C++
- 🧰 **Frameworks**: FastAPI, SQLAlchemy, React Native (Expo), SwiftUI, Hugo
- ☁️ **Cloud**: AWS (S3, ECR, ECS, Sagemaker, Bedrock, Timestream), Railway, Cloudflare Pages
- 📊 **Databricks**: Unity Catalog, Delta Lake, PySpark, Workflows
- 🛠️ **IaC**: OpenTofu, Serverless Framework
- 🧠 **ML & GenAI**: MLflow, Huggingface; OpenAI, Anthropic, Bedrock, Groq, Ollama, Deepeval
- 🤖 **Agentic Dev**: Claude Code (Skills, Hooks, MCP-Server, Sub-Agents)

---

## Berufserfahrung

### Seit 2026: Senior Full Stack Data Scientist @ **Krombacher KSA**

- Beförderung zum Senior in 01/2026
- Fokus auf agentische Entwicklungs-Workflows mit Claude Code (Skills, Hooks, MCP-Server, Sub-Agents) zur Beschleunigung der AI-Delivery
- Weiterhin Verantwortung für AWS- und Databricks-basierte ML- und GenAI-Services

### 2022 – 2025: Data Scientist @ **Krombacher KSA**

- Full-Stack-Data-Science: Klassifikations- und Forecasting-Projekte
- AWS-Infrastruktur mit IaC (OpenTofu, Serverless Framework)
- Databricks-Plattform mit Unity Catalog, Delta Lake und Workflows für Produktions-ML-Pipelines
- Klippa-Replacement-PoC mit AWS Textract + Bedrock (Claude 3.5 Sonnet), Evaluation mit Deepeval, Leitung zweier Werkstudenten — −80 % Kosten und +16 % Detection-Quality

### 2020 – 2022: Data Scientist @ **Bosch Rexroth, Big Data and Simulation**

- Entwicklung und AWS-Migration von ODiN (Predictive Maintenance)
- Datenvisualisierung, Kundenbetreuung und Dashboard-Erstellung mit Python

### 2016 – 2020: Promotionsstudent @ **Bosch Rexroth, CoC Strömungs- und Strukturmechanik**

- Multidisziplinäre Optimierungs-Workflows für Ventilgehäuse
- Lebensdauer-Tool in C++
- Kooperation mit den Universitäten München, Kaiserslautern und Erlangen

### 2012 – 2016: Entwicklungsingenieur @ **Bosch Rexroth, Ventilentwicklung**

- Simulation und Optimierung von Hydraulikventilen
- Betreuung von Praktikanten und Abschlussarbeiten

---

## Personal Projects

### 2026: mAI Tasting (Whisky & Wine)

*Tech: FastAPI, React Native, OpenAI GPT-4o, Railway*

Zwei Production-iOS-Apps end-to-end auf einem geteilten FastAPI-Backend (Railway EU). [mAI Whisky und mAI Wine](https://maitasting.app) sind beide live im App Store. 12+ AI-Endpoints mit GPT-4o-Vision (Flaschen-/Etiketten-Erkennung, Verkostungs-Reihenfolge, Aromen-Fingerprints, Sammlungs-Diversität, gewichtete User-Aroma-Profile). Monorepo mit npm workspaces, JWT-Auth, EAS-Builds, Universal Links via AASA, Freemium-Modell. → [Blog-Post](/posts/mai-tasting/)

### 2026: Drink-Booking iPad App

*Tech: Swift, SwiftUI, SwiftData, CloudKit*

Native iPad-Kiosk-App für die Vereinstheke des TC Blau-Weiß Attendorn: digitale Strichliste, PIN-Login, Admin-Panel, CSV-/PDF-Export. Multi-iPad-Sync via CloudKit, Guided-Access als Kiosk-Lockdown, Master-PIN als Fallback im iOS-Keychain — ersetzt die analoge Strichliste der Vereinsmitglieder. → [Blog-Post](/posts/tcbw-getraenkebuchung/)

### 2026: TC Blau-Weiß Website

*Tech: Hugo, DecapCMS, Cloudflare Pages*

Ablösung der Legacy-WordPress-Seite durch eine statische, Git-basierte Architektur — live unter [tc-bw-attendorn.de](https://tc-bw-attendorn.de). Keine Angriffsfläche, Sub-1s-Ladezeiten via globales CDN, 0 €/Monat Hosting auf Cloudflare-Pages-Free-Tier. Headless CMS (DecapCMS) ermöglicht es Vorstandsmitgliedern, Inhalte ohne Markdown- oder Git-Kenntnisse zu pflegen. → [Blog-Post](/posts/tcbw-website/)

### 2024 – heute: MyTapo Energy Monitoring

*Tech: Python, InfluxDB, Grafana, Docker*

Echtzeit-Monitoring von TP-Link-Tapo-P110-Smartplugs; Zeitreihen-Speicherung in InfluxDB. Event-Detection-Pipeline klassifiziert Geräte-Events (Espresso, Waschmaschine, TV, Solar) automatisch und löst Pushover-Benachrichtigungen aus. AWTRIX-Pixel-Clock-Integration; Grafana-Dashboards; dockerisiertes Multi-Service-Deployment auf der Synology NAS. → [Blog-Post](/posts/Tapo/)

### 2024: AI Picture Book

*Tech: GPT-4, DALL-E 3, ElevenLabs*

Kinder-Bilderbuch mit AI-generierten Illustrationen und Erzählung; geklonte Stimmen via ElevenLabs, GPT-Vision für Charakter-Analyse. → [Blog-Post](/posts/NarrAItive/)

---

## Talks & Publications

### 02/2026: Podcast-Gast — Data Science Deep Dive #88 (INWT)

["Anomalie-Erkennung im Loyalty-Programm bei Krombacher"](https://www.podbean.com/ew/pb-apyrq-1a577b8). Diskussion zu Trust-Score-Modellierung mit Isolation Forest, Feature Engineering und tagesaktuellem Update-Workflow auf Databricks — verdächtige Aktivitäten erkennen, ohne ehrliche Power-User zu bestrafen.

---

## Ausbildung

### 2016 – 2020: Promotion in Simulationsmethoden @ **Bosch Rexroth**

### 2006 – 2012: Computational Engineering Science @ **RWTH Aachen**

- Schwerpunkt: Verbrennung und Strömungsmechanik
- Diplomarbeit (Note 1,3): Optimierung von Ventilgehäusen mittels evolutionärer Strategien
- Abschlussnote: 1,9

---

## Sprachen

- Deutsch (Muttersprache)
- Englisch (Fließend)
- Spanisch (Grundkenntnisse)
- Französisch (Grundkenntnisse)

---

## Off the Clock

- Bundesliga (BVB)
- Tennis (TC Blau-Weiß Attendorn)
- Kochen für Freunde
- Krombacher field-testing
- eSports
