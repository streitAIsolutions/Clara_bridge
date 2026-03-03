# ARCHITECTURE.md - Clara Bridge System-Architektur

**Zweck:** Technische Referenz fuer Clara Bridge. Beschreibt das System als Ganzes, Datenmodell, Entscheidungen und Constraints. Ergaenzt die 3MD (PROJECT_BRAIN.md = Status, SESSION_LOG.md = Chronik, TODO.md = Aufgaben).

**Letztes Update:** 3. Maerz 2026 (v1 - Konzeptphase)

---

## 1. System-Ueberblick

Clara Bridge automatisiert den Angebotsworkflow zwischen Architekturbuero, Handwerksbetrieb (E&W) und Lieferant (ekookna.pl).

```
Architekturbuero          E&W (Human-in-the-Loop)          Lieferant (PL)
      |                          |                               |
      |--- Anfrage (DE) ------->|                               |
      |                          |--- Forward an Bridge -------->|
      |                          |                               |
      |                   [Bridge: Extrahieren,                  |
      |                    Uebersetzen, Validieren,              |
      |                    Kalkulieren]                          |
      |                          |                               |
      |                          |<-- Review (DE) --------------|
      |                          |--- Approval ----------------->|
      |                          |------------- Anfrage (PL) -->|
      |                          |<------------ Angebot (PL) ---|
      |                          |<-- Uebersetzung (DE) --------|
      |                          |    + Pruefbericht            |
      |                          |                               |
      |<-- E&W-Angebot (DE) ----|                               |
```

---

## 2. Tech Stack

| Komponente | Technologie | Begruendung |
|------------|-------------|-------------|
| Backend | FastAPI (Python) | Gleich wie Clara Voice, Kompetenz vorhanden |
| Hosting | Railway (eigener Service, EU) | Shared Plattform, eigener Container |
| Datenbank | PostgreSQL (eigene DB) | Keine Datenvermischung mit Voice |
| KI | Anthropic Claude Sonnet | Qualitaet fuer Fachterminologie, Latenz irrelevant |
| E-Mail | Gmail API | E&W nutzt Google Suite, Test-Account vorhanden |
| PDF-Parsing | pdfplumber + Claude Vision | Strukturiert + Fallback fuer Bilder |
| Dokument-Erstellung | docx-js / reportlab | Angebote + Reports |
| Benachrichtigung | Telegram Bot | Shared mit Clara Voice |
| Version Control | GitHub (streitAIsolutions/Clara_bridge) | Eigenes Repo |

---

## 3. Projekt-Struktur (geplant)

```
Clara_bridge/
|
+-- app.py                      # FastAPI Server, Routen
+-- requirements.txt            # Python-Pakete
+-- Dockerfile                  # Railway Deployment
|
+-- backend/
|   +-- __init__.py
|   +-- email_service.py        # Gmail API (Inbound + Outbound)
|   +-- translation_service.py  # Claude Uebersetzung DE/PL + Fachterminologie
|   +-- document_service.py     # PDF-Parsing, Anforderungs-Extraktion
|   +-- validation_service.py   # Angebot vs. Anforderungen Abgleich
|   +-- calculation_service.py  # E&W-Aufschlaege, Angebotserstellung
|   +-- project_service.py      # Projekt-CRUD, Status-Management
|   +-- models.py               # SQLAlchemy ORM
|   +-- database.py             # DB Engine, Pool, Migrations
|   +-- telegram_service.py     # Notifications
|   +-- terminology.py          # Fachterminologie-Loader
|
+-- frontend/
|   +-- index.html              # Dashboard (Phase 5)
|
+-- data/
|   +-- terminology_de_pl.json  # Fachterminologie-DB
|
+-- docs/
|   +-- PROJECT_BRAIN.md
|   +-- SESSION_LOG.md
|   +-- TODO.md
|   +-- ARCHITECTURE.md
|   +-- TERMINOLOGY.md
|   +-- CLARA_BRIDGE_CONCEPT.md
|
+-- tests/
    +-- test_translation.py     # Uebersetzungs-Tests
    +-- test_validation.py      # Validierungs-Tests
```

---

## 4. Datenmodell

### 4.1 Kern-Tabellen

**projects** - Ein Projekt pro Angebotsanfrage
- id, name (z.B. "Kom. Kern - Bellerstr. 31")
- architect_name, architect_email
- supplier_id (FK suppliers)
- status (RECEIVED, SENT_TO_SUPPLIER, IN_REVISION, OFFER_RECEIVED, OFFER_VALIDATED, EW_OFFER_DRAFTED, EW_OFFER_SENT, COMPLETED)
- property_address (Baustellenadresse)
- created_at, updated_at

**suppliers** - Lieferanten (Multi-Supplier ready)
- id, name, contact_name, email, language, notes

**requirements** - Extrahierte Anforderungen aus Architekten-PDF
- id, project_id (FK projects)
- position (F-001, F-002, ...)
- room, qty, width, height, opening_direction
- brh, wall_thickness
- u_value, security_class, glazing_type
- frame_color_inside, frame_color_outside
- window_sill_depth, roller_shutter_type
- special_notes
- drawing_image_path

