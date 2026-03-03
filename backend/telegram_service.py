"""
Telegram-Service: Notifications + Draft-Freigabe via Inline Keyboard.
Shared Bot mit Clara Voice — Bridge-Messages mit Prefix "[Bridge]".
"""

import json
import logging
from datetime import datetime

import httpx

from backend.config import settings

logger = logging.getLogger("bridge.telegram")

TELEGRAM_API = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}"

_webhook_active = False


async def setup_telegram():
    """Telegram Webhook einrichten fuer Callback-Handling."""
    if not settings.TELEGRAM_BOT_TOKEN:
        logger.warning("TELEGRAM_BOT_TOKEN not set. Telegram disabled.")
        return
    logger.info("Telegram service initialized.")


async def send_message(text: str, reply_markup: dict = None):
    """Telegram-Nachricht senden."""
    if not settings.TELEGRAM_BOT_TOKEN or not settings.TELEGRAM_CHAT_ID:
        logger.warning("Telegram not configured. Message not sent.")
        return None

    payload = {
        "chat_id": settings.TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{TELEGRAM_API}/sendMessage", json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Telegram send failed: {response.text}")
            return None


async def send_translation_preview(
    email_id: int,
    project_name: str,
    from_addr: str,
    subject: str,
    original_text: str,
    translated_text: str,
    confidence_notes: list[str],
    draft_id: str,
):
    """Uebersetzungs-Preview mit Freigabe-Buttons an Till senden."""
    confidence_warning = ""
    if confidence_notes:
        notes_text = "\n".join(f"  • {n}" for n in confidence_notes)
        confidence_warning = f"\n⚠️ <b>Unklare Begriffe:</b>\n{notes_text}\n"

    original_preview = original_text[:300]
    if len(original_text) > 300:
        original_preview += "..."

    translated_preview = translated_text[:400]
    if len(translated_text) > 400:
        translated_preview += "..."

    text = f"""🌉 <b>[Bridge] Neue Uebersetzung</b>

📁 <b>Projekt:</b> {project_name}
📧 <b>Von:</b> {from_addr}
📋 <b>Betreff:</b> {subject}

📝 <b>Original:</b>
<i>{original_preview}</i>

🔄 <b>Uebersetzung:</b>
{translated_preview}
{confidence_warning}
⏳ Warte auf Freigabe..."""

    reply_markup = {
        "inline_keyboard": [
            [
                {
                    "text": "✅ Freigeben",
                    "callback_data": json.dumps(
                        {"action": "approve", "email_id": email_id, "draft_id": draft_id}
                    ),
                },
                {
                    "text": "❌ Ablehnen",
                    "callback_data": json.dumps(
                        {"action": "reject", "email_id": email_id, "draft_id": draft_id}
                    ),
                },
            ]
        ]
    }

    await send_message(text, reply_markup)


async def send_confirmation(action: str, project_name: str, to_addr: str):
    """Bestaetigungsnachricht nach Freigabe/Ablehnung."""
    if action == "approve":
        text = f"🌉 ✅ <b>[Bridge] Gesendet!</b>\n📁 {project_name}\n📧 An: {to_addr}"
    else:
        text = f"🌉 ❌ <b>[Bridge] Abgelehnt.</b>\n📁 {project_name}\nDraft wurde geloescht."

    await send_message(text)


async def send_project_assignment_request(
    email_id: int, from_addr: str, subject: str, projects: list
):
    """Manuelle Projekt-Zuordnung anfordern (Fallback)."""
    text = f"""🌉 ❓ <b>[Bridge] Projekt-Zuordnung</b>

📧 Neue Mail von: {from_addr}
📋 Betreff: {subject}

Welchem Projekt zuordnen?"""

    buttons = []
    for p in projects[:4]:
        buttons.append([{
            "text": p.name[:40],
            "callback_data": json.dumps(
                {"action": "assign", "email_id": email_id, "project_id": p.id}
            ),
        }])
    buttons.append([{
        "text": "➕ Neues Projekt",
        "callback_data": json.dumps({"action": "new_project", "email_id": email_id}),
    }])

    reply_markup = {"inline_keyboard": buttons}
    await send_message(text, reply_markup)


async def handle_callback(callback_data: str) -> dict:
    """Telegram Callback Query verarbeiten.
    Wird vom FastAPI Webhook-Endpoint aufgerufen.
    """
    data = json.loads(callback_data)
    action = data.get("action")

    if action == "approve":
        return await handle_approve(data["email_id"], data["draft_id"])
    elif action == "reject":
        return await handle_reject(data["email_id"], data["draft_id"])
    elif action == "assign":
        return await handle_assign(data["email_id"], data["project_id"])
    else:
        logger.warning(f"Unknown callback action: {action}")
        return {"status": "unknown_action"}


async def handle_approve(email_id: int, draft_id: str) -> dict:
    """Draft freigeben und senden."""
    from backend.email_service import send_draft
    from backend.database import get_session
    from backend.models import Email, EmailStatus
    from sqlalchemy import update

    success = await send_draft(draft_id)

    if success:
        async with get_session() as session:
            await session.execute(
                update(Email)
                .where(Email.id == email_id)
                .values(status=EmailStatus.SENT, sent_at=datetime.utcnow())
            )
        return {"status": "sent"}
    else:
        return {"status": "send_failed"}


async def handle_reject(email_id: int, draft_id: str) -> dict:
    """Draft ablehnen und loeschen."""
    from backend.email_service import delete_draft
    from backend.database import get_session
    from backend.models import Email, EmailStatus
    from sqlalchemy import update

    await delete_draft(draft_id)

    async with get_session() as session:
        await session.execute(
            update(Email)
            .where(Email.id == email_id)
            .values(status=EmailStatus.REJECTED)
        )

    return {"status": "rejected"}


async def handle_assign(email_id: int, project_id: int) -> dict:
    """E-Mail manuell einem Projekt zuordnen."""
    from backend.database import get_session
    from backend.models import Email
    from sqlalchemy import update

    async with get_session() as session:
        await session.execute(
            update(Email).where(Email.id == email_id).values(project_id=project_id)
        )

    return {"status": "assigned", "project_id": project_id}
