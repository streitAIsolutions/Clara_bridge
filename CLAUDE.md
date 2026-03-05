# CLAUDE.md — Clara Bridge OP

**Zweck:** Standing Instructions für Claude Code (Operations). Wird bei jedem Session-Start gelesen.

---

## Projekt-Kontext

Clara Bridge ist ein KI-gestützter Beschaffungsassistent für Handwerksbetriebe. Automatisiert den Angebotsworkflow zwischen Auftraggeber (Architekturbüro), Handwerksbetrieb (Eulen & Weischer) und Lieferant (ekookna.pl, Polnisch).

**Status:** Phase 1 in Entwicklung. Repo live, Gmail OAuth eingerichtet, Railway ausstehend.
**Repo:** streitAIsolutions/Clara_bridge
**Lokaler Pfad:** ~/Documents/2.\ Business/11.\ STREIT\ AI\ SOULTIONS/1.\ Streit\ AI\ Solutions/1.\ Projekt\ \[Clara\]/Clara\ -\ Bridge\ MVP/1.\ Software

---

## Session-Start Pflicht

1. Lies docs/PROJECT_BRAIN.md
2. Lies docs/SESSION_LOG.md (letzte 2 Sessions)
3. Lies docs/TODO.md
4. Prüfe docs/CLARA_SYSTEM.md auf cross-service Einträge

---

## Arbeitsstruktur: 2-Chat-System

Du bist OP (Operations). Ein separater QG-Chat existiert im Bridge-Projektordner.

- Max. 5 Änderungen pro Session, dann STOPP und QG-Review einfordern
- Änderungszähler laut mitzählen: "[Änderung 2/5: P1.15 Telegram Webhook, Stufe B]"
- Jede Session endet mit ZIP + QG_REPORT.md an Loris

**QG_REPORT.md Format:**
```
## QG Report — [Feature] — [Datum]

Änderungen (X/5):
1. [Was, Stufe A/B/C]

Vorgeschlagene Review-Tiefe: Full / Light / Minimal

Pre-Flight-Check:
- Telegram Webhook erreichbar?
- DB-Writes korrekt?
- token.json nicht im Commit?
- ENV Variables dokumentiert?

Test-Ergebnisse: X/Y bestanden
CLARA_SYSTEM.md Update nötig: Ja/Nein + was
```

---

## Autonomie-Stufen

**Stufe A — Direkt umsetzen (kein QG):**
- Bug-Fixes unter 20 Zeilen, keine Architektur-Änderung
- Tests bestehen

**Stufe B — Deploy first, QG review later:**
- Größere Änderungen innerhalb bestehender Architektur
- Tests bestehen, QG-Report mitschicken

**Stufe C — QG vor Deploy:**
- Neue Phasen, Architektur-Änderungen, Datenmodell-Änderungen
- Alles was Shared Resources oder Clara Voice betrifft

---

## Deploy-Workflow

```
cd ~/Documents/2.\ Business/11.\ STREIT\ AI\ SOULTIONS/1.\ Streit\ AI\ Solutions/1.\ Projekt\ \[Clara\]/Clara\ -\ Bridge\ MVP/1.\ Software && unzip -o ~/Downloads/<DATEINAME>.zip && git add -A && git commit -m "<COMMIT>" && git push
```

Nach jedem relevanten Change: python3 tests/test_translation.py

---

## Aktive Blocker

- token.json: In .gitignore — niemals committen. Für Railway als ENV Variable (JSON-String)
- Telegram Webhook: /telegram/webhook fehlt in app.py — Callbacks kommen nicht an
- Railway: Noch nicht deployed

---

## 5MD Pflege

Nach max. 5 Änderungen oder Session-Ende:
docs/PROJECT_BRAIN.md, SESSION_LOG.md, TODO.md, ARCHITECTURE.md, TERMINOLOGY.md aktualisieren.
Als ZIP mit Terminal-Command liefern.

Bei cross-service Entscheidungen: CLARA_SYSTEM.md aktualisieren und Loris liefern.

---

## Session-Ende Pflicht

HANDOFF — NÄCHSTE SESSION:
- Ziel: [Was als nächstes]
- Dateien benötigt: [Welche Files]
- Offene Entscheidungen: [Was Loris klären muss]
- Autonomie-Stufe: [A/B/C]
- CLARA_SYSTEM.md: [Update nötig? Ja/Nein + was]

---

## Shared Resources

Bridge teilt mit Clara Voice:
- Telegram Bot: @eulen_weischer_bot — Bridge IMMER mit Prefix "[Bridge]"
- Railway Account: eigener Service, gleicher Account
- Anthropic API Key: gleicher Key

Bridge hat EIGENE: PostgreSQL DB, GitHub Repo, Gmail API

---

## Technische Constraints

- Claude Sonnet für Übersetzungen
- TERMINOLOGY.md immer als System-Kontext bei Übersetzungen mitgeben
- Gmail Polling 5 Min
- Human-in-the-Loop: Telegram Inline Keyboard (Freigeben/Bearbeiten/Ablehnen)
- Thread-Zuordnung: Gmail Thread-ID → Subject-Parsing → manueller Fallback
- E-Mail-Routing Phase 1: Alles über E&W

---

## Über Loris

- Terminal-erfahren, Code braucht Erklärungen
- Bash-Befehle OHNE Kommentare (Copy-Paste ready), Erklärungen NACH dem Code-Block
- Sparringspartner — ehrliche Bewertung, nicht Gefälligkeit
