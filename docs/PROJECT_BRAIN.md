# PROJECT BRAIN - Clara Bridge (KI-Beschaffungsassistent)

## Neuer Chat? Starte hier!

1. **Lies diese Datei** - Verstehe das Projekt, die Arbeitsstruktur, den Tech Stack
2. **Lies SESSION_LOG.md** (letzte 2-3 Sessions) - Verstehe wo wir stehen
3. **Lies TODO.md** - Verstehe was ansteht

**Aktueller Stand (06.03.2026):**
- **Phase 1 deployed** — Service live auf Railway
- **Railway URL:** `https://clara-bridge-production.up.railway.app`
- **Repo live:** `streitAIsolutions/Clara_bridge` auf GitHub
- **Gmail OAuth:** Token als ENV Variable auf Railway, Polling aktiv
- **Google Cloud:** Gmail API aktiviert, OAuth konfiguriert
- **Railway:** Service + PostgreSQL live, alle 14 ENV Variables gesetzt ✅
- **Telegram Webhook:** Registriert und aktiv ✅
- **E2E-Test:** Bestanden (4 Durchlaeufe, Happy Path komplett) ✅
- **Noch offen:** Webhook Secret Token (Sicherheit), ANTHROPIC_MODEL String verifizieren
- **Naechster Schritt:** Uebersetzungsqualitaet bewerten, Webhook Secret Token, "Bearbeiten"-Flow

**Entscheidungen Phase 1 (03.03.2026):**
- E-Mail-Routing: Alles ueber E&W (Direktmodus spaeter als Feature-Flag)
- Draft-Freigabe: Telegram Inline Keyboard (Buttons: Freigeben/Bearbeiten/Ablehnen)
- Judyta wird informiert: Nur noch auf Polnisch antworten
- Thread-Zuordnung: Gmail Thread-ID primaer, Subject-Parsing Fallback, manuelle Zuordnung via Telegram letzter Fallback
- Gmail Polling: 5 Min Intervall (Pub/Sub erst wenn noetig)

---

## Was ist Clara Bridge?

KI-gestuetzter Beschaffungsassistent fuer Handwerksbetriebe. Automatisiert den Angebotsworkflow zwischen Auftraggeber (Architekturbuero), Handwerksbetrieb und Lieferant.

**Drei Kernfunktionen:**
1. **Uebersetzungs-Relay DE↔PL** mit Human-in-the-Loop (jede E-Mail ueber E&W)
2. **Dokumenten-Umformatierung** — Architekten-PDFs → E&W-Design
3. **Angebotsvalidierung + Kalkulation** — Automatischer Abgleich + E&W-Aufschlaege

**Im Clara-Oekosystem:**

| Modul | Funktion | Status | Projekt |
|-------|----------|--------|---------|
| Clara Voice | KI-Telefonassistent | Live (Frank) | Eigenes Claude-Projekt |
| **Clara Bridge** | **KI-Beschaffungsassistent** | **Phase 1 deployed** | **Dieses Projekt** |

---

## Pilot-Kunde & Beteiligte

| Rolle | Wer | Kontakt |
|-------|-----|---------|
| Handwerksbetrieb | Montagetechnik Eulen und Weischer GmbH | info@eulen-weischer.de |
| Ansprechpartner E&W | Tilmann Weischer ("Till") | 0171 357 7455 |
| Lieferant (Pilot) | ekookna.pl | judyta.klima@ekookna.pl |
| Ansprechpartnerin Lieferant | Judyta Klima | — |
| Lieferanten-Sprache | Polnisch (PL) | — |
| Typische Auftraggeber | Architekturbueros (z.B. maxmartin architekten, Alma Kern) | — |

**Kernproblem das Bridge loest:** Die Kommunikation zwischen E&W und ekookna.pl ist fehleranfaellig. Judyta versteht technische Anforderungen auf Deutsch nicht immer korrekt, was zu fehlerhaften Angeboten und vielen Korrekturschleifen fuehrt. Bridge uebersetzt fachlich korrekt ins Polnische und validiert die Angebote automatisch.

---

## Phasen-Plan

| Phase | Inhalt | Status | Abhaengigkeiten |
|-------|--------|--------|-----------------|
| 1 | E-Mail Relay + Uebersetzung DE↔PL | **DEPLOYED** | Gmail API ✅, Repo ✅, Railway ✅ |
| 2 | PDF-Parsing + Anforderungs-Extraktion | Geplant | Phase 1, Beispiel-PDFs |
| 3 | Angebotsvalidierung (Quality Gate) | Geplant | Phase 2, ekookna Angebots-PDF |
| 4 | Kalkulation + E&W-Angebot | Geplant | Phase 3, E&W Kalkulationsregeln |
| 5 | Dashboard + Multi-Supplier | Geplant | Phase 4 |

