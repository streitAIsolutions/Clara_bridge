# TODO - Clara Bridge (KI-Beschaffungsassistent)

---

## Aktuelle Prioritaeten

1. **GitHub Repo anlegen** - streitAIsolutions/Clara_bridge
2. **Gmail OAuth Credentials pruefen** - Google Cloud Console checken
3. **Phase 1 Implementierung starten** - Grundstruktur + Gmail + Uebersetzung

---

## Phase 1: E-Mail Relay + Uebersetzung (IN ARBEIT)

### 1A: Setup & Infrastruktur
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.1 | GitHub Repo anlegen + Grundstruktur (siehe ARCHITECTURE.md) | Offen | Hoch |
| P1.2 | Railway Service aufsetzen (eigener Container) | Offen | Hoch |
| P1.3 | PostgreSQL DB aufsetzen (eigene DB) + Basis-Tabellen | Offen | Hoch |

### 1B: Gmail Integration
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.4 | Gmail OAuth Credentials pruefen/einrichten | Offen | Hoch |
| P1.5 | Gmail Inbound: Polling alle 5 Min (neue Mails erkennen) | Offen | Hoch |
| P1.6 | Gmail Outbound: Draft erstellen + senden nach Freigabe | Offen | Hoch |
| P1.7 | Thread-Erkennung: Gmail Thread-ID + Subject-Parsing Fallback | Offen | Hoch |
| P1.8 | Attachment-Handling: Durchreichen (PDFs etc.) | Offen | Hoch |

### 1C: Uebersetzung
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.9 | Uebersetzungs-Engine DE→PL (Claude Sonnet + TERMINOLOGY.md) | Offen | Hoch |
| P1.10 | Uebersetzungs-Engine PL→DE (Claude Sonnet + TERMINOLOGY.md) | Offen | Hoch |
| P1.11 | Spracherkennung (DE vs PL) | Offen | Mittel |
| P1.12 | Low-Confidence Markierung bei unbekannten Begriffen | Offen | Mittel |

### 1D: Telegram Human-in-the-Loop
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.13 | Telegram: Notification bei neuer Inbound-Mail | Offen | Hoch |
| P1.14 | Telegram: Uebersetzungs-Preview + Inline Keyboard (Freigeben/Bearbeiten/Ablehnen) | Offen | Hoch |
| P1.15 | Telegram: Callback-Handling (Freigabe → Draft senden) | Offen | Hoch |
| P1.16 | Telegram: Manuelle Projekt-Zuordnung (Fallback) | Offen | Mittel |

### 1E: Projekt-Management
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.17 | Projekt-Anlage bei neuer Anfrage (automatisch + manuell) | Offen | Mittel |
| P1.18 | Basis-Status-Tracking pro Projekt | Offen | Mittel |
| P1.19 | E-Mail-Status-Tracking (RECEIVED→DRAFT→APPROVED→SENT) | Offen | Hoch |

### 1F: Testing
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.20 | End-to-End Test: Inbound Mail → Uebersetzung → Draft → Freigabe → Send | Offen | Hoch |
| P1.21 | Uebersetzungsqualitaet testen mit Kom. Kern Korrespondenz | Offen | Hoch |

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

## Technische Entscheidungen

| # | Entscheidung | Optionen | Status |
|---|-------------|----------|--------|
| T1 | Gmail Polling vs. Push (Pub/Sub) | Polling (einfach) vs. Push (sofort) | **Entschieden: Polling 5 Min fuer MVP** |
| T2 | Thread-Erkennung | Gmail Thread-ID + Subject-Parsing + manueller Fallback | **Entschieden: 3-stufig** |
| T3 | ekookna Angebots-PDF Format | Brauchen Beispiel-PDF von E&W | Offen (Phase 3) |
| T4 | Zeichnungen: Raster vs. Vektor | Abhaengig von Architekten-PDF | Offen (Phase 2) |
| T5 | Draft-Freigabe Mechanismus | Telegram Inline Keyboard | **Entschieden** |
| T6 | E-Mail-Routing Phase 1 | Alles ueber E&W, Direktmodus spaeter | **Entschieden** |

---

## Erledigt

| # | Item | Datum |
|---|------|-------|
| Konzept | CLARA_BRIDGE_CONCEPT.md erstellt und freigegeben | 03.03.2026 |
| 5MD | Dokumentationsstruktur aufgesetzt | 03.03.2026 |
| Flow | Phase 1 Flow-Diagramm (4 Flows, interaktiv) | 03.03.2026 |
| O4 | E-Mail-Routing geklaert: Phase 1 ueber E&W | 03.03.2026 |
| T1 | Gmail Polling 5 Min beschlossen | 03.03.2026 |
| T2 | Thread-Erkennung 3-stufig beschlossen | 03.03.2026 |
| T5 | Draft-Freigabe via Telegram beschlossen | 03.03.2026 |
| T6 | E-Mail-Routing Phase 1 beschlossen | 03.03.2026 |
