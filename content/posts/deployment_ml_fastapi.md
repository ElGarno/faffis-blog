+++
date = '2025-04-10T20:12:12+02:00'
draft = false
+++

# Deployment via Fast-API

## Einleitung

In der heutigen digitalen Welt ist die Bereitstellung von Anwendungen entscheidend für den Erfolg eines Projekts. FastAPI hat sich als leistungsstarkes Framework für die Entwicklung von APIs etabliert. In diesem Artikel werden wir die Vorteile und Schritte zur Bereitstellung einer Anwendung mit FastAPI im Rahmen des Loyalty-Projekts der Krombacher Brauerei erläutern.

## Funktionsfähiger Case

Eine funktionsfähige Version des Frameworks ist im Loyalty-Projekt zu finden. Der Code ist [hier](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/tree/master/src/Fraud_Detection) verfügbar.

## Vorteile von FastAPI

Die Verwendung von FastAPI bietet zahlreiche Vorteile:

- **Höchste Flexibilität**: FastAPI ermöglicht eine einfache Anpassung und Erweiterung der API.
- **Bessere Performance**: Im Vergleich zu Lambda-Funktionen entfällt der Cold-Start, was die Reaktionszeiten verbessert.
- **Swagger-Dokumentation**: FastAPI generiert automatisch eine Swagger-Dokumentation für die Endpunkte, die verschiedene Stufen wie /health, /predict1, /predict2 usw. umfasst.
- **Geringere Kosten**: Es wird kein Sagemaker-Endpoint benötigt, was die Kosten senkt.
- **Besseres Monitoring**: Alle Endpunkte können innerhalb eines ECS-Clusters überwacht werden.
- **Sicherheitslevel**: HTTPS und x-api-key bieten ein vergleichbares Sicherheitsniveau.
- **Eigene Domäne**: Die Anwendung kann in einer spezifischen "informationshaltigen" Domäne betrieben werden.

## Schritte zum Deployment

Hier sind die Schritte, die für das Deployment einer FastAPI-Anwendung erforderlich sind:

1. **FastAPI-Skript anpassen**: Passen Sie das [FastAPI-Skript](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/fastapi_app.py) an Ihre Bedürfnisse an.
   
2. **serverless.yml anpassen**: Ändern Sie die Punkte in der [serverless.yml](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/serverless.yml), die mit "edit manually" kommentiert sind.

3. **Weitere Elemente erstellen**: 
   - **securityGroupIds**: 
     - Inbound-Traffic: Ports 80 (HTTP), 443 (HTTPS), 8000 (Load Balancer) zulassen.
     - Outbound-Rules: Alle IPv4-Traffic zulassen.
   - **TaskRoleArn**: Passen Sie die Policy in dieser Rolle an, um die Berechtigungen innerhalb der FastAPI-App zu steuern.
   - **ExecutionRoleArn**: Diese Rolle vergibt Rechte zum Zugriff auf ECR, ECS usw. zur Erstellung der Infrastruktur.
   - **Ports anpassen**: Stellen Sie sicher, dass die Container-Ports entsprechend dem Docker-Container angepasst werden.

4. **Dockerfile anpassen**: Passen Sie das [Dockerfile](https://gitlab.com/krombacher-brauerei/datascience_krombacher/loyalty/-/blob/master/src/Fraud_Detection/Dockerfile) an.

5. **App Container bauen**: Führen Sie die Schritte zum Bauen, Taggen, Anmelden und Pushen des Containers durch.

6. **Container-ARN eintragen**: Tragen Sie die Container-ARN in der serverless.yml unter "resources->Resources->ECSTaskDefinition->Properties->ContainerDefinitions→Image" ein.

7. **Deployment durchführen**: Führen Sie den Befehl `sls deploy` aus.

8. **Endpunkt verfügbar machen**: Der Endpunkt ist nun unter der DNS des Load-Balancers verfügbar und kann auf die "unsere" kbpim-Domain gemappt werden.

9. **Route 53 konfigurieren**:
   - Gehen Sie zu Hosted Zones → datascience.dev.kbpim.
   - Erstellen Sie einen Record.
   - Wählen Sie den Record-Typ A und geben Sie den Namen des Projekts (spätere Subdomain) an, Alias aktivieren.
   - Leiten Sie den Traffic zum Application Load Balancer (ALB) weiter.
   - Wählen Sie einfaches Routing.

## Architektur

Die Architektur der Anwendung sollte so gestaltet sein, dass sie die oben genannten Vorteile und Schritte unterstützt. Eine gut durchdachte Architektur ermöglicht eine effiziente Nutzung der Ressourcen und eine reibungslose Interaktion zwischen den verschiedenen Komponenten der Anwendung.

## Fazit

Die Bereitstellung einer Anwendung mit FastAPI bietet viele Vorteile, darunter Flexibilität, Performance und Kostene