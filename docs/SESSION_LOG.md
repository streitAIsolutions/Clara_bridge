# Session Log - Clara Bridge (KI-Beschaffungsassistent)

## Neuer Chat? Lies die letzten 2-3 Sessions!

Die neuesten Sessions stehen oben. Fuer Projekt-Kontext siehe PROJECT_BRAIN.md, fuer Aufgaben siehe TODO.md.

---

## 2026

### Session 03.03.2026-B (Operations)

**Teilnehmer:** Loris + Claude (Operations)

**Ziel:** Phase 1 Flow definieren, Projektstruktur bauen, GitHub Repo aufsetzen, Gmail OAuth einrichten

**Erreicht:**

#### Flow-Design
- 4 Flows als interaktives React-Diagramm (Happy Path, Antwort, Korrektur, Edge Cases)
- Happy Path: Architekten-Anfrage → Bridge übersetzt → Telegram-Review → Freigabe → Judyta
- Alle Edge Cases dokumentiert: Projekt-Zuordnung fehlgeschlagen, Low-Confidence, Ablehnung, API-Fehler

#### Entscheidungen
- O4 geklärt: Phase 1 alles über E&W, Direktmodus später als Feature-Flag
- Draft-Freigabe: Telegram Inline Keyboard (Freigeben/Bearbeiten/Ablehnen), kein Gmail-Draft-Interface
- Spracherkennung: Judyta wird informiert nur noch PL zu schreiben → Vereinfachung
- Thread-Zuordnung: Gmail Thread-ID primär, Subject-Parsing Fallback, manuelle Zuordnung via Telegram
- Gmail Polling: 5 Min Intervall (Pub/Sub erst wenn nötig)
- E-Mail-Status-Flow: RECEIVED → DRAFT → APPROVED_BY_EW → SENT / REJECTED

#### Projektstruktur (27 Dateien)
- app.py — FastAPI Server, Polling-Loop, /health, /projects
- backend/email_service.py — Gmail Inbound-Polling, Draft-Erstellung, Attachment-Handling
- backend/translation_service.py — Claude Sonnet DE↔PL, TERMINOLOGY.md Kontext
- backend/telegram_service.py — Inline Keyboard, Callback-Handling
- backend/project_service.py — 3-stufige Thread-Zuordnung
- backend/models.py — Alle Tabellen (Phase 1 aktiv, Phase 2-4 Stubs)
- backend/config.py, database.py, terminology.py
- data/terminology_de_pl.json
- tests/test_translation.py (echte Kom. Kern Korrespondenz als Testdaten)
- docs/ — 5MD vollständig

#### Lokaler Pfad
`/Users/loriss/Documents/2. Business/11. STREIT AI SOULTIONS/1. Streit AI Solutions/1. Projekt [Clara]/Clara - Bridge MVP/1. Software/`

#### GitHub Repo
- streitAIsolutions/Clara_bridge — live, 2 Commits (Initial + Phase 1 Code)
- HTTPS Remote, SSH noch nicht eingerichtet

#### Gmail OAuth
- Google Cloud Projekt: Frank-Calendar (wiederverwendet)
- Gmail API aktiviert
- OAuth Consent Screen konfiguriert, frank.eulen.weischer@gmail.com als Test-User
- credentials.json: client_secret_924423517309-....json
- token.json: Generiert, liegt in 1. Software/, in .gitignore gesichert

**Fehlend nach Session-Ende:**
- Telegram Webhook-Endpoint in app.py fehlt (kein /telegram/webhook)
- Railway noch nicht aufgesetzt
- Kein E2E-Test gelaufen

**5MD-Updates:**
- PROJECT_BRAIN: O4 geklärt, Entscheidungen Phase 1 ergänzt
- TODO: 21 konkrete Tasks in 6 Untergruppen (P1.1-P1.21)
- SESSION_LOG: Diese Session
- ARCHITECTURE: Phase 1 Entscheidungen (Polling, Thread-Zuordnung, Routing, Telegram, Status-Flow)
- TERMINOLOGY: Keine Änderung

### Session 03.03.2026-B (Phase 1 Flow-Design im Clara Bridge Projekt)

**Teilnehmer:** Loris + Claude

**Ziel:** Phase 1 Flow definieren, Offene Punkte klaeren, Blaupause fuer Implementierung

