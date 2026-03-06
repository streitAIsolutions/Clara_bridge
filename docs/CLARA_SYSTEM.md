# CLARA_SYSTEM.md — Clara Ökosystem Übersicht

**Zweck:** Zentrales Synchronisations-Dokument. Liegt als PK in ALLEN Clara Projekt-Ordnern. Gibt jedem Chat den Überblick über das Gesamtsystem — was existiert, wer woran arbeitet, und welche Entscheidungen andere Services betreffen.

**Letztes Update:** 6. März 2026 (v4 — Clara Bridge Phase 1 live)

---

## PFLICHT FÜR JEDEN CHAT

### Beim Lesen (Session-Start)
- Lies CLARA_SYSTEM.md vor Arbeitsbeginn
- Prüfe ob es Einträge im Cross-Service Changelog gibt die deine Arbeit betreffen
- Wenn ja: Berücksichtige sie aktiv bei deiner Arbeit

### Beim Arbeiten (während der Session)
Wenn du eine Entscheidung triffst oder etwas implementierst das **einen anderen Service betrifft**, muss das ins Cross-Service Changelog. Erkenne diese Situationen selbst:

- Shared Resource geändert (DB-Schema, Telegram Bot, API Key, etc.)
- Architektur-Entscheidung die Service-Grenzen betrifft
- Neues Feature das von einem anderen Service genutzt werden soll
- Interface/API das ein anderer Service aufruft
- Datenmodell-Änderung die Auswirkungen auf shared DB hat
- Abhängigkeit von einem anderen Service entdeckt oder aufgelöst

**Aktion:**
Wenn du eine cross-service Entscheidung erkennst, aktualisiere CLARA_SYSTEM.md selbst:
1. Trage den Changelog-Eintrag ein (Sektion 6)
2. Aktualisiere betroffene Sektionen (Abhängigkeiten, Blocker, Architektur-Entscheidungen) falls nötig
3. Aktualisiere das "Letztes Update" Datum im Header
4. Liefere Loris die aktualisierte Datei mit dem Hinweis: "CLARA_SYSTEM.md aktualisiert — bitte in alle Projekt-Ordner synchronisieren."

Wenn du unsicher bist ob etwas cross-service relevant ist: Lieber einmal zu viel melden als einmal zu wenig.

### Nach der Session (5MD-Update)
Bei der regulären 5MD-Aktualisierung prüfen:
- Hat sich der Status dieses Services geändert? → Service-Landkarte aktualisieren
- Gibt es neue Shared Resources? → Sektion 2 aktualisieren
- Gibt es neue Abhängigkeiten? → Sektion 3 aktualisieren

---

## 1. Service-Landkarte

| Service | Funktion | Status | Projekt-Ordner | DB |
|---------|----------|--------|----------------|----|
| **Clara Voice** | KI-Telefonassistent (Frank) | **LIVE** | Clara Voice (OP + QG) | PostgreSQL (Railway) |
| **Clara Chat** | WhatsApp-Bot (Frank Chat) | **LIVE** | Clara Voice (chat/ Ordner) | Shared mit Voice |
| **Clara Core** | Shared Business Logic | **LIVE** | Clara Voice (shared/ Ordner) | — (Library, keine eigene DB) |
| **Clara Bridge** | KI-Beschaffungsassistent | **Phase 1 LIVE** | Clara Bridge | PostgreSQL (eigene DB) |
| **Clara CRM** (F17) | Kunden-Wissensbasis | **Roadmap** | Clara Voice | Shared mit Voice |

### Produkt-Cluster

**Cluster A — Endkunden-Services (geteilte DB + Business Logic):**
- Clara Voice, Clara Chat, Clara Core, Clara CRM
- Gleicher Projekt-Ordner, gleiches Repo, gleiche PostgreSQL-DB
- Shared: models.py, calendar_service, maps_service, customer_service, settings_service, messaging_service

