---

##Testprotokoll – GUI (Rolle 4)

### 24.02.2026 – GUI Tests & Vollständigkeitsprüfung

Durchgeführte Tests:
- Start der Anwendung mit `python -m src.ui`
- Überprüfung aller Tabs (Artikel, Lagerbewegungen, Berichte)
- Test der Artikelanzeige in der Tabelle
- Test der Buttons (Hinzufügen, Aktualisieren, Löschen)
- Überprüfung der GUI-Struktur auf Vollständigkeit

Ergebnis:
- GUI startet fehlerfrei.
- Artikel werden korrekt angezeigt.
- Dialog zum Hinzufügen funktioniert.
- Aktualisieren lädt die aktuellen Daten vom Service.
- Lagerbewegungen werden aktuell noch nicht angezeigt.

Feststellung:
- Die Funktionalität für Lagerbewegungen ist im Backend noch nicht vollständig implementiert.
- Zuständige Teammitglieder wurden darüber informiert.

---

### 03.03.2026 – Systemtest mit Startbefehl

Durchgeführter Test:
- Start der Anwendung über Terminal mit:
  `python -m src.ui`

Ergebnis:
- GUI startet korrekt.
- Es wurde festgestellt, dass aktuell noch keine Datenbank angebunden ist.
- Es werden derzeit nur Testdaten verwendet.

Feststellung:
- Die Datenbank-Implementierung ist noch nicht vorhanden.
- Zuständig für die Datenbank ist Mert (Backend-Verantwortlicher).
- Die GUI ist vorbereitet, um mit einer zukünftigen Datenbankanbindung zu funktionieren.

---