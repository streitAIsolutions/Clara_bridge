# TODO - Clara Bridge (KI-Beschaffungsassistent)

---

## Aktuelle Prioritaeten

1. **Offene Punkte mit E&W klaeren (O1-O6)** - Siehe PROJECT_BRAIN.md
2. **GitHub Repo anlegen** - streitAIsolutions/Clara_bridge
3. **Phase 1 starten** - Gmail API Integration + Uebersetzungs-Relay

---

## Phase 1: E-Mail Relay + Uebersetzung (ALS NAECHSTES)

| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.1 | GitHub Repo anlegen + Grundstruktur | Offen | Hoch |
| P1.2 | Railway Service aufsetzen (eigener Container) | Offen | Hoch |
| P1.3 | PostgreSQL DB aufsetzen (eigene DB) | Offen | Hoch |
| P1.4 | Gmail API Integration (Inbound: Polling oder Pub/Sub) | Offen | Hoch |
| P1.5 | Gmail API Integration (Outbound: E-Mails senden) | Offen | Hoch |
| P1.6 | E-Mail-Erkennung: Neue Anfrage vs. Antwort (Thread-ID) | Offen | Hoch |
| P1.7 | Uebersetzungs-Engine DE zu PL (Claude Sonnet + Fachterminologie) | Offen | Hoch |
| P1.8 | Uebersetzungs-Engine PL zu DE (Claude Sonnet + Fachterminologie) | Offen | Hoch |
| P1.9 | Human-in-the-Loop: Draft an E&W zur Freigabe | Offen | Hoch |
| P1.10 | Projekt-Anlage bei neuer Anfrage (automatisch oder manuell) | Offen | Mittel |
| P1.11 | Telegram-Notification bei neuen Nachrichten | Offen | Mittel |
| P1.12 | Basis-Status-Tracking pro Projekt | Offen | Mittel |
| P1.13 | Attachment-Handling (Weiterleitung von PDFs etc.) | Offen | Hoch |
| P1.14 | End-to-End Test mit echtem E-Mail-Flow | Offen | Hoch |

---

## Phase 2: PDF-Parsing + Anforderungs-Extraktion (nach Phase 1)

| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P2.1 | Fensterlisten-Parser (maxmartin-Format als Startpunkt) | Offen | Hoch |
| P2.2 | Tabellen-Extraktion (pdfplumber) | Offen | Hoch |
| P2.3 | Zeichnungen-Extraktion (Bilder aus PDF) | Offen | Mittel |
| P2.4 | Strukturierte Anforderungen in DB speichern | Offen | Hoch |
| P2.5 | Review-Dokument fuer E&W generieren | Offen | Mittel |
| P2.6 | Claude Vision Fallback fuer unstrukturierte PDFs | Offen | Mittel |
| P2.7 | E&W-Template Integration (wenn Template vorhanden, O1) | Offen | Mittel |

---

## Phase 3: Angebotsvalidierung (nach Phase 2)

| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P3.1 | Lieferanten-Angebot PDF parsen (ekookna-Format) | Offen | Hoch |
| P3.2 | Position-fuer-Position Abgleich gegen Anforderungen | Offen | Hoch |
| P3.3 | Confidence-Score pro Pruefpunkt | Offen | Hoch |
| P3.4 | Pruefbericht generieren fuer E&W | Offen | Hoch |
| P3.5 | Abweichungen-Report mit konkreten Werten | Offen | Hoch |

---

## Phase 4: Kalkulation + E&W-Angebot (nach Phase 3)

| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P4.1 | Kalkulationsregeln-Dashboard (Stundensaetze, Aufschlaege) | Offen | Hoch |
| P4.2 | Standard-Template + Pro-Projekt-Anpassung | Offen | Hoch |
| P4.3 | Automatische Berechnung (Lieferantenpreis + Aufschlaege) | Offen | Hoch |
| P4.4 | E&W-Angebotsdokument generieren (PDF) | Offen | Hoch |

---

## Phase 5: Dashboard + Multi-Supplier (nach Phase 4)

| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P5.1 | Web-Dashboard: Projektliste, Status-Pipeline | Offen | Hoch |
| P5.2 | E-Mail-Verlauf pro Projekt einsehbar | Offen | Mittel |
| P5.3 | Multi-Supplier Support (nicht nur ekookna) | Offen | Mittel |
| P5.4 | Multi-Sprachen Support (nicht nur PL) | Offen | Niedrig |
| P5.5 | Archiv: Abgeschlossene Projekte durchsuchbar | Offen | Niedrig |

---

## Offene Bugs

Noch keine (Projekt in Konzeptphase).

---

## Technische Entscheidungen (offen)

| # | Entscheidung | Optionen | Status |
|---|-------------|----------|--------|
| T1 | Gmail Polling vs. Push (Pub/Sub) | Polling (einfach) vs. Push (sofort) | Offen, Empfehlung: Polling fuer MVP |
| T2 | Thread-Erkennung | Gmail Thread-ID vs. Subject-Parsing | Offen |
| T3 | ekookna Angebots-PDF Format | Brauchen Beispiel-PDF von E&W | Offen |
| T4 | Zeichnungen: Raster vs. Vektor | Abhaengig von Architekten-PDF | Offen |

---

## Erledigt

| # | Item | Datum |
|---|------|-------|
| Konzept | CLARA_BRIDGE_CONCEPT.md erstellt und freigegeben | 03.03.2026 |
| 5MD | Dokumentationsstruktur aufgesetzt | 03.03.2026 |
