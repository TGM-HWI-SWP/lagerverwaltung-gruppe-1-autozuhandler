# Changelog - Dominik Stojanovic

Persönliches Changelog für Dominik Stojanovic, Rolle: GUI & Interaktion

---

## [v0.1] - 2026-02-10

### Implementiert

- Projektmanagement-Dokumentation für Lagerverwaltungssystem erstellt
- GUI-Skizze für Autozubehör-Lagerverwaltung entworfen
- Projekt-Repository beigetreten und Entwicklungsumgebung in Visual Studio Code eingerichtet
- Überblick über bestehende GUI in src/ui/__init__.py gemacht

### Tests geschrieben

- Noch keine automatischen Tests
- Manuelle Überprüfung der GUI-Skizze und Struktur

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
- GUI von einer Datei (__init__.py) in mehrere Dateien aufgeteilt:
  - main_window.py
  - dialogs.py
  - __main__.py
- GUI an Projekt-Thema „Autozubehör-Lagerverwaltung“ angepasst
- Artikel-Dialog für Autozubehör erstellt
- Artikelliste-GUI mit PyQt6 umgesetzt
- Service-Anbindung der GUI vorbereitet

### Tests geschrieben

- Manuelle Tests:
  - GUI startet ohne Fehler
  - Artikel-Dialog öffnet korrekt
  - Artikelliste aktualisiert sich

### Commits

Refactor: Split GUI into multiple modules

Feat: Add ArticleDialogWindow for auto accessories

Feat: Implement main window layout with PyQt6	

Docs: Update GUI according to auto accessories topic

### Mergekonflikt(e)

- Keine

---

## Zusammenfassung

**Gesamt implementierte Features:** GUI-Skizze, GUI-Refactoring, Autozubehör-Anpassung
**Gesamt geschriebene Tests:** Manuelle GUI-Tests
**Gesamt Commits:** Wird nach Projektende ergänzt
**Größte Herausforderung:** Struktur der bestehenden GUI verstehen und korrekt refaktorisieren
**Schönste Code-Zeile:** Aufteilung der GUI in separate Dateien für bessere Wartbarkeit

---

**Changelog erstellt von:** Dominik Stojanovic
**Letzte Aktualisierung:** 2026-02-17