**Entscheidungen:**
1. **O4 geklaert:** Phase 1 alles ueber E&W. Spaeter Direktmodus als Feature-Flag
2. **Draft-Freigabe:** Telegram Inline Keyboard (Buttons: Freigeben/Bearbeiten/Ablehnen)
3. **Spracherkennung:** Judyta wird informiert nur noch PL zu schreiben. Trotzdem simple Erkennung einbauen
4. **Thread-Zuordnung:** Gmail Thread-ID primaer → Subject-Parsing Fallback → Manuelle Zuordnung via Telegram letzter Fallback
5. **Gmail Polling:** 5 Min Intervall fuer MVP (Pub/Sub spaeter)

**Ergebnisse:**
- Interaktives Flow-Diagramm erstellt (React, 4 Flows):
  - Happy Path: Architekten-Anfrage → Uebersetzung → Telegram-Review → Judyta (7 Steps)
  - Antwort-Flow: Judyta PL → Bridge → Till DE (4 Steps)
  - Korrektur-Flow: Till DE Korrekturen → Bridge → Judyta PL (5 Steps)
  - Edge Cases: Projekt-Zuordnung, Low-Confidence, Ablehnung, API-Fehler, Attachment-Limit (5 Cases)
- PROJECT_BRAIN.md, TODO.md, SESSION_LOG.md aktualisiert

**Naechste Schritte:**
- GitHub Repo anlegen (streitAIsolutions/Clara_bridge)
- Gmail OAuth Credentials pruefen/einrichten
- Phase 1 Implementierung starten: Grundstruktur + Gmail Integration

---

### Session 03.03.2026 (Konzeption im Clara Voice QG Chat)

**Teilnehmer:** Loris + Claude

**Ziel:** Feature-Idee evaluieren, Konzept erstellen, Projektstruktur aufsetzen

**Kontext:** E&W hat Schwierigkeiten in der Kommunikation mit polnischem Fensterlieferanten (ekookna.pl). Angebotsanfragen von Architekturbueros muessen manuell uebersetzt, kontrolliert und kalkuliert werden. Fehleranfaellig und zeitintensiv.

**Ausgangsmaterial analysiert:**
- Angebotsanfrage von Alma Kern (maxmartin architekten) fuer Bellerstrasse 31, Huerth
- Fensterliste mit 15 Positionen (F-001 bis F-015), EG/1.OG/DG
- Komplette E-Mail-Korrespondenz E&W mit ekookna.pl (Kom. Kern): 7 Seiten, 8+ Korrekturschleifen
- Anforderungen: U-Wert 0,95, RC2/RC3, VSG, Rolllaeden, Fensterbaenke Alu 22cm

**Entscheidungen:**
1. Alleinstehend unter Clara-Dach: eigenes Repo, eigene DB, eigenes Claude-Projekt
2. Codename: Clara Bridge (Bruecke zwischen E&W und Lieferanten)
3. E-Mail-basiert (Gmail API): E&W arbeitet mit Google Suite, Test-Account vorhanden
4. Sonnet fuer Uebersetzung: Fachterminologie erfordert hohe Sprachqualitaet, Latenz irrelevant
5. Angebotsvalidierung als Kernfeature: nicht Nice-to-have, von Anfang an im Design
6. 5 Phasen: Relay, PDF-Parsing, Validierung, Kalkulation, Dashboard
7. 5MD-Struktur mit TERMINOLOGY.md statt PROMPT_REGISTRY.md

**Ergebnisse:**
- CLARA_BRIDGE_CONCEPT.md erstellt (vollstaendiges Projektkonzept)
- 5MD-Dokumentation aufgesetzt (PROJECT_BRAIN, SESSION_LOG, TODO, ARCHITECTURE, TERMINOLOGY)
- 6 offene Punkte fuer E&W identifiziert (O1-O6)
- Initiale Fachterminologie-Liste DE/PL aus Korrespondenz extrahiert (16 Begriffe)

**Naechste Schritte:**
- Offene Punkte O1-O6 mit E&W klaeren
- GitHub Repo anlegen
- Claude-Projekt Clara Bridge aufsetzen mit 5MD als PK
- Phase 1 starten: Gmail API + Uebersetzungs-Relay
