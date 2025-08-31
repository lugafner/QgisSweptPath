# Benutzerhandbuch
*QgisSweptPath Version 0.1.0*

---

## Inhalt
- [Einleitung](#einleitung)
- [Kurzanleitung](#kurzanleitung)
  - [QgisSweptPath starten](#qgissweptpath-starten)
  - [Fahrzeug- und Pfadlayer erstellen](#fahrzeug--und-pfadlayer-erstellen)
  - [Fahrzeug auswählen](#fahrzeug-auswählen)
  - [Fahrzeug platzieren](#fahrzeug-platzieren)
  - [Simulation starten](#simulation-starten)
  - [Fahren](#fahren)
- [Einstellungen](#einstellungen)
  - [Layer](#layer)
  - [Plot Einstellungen](#plot-einstellungen)
  - [Layerdarstellung](#layerdarstellung)
  - [Benutzerfahrzeuge](#benutzerfahrzeuge)
  - [Karteneinstellungen](#karteneinstellungen)
  - [Frame basierte simulation](#frame-basierte-simulation)
  - [Schritt basierte simulation](#schritt-basierte-simulation)
  - [Pfadbearbeitung](#pfadbearbeitung)

---

## Einleitung
Mit dem Plug-in **QgisSweptPath** können direkt im QGIS grobe Abklärungen zur Befahrbarkeit von Strassen, Knoten oder Haltestellen 
des öffentlichen Verkehrs durchgeführt werden. Dank der Integration in QGIS können als Hintergrund alle möglichen verfügbaren Geodaten
verwendet werden, wie zum Beispiel Orthofotos, Daten der amtlichen Vermessung oder auch georeferenzierte PDF oder Bilder. Ausserdem kann
die Darstellung der Schleppkurven wie alle QGIS-Layer beliebig angepasst, und die Geometrien weiter bearbeitet werden.

Das Plug-in ist für schnelle Grobabklärungen konzipiert und erreicht wohl nie die Genauigkeit und Benutzerfreundlichkeit von CAD-basierten
Tools für Ingenieure. Ausserdem ist das Tool insbesondere für Anwender geeignet, die für ihre Projekte ohnehin mit QGIS arbeiten und
so kein zusätzliches Programm für die Schleppkurvensimulationen einsetzen müssen.

QgisSweptPath ist ein reines Freizeitprojekt und wird von einzelnen Privatpersonen betreut und weiterentwickelt. Aus diesem Grund
gibt es keinen Support für Anwender. Falls Sie aber Fehler entdecken, oder sich in der Weiterentwicklung einbringen möchten, können Sie ihr
Anliegen gerne im offiziellen [Github-Repository](https://github.com/lugafner/QgisSweptPath) als [Issue](https://github.com/lugafner/QgisSweptPath/issues) erfassen.

[![Static Badge](https://img.shields.io/badge/Github-QgisSweptPath-ad0000?style=for-the-badge&logoColor=%23ffffff&color=ad0000)](https://github.com/lugafner/QgisSweptPath)


## Kurzanleitung
### QgisSweptPath starten
aaa

### Fahrzeug- und Pfadlayer erstellen
aaa

### Fahrzeug auswählen
aaa

### Fahrzeug platzieren
aaa

### Simulation starten
aaa

### Fahren
aaa

## Einstellungen
### Layer
*Vehicle layer und Path layer*

aaa

### Plot Einstellungen
*Print path, Print interval und print distance*

aaa

### Layerdarstellung
*Default vehicle layer style und Default path layer style*

aaa

### Benutzerfahrzeuge
*User vehicle packages*

aaa

### Karteneinstellungen
*Minimum speed, Auto map movement, Min. border distance und Border distance units*

aaa

### Frame basierte simulation
*Frame based simulation,Frames, Acceleration/deceleration, Steering time, Key steer left, Key steer right, Key speed up und Key speed down*

aaa

### Schritt basierte simulation
*Step based simulation, Step distance, Speed change step und Steer change step*

aaa

### Pfadbearbeitung
*Dissolve path und Dissolve by fields*

Funktionen in Version 0.1.0 noch nicht verfügbar.

---

## Disclaimer
Bei der Entwicklung des Plug-ins wird darauf geachtet, dass die Schleppkurven möglichst den realen Fahrzeugen entsprechen
und die Simulationsergebnisse werden nach bestem Wissen und Gewissen geprüft. Dennoch kann nicht gewährleistet werden, dass
die Simulation in allen Fällen die Realität korrekt abbildet. Die Entwickler übernehmen keine Verantwortung für die Richtigkeit und
Genauigkeit der mit diesem Plug-in durchgeführten Schleppkurvenprüfungen. Für die Überprüfung und Plausibilisierung der Simulationsergebnisse
ist der Anwender selber verantwortlich.