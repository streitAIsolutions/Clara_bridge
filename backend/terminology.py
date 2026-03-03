"""
Fachterminologie-Loader.
Laedt TERMINOLOGY.md als Kontext fuer Claude-Uebersetzungen.
Spaeter: JSON-Format mit Lieferanten-spezifischen Varianten.
"""

import json
import logging
from pathlib import Path

logger = logging.getLogger("bridge.terminology")

_cached_terminology = None

TERMINOLOGY_MD_PATH = Path(__file__).parent.parent / "data" / "terminology_de_pl.json"
TERMINOLOGY_FALLBACK = Path(__file__).parent.parent / "docs" / "TERMINOLOGY.md"


def load_terminology() -> str:
    """Terminologie als formatierten String fuer Claude System-Prompt laden.

    Prioritaet:
    1. JSON-Datei (data/terminology_de_pl.json) - strukturiert
    2. Markdown-Datei (docs/TERMINOLOGY.md) - Fallback
    3. Eingebettete Basis-Terminologie - Notfall-Fallback
    """
    global _cached_terminology
    if _cached_terminology is not None:
        return _cached_terminology

    if TERMINOLOGY_MD_PATH.exists():
        try:
            with open(TERMINOLOGY_MD_PATH, "r", encoding="utf-8") as f:
                terms = json.load(f)
            _cached_terminology = format_terminology_json(terms)
            logger.info(f"Terminology loaded from JSON: {len(terms)} entries")
            return _cached_terminology
        except Exception as e:
            logger.warning(f"Failed to load JSON terminology: {e}")

    if TERMINOLOGY_FALLBACK.exists():
        try:
            with open(TERMINOLOGY_FALLBACK, "r", encoding="utf-8") as f:
                _cached_terminology = f.read()
            logger.info("Terminology loaded from Markdown fallback")
            return _cached_terminology
        except Exception as e:
            logger.warning(f"Failed to load Markdown terminology: {e}")

    _cached_terminology = get_embedded_terminology()
    logger.warning("Using embedded fallback terminology")
    return _cached_terminology


def format_terminology_json(terms: list) -> str:
    """JSON-Terminologie in lesbaren String formatieren."""
    lines = ["Deutsch → Polnisch Fachterminologie Fensterbau:\n"]
    for entry in terms:
        de = entry.get("de", "")
        pl = entry.get("pl", "")
        note = entry.get("note", "")
        line = f"- {de} → {pl}"
        if note:
            line += f" ({note})"
        lines.append(line)
    return "\n".join(lines)


def reload_terminology():
    """Cache invalidieren (z.B. nach Update via Dashboard)."""
    global _cached_terminology
    _cached_terminology = None
    logger.info("Terminology cache cleared.")


def get_embedded_terminology() -> str:
    """Eingebettete Basis-Terminologie als Notfall-Fallback."""
    return """Deutsch → Polnisch Fachterminologie Fensterbau:

- Fenster → Okno
- Fensterbank (aussen) → Parapet okienny (zewnętrzny)
- Fensterbankanschlussprofil (FB30) → Profil podparapetowy (FB30)
- Fensterfluegel → Skrzydło okienne
- Fensterrahmen → Rama okienna
- Haustuer → Drzwi wejściowe
- Verglasung → Szklenie
- Dreifachverglasung → Szyba trzyszybowa
- Verbundsicherheitsglas (VSG) → Szkło bezpieczne klejone (VSG)
- Einscheibensicherheitsglas (ESG) → Szkło bezpieczne hartowane (ESG)
- Warme Kante → Ciepła ramka dystansowa
- Einbruchschutz → Ochrona antywłamaniowa
- Widerstandsklasse RC2 → Klasa odporności RC2
- Widerstandsklasse RC3 → Klasa odporności RC3
- Beschlag → Okucie
- Beschlagssicherheit X hoeher → Okucie o X klasę wyżej
- Dreh-Kipp → Rozwierno-uchylne (RU)
- Festverglast (FIX) → Szklenie stałe (FIX)
- Stulpfluegel → Skrzydło sztulpowe
- Rollladenkasten → Skrzynka roletowa
- Rollladen → Roleta zewnętrzna
- Insektenschutz → Moskitiera
- Putzendstuck → Zaślepka tynkowa
- Montagebohrungen → Otwory montażowe
- Waermedurchgangskoeffizient (Uw) → Współczynnik przenikania ciepła (Uw)
- Bruestungshoehe (BRH) → Wysokość parapetu (BRH)
- Foliert → Foliowany
- Holzoptik → Imitacja drewna
- Angebot → Oferta
- Angebotsanfrage → Zapytanie ofertowe
- Bestellung → Zamówienie
- Proforma(-Rechnung) → Faktura proforma
- Kommission (Kom.) → Komisja / Zlecenie
- Liefertermin → Termin dostawy
- Baustelle → Plac budowy
"""
