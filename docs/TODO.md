# TODO - Clara Bridge (KI-Beschaffungsassistent)

---

## Aktuelle Prioritaeten

1. **Uebersetzungsqualitaet bewerten** — echte Kom. Kern Mails pruefen, Terminologie-Luecken finden
2. **"Bearbeiten"-Flow** — Dritter Button neben Freigeben/Ablehnen, Implementierung klären
3. **Attachment-Handling E2E testen** — PDFs durchreichen verifizieren

---

## Phase 1: E-Mail Relay + Uebersetzung (LIVE)

### 1A: Setup & Infrastruktur
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.1 | GitHub Repo anlegen + Grundstruktur (27 Dateien) | **ERLEDIGT** | Hoch |
| P1.2 | Railway Service aufsetzen (eigener Container) | **ERLEDIGT** | Hoch |
| P1.3 | PostgreSQL DB aufsetzen (eigene DB) + Basis-Tabellen | **ERLEDIGT** | Hoch |

### 1B: Gmail Integration
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.4 | Gmail OAuth Credentials prüfen/einrichten | **ERLEDIGT** | Hoch |
| P1.5 | Gmail Inbound: Polling alle 5 Min (neue Mails erkennen) | **LIVE** | Hoch |
| P1.6 | Gmail Outbound: Draft erstellen + senden nach Freigabe | **LIVE** | Hoch |
| P1.7 | Thread-Erkennung: Gmail Thread-ID + Subject-Parsing Fallback | **LIVE** | Hoch |
| P1.8 | Attachment-Handling: Durchreichen (PDFs etc.) | **Im Code** | Hoch |

### 1C: Uebersetzung
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.9 | Uebersetzungs-Engine DE→PL (Claude Sonnet + TERMINOLOGY.md) | **LIVE** | Hoch |
| P1.10 | Uebersetzungs-Engine PL→DE (Claude Sonnet + TERMINOLOGY.md) | **LIVE** | Hoch |
| P1.11 | Spracherkennung (DE vs PL) | **LIVE** | Mittel |
| P1.12 | Low-Confidence Markierung bei unbekannten Begriffen | **LIVE** | Mittel |

### 1D: Telegram Human-in-the-Loop
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.13 | Telegram: Notification bei neuer Inbound-Mail | **LIVE** | Hoch |
| P1.14 | Telegram: Uebersetzungs-Preview + Inline Keyboard (Freigeben/Ablehnen) | **LIVE** | Hoch |
| P1.15 | Telegram: Callback-Handling — /telegram/webhook Endpoint | **LIVE** | Hoch |
| P1.16 | Telegram: Manuelle Projekt-Zuordnung (Fallback) | **Im Code** | Mittel |

### 1E: Projekt-Management
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.17 | Projekt-Anlage bei neuer Anfrage (automatisch + manuell) | **LIVE** | Mittel |
| P1.18 | Basis-Status-Tracking pro Projekt | **LIVE** | Mittel |
| P1.19 | E-Mail-Status-Tracking (RECEIVED→DRAFT→APPROVED→SENT) | **LIVE** | Hoch |

### 1F: Testing
| # | Aufgabe | Status | Prio |
|---|---------|--------|------|
| P1.20 | End-to-End Test: Inbound Mail → Uebersetzung → Draft → Freigabe → Send | **ERLEDIGT** (4 Durchlaeufe, Happy Path bestanden) | Hoch |
| P1.21 | Uebersetzungsqualitaet testen mit Kom. Kern Korrespondenz | **Offen** | Hoch |

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

| # | Bug | Status | Entdeckt |
|---|-----|--------|----------|
| B1 | ~~Webhook Secret Token fehlt~~ | **ERLEDIGT** | 06.03.2026 |
| B2 | "Bearbeiten"-Button fehlt in Telegram Preview (nur Freigeben/Ablehnen) | Offen | 06.03.2026 |

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
| T7 | callback_data Format | Kurze Keys (a/e/p), draft_id aus DB | **Entschieden: 64-byte Limit** |

---

## Erledigt

| # | Item | Datum |
|---|------|-------|
| P1.2 | Railway Service aufgesetzt + deployed | 06.03.2026 |
| P1.3 | PostgreSQL DB live auf Railway | 06.03.2026 |
| P1.15 | Telegram Webhook Endpoint implementiert | 06.03.2026 |
| P1.20 | E2E-Test bestanden (4 Durchlaeufe) | 06.03.2026 |
| Konzept | CLARA_BRIDGE_CONCEPT.md erstellt und freigegeben | 03.03.2026 |
| 5MD | Dokumentationsstruktur aufgesetzt | 03.03.2026 |
| Flow | Phase 1 Flow-Diagramm (4 Flows, interaktiv) | 03.03.2026 |
| O4 | E-Mail-Routing geklaert: Phase 1 ueber E&W | 03.03.2026 |
| T1 | Gmail Polling 5 Min beschlossen | 03.03.2026 |
| T2 | Thread-Erkennung 3-stufig beschlossen | 03.03.2026 |
| T5 | Draft-Freigabe via Telegram beschlossen | 03.03.2026 |
| T6 | E-Mail-Routing Phase 1 beschlossen | 03.03.2026 |