Details zu jeder Phase: Siehe ARCHITECTURE.md Sektion 5.

---

## Offene Punkte (von E&W zu klaeren)

| # | Frage | Relevant ab | Status |
|---|-------|-------------|--------|
| O1 | Hat E&W ein Angebots-Template? | Phase 2 | Offen |
| O2 | Wie berechnet E&W Aufschlaege? (%, fix, Fenstertyp?) | Phase 4 | Offen |
| O3 | Welche E-Mail-Adresse bei Go-Live? | Phase 1 Go-Live | Offen |
| O4 | Frank direkt an Judyta oder immer ueber E&W? | Phase 1 | **Geklaert:** Phase 1 alles ueber E&W. Spaeter Direktmodus als Feature-Flag |
| O5 | Weitere Lieferanten neben ekookna.pl? | Phase 5 | Offen |
| O6 | Wie viele Projekte laufen parallel? | Phase 1 | Offen |

---

## Tech Stack

| Komponente | Technologie |
|------------|-------------|
| Backend | FastAPI (Python) |
| Hosting | Railway (eigener Service, EU) |
| Datenbank | PostgreSQL (eigene DB) |
| KI | Anthropic Claude API (Sonnet — Qualitaet > Latenz) |
| E-Mail | Gmail API (frank.eulen.weischer@gmail.com) |
| Benachrichtigung | Telegram Bot (shared mit Clara Voice) |
| PDF-Verarbeitung | pdfplumber + Claude Vision (Fallback) |
| Dokumenten-Erstellung | docx-js / reportlab |
| Version Control | GitHub (`streitAIsolutions/Clara_bridge`) |

---

## Arbeitsstruktur

### 2-Chat-System (aktiv ab 05.03.2026)
- **OP (Operations):** Claude Code im Terminal — implementiert, liefert ZIP + QG_REPORT.md
- **QG (Quality Gate):** Separater Chat im Bridge-Projektordner — nur Review, kein Implementieren
- **Loris:** Bindeglied zwischen OP und QG
- Max. 5 Aenderungen pro OP-Session, dann QG-Pflicht

### Dokumentations-System (5MD)
- **PROJECT_BRAIN.md** ← DIESE DATEI (Status, Kontext, Beteiligte)
- **SESSION_LOG.md** (Chronik aller Sessions)
- **TODO.md** (Aufgaben, Bugs, Features)
- **ARCHITECTURE.md** (Technische Referenz, Datenmodell, Entscheidungen)
- **TERMINOLOGY.md** (Fensterbau-Fachterminologie DE↔PL — ersetzt PROMPT_REGISTRY.md)

### Regeln
- Nach max. 5 Aenderungen: 5MD aktualisieren
- Code-Dateien NICHT in PK (fressen Context Window)
- ARCHITECTURE.md zeigt welche Datei wofuer zustaendig ist → gezielt anfordern
- Bei strategischen Entscheidungen die Clara Voice betreffen: Loris informiert das andere Projekt

---

## User-Infos

| Info | Wert |
|------|------|
| Name | Loris |
| Firma | Streit AI Solutions |
| Level | Terminal gut, Code braucht Erklaerungen |
| Stil | Bash-Befehle ohne Kommentare (Copy-Paste ready) |
| Kommunikation | Direkt, ehrlich, Sparringspartner |
| Workflow | ZIP mit geaenderten Dateien, unzip -o, git push |

---

## Changelog

### 06.03.2026
- Phase 1 deployed auf Railway
- Telegram Webhook Endpoint implementiert + registriert
- Railway Service + PostgreSQL + 14 ENV Variables aufgesetzt
- DATABASE_URL asyncpg-Driver Fix
- Alle 4 Checks gruen: /health, DB, Webhook, Gmail Polling

### 05.03.2026
- 5MD auf aktuellen Code-Stand gebracht (war veraltet)

### 03.03.2026 (Session B)
- GitHub Repo live: streitAIsolutions/Clara_bridge
- Phase 1 Grundstruktur implementiert (27 Dateien):
  - app.py, email_service.py, translation_service.py, telegram_service.py, project_service.py
  - models.py (Phase 1 aktiv + Phase 2-4 Stubs), database.py, config.py
  - tests/test_translation.py, data/terminology_de_pl.json
- Google Cloud: Gmail API aktiviert, OAuth konfiguriert
- Gmail Token generiert fuer frank.eulen.weischer@gmail.com
- token.json in .gitignore gesichert
- Fehlend: Telegram Webhook-Endpoint, Railway Deploy, E2E-Test
