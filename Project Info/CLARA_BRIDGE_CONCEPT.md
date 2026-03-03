# Clara Bridge — Projekt-Konzept

**Codename:** Clara Bridge
**Pilot-Kunde:** Eulen & Weischer Montagetechnik GmbH (E&W)
**Lieferant (Pilot):** ekookna.pl (Ansprechpartnerin: Judyta Klima)
**Status:** Konzeptphase
**Erstellt:** 03.03.2026
**Autor:** Loris (Streit AI Solutions) + Claude (QG)

---

## 1. Vision

Clara Bridge ist ein KI-gestützter Beschaffungsassistent für Handwerksbetriebe. Er automatisiert den Angebotsworkflow zwischen Auftraggeber (Architekturbüro), Handwerksbetrieb und Lieferant — inklusive Übersetzung, Dokumenten-Umformatierung, Angebotsvalidierung und Kalkulation.

**Für E&W konkret:** Frank Bridge nimmt Angebotsanfragen von Architekturbüros entgegen, kommuniziert mit dem polnischen Fensterlieferanten (ekookna.pl), prüft die Angebote auf Korrektheit, und erstellt das E&W-Angebot für das Architekturbüro.

**Im Clara-Ökosystem:**

| Modul | Funktion | Status |
|-------|----------|--------|
| Clara Voice | KI-Telefonassistent | Live (Frank) |
| **Clara Bridge** | **KI-Beschaffungsassistent** | **Konzeptphase** |
| Clara [weitere] | Zukünftige Module | Geplant |

---

## 2. Der Workflow (End-to-End)

```
ARCHITEKTURBÜRO                    E&W                         LIEFERANT (PL)
      |                             |                               |
      |--- Anfrage + Fensterliste ->|                               |
      |                             |--- Forward an Frank ---------->|
      |                             |                               |
      |                     [Frank extrahiert Anforderungen,         |
      |                      erstellt E&W-Dokument,                  |
      |                      bereitet DE + PL Version vor]           |
      |                             |                               |
      |                             |<-- DE Review an E&W           |
      |                             |--- E&W gibt OK --------------->|
      |                             |------------ PL an Lieferant ->|
      |                             |                               |
      |                             |<----------- PL Antwort -------|
      |                     [Frank übersetzt PL→DE,                  |
      |                      prüft gegen Anforderungen]              |
      |                             |                               |
      |                             |<-- DE + Prüfbericht an E&W    |
      |                             |                               |
      |                      ... Korrekturschleifen ...              |
      |                             |                               |
      |                     [Angebot final — Frank kalkuliert        |
      |                      E&W-Aufschläge + Montagekosten]         |
      |                             |                               |
      |                             |<-- Fertiges E&W-Angebot       |
      |                             |--- E&W prüft + gibt OK ------>|
      |<-- E&W-Angebot -------------|                               |
```

### 2.1 Die drei Kernfunktionen

**F1: Übersetzungs-Relay (DE ↔ PL) mit Human-in-the-Loop**
- E&W leitet Anfrage per E-Mail an Frank weiter
- Frank erstellt deutsche Review-Version + polnische Version für Lieferant
- E&W gibt OK → Frank sendet polnische Version
- Lieferant antwortet auf Polnisch → Frank übersetzt ins Deutsche
- Jede E-Mail geht über E&W als Checkpoint (Human-in-the-Loop)
- Fensterbau-Fachterminologie DE↔PL korrekt übersetzen (FB30, VSG, RC2/RC3, Uw-Werte etc.)

**F2: Dokumenten-Umformatierung**
- Fensterliste vom Architekturbüro wird extrahiert (PDF-Parsing)
- Technische Daten + Zeichnungen werden in E&W-Template übertragen
- Strukturierte Anforderungsliste wird gespeichert (Basis für Angebotsvalidierung)

**F3: Angebotskalkulation + Validierung**
- Angebotsvalidierung: Automatischer Abgleich Lieferanten-Angebot ↔ Anforderungen
  - Position für Position: Maße, U-Wert, Sicherheitsklasse, Verglasung, Fensterbänke, Rollläden
  - Abweichungen markiert mit Confidence-Score
  - Report an E&W: "3 Abweichungen gefunden, 2 Positionen nicht prüfbar"
