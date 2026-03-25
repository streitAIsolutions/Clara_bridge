# QG_CHECKLIST.md — Clara Bridge Quality Gate

**Zweck:** Review-Checkliste für jeden QG-Zyklus. Bridge-spezifisch.
**Letztes Update:** 06.03.2026

---

## 1. CLAUDE.md Aktualität (bei jedem Full Review)
- [ ] Status-Zeile aktuell (Railway URL, Phase)?
- [ ] Aktive Blocker aktuell (erledigte entfernt)?
- [ ] 5MD Workflow korrekt dokumentiert?
- [ ] CLARA_SYSTEM.md in docs/ aktuell?
- [ ] Wenn CLARA_SYSTEM.md geändert: ZIP-Flag gesetzt (SYNC_CLARA_SYSTEM)?

## 2. Code-Review

### DB-Writes
- [ ] Jedes session.execute(update(...)) hat await session.commit() danach?
- [ ] datetime.now(timezone.utc) statt datetime.utcnow()?

### Token + Secrets
- [ ] token.json nicht im Commit (in .gitignore)?
- [ ] Keine Credentials hardcoded?

### Telegram
- [ ] handle_callback() behandelt alle Fälle explizit (approve/reject/assign/new_project)?
- [ ] Unbekannte Actions werden geloggt (kein else: pass)?
- [ ] setup_telegram() loggt Webhook-Registrierung?

### HTTP Clients
- [ ] httpx.AsyncClient() immer mit async with Context Manager?

## 3. Deploy-Checkliste
- [ ] ENV Variables vollständig (alle 14 aus .env.example)?
- [ ] Railway /health antwortet?
- [ ] Telegram Webhook in Logs bestätigt?
- [ ] Gmail Polling aktiv in Logs?

## 4. 5MD Pflege
- [ ] SESSION_LOG aktuell?
- [ ] TODO aktuell (erledigte Tasks als erledigt markiert)?
- [ ] PROJECT_BRAIN Status aktuell?

## 5. Bekannte Fallen

| Falle | Erklärung | Entdeckt bei |
|-------|-----------|-------------|
| session.commit() vergessen | execute(update()) ohne commit() ist stilles No-Op | QG Review 05.03.2026 |
| datetime.utcnow() deprecated | Railway läuft Python 3.11+, timezone.utc verwenden | QG Review 05.03.2026 |
| httpx ohne Context Manager | Resource-Leak auf Railway | QG Review 05.03.2026 |
| Webhook ohne Secret Token | Öffentlicher Endpoint ohne Auth — vor Go-Live fixen | QG Auflage 05.03.2026 |
| import mitten in Funktion | Imports gehören an Dateianfang | QG Review 05.03.2026 |
| callback_data > 64 bytes | Telegram-Limit: kurze Keys (a/e/p) verwenden, draft_id aus DB holen statt in Button-Payload | E2E Test 06.03.2026 |
| HTML in Telegram-Messages | User-Daten (E-Mail-Adressen, Projektnamen) mit html_escape() wrappen — sonst 400 Bad Request | E2E Test 06.03.2026 |
| Railway hat keinen SQL-Editor | Railway Dashboard zeigt zwar Tabellen im Data-Tab, aber kein Query-Interface für ALTER TABLE etc. Migrationen immer per psql mit DATABASE_PUBLIC_URL aus Railway Variables ausführen. | Session 06.03.2026-B |