**supplier_offers** - Angebote vom Lieferanten
- id, project_id, version (Korrekturschleife 1, 2, 3...)
- position (FK requirements.position)
- offered_u_value, offered_security_class, offered_glazing
- unit_price, total_price
- raw_pdf_path

**validations** - Abgleich Anforderung vs. Angebot
- id, project_id, offer_version
- position, field_name
- required_value, offered_value
- status (OK, DEVIATION, UNCHECKED)
- confidence_score (0.0 - 1.0)

**ew_calculations** - E&W-Aufschlag pro Position
- id, project_id, position
- supplier_price, markup_percent, markup_fixed
- labor_hours, labor_rate
- total_ew_price

**emails** - Kompletter Kommunikationsverlauf
- id, project_id
- direction (INBOUND, OUTBOUND)
- from_addr, to_addr, subject
- body_original, body_translated
- original_language, translated_language
- attachments (JSON array)
- gmail_thread_id, gmail_message_id
- status (RECEIVED, DRAFT, APPROVED_BY_EW, SENT)
- sent_at

**calculation_templates** - Wiederverwendbare Kalkulationsregeln
- id, name, is_default
- default_markup_percent
- default_labor_rate_per_hour
- labor_hours_per_window_type (JSON)
- travel_cost_flat

### 4.2 Beziehungen

```
suppliers (1) --> projects (N) --> requirements (N)
                              --> supplier_offers (N)
                              --> validations (N)
                              --> ew_calculations (N)
                              --> emails (N)
calculation_templates (1) --> projects (N)
```

---

## 5. Phasen-Details

### Phase 1: E-Mail Relay + Uebersetzung
- Gmail API: Polling (5 Min Intervall) oder Pub/Sub
- Thread-Management via Gmail Thread-ID
- Uebersetzung: Claude Sonnet mit Fachterminologie-Kontext
- Human-in-the-Loop: Jede ausgehende Mail als Draft, E&W gibt frei
- Attachments: Durchreichen ohne Verarbeitung (Phase 2)
- Geschaetzter Aufwand: 3-5 Arbeitstage

### Phase 2: PDF-Parsing + Anforderungs-Extraktion
- pdfplumber fuer Tabellen (Fensterliste)
- Bild-Extraktion fuer Zeichnungen (pdfimages / pypdf)
- Claude Vision als Fallback fuer unstrukturierte PDFs
- Anforderungen strukturiert in DB speichern
- Geschaetzter Aufwand: 3-4 Arbeitstage

### Phase 3: Angebotsvalidierung
- Lieferanten-PDF parsen (Format-spezifisch, ekookna zuerst)
- Automatischer Abgleich Position fuer Position
- Confidence-Score (hoch wenn exakter Match, niedrig wenn Feld fehlt)
- Pruefbericht als Dokument fuer E&W
- Geschaetzter Aufwand: 4-6 Arbeitstage

### Phase 4: Kalkulation + E&W-Angebot
- Dashboard fuer Kalkulationsregeln
- Standard-Template + Pro-Projekt Override
- PDF-Generierung im E&W-Design
- Geschaetzter Aufwand: 4-6 Arbeitstage

### Phase 5: Dashboard + Multi-Supplier
- Web-UI: Projektliste, Status-Pipeline, E-Mail-Verlauf
- Multi-Supplier + Multi-Language
- Geschaetzter Aufwand: 5-8 Arbeitstage

---

## 6. Shared Infrastructure mit Clara Voice

| Komponente | Shared? | Details |
|------------|---------|---------|
| Railway Account | Ja | Eigener Service unter gleichem Account |
| Anthropic API Key | Ja | Gleicher Key, getrennte Nutzung |
| Telegram Bot | Ja | Gleicher Bot, Bridge-spezifische Messages |
| PostgreSQL | Nein | Eigene DB-Instanz |
| GitHub | Nein | Eigenes Repo |
| Codebase | Nein | Komplett getrennt |

---

## 7. Bekannte Constraints

1. Gmail API Rate Limits: 250 Quota Units/User/Sekunde (kein Problem bei E&W-Volumen)
2. Gmail Attachment Limit: 25 MB pro E-Mail
3. Claude Vision: Max 20 MB pro Bild, max 5 Bilder pro Request
4. ekookna PDF-Format: Unbekannt, brauchen Beispiel
5. Architekten-PDF Formate: Variieren pro Buero, iterative Erweiterung noetig

---

## 8. Kosten-Abschaetzung (monatlich, nach Go-Live)

| Posten | Geschaetzt | Basis |
|--------|-----------|-------|
| Railway (Server) | 5-10 USD | Hobby Plan |
| Railway (PostgreSQL) | 5-10 USD | Eigene DB |
| Anthropic API (Sonnet) | 5-20 USD | 50-200 Uebersetzungen/Monat |
| Gmail API | 0 USD | Kostenlos |
| Telegram | 0 USD | Kostenlos |
| Gesamt | ca. 15-40 USD/Monat | |
