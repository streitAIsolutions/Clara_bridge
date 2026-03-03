"""
Uebersetzungs-Engine DE<>PL mit Claude Sonnet.
Nutzt TERMINOLOGY.md als Fachterminologie-Kontext.
"""

import logging
from pathlib import Path

import anthropic

from backend.config import settings
from backend.terminology import load_terminology

logger = logging.getLogger("bridge.translation")

_client = None


def get_client():
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    return _client


SYSTEM_PROMPT = """Du bist Clara Bridge, ein KI-Uebersetzungsassistent fuer den Fensterbau.
Du uebersetzt E-Mails zwischen einem deutschen Handwerksbetrieb (Montagetechnik Eulen und Weischer GmbH)
und einem polnischen Fensterlieferanten (ekookna.pl).

WICHTIG:
- Uebersetze fachlich korrekt mit der bereitgestellten Terminologie
- Behalte Masse in mm bei (ausser explizit anders angegeben)
- Abkuerzungen wie FB30, VSG, RC2 bleiben in beiden Sprachen gleich
- Bei Unsicherheit: Original in [eckigen Klammern] beibehalten und als Confidence-Note markieren
- Behalte den informellen Ton bei (die Kommunikation ist per "du"/"Hi")
- Uebersetze keine Firmennamen, Adressen oder E-Mail-Signaturen
- Gib die Uebersetzung als reinen Text zurueck, keine Erklaerungen

FACHTERMINOLOGIE:
{terminology}
"""

TRANSLATION_PROMPT = """Uebersetze die folgende E-Mail von {source_lang} nach {target_lang}.

Falls Begriffe unklar sind oder nicht in der Terminologie-Liste stehen,
markiere sie mit [???BEGRIFF???] und liste sie am Ende unter "CONFIDENCE_NOTES:" auf.

E-Mail:
---
{text}
---

Antwort-Format:
TRANSLATION:
[Uebersetzter Text]

CONFIDENCE_NOTES:
[Liste unklarer Begriffe, oder "Keine" wenn alles klar]
"""


async def translate_email(text: str, subject: str = "") -> dict:
    """E-Mail uebersetzen. Erkennt Sprache automatisch und uebersetzt in die andere.

    Returns:
        {
            "translated_text": str,
            "source_language": "de" | "pl",
            "target_language": "pl" | "de",
            "confidence_notes": list[str],
        }
    """
    if not text.strip():
        return {
            "translated_text": "",
            "source_language": "unknown",
            "target_language": "unknown",
            "confidence_notes": [],
        }

    client = get_client()
    terminology = load_terminology()

    full_text = f"Betreff: {subject}\n\n{text}" if subject else text

    detection_and_translation = client.messages.create(
        model=settings.ANTHROPIC_MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT.format(terminology=terminology),
        messages=[
            {
                "role": "user",
                "content": f"""Erkenne zuerst die Sprache des folgenden Textes (DE oder PL).
Uebersetze dann in die jeweils andere Sprache.

Antworte EXAKT in diesem Format:
SOURCE_LANG: [de oder pl]
TARGET_LANG: [pl oder de]

TRANSLATION:
[Uebersetzter Text]

CONFIDENCE_NOTES:
[Unklare Begriffe oder "Keine"]

Text:
---
{full_text}
---""",
            }
        ],
    )

    response_text = detection_and_translation.content[0].text
    return parse_translation_response(response_text)


def parse_translation_response(response: str) -> dict:
    """Claude-Antwort parsen."""
    result = {
        "translated_text": "",
        "source_language": "unknown",
        "target_language": "unknown",
        "confidence_notes": [],
    }

    lines = response.strip().split("\n")
    current_section = None
    translation_lines = []
    confidence_lines = []

    for line in lines:
        line_stripped = line.strip()

        if line_stripped.startswith("SOURCE_LANG:"):
            result["source_language"] = line_stripped.split(":", 1)[1].strip().lower()
            continue
        if line_stripped.startswith("TARGET_LANG:"):
            result["target_language"] = line_stripped.split(":", 1)[1].strip().lower()
            continue
        if line_stripped == "TRANSLATION:":
            current_section = "translation"
            continue
        if line_stripped == "CONFIDENCE_NOTES:":
            current_section = "confidence"
            continue

        if current_section == "translation":
            translation_lines.append(line)
        elif current_section == "confidence":
            if line_stripped and line_stripped.lower() != "keine":
                confidence_lines.append(line_stripped)

    result["translated_text"] = "\n".join(translation_lines).strip()
    result["confidence_notes"] = confidence_lines

    return result
