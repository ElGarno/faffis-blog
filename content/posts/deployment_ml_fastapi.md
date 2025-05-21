+++
date = '2025-04-10T20:12:12+02:00'
draft = false
title = 'Deployment via Fast-API'
cover.thumbnail = "/images/covers/generated/blog_deployment_ml_fastapi_thumb.webp"
cover.alt = "Verschiedene Services für das Deployment von ml-Modellen" #
cover.caption = "Deployment Services für ML-Modelle" 
cover.relative = false
cover.hidden = false
tags = ["Deployment", "FastAPI", "Python", "Web Development", "API"] 
+++

## Einleitung

In der heutigen digitalen Welt ist die Bereitstellung von Anwendungen entscheidend für den Erfolg eines Projekts. FastAPI hat sich als leistungsstarkes Framework für die Entwicklung von APIs etabliert. In diesem Artikel werden wir die Vorteile und Schritte zur Bereitstellung einer Anwendung mit FastAPI im Rahmen des Loyalty-Projekts der Krombacher Brauerei erläutern und zusätzlich die Eignung von FastAPI für das Deployment von Machine Learning (ML)-Modellen beleuchten.

## Funktionsfähiger Case

Eine funktionsfähige Version des Frameworks ist im Loyalty-Projekt zu finden.

## Vorteile von FastAPI

Die Verwendung von FastAPI bietet zahlreiche Vorteile:

- **Höchste Flexibilität**: FastAPI ermöglicht eine einfache Anpassung und Erweiterung der API.
- **Bessere Performance**: Im Vergleich zu Lambda-Funktionen entfällt der Cold-Start, was die Reaktionszeiten verbessert.
- **Swagger-Dokumentation**: FastAPI generiert automatisch eine Swagger-Dokumentation für die Endpunkte, die verschiedene Stufen wie /health, /predict1, /predict2 usw. umfasst.
- **Geringere Kosten**: Es wird kein Sagemaker-Endpoint benötigt, was die Kosten senkt.
- **Besseres Monitoring**: Alle Endpunkte können innerhalb eines ECS-Clusters überwacht werden.
- **Sicherheitslevel**: HTTPS und x-api-key bieten ein vergleichbares Sicherheitsniveau.
- **Eigene Domäne**: Die Anwendung kann in einer spezifischen "informationshaltigen" Domäne betrieben werden.

## Warum FastAPI für ML-Modelle?

FastAPI eignet sich besonders gut für das Deployment von Machine Learning-Modellen aus mehreren Gründen:

1. **Asynchrone Verarbeitung**: FastAPI unterstützt asynchrone Programmierung, was bedeutet, dass Anfragen parallel verarbeitet werden können. Dies ist besonders vorteilhaft für ML-Modelle, die oft rechenintensive Vorhersagen durchführen.

2. **Einfache Integration**: FastAPI lässt sich leicht mit gängigen ML-Bibliotheken wie TensorFlow, PyTorch und Scikit-Learn integrieren. Dies ermöglicht eine nahtlose Bereitstellung von Modellen als API-Endpunkte.

3. **Schnelle Entwicklung**: Die Verwendung von Python-Typen und die automatische Generierung von Dokumentationen beschleunigen den Entwicklungsprozess, was für Teams, die schnell auf Änderungen reagieren müssen, von Vorteil ist.

4. **Validierung und Serialisierung**: FastAPI bietet eingebaute Validierungs- und Serialisierungsfunktionen, die sicherstellen, dass die Eingabedaten für ML-Modelle korrekt sind, bevor sie verarbeitet werden.

## Voraussetzungen für das Deployment

Um FastAPI für das Deployment von ML-Modellen zu nutzen, sind einige Voraussetzungen erforderlich:

- **Python-Umgebung**: FastAPI benötigt Python 3.6 oder höher.
- **ML-Bibliotheken**: Installieren Sie die erforderlichen ML-Bibliotheken, die Sie für Ihr Modell benötigen (z.B. TensorFlow, PyTorch).
- **Docker**: Für die Containerisierung der Anwendung ist Docker erforderlich.
- **Cloud-Dienste**: Wenn Sie die Anwendung in der Cloud bereitstellen möchten, benötigen Sie Zugang zu Diensten wie AWS, Azure oder Google Cloud.

## Schwächen von FastAPI

