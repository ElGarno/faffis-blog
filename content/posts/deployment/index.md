+++
date = '2025-04-10T20:12:12+02:00'
draft = false
title = 'Deployment mit FastAPI'
cover.image = "blog_deployment_ml_fastapi.webp"
cover.alt = "Verschiedene Services für das Deployment von ML-Modellen"
cover.caption = "Deployment Services für ML-Modelle"
cover.relative = true
tags = ["Deployment", "FastAPI", "Python", "Webentwicklung", "API"]
+++

In der heutigen digitalen Welt ist das Deployment von Anwendungen entscheidend für den Projekterfolg. FastAPI hat sich als leistungsstarkes Framework für die Entwicklung von APIs etabliert. In diesem Artikel erläutern wir die Vorteile und Schritte für das Deployment einer Anwendung mit FastAPI im Kontext des Loyalty-Projekts der Krombacher Brauerei. Außerdem zeigen wir, warum sich FastAPI besonders gut für das Deployment von Machine-Learning-(ML)-Modellen eignet.

---

## Funktionaler Anwendungsfall

Eine funktionierende Version des Frameworks ist im Loyalty-Projekt verfügbar.

---

## Vorteile von FastAPI

Die Nutzung von FastAPI bietet zahlreiche Vorteile:

- **Maximale Flexibilität**: FastAPI ermöglicht eine einfache Anpassung und Erweiterung der API.
- **Bessere Performance**: Im Vergleich zu Lambda-Funktionen entfällt der Cold Start, was die Reaktionszeit verbessert.
- **Swagger-Dokumentation**: FastAPI generiert automatisch eine Swagger-Dokumentation für die Endpunkte (z. B. /health, /predict1, /predict2 usw.).
- **Geringere Kosten**: Es wird kein Sagemaker-Endpunkt benötigt, was die Kosten reduziert.
- **Besseres Monitoring**: Alle Endpunkte können im ECS-Cluster überwacht werden.
- **Sicherheitsniveau**: HTTPS und x-api-key bieten ein vergleichbares Sicherheitsniveau.
- **Eigene Domain**: Die Anwendung kann unter einer eigenen, informationsreichen Domain betrieben werden.

---

## Warum FastAPI für ML-Modelle?

FastAPI eignet sich besonders gut für das Deployment von Machine-Learning-Modellen aus mehreren Gründen:

1. **Asynchrone Verarbeitung**: FastAPI unterstützt asynchrones Programmieren, wodurch Anfragen parallel verarbeitet werden können – ideal für rechenintensive ML-Vorhersagen.

2. **Einfache Integration**: FastAPI lässt sich leicht mit gängigen ML-Bibliotheken wie TensorFlow, PyTorch oder Scikit-Learn verbinden. So können Modelle nahtlos als API-Endpunkte bereitgestellt werden.

3. **Schnelle Entwicklung**: Durch Python-Typisierung und automatische Dokumentation kann die Entwicklung beschleunigt werden – hilfreich für Teams mit schnellem Anpassungsbedarf.

4. **Validierung und Serialisierung**: FastAPI bietet eingebaute Validierungs- und Serialisierungsfunktionen, um sicherzustellen, dass Eingabedaten korrekt sind.

5. **Skalierbarkeit**: FastAPI-Anwendungen können mit Docker und Kubernetes einfach skaliert werden – wichtig bei schwankender Auslastung.

---

## Voraussetzungen für das Deployment

Folgende Voraussetzungen sollten für das Deployment erfüllt sein:

- **Python-Umgebung**: FastAPI benötigt Python 3.6 oder höher.
- **ML-Bibliotheken**: Installation der benötigten Bibliotheken wie TensorFlow oder PyTorch.
- **Docker**: Für die Containerisierung der Anwendung erforderlich.
- **Cloud-Dienste**: Zugang zu AWS, Azure oder Google Cloud, wenn eine Cloud-Deployment geplant ist.

---

## Schwächen von FastAPI

Neben den vielen Vorteilen gibt es auch einige Schwächen:

1. **Lernkurve**: Die Einführung in asynchrones Programmieren kann herausfordernd sein.

2. **Leistung unter hoher Last**: Unter sehr hoher Last (z. B. tausende gleichzeitige Anfragen) kann es ohne Skalierung zu Engpässen kommen.

3. **Weniger Community-Ressourcen**: Im Vergleich zu älteren Frameworks wie Flask oder Django gibt es weniger Plugins und Beiträge.

4. **Begrenzte integrierte Features**: FastAPI ist bewusst schlank gehalten und bietet keine eingebauten Lösungen für z. B. Authentifizierung oder Datenbankanbindung.

---

## Schritte für das Deployment

1. **FastAPI-Skript anpassen**: Die API auf deine Anforderungen zuschneiden.

2. **serverless.yml modifizieren**: Änderungen an den Stellen vornehmen, die mit "edit manually" kommentiert sind:  
   [serverless.yml](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/serverless.yml)

3. **Zusätzliche Elemente erstellen**:
    - **ECS-Cluster**: Für die Ausführung der App.
    - **securityGroupIds**:
        - Eingehender Traffic: Ports 80, 443, 8000.
        - Ausgehend: IPv4 erlauben.
    - **TaskRoleArn**: Berechtigungen für die Anwendung definieren.
    - **ExecutionRoleArn**: Rechte für Zugriff auf ECR, ECS etc.
    - **Ports anpassen**: Docker-Portfreigabe sicherstellen.

4. **Dockerfile anpassen**:  
   [Dockerfile](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/Dockerfile)

5. **App-Container bauen**:  
   Mit `docker build`, `docker tag`, `docker login` und `docker push`.

6. **Container-ARN eintragen**:  
   Im serverless.yml unter `resources -> Resources -> ECSTaskDefinition -> Properties -> ContainerDefinitions -> Image`.

7. **Deployment durchführen**:  
   Mit `sls deploy` die App in der Cloud bereitstellen.

8. **Endpoint verfügbar machen**:  
   Der Endpoint ist über den DNS des Load Balancers erreichbar und kann mit der kbpim-Domain verknüpft werden.

9. **Route 53 konfigurieren**:
    - In Hosted Zones gehen
    - A-Record erstellen
    - Subdomain angeben, Alias aktivieren
    - Auf den Application Load Balancer weiterleiten
    - Einfaches Routing auswählen

---

## Architektur

Die Architektur sollte auf Effizienz und gute Integration aller Komponenten ausgelegt sein. Eine durchdachte Architektur sorgt für optimale Ressourcennutzung und stabile Kommunikation.

---

## Fazit

Das Deployment mit FastAPI bringt viele Vorteile – von Flexibilität über Performance bis zur Kosteneffizienz. Gerade für ML-Modelle ist FastAPI ideal: schnelle Entwicklung, einfache Integration und solide Skalierbarkeit. Trotz kleinerer Schwächen ist FastAPI ein starkes Werkzeug für moderne APIs und ML-Anwendungen.