**Cluster B — Beschaffung (eigenständig):**
- Clara Bridge
- Eigenes Repo, eigene DB, eigener Workflow
- Shared mit Cluster A: nur Infrastruktur (Railway, Anthropic Key, Telegram Bot)

---

## 2. Shared Resources

| Resource | Genutzt von | Details |
|----------|-------------|---------|
| Railway Account | Alle | Eigener Service pro Modul, europe-west4 |
| Anthropic API Key | Alle | Ein Key, getrennte Nutzung |
| Telegram Bot | Voice + Chat + Bridge | @eulen_weischer_bot — Voice: normale Messages, Chat: "[Chat]" Prefix, Bridge: "[Bridge]" Prefix |
| PostgreSQL (Voice-DB) | Voice, Chat, Core, CRM | Shared DB, 11+ Tabellen |
| PostgreSQL (Bridge-DB) | Bridge | Eigene DB, eigenes Schema |
| GitHub Org | Alle | streitAIsolutions/ |
| Twilio | Voice, Chat | Voice: Anrufe + WhatsApp Outbound. Chat: WhatsApp Inbound + Outbound |
| Google Calendar | Voice, Chat | Shared Calendar API für Terminbuchung |
| Google Maps | Voice, Chat | Geocoding, Servicegebiet |
| Gmail API | Bridge | frank.eulen.weischer@gmail.com |

---

## 3. Abhängigkeiten zwischen Services

### Voice → Chat
- Chat nutzt dieselben Tools (calendar_service, maps_service, customer_service)
- Chat nutzt dieselben DB-Tabellen (customers, appointments, companies)
- Änderungen an Shared Tools müssen "shared-ready" sein (keine Voice-spezifische Logik)
- Twilio WhatsApp Webhook: Aktuell auf Voice konfiguriert. Bei Chat-Launch umkonfigurieren oder routen

### Voice → CRM (F17)
- CRM erweitert die Kunden-DB um strukturierte Historie
- Voice schreibt in CRM (nach Anruf: was wurde besprochen)
- Voice liest aus CRM (bei Anruf: Kundenhistorie in Prompt)

### Chat → Voice
- Chat kann Termine buchen/ändern/stornieren die Voice sieht
- Gleiche appointment_created Logik, gleiche Doppelbuchungs-Checks

### Bridge → Voice/Chat
- Keine direkte Abhängigkeit (eigene DB, eigener Workflow)
- Shared: Telegram Bot (Namespace-Trennung via Prefix)

---

## 4. Aktive Architektur-Entscheidungen

| Datum | Entscheidung | Betrifft | Entschieden in |
|-------|-------------|----------|----------------|
| 04.03.2026 | Frank Chat als eigener Railway-Service, shared DB mit Voice | Voice, Chat | Voice QG |
| 04.03.2026 | clara-core als shared/ Ordner im Monorepo (später Package) | Voice, Chat, Core | Voice QG |
| 04.03.2026 | Session-Timeout Chat: Termin+90min / 24h Inaktivität / explizit | Chat | Voice QG |
| 04.03.2026 | Reihenfolge: F2+F3 → clara-core → Chat MVP → F12 | Voice, Chat | Voice QG |
| 04.03.2026 | F2+F3 Tools müssen shared-ready sein (Business Logic in calendar_service) | Voice, Chat | Voice QG |
| 04.03.2026 | F17 Kunden-Wissensbasis auf Roadmap (nach Chat MVP) | Voice, Chat, CRM | Voice QG |
| 03.03.2026 | Bridge: eigene DB, eigenes Repo, kein shared Code mit Voice | Bridge, Voice | Voice QG + Bridge |
| 03.03.2026 | Telegram Bot shared, Bridge nutzt "[Bridge]" Prefix | Voice, Bridge | Bridge |

---

## 5. Aktive Blocker (Cross-Service)

| Blocker | Betrifft | Status |
|---------|----------|--------|
| Hybrid Routing (_pick_model zählt tool_results) | Voice | Offen — NICHT aktivieren |
| WhatsApp Schweizer Nummer → Produktionsnummer | Voice, Chat | Bei Go-Live ersetzen |
| create_appointment Prompt-Härtung verifizieren | Chat | Offen — Logs nach nächstem WhatsApp-Test prüfen |