- Angebotskalkulation: Lieferantenpreis + E&W-Aufschläge = E&W-Angebot
  - Dashboard für Kalkulationsparameter (Stundensätze, Aufschläge pro Fenstertyp etc.)
  - Standard-Kalkulation als Template, pro-Projekt feinjustierbar
  - Fertiges Angebotsdokument im E&W-Design

---

## 3. Architektur

### 3.1 Systemübersicht

```
                    Gmail API (frank.eulen.weischer@gmail.com)
                              ↕
                    ┌─────────────────────┐
                    │   Clara Bridge      │
                    │   (FastAPI Server)  │
                    ├─────────────────────┤
                    │ Email Handler       │ ← Inbound/Outbound E-Mail
                    │ Translation Engine  │ ← Claude API (DE↔PL, Fachterminologie)
                    │ Document Processor  │ ← PDF Parsing, Template Generation
                    │ Requirement Tracker │ ← Anforderungen extrahieren + speichern
                    │ Offer Validator     │ ← Angebot ↔ Anforderungen abgleichen
                    │ Price Calculator    │ ← E&W-Aufschläge + Angebotsberechnung
                    │ Project Manager     │ ← Status-Tracking pro Projekt
                    └─────────────────────┘
                              ↕
                    ┌─────────────────────┐
                    │   PostgreSQL        │
                    │   (Projects, Reqs,  │
                    │    Offers, Config)  │
                    └─────────────────────┘
```

### 3.2 Alleinstehend vs. Shared Infrastructure

| Komponente | Shared mit Clara Voice? | Begründung |
|------------|------------------------|------------|
| Railway Hosting | Ja (eigener Service) | Gleiche Plattform, eigener Container |
| PostgreSQL | Eigene DB oder eigenes Schema | Keine Datenvermischung |
| Anthropic API Key | Ja | Gleicher Account, gleiche Kosten-Transparenz |
| GitHub | Eigenes Repo ODER Monorepo | Entscheidung unten |
| Telegram Bot | Ja (gleicher Bot, andere Notifications) | E&W nutzt bereits den Bot |
| Google Suite | Eigenes Gmail-Konto (frank.eulen.weischer@gmail.com) | Schon vorhanden |

**Repo-Entscheidung:** Eigenes Repo (`streitAIsolutions/Clara_bridge`).
Begründung: Komplett andere Domäne (asynchron, E-Mail, Dokumente vs. Echtzeit, Telefon, Audio). Monorepo würde Komplexität erhöhen ohne echten Nutzen. Shared Libraries (falls nötig) können als Packages extrahiert werden.

### 3.3 Datenmodell (Kern)

```
projects
├── id, name (z.B. "Kom. Kern - Bellerstr. 31")
├── architect_name, architect_email
├── supplier_id → suppliers
├── status (enum: RECEIVED, SENT_TO_SUPPLIER, IN_REVISION, OFFER_RECEIVED, 
│          OFFER_VALIDATED, EW_OFFER_DRAFTED, EW_OFFER_SENT, COMPLETED)
├── created_at, updated_at
│
├── requirements (extrahiert aus Architekten-Fensterliste)
│   ├── position (F-001, F-002, ...)
│   ├── room, qty, width, height, opening_direction
│   ├── brh, wall_thickness
│   ├── u_value, security_class (RC2/RC3)
│   ├── glazing_type, frame_color_inside, frame_color_outside
│   ├── window_sill_depth, roller_shutter (bool + type)
│   ├── special_notes
│   └── drawing_image_path (extrahierte Zeichnung)
│
├── supplier_offers (von Lieferant empfangen)
│   ├── version (1, 2, 3... pro Korrekturschleife)
│   ├── position → requirements.position
│   ├── offered_u_value, offered_security_class, ...
│   ├── unit_price, total_price
│   └── raw_pdf_path
│
├── validations (Abgleich Anforderung ↔ Angebot)
│   ├── position
│   ├── field, required_value, offered_value
│   ├── status (OK / DEVIATION / UNCHECKED)
│   └── confidence_score
│
├── ew_calculations (E&W-Aufschlag pro Position)
│   ├── position
│   ├── supplier_price, markup, labor_hours, labor_rate
│   └── total_ew_price
│
└── emails (Kommunikationsverlauf)
    ├── direction (INBOUND / OUTBOUND)
    ├── from_addr, to_addr, subject, body_de, body_pl
    ├── attachments (JSON array of file paths)
    ├── status (DRAFT, SENT, APPROVED_BY_EW)
    └── sent_at

suppliers
├── id, name (z.B. "ekookna.pl")
├── contact_name (z.B. "Judyta Klima")
├── email
├── language (z.B. "pl")
└── notes

calculation_templates
├── id, name (z.B. "Standard Neueinbau")
├── default_markup_percent
├── default_labor_rate_per_hour
├── default_labor_hours_per_window_type (JSON)
├── travel_cost_flat
└── is_default (bool)
```

---

## 4. Phasen-Plan

### Phase 1: E-Mail Relay + Übersetzung (MVP)
**Ziel:** E&W kann Anfragen an Frank weiterleiten, Frank übersetzt DE↔PL, E&W hat Human-in-the-Loop Kontrolle.

**Scope:**
- Gmail API Integration (Inbound + Outbound)
- E-Mail-Erkennung: Neue Anfrage vs. Antwort auf bestehenden Thread
- Übersetzung DE→PL und PL→DE via Claude (mit Fensterbau-Fachterminologie)
- Human-in-the-Loop: Jede ausgehende E-Mail geht erst als Draft an E&W zur Freigabe
- Projekt-Anlage (manuell: E&W forwarded = neues Projekt)
- Telegram-Notification bei neuen Nachrichten
- Basis-Status-Tracking (welches Projekt, welcher Stand)

**Nicht in Phase 1:**
- PDF-Parsing / Dokumenten-Umformatierung
- Angebotsvalidierung
- Kalkulation
- Dashboard

**Tech-Stack Phase 1:**
- FastAPI (Python), Railway
- Gmail API (Push Notifications via Google Pub/Sub oder Polling)
- Anthropic Claude API (Sonnet für Übersetzung — Qualität > Kosten)
- PostgreSQL
- Telegram Bot (Notifications)

**Geschätzter Aufwand:** 3-5 Arbeitstage

---

### Phase 2: PDF-Parsing + Anforderungs-Extraktion
**Ziel:** Frank extrahiert Fensterlisten aus Architekten-PDFs und speichert Anforderungen strukturiert.

**Scope:**
- PDF-Upload-Verarbeitung (Attachments aus E-Mails)
- Fensterlisten-Parser: Tabellen + Zeichnungen extrahieren
- Strukturierte Anforderungen in DB speichern
- Zeichnungen extrahieren und speichern (für spätere Dokument-Umformatierung)
- Review-Dokument für E&W generieren (zusammengefasste Anforderungen)

**Herausforderung:** Verschiedene Architekturbüros haben verschiedene PDF-Formate. Phase 2 startet mit maxmartin-Format, wird iterativ erweitert.

**Geschätzter Aufwand:** 3-4 Arbeitstage

---

### Phase 3: Angebotsvalidierung (Quality Gate)
**Ziel:** Frank prüft Lieferanten-Angebote automatisch gegen extrahierte Anforderungen.

**Scope:**
- Lieferanten-Angebot PDF parsen (ekookna-Format)
- Position-für-Position-Abgleich: Maße, U-Wert, Sicherheitsklasse, Verglasung, Fensterbänke
- Confidence-Score pro Prüfpunkt
- Prüfbericht generieren für E&W
- Abweichungen highlighten mit konkreten Angaben ("Gefordert: RC3, Angeboten: RC2")

**Herausforderung:** Lieferanten-PDFs sind oft unstrukturiert. Claude Vision könnte hier helfen (PDF als Bild → strukturierte Daten).

**Geschätzter Aufwand:** 4-6 Arbeitstage

---

### Phase 4: Kalkulation + E&W-Angebot
**Ziel:** Frank erstellt das fertige E&W-Angebot basierend auf Lieferantenpreisen + E&W-Aufschlägen.

**Scope:**
- Kalkulationsregeln-Dashboard (Stundensätze, Aufschläge, Materialkosten)
- Standard-Template + Pro-Projekt-Anpassung
- Automatische Berechnung: Lieferantenpreis + Aufschlag + Montage + Anfahrt
- E&W-Angebotsdokument generieren (E&W-Design, professionelles Layout)
- Export als PDF

**Voraussetzung:** E&W-Angebotstemplate und Kalkulationsregeln von E&W erhalten.

**Geschätzter Aufwand:** 4-6 Arbeitstage

---

### Phase 5: Dashboard + Multi-Supplier
**Ziel:** E&W hat Übersicht über alle Projekte, kann Status einsehen, Kalkulation anpassen.

**Scope:**
- Web-Dashboard: Projektliste, Status-Pipeline, E-Mail-Verlauf
- Kalkulationsregeln-Editor (global + pro Projekt)
- Mehrere Lieferanten unterstützen (nicht nur ekookna.pl)
- Mehrere Sprachen (nicht nur PL — z.B. CZ, SK, EN)
- Archiv: Abgeschlossene Projekte durchsuchbar

**Geschätzter Aufwand:** 5-8 Arbeitstage

---

## 5. Tech-Entscheidungen

### Warum Gmail API statt SendGrid/Mailgun?
- E&W arbeitet bereits mit Google Suite
- Test-Account (frank.eulen.weischer@gmail.com) existiert
- Bei Go-Live: Wechsel auf offizielle E&W-Adresse (DNS-Änderung, kein Code-Änderung)
- E-Mails sehen für alle Parteien wie normale E-Mails aus
- Attachments werden nativ gehandelt
- Kein zusätzlicher Provider nötig

### Warum Sonnet statt Haiku für Übersetzung?
- Fachterminologie DE↔PL erfordert höhere Sprachkompetenz
- Fehler in der Übersetzung = falsche Fenster bestellt = teuer
- Asynchroner Workflow → Latenz irrelevant (keine Echtzeit)
- Kosten pro E-Mail ~$0.01-0.05 — vernachlässigbar bei E&W-Volumen

### Warum Claude für PDF-Parsing statt nur pdfplumber?
- Architekten-PDFs haben unterschiedliche Formate
- pdfplumber für strukturierte Tabellen-Extraktion
- Claude Vision als Fallback für unstrukturierte/bildbasierte PDFs
- Kombination: pdfplumber extrahiert was es kann, Claude interpretiert den Rest

### Warum eigenes Repo statt Monorepo mit Clara Voice?
- Komplett andere Domäne (asynchron vs. Echtzeit)
- Unabhängige Deploy-Zyklen
- Kein Risiko für Frank (Telefonassistent) bei Bridge-Changes
- Shared Libraries können später als Packages extrahiert werden

---

## 6. Fensterbau-Fachterminologie (DE ↔ PL)

Kritisch für korrekte Übersetzung. Initiale Liste (wird erweitert):

| Deutsch | Polnisch | Kontext |
|---------|----------|---------|
| Fensterbank | Parapet okienny | Außen: Aluminium, Ausladung in cm |
| Fensterbankanschlussprofil (FB30) | Profil podparapetowy (FB30) | Verbindungsprofil Fenster↔Fensterbank |
| Beschlagssicherheit | Klasa bezpieczeństwa okuć | RC1, RC2, RC3 |
| Verglasung (VSG) | Szklenie (VSG) | Verbundsicherheitsglas |
| Dreifachverglasung | Szyba trzyszybowa | Für U-Wert ≤ 0,95 |
| Wärmedurchgangskoeffizient (Uw) | Współczynnik przenikania ciepła (Uw) | W/m²K |
| Rollladenkasten | Skrzynka roletowa | Typ, Maße, gedämmt/ungedämmt |
| Stulpflügel | Skrzydło sztulpowe | Öffnungsart ohne Mittelpfosten |
| Festverglast | Szklenie stałe (FIX) | Nicht öffenbar |
| Warme Kante | Ciepła ramka dystansowa | Abstandhalter in Isolierverglasung |
| Brüstungshöhe (BRH) | Wysokość parapetu (BRH) | Maß ab Fußboden |
| Einbruchschutz | Ochrona antywłamaniowa | RC-Klassen |
| Putzendstück | Zaślepka tynkowa | Abschluss Fensterbank |
| Montagebohrungen | Otwory montażowe | Links/Rechts |
| Transportschutzart | Rodzaj ochrony transportowej | Folierung etc. |
| Förderfähig | Kwalifikujący się do dofinansowania | Bezug auf KfW/BAFA |

Diese Liste wird als Knowledge Base in der DB gespeichert und kann über das Dashboard erweitert werden. Claude erhält sie als Kontext bei jeder Übersetzung.

---

## 7. Offene Punkte (vor Phase 1)

### Von E&W zu klären

| # | Frage | Warum relevant | Priorität |
|---|-------|---------------|-----------|
| O1 | Hat E&W ein Angebots-Template (Design/Layout)? | Für F2 + F4 (Dokument-Umformatierung + Angebotserstellung) | Phase 2 |
| O2 | Wie berechnet E&W aktuell die Aufschläge? (%, fix, nach Fenstertyp?) | Für F3 (Kalkulation) | Phase 4 |
| O3 | Welche E-Mail-Adresse soll Frank bei Go-Live nutzen? | DNS + Gmail Setup | Phase 1 Go-Live |
| O4 | Soll Frank direkt an Judyta antworten oder immer über E&W? | Workflow-Design. Empfehlung: Immer über E&W in Phase 1 | Phase 1 |
| O5 | Gibt es weitere Lieferanten neben ekookna.pl? | Multi-Supplier Planung | Phase 5 |
| O6 | Wie viele Projekte laufen parallel? (Volumen-Abschätzung) | Infra-Sizing, Gmail Quotas | Phase 1 |

### Technisch zu klären

| # | Frage | Entscheidung nötig für |
|---|-------|----------------------|
| T1 | Gmail Polling vs. Push (Pub/Sub)? Empfehlung: Polling (5min) für MVP, Push für Scale | Phase 1 |
| T2 | Wie erkennt Frank ob eine E-Mail eine neue Anfrage oder Antwort ist? Thread-ID + Subject-Parsing | Phase 1 |
| T3 | ekookna.pl Angebots-Format: PDF-Struktur analysieren (brauchen Beispiel-PDF) | Phase 3 |
| T4 | Zeichnungen aus Architekten-PDF: Raster-Bilder oder Vektor? Extraktions-Strategie | Phase 2 |

---

## 8. Risiken

| Risiko | Schwere | Mitigation |
|--------|---------|------------|
| Übersetzungsfehler bei Fachtermini | Hoch | Fachterminologie-DB + Human-in-the-Loop + Confidence-Score |
| PDF-Parsing scheitert bei unbekanntem Format | Mittel | Claude Vision als Fallback, iterative Format-Erweiterung |
| E&W vergisst Human-in-the-Loop Schritt | Mittel | Telegram-Reminder, kein Auto-Send ohne Approval |
| Gmail API Rate Limits | Niedrig | Polling-Intervall anpassen, Batch-Processing |
| Lieferant ändert Angebots-Format | Mittel | Flexibler Parser (Claude-basiert statt Regex) |

---

## 9. Kosten-Abschätzung (laufend, nach Go-Live)

| Posten | Geschätzt/Monat | Basis |
|--------|-----------------|-------|
| Railway (Server) | ~$5-10 | Hobby Plan, eigener Service |
| Railway (PostgreSQL) | ~$5-10 | Eigene DB oder Shared |
| Anthropic API (Sonnet) | ~$5-20 | ~50-200 Übersetzungen/Monat |
| Gmail API | $0 | Kostenlos bis 1 Mrd. Requests/Tag |
| Telegram | $0 | Kostenlos |
| **Gesamt** | **~$15-40/Monat** | |

---

## 10. Nächster Schritt

1. Loris klärt offene Punkte O1-O6 mit E&W
2. Phase 1 starten: Gmail API Integration + Übersetzungs-Relay
3. Eigenes Repo anlegen: `streitAIsolutions/Clara_bridge`
4. Test mit echtem E-Mail-Flow: Loris simuliert Architekten-Anfrage → Frank übersetzt → Loris prüft
