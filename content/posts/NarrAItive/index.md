+++
date = '2025-06-02T13:10:12+02:00'
draft = false
title = '🚀 NarrAItive - Die digitalen Kinder-Bilderbücher der Zukunft'
cover.image = "NarrAItive_logo.webp" 
cover.alt = "NarrAItive Logo" 
cover.caption = "NarrAItive - Die digitalen Kinder-Bilderbücher der Zukunft"
tags = ["NarrAItive", "Kinderbuch", "AI", "Dall-E-3", "Elevenlabs", "Streamlit"] 
cover.relative = true
+++

## Motivation

Eines Sonntags im Jahr 2023 saß ich im Wohnzimmer und staunte über die Berge an Bilderbüchern für unsere Kinder.
ChatGPT war noch recht neu und als Bilderstellungstool gab es zu dem Zeitpunkt "nur" Midjourney und andere schwächere text-2-image Tools wie stable diffusion oder dall-e-2.
Doch ich hatte die Idee eines hoch-individuellen Kinderbuchs mit auf Basis von Streamlit mit Hilfe von ChatGPT und Midjourney. Ich recherchierte zunächst, wie ich Midjourney über Python ansprechen kann, doch das Ergebnis, dass es dazu keine offizielle API gibt war zunächst ernüchternd. 
Nachdem nach den ersten Tests jedoch Dall-E-3 erschien, stand dem ersten POC nichts mehr im Wege. Nach einem Monat stand eine Version, welche die ursprüngliche Idee bei weitem übertraf - mit einer Historie der erstellten Geschichten, einer automatischen Einbettung der Hauptcharaktere, mit einer Vorlesefunktion und Voice-Cloning der Liebsten.

---

## Von der Idee zur fertigen Geschichte

In einem Eingabefeld in Streamlit lässt sich der Plot der Geschichte in Stichworten oder einem kurzen Satz eingeben wie z.B. "Emilia reist mit einem Einhorn nach Italien".
Daraufhin werden die Charaktere in der Geschichte nach Bekanntheit analysiert. In diesem Fall ist Emilia unbekannt und es müssen weitere Informationen bezüglich des Aussehens bereitgestellt werden. Glücklicherweise werden die unbekannten Charaktere automatisch detektiert und die fehlenden Informationen können dann entweder durch Texteingabe oder aus einem Bild extrahiert werden, welches hochgeladen werden kann.
Im Anschluss wird die Geschichte mit einem LLM generiert. Hierzu wird die Geschichte in 10 Teil-Abschnitte untergliedert und als JSON gespeichert.
Direkt daran schließt sich die Bildgenerierung an, bei der zu jedem Kapitel ein passendes Bild erstellt wird. 
Des Weiteren kann bei der Erstellung eingestellt werden, welche "Stimme" die Geschichten "vorlesen" soll (auch neue Stimmen können geklont werden).
Elevenlabs generiert nun aus den einzelnen Kapiteln die zugehörige Audiospur.
Sowohl die Geschichte, als auch die Bilder und die Tonspuren werden gespeichert. Die größeren Files wie Bilder und Audio-files werden dabei in einem S3-Bucket auf AWS gespeichert, die Geschichte und die Verlinkungen auf die Bilder etc. dagegen in einer Datenbank (ehemals PostgreSQL auf AWS, dann aber aufgrund des Preises in einer DuckDB)
Somit lassen sich einmal generierte Geschichten auch nachträglich schnell immer wieder angucken.

---

## Tools / Flowchart

![NarrAItive_Flowchart](/images/content/NarrAItive_tools.webp)
Die folgenden Tools / Modelle werden genutzt:

- GPT4o (Storyplot)
- DallE-3 (images)
- Elevenlabs (voice cloning und text2speech)
- GPT-Vision (Extrahiere Informationen aus Bildern)
- Amazon S3 (Speichern der Bilder und Audio-Files)
- DuckDB (Speichern der Segmente, Stories, Charaktere, Pfade der Bilder und Audio-files)
- Streamlit (Frontend und zusammenführen aller Komponenten)

---

## Mögliche Weiterentwicklungen

- Charakterdatenbank um diese nicht immer erneut beschreiben zu müssen
- Vorabsuche nach bereits generierten Geschichten zu einem ähnlichen Thema
- Bewertungsfunktion der Geschichten 
- Öffnen für community
- Speichern der Stories auf AWS
- Print Funktion und Lieferung nach Hause
- Konsistenz der Bilderstellung nun möglich
- Erstellung einer echten App
- Preisvergleich der verschiedenen Tools (vor allem Bild und Vertonung)
