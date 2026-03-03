# Clara Bridge

KI-Beschaffungsassistent für Handwerksbetriebe. Automatisiert den Angebotsworkflow zwischen Auftraggeber (Architekturbuero), Handwerksbetrieb und Lieferant.

## Kernfunktionen

1. **Übersetzungs-Relay DE↔PL** mit Human-in-the-Loop
2. **Dokumenten-Umformatierung** — Architekten-PDFs → E&W-Design
3. **Angebotsvalidierung + Kalkulation** — Automatischer Abgleich + E&W-Aufschläge

## Tech Stack

- **Backend:** FastAPI (Python)
- **DB:** PostgreSQL (async via SQLAlchemy)
- **KI:** Anthropic Claude Sonnet (Übersetzung + Fachterminologie)
- **E-Mail:** Gmail API
- **Notifications:** Telegram Bot
- **Hosting:** Railway (EU)

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# .env befüllen
uvicorn app:app --reload
```

## Phasen

| Phase | Inhalt | Status |
|-------|--------|--------|
| 1 | E-Mail Relay + Übersetzung | In Arbeit |
| 2 | PDF-Parsing + Anforderungs-Extraktion | Geplant |
| 3 | Angebotsvalidierung | Geplant |
| 4 | Kalkulation + E&W-Angebot | Geplant |
| 5 | Dashboard + Multi-Supplier | Geplant |

## Dokumentation

Siehe `docs/` Ordner:
- `PROJECT_BRAIN.md` — Status, Kontext, Beteiligte
- `ARCHITECTURE.md` — Technische Referenz
- `TERMINOLOGY.md` — Fachterminologie DE↔PL
- `TODO.md` — Aufgaben
- `SESSION_LOG.md` — Chronik

## Teil des Clara-Ökosystems

| Modul | Funktion | Status |
|-------|----------|--------|
| Clara Voice | KI-Telefonassistent | Live |
| **Clara Bridge** | **KI-Beschaffungsassistent** | **Phase 1** |
