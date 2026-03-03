# Changelog - Dominik Stojanovic

Persönliches Changelog für Dominik Stojanovic, Rolle: GUI & Interaktion

---

## [v0.1] - 2026-02-10

### Implementiert

- Projektmanagement-Dokumentation für das Lagerverwaltungssystem erstellt
- GUI-Skizze für das Thema „Autozubehör-Lagerverwaltung“ entworfen
- Repository beigetreten und Entwicklungsumgebung in Visual Studio Code eingerichtet
- Erste Analyse der bestehenden GUI in `src/ui/__init__.py`

### Tests geschrieben

- Manuelle Überprüfung der GUI-Skizze und Projektstruktur

### Commits

Feat: Add PM documentation  
Docs: Add GUI sketch for auto accessories warehouse  
Setup: Join repository and setup VS Code environment  

### Mergekonflikt(e)

- Keine

---

## [v0.2] - 2026-02-12

### Implementiert

- Bestehende GUI analysiert und refaktorisiert
- GUI von einer einzelnen Datei (`__init__.py`) in mehrere Module aufgeteilt:
  - `main_window.py`
  - `dialogs.py`
  - `__main__.py`
- GUI an Projekt-Thema „Autozubehör“ angepasst
- Artikel-Dialog mit PyQt6 umgesetzt
- Artikellisten-Ansicht mit Tabelle implementiert
- Service-Injection eingeführt (UI greift nicht direkt auf Repository zu)

### Tests geschrieben

- Manuelle Tests:
  - GUI startet fehlerfrei
  - Artikel-Dialog öffnet korrekt
  - Artikelliste wird geladen und angezeigt

### Commits

Refactor: Split GUI into multiple modules  
Feat: Add ArticleDialogWindow for auto accessories  
Feat: Implement main window layout with PyQt6  
Docs: Update GUI according to auto accessories topic  

### Mergekonflikt(e)

- Keine

---

## [v0.3] - 2026-02-17

### Implementiert

- Persönliches Changelog erstellt und Template entfernt
- Für jedes Gruppenmitglied separate Changelog-Datei angelegt
- Projekt-PDF im Repository bereitgestellt
- Testdaten (data.json) in Zusammenarbeit mit Team integriert
- Aktualisieren-, Löschen- und Hinzufügen-Buttons in der GUI implementiert
- Nach Rollenklärung Backend-Logik wieder aus der GUI entfernt (Trennung Frontend/Backend konsequent umgesetzt)

### Tests geschrieben

- Funktionstest der Buttons (Aktualisieren, Löschen, Hinzufügen)
- Überprüfung der Service-Anbindung
- Kontrolle der Architekturtrennung (GUI greift nicht direkt auf Daten zu)

### Commits

Feat: Implement refresh and delete functionality  
Refactor: Remove backend logic from GUI  
Docs: Add personal changelog files  

### Mergekonflikt(e)

- Keine

---

## [v0.4] - 2026-02-24

### Implementiert

- Vollständigkeitstest der GUI durchgeführt
- Überprüfung aller Tabs (Artikel, Lagerbewegungen, Berichte)
- Rückmeldung an zuständige Teammitglieder bezüglich fehlender Lagerbewegungs-Funktionalität

### Tests geschrieben

- Systemtest der GUI
- Überprüfung der Anzeige-Logik
- Navigationstest zwischen Tabs

### Mergekonflikt(e)

- Keine

---

## [v0.5] - 2026-03-03

### Implementiert

- Systemstart über `python -m src.ui` getestet
- Analyse der aktuellen Datenstruktur durchgeführt
- Festgestellt, dass noch keine Datenbank angebunden ist
- Backend-Verantwortlichen über fehlende Datenbankanbindung informiert

### Tests geschrieben

- Starttest über Terminal
- Überprüfung der GUI ohne persistente Datenbank

### Mergekonflikt(e)

- Keine

---

## Zusammenfassung

**Gesamt implementierte Features:**
- GUI-Konzeption und vollständige Umsetzung
- Refaktorierung in modulare Struktur
- Anbindung an WarehouseService
- Testdaten-Integration
- Architekturtrennung Frontend/Backend umgesetzt

**Gesamt geschriebene Tests:**
- Mehrere manuelle GUI-Tests
- Vollständigkeitsprüfung
- Systemstart-Test

**Gesamt Commits:**
- Mehrere Feature-, Refactor- und Dokumentations-Commits

**Größte Herausforderung:**
Klare Trennung zwischen Frontend (GUI) und Backend-Logik sowie Refaktorierung der bestehenden GUI-Struktur.

**Schönste Code-Zeile:**
Service-Injection in das MainWindow zur sauberen Architekturtrennung.

---

**Changelog erstellt von:** Dominik Stojanovic  
**Letzte Aktualisierung:** 2026-03-03