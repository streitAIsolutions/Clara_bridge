# CLAUDE.md — Clara Bridge OP

**Zweck:** Standing Instructions für Claude Code (Operations). Wird bei jedem Session-Start gelesen.

---

## Projekt-Kontext

Clara Bridge ist ein KI-gestützter Beschaffungsassistent für Handwerksbetriebe. Automatisiert den Angebotsworkflow zwischen Auftraggeber (Architekturbüro), Handwerksbetrieb (Eulen & Weischer) und Lieferant (ekookna.pl, Polnisch).

**Status:** Phase 1 deployed. Railway live: https://clara-bridge-production.up.railway.app
**Repo:** streitAIsolutions/Clara_bridge
**Lokaler Pfad:** ~/Documents/2.\ Business/11.\ STREIT\ AI\ SOULTIONS/1.\ Streit\ AI\ Solutions/1.\ Projekt\ \[Clara\]/Clara\ -\ Bridge\ MVP/1.\ Software

---

## Session-Start Pflicht

1. Lies docs/PROJECT_BRAIN.md
2. Lies docs/SESSION_LOG.md (letzte 2 Sessions)
3. Lies docs/TODO.md
4. Prüfe docs/CLARA_SYSTEM.md auf cross-service Einträge
5. Gib Loris einen strukturierten Überblick:
   - Offene Bugs (aus TODO.md)
   - Auflagen aus letztem QG-Verdict (aus CLAUDE.md Aktive Blocker)
   - Nächste Tasks (aus TODO.md Aktuelle Prioritäten)
   Loris entscheidet dann was diese Session angegangen wird.

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

## QG ZIP Workflow

Nach jeder Session (oder bei 5/5 Änderungen) liefert OP einen ZIP in Downloads mit:
- QG_REPORT.md
- Alle geänderten Code-Dateien

ZIP-Name zeigt Review-Tiefe:
- clara_bridge_qg_full.zip → Full Review
- clara_bridge_qg_light.zip → Light Review
- clara_bridge_qg_minimal.zip → Minimal Review

Loris legt den ZIP direkt im QG-Chat ab. Kein manuelles Sortieren, kein Human Error.

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

## Aktive Blocker + Auflagen nächste Session

- Webhook Secret Token: vor Go-Live mit echten Mails implementieren
- datetime.utcnow in models.py ersetzen durch datetime.now(timezone.utc)
- double-commit vereinheitlichen: entweder auto-commit in get_session() ODER explizit in Handlern, nicht beides
- QG_CHECKLIST.md: P4A Verglasung in TERMINOLOGY.md ergänzen

---

## 5MD Pflege

OP hält alle MDs immer aktuell im Repo (committen + pushen nach jeder Änderung).

Wenn Loris die PK aktualisieren muss, liefert OP einen ZIP mit ALLEN PK-Dateien:
- docs/PROJECT_BRAIN.md
- docs/SESSION_LOG.md
- docs/TODO.md
- docs/ARCHITECTURE.md
- docs/TERMINOLOGY.md
- docs/QG_CHECKLIST.md
- docs/CLARA_SYSTEM.md

Loris löscht alle bestehenden PK-Dateien und lädt den kompletten Block neu rein.
CLAUDE.md gehört NICHT in den ZIP — bleibt im Repo-Root für OP.

SONDERFALL CLARA_SYSTEM.md: Wenn sie geändert wurde, ZIP-Name mit Flag:
clara_bridge_pk_SYNC_CLARA_SYSTEM.zip
→ Loris muss sie dann in BEIDE PKs laden (Bridge + Voice).
Wenn nicht geändert: clara_bridge_pk.zip

---

## Session-Ende Pflicht

Session endet bei einem von zwei Triggern:
1. 5/5 Änderungen erreicht → STOPP, QG ZIP liefern, auf Verdict warten
2. Session-Ziel erreicht → Session-Ende einleiten

Reihenfolge ist fix:

**Schritt 1 — QG ZIP liefern (immer):**
- clara_bridge_qg_full/light/minimal.zip
- Enthält: QG_REPORT.md + alle geänderten Code-Dateien
- Warten auf QG Verdict

**Schritt 2 — Erst nach APPROVED:**
- Bei REJECTED oder BEDINGT APPROVED: fixen, neuen QG ZIP liefern
- Bei APPROVED: weiter mit Schritt 3

**Schritt 3 — PK ZIP liefern (nur wenn 5MD geändert):**
- clara_bridge_pk.zip ODER clara_bridge_pk_SYNC_CLARA_SYSTEM.zip
- Enthält alle 7 PK-Dateien (auch unveränderte)

**Schritt 4 — Handoff-Block (immer):**
- Ziel: [Was als nächstes]
- Dateien benötigt: [Welche Files]
- Offene Entscheidungen: [Was Loris klären muss]
- Autonomie-Stufe: [A/B/C]
- CLARA_SYSTEM.md: [Update nötig? Ja/Nein + was]

Der Handoff-Block ist das klare Signal: Session durch.

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