---

## 6. Cross-Service Changelog

Neueste Einträge oben. Jeder Eintrag: Datum, Quelle, Was, Betrifft.

| Datum | Quelle | Entscheidung | Betrifft |
|-------|--------|-------------|----------|
| 06.03.2026 | Bridge OP | Clara Bridge Phase 1 live: https://clara-bridge-production.up.railway.app, Gmail Polling aktiv, Telegram Human-in-the-Loop funktioniert. E2E-Test bestanden (4 Durchlaeufe). | Bridge, Voice |
| 05.03.2026 | Bridge QG | Clara Bridge auf 2-Chat-System umgestellt (OP=Claude Code, QG=separater Chat). Bridge Status: Phase 1 in Entwicklung (Repo live, Gmail OAuth, Railway ausstehend) | Bridge |
| 04.03.2026 | Voice QG | F18 Frank Chat LIVE: eigener Railway-Service (frank-chat-production.up.railway.app), Twilio WhatsApp Inbound Webhook auf Chat umkonfiguriert | Chat, Voice |
| 04.03.2026 | Voice QG | clara-core LIVE: shared/ Ordner deployed, Voice + Chat importieren aus shared/ | Voice, Chat, Core |
| 04.03.2026 | Voice QG | shared/models.py: +ChatSession Tabelle (12. Tabelle in shared DB) | Voice, Chat |
| 04.03.2026 | Voice QG | Telegram-Notifications Chat: Termin/Storno/Umbuchung via WhatsApp, asyncio.create_task | Chat |
| 04.03.2026 | Voice QG | F2+F3 QG Review: Business Logic muss in calendar_service (nicht ai_service) damit Chat dieselben Tools nutzen kann. Blocker für Deploy. | Voice OP, Chat |
| 04.03.2026 | Voice QG | Frank Chat Architektur definiert: eigener Railway-Service, shared DB, eigener Prompt, Session-Management in DB | Chat, Voice |
| 04.03.2026 | Voice QG | Implementierungs-Reihenfolge: F2+F3 → clara-core → Chat MVP → F12 | Voice, Chat, Bridge |
| 04.03.2026 | Voice QG | F4 Phase 7 Error-Handling deployed (Graceful Degradation, Claude Retry, Deepgram Fatal) | Voice |
| 04.03.2026 | Voice QG | F14 Service-Zeitprofile deployed (profilbasierte Öffnungszeiten) | Voice |
| 03.03.2026 | Bridge | Phase 1 Flow definiert (4 Flows), Telegram shared mit Voice via Prefix | Bridge, Voice |
| 03.03.2026 | Voice QG | F11 WhatsApp live, Template approved, Anrufnummer-Vorrang | Voice |

---

## 7. Pflege-Regeln

1. **CLARA_SYSTEM.md liegt in ALLEN Projekt-Ordnern als PK** — identische Kopie überall
2. **Chats tragen selbst ein** — Wenn eine cross-service Entscheidung fällt, aktualisiert der Chat CLARA_SYSTEM.md direkt (Changelog, Abhängigkeiten, Blocker, etc.) und liefert Loris die aktualisierte Datei
3. **Loris synchronisiert** — Kopiert die aktualisierte Datei in alle Projekt-Ordner (PK). Kein weiterer Aufwand
4. **Aktualisierung nach Bedarf, nicht nach Zeitplan** — nur wenn cross-service Entscheidung fällt
5. **Kurz halten** — max 3 Seiten. Kein Ersatz für projekt-spezifische 5MD
6. **Kein Duplikat von 5MD** — CLARA_SYSTEM.md enthält NUR was für andere Services relevant ist. Projekt-interne Details bleiben in den jeweiligen 5MD
7. **Letztes Update Datum** — Bei jeder Änderung das Datum im Header aktualisieren