Trotz der vielen Vorteile gibt es auch einige Schwächen, die bei der Verwendung von FastAPI berücksichtigt werden sollten:

1. **Lernkurve**: Für Entwickler, die neu in der asynchronen Programmierung sind, kann die Lernkurve steil sein. Es erfordert ein gewisses Verständnis von asynchronen Konzepten.

2. **Performance bei sehr hohen Lasten**: Während FastAPI für die meisten Anwendungen sehr performant ist, kann es bei extrem hohen Lasten (z.B. Tausende von gleichzeitigen Anfragen) zu Engpässen kommen, wenn die Infrastruktur nicht entsprechend skaliert ist.

3. **Weniger Community-Ressourcen**: Im Vergleich zu älteren Frameworks wie Flask oder Django gibt es möglicherweise weniger Community-Ressourcen und -Plugins, was die Lösung spezifischer Probleme erschweren kann.

## Schritte zum Deployment

Hier sind die Schritte, die für das Deployment einer FastAPI-Anwendung erforderlich sind:

1. **FastAPI-Skript anpassen**: Passen Sie das Fast-Api-Skript an Ihre Bedürfnisse an.
   
2. **serverless.yml anpassen**: Ändern Sie die Punkte in der [serverless.yml](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/serverless.yml), die mit "edit manually" kommentiert sind.

3. **Weitere Elemente erstellen**: 
   - **securityGroupIds**: 
     - Inbound-Traffic: Ports 80 (HTTP), 443 (HTTPS), 8000 (Load Balancer) zulassen.
     - Outbound-Rules: Alle IPv4-Traffic zulassen.
   - **TaskRoleArn**: Passen Sie die Policy in dieser Rolle an, um die Berechtigungen innerhalb der FastAPI-App zu steuern.
   - **ExecutionRoleArn**: Diese Rolle vergibt Rechte zum Zugriff auf ECR, ECS usw. zur Erstellung der Infrastruktur.
   - **Ports anpassen**: Stellen Sie sicher, dass die Container-Ports entsprechend dem Docker-Container angepasst werden.

4. **Dockerfile anpassen**: Passen Sie das [Dockerfile](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/Dockerfile) an, um sicherzustellen, dass alle Abhängigkeiten und das ML-Modell korrekt integriert sind.

5. **App Container bauen**: Führen Sie die Schritte zum Bauen, Taggen, Anmelden und Pushen des Containers durch. Dies kann mit Docker-Befehlen wie `docker build`, `docker tag`, `docker login` und `docker push` erfolgen.

6. **Container-ARN eintragen**: Tragen Sie die Container-ARN in der serverless.yml unter "resources->Resources->ECSTaskDefinition->Properties->ContainerDefinitions→Image" ein.

7. **Deployment durchführen**: Führen Sie den Befehl `sls deploy` aus, um die Anwendung in der Cloud bereitzustellen.

8. **Endpunkt verfügbar machen**: Der Endpunkt ist nun unter der DNS des Load-Balancers verfügbar und kann auf die "unsere" kbpim-Domain gemappt werden.

9. **Route 53 konfigurieren**:
   - Gehen Sie zu Hosted Zones
   - Erstellen Sie einen Record.
   - Wählen Sie den Record-Typ A und geben Sie den Namen des Projekts (spätere Subdomain) an, Alias aktivieren.
   - Leiten Sie den Traffic zum Application Load Balancer (ALB) weiter.
   - Wählen Sie einfaches Routing.

## Architektur

Die Architektur der Anwendung sollte so gestaltet sein, dass sie die oben genannten Vorteile und Schritte unterstützt. Eine gut durchdachte Architektur ermöglicht eine effiziente Nutzung der Ressourcen und eine reibungslose Interaktion zwischen den verschiedenen Komponenten der Anwendung. 

## Fazit

Die Bereitstellung einer Anwendung mit FastAPI bietet viele Vorteile, darunter Flexibilität, Performance und Kosteneffizienz. Insbesondere für Machine Learning-Modelle ist FastAPI eine ausgezeichnete Wahl, da es eine schnelle Entwicklung und einfache Integration ermöglicht. Trotz einiger Schwächen, wie der Lernkurve und der Performance bei extremen Lasten, bleibt FastAPI ein leistungsstarkes Werkzeug für moderne API-Entwicklung und das Deployment von ML-Modellen.