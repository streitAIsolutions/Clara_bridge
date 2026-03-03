"""
Uebersetzungs-Tests.
Testet DE→PL und PL→DE mit Fensterbau-Fachterminologie.
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SAMPLE_DE_EMAIL = """Hi Judyta,

danke für das Angebot. Bitte ändere:

Alle Fenster brauchen Uwert 0,95 oder besser also dreifachverglast.
Und wieviel teurer wäre es, wenn wir alle Fenster in P4A Verglasung außen hätten?

Die Fenster 1-7 brauchen Beschlagssicherheit 2 höher. Machst du sonst noch Anpassungen für RC3?
Alle anderen Fenster brauchen Beschlagssicherheit 1 höher. Machst du sonst noch Anpassungen für RC2?

Alle Fenster außer 10 und 11 sollen Rollladen bekommen.

Die Fensterbänke fehlen noch im Angebot, bitte ergänze sie. (Alu, Ausladung 22 cm)

Pos 3-15: Bitte FB30 ergänzen (Fensterbankanschlussprofil was mittig sitzt und 30 mm hoch ist).
Bitte die Länge der Fensterbänke auf die Breite der Fenster anpassen.
Und mit Putzendstücken versehen.

Viele Grüße
Till"""


SAMPLE_PL_EMAIL = """Cześć Till,

w załączniku poprawiona oferta.

Szkło zostało wybrane przez technika.
Klasa odporności RC2 jest uwzględniona, ale nie mamy certyfikatu.
Parapety zewnętrzne mają takie same wymiary jak okna.

Pozdrawiam,
Judyta"""


EXPECTED_TERMS_DE_TO_PL = [
    "trzyszybowa",
    "RC3",
    "RC2",
    "roleta",
    "parapet",
    "profil podparapetowy",
    "FB30",
    "zaślepka tynkowa",
]

EXPECTED_TERMS_PL_TO_DE = [
    "RC2",
    "Zertifikat",
    "Fensterbank",
    "Techniker",
]


async def test_translation_de_to_pl():
    """Test DE→PL Uebersetzung mit echtem API-Call."""
    from backend.translation_service import translate_email

    print("=" * 60)
    print("TEST: DE → PL Uebersetzung")
    print("=" * 60)

    result = await translate_email(SAMPLE_DE_EMAIL, "Änderungen Kom. Kern")

    print(f"\nSource: {result['source_language']}")
    print(f"Target: {result['target_language']}")
    print(f"\nTranslation:\n{result['translated_text']}")
    print(f"\nConfidence Notes: {result['confidence_notes']}")

    assert result["source_language"] == "de", f"Expected 'de', got '{result['source_language']}'"
    assert result["target_language"] == "pl", f"Expected 'pl', got '{result['target_language']}'"
    assert result["translated_text"], "Translation is empty"

    translated_lower = result["translated_text"].lower()
    for term in EXPECTED_TERMS_DE_TO_PL:
        if term.lower() in translated_lower:
            print(f"  ✅ Found: {term}")
        else:
            print(f"  ⚠️  Missing: {term}")

    print("\n✅ DE→PL test passed")


async def test_translation_pl_to_de():
    """Test PL→DE Uebersetzung mit echtem API-Call."""
    from backend.translation_service import translate_email

    print("=" * 60)
    print("TEST: PL → DE Uebersetzung")
    print("=" * 60)

    result = await translate_email(SAMPLE_PL_EMAIL, "Odp: Kom. Kern")

    print(f"\nSource: {result['source_language']}")
    print(f"Target: {result['target_language']}")
    print(f"\nTranslation:\n{result['translated_text']}")
    print(f"\nConfidence Notes: {result['confidence_notes']}")

    assert result["source_language"] == "pl", f"Expected 'pl', got '{result['source_language']}'"
    assert result["target_language"] == "de", f"Expected 'de', got '{result['target_language']}'"
    assert result["translated_text"], "Translation is empty"

    translated_lower = result["translated_text"].lower()
    for term in EXPECTED_TERMS_PL_TO_DE:
        if term.lower() in translated_lower:
            print(f"  ✅ Found: {term}")
        else:
            print(f"  ⚠️  Missing: {term}")

    print("\n✅ PL→DE test passed")


if __name__ == "__main__":
    print("Clara Bridge - Translation Tests")
    print("Benötigt: ANTHROPIC_API_KEY in .env\n")

    asyncio.run(test_translation_de_to_pl())
    print()
    asyncio.run(test_translation_pl_to_de())
