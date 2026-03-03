# PROJECT BRAIN - Clara Bridge (KI-Beschaffungsassistent)

## Neuer Chat? Starte hier!

1. **Lies diese Datei** - Verstehe das Projekt, die Arbeitsstruktur, den Tech Stack
2. **Lies SESSION_LOG.md** (letzte 2-3 Sessions) - Verstehe wo wir stehen
3. **Lies TODO.md** - Verstehe was ansteht

**Aktueller Stand (03.03.2026):**
- **Konzeptphase abgeschlossen** — CLARA_BRIDGE_CONCEPT.md erstellt und freigegeben
- **Kein Code geschrieben** — Projekt startet mit Phase 1 (E-Mail Relay + Uebersetzung)
- **Repo noch nicht angelegt** — `streitAIsolutions/Clara_bridge` geplant
- **Test-Gmail:** frank.eulen.weischer@gmail.com (vorhanden)
- **Naechster Schritt:** Offene Punkte mit E&W klaeren (O1-O6), dann Phase 1 starten

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
| **Clara Bridge** | **KI-Beschaffungsassistent** | **Konzeptphase** | **Dieses Projekt** |

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
| 1 | E-Mail Relay + Uebersetzung DE↔PL | **ALS NAECHSTES** | Gmail API, Repo-Setup |
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
| O4 | Frank direkt an Judyta oder immer ueber E&W? | Phase 1 | Offen (Empfehlung: ueber E&W) |
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

### Einzelchat (vorerst)
Clara Bridge startet mit einem einzelnen Chat (Operations + QG kombiniert). Bei steigender Komplexitaet auf 2-Chat-System splitten (wie bei Clara Voice).

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

### 03.03.2026
- Projekt-Konzept erstellt (CLARA_BRIDGE_CONCEPT.md)
- 5MD-Struktur aufgesetzt
- Entscheidungen: Eigenes Repo, eigenes Claude-Projekt, Gmail API, Sonnet fuer Uebersetzung
- Codename "Clara Bridge" gewaehlt
