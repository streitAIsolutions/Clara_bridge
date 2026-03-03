"""
Gmail API Service - Inbound Polling, Draft-Erstellung, Senden.
Phase 1: Polling alle 5 Min, Drafts erstellen, nach Freigabe senden.
"""

import base64
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from backend.config import settings
from backend.database import get_session
from backend.models import Email, EmailDirection, EmailStatus
from backend.translation_service import translate_email
from backend.project_service import assign_project
from backend.telegram_service import send_translation_preview

logger = logging.getLogger("bridge.email")

_service = None


def get_gmail_service():
    """Gmail API Service initialisieren."""
    global _service
    if _service is not None:
        return _service

    if not settings.GMAIL_TOKEN_JSON:
        logger.warning("GMAIL_TOKEN_JSON not set. Gmail disabled.")
        return None

    token_data = json.loads(settings.GMAIL_TOKEN_JSON)
    creds = Credentials.from_authorized_user_info(token_data)
    _service = build("gmail", "v1", credentials=creds)
    logger.info("Gmail API service initialized.")
    return _service


async def poll_inbox():
    """Neue E-Mails abholen und verarbeiten."""
    service = get_gmail_service()
    if not service:
        return

    try:
        results = service.users().messages().list(
            userId="me",
            q="is:unread -from:me",
            maxResults=10,
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            return

        logger.info(f"Found {len(messages)} new messages.")

        for msg_meta in messages:
            msg_id = msg_meta["id"]
            await process_inbound_message(service, msg_id)

    except Exception as e:
        logger.error(f"Gmail polling error: {e}")
        raise


async def process_inbound_message(service, msg_id: str):
    """Einzelne eingehende Mail verarbeiten."""
    async with get_session() as session:
        from sqlalchemy import select

        existing = await session.execute(
            select(Email).where(Email.gmail_message_id == msg_id)
        )
        if existing.scalar_one_or_none():
            return

    msg = service.users().messages().get(
        userId="me", id=msg_id, format="full"
    ).execute()

    headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
    thread_id = msg.get("threadId", "")
    from_addr = headers.get("From", "")
    to_addr = headers.get("To", "")
    subject = headers.get("Subject", "")

    body = extract_body(msg["payload"])
    attachments = extract_attachment_info(msg["payload"], msg_id)

    logger.info(f"Processing: {subject} (from: {from_addr})")

    project = await assign_project(thread_id=thread_id, subject=subject, from_addr=from_addr)

    translation_result = await translate_email(body, subject)

    async with get_session() as session:
        email_record = Email(
            project_id=project.id if project else None,
            direction=EmailDirection.INBOUND,
            from_addr=from_addr,
            to_addr=to_addr,
            subject=subject,
            body_original=body,
            body_translated=translation_result["translated_text"],
            original_language=translation_result["source_language"],
            translated_language=translation_result["target_language"],
            attachments=attachments,
            gmail_thread_id=thread_id,
            gmail_message_id=msg_id,
            status=EmailStatus.RECEIVED,
        )
        session.add(email_record)
        await session.flush()
        email_id = email_record.id

    draft_id = await create_draft(
        to_addr=determine_recipient(from_addr),
        subject=build_reply_subject(subject),
        body=translation_result["translated_text"],
        thread_id=thread_id,
        original_attachments=attachments,
        msg_id=msg_id,
        service=service,
    )

    async with get_session() as session:
        from sqlalchemy import update

        await session.execute(
            update(Email)
            .where(Email.id == email_id)
            .values(gmail_draft_id=draft_id, status=EmailStatus.DRAFT)
        )

    await send_translation_preview(
        email_id=email_id,
        project_name=project.name if project else "Unbekannt",
        from_addr=from_addr,
        subject=subject,
        original_text=body[:500],
        translated_text=translation_result["translated_text"][:500],
        confidence_notes=translation_result.get("confidence_notes", []),
        draft_id=draft_id,
    )

    service.users().messages().modify(
        userId="me",
        id=msg_id,
        body={"removeLabelIds": ["UNREAD"]},
    ).execute()

    logger.info(f"Processed mail {msg_id}. Draft created: {draft_id}")


def extract_body(payload) -> str:
    """E-Mail Body extrahieren (text/plain bevorzugt)."""
    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain" and "data" in part.get("body", {}):
                return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8")
            if "parts" in part:
                result = extract_body(part)
                if result:
                    return result
    elif "body" in payload and "data" in payload["body"]:
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8")
    return ""


def extract_attachment_info(payload, msg_id: str) -> list:
    """Attachment-Metadaten extrahieren (Phase 1: nur Info, kein Download)."""
    attachments = []
    if "parts" not in payload:
        return attachments

    for part in payload["parts"]:
        if part.get("filename") and part["filename"] != "":
            attachments.append({
                "filename": part["filename"],
                "mime_type": part.get("mimeType", ""),
                "size": part.get("body", {}).get("size", 0),
                "attachment_id": part.get("body", {}).get("attachmentId", ""),
                "gmail_message_id": msg_id,
            })
    return attachments


def determine_recipient(from_addr: str) -> str:
    """Empfaenger bestimmen basierend auf Absender.
    Phase 1: Alles ueber E&W.
    - Mail von Judyta/ekookna → Draft an E&W
    - Mail von E&W/sonstige → Draft an Judyta
    """
    if "ekookna" in from_addr.lower():
        return settings.EW_EMAIL
    return settings.SUPPLIER_EMAIL


def build_reply_subject(subject: str) -> str:
    """Reply-Subject bauen."""
    if subject.lower().startswith(("re:", "aw:", "odp:")):
        return subject
    return f"Re: {subject}"


async def create_draft(
    to_addr: str,
    subject: str,
    body: str,
    thread_id: str,
    original_attachments: list,
    msg_id: str,
    service,
) -> str:
    """Gmail Draft erstellen mit uebersetztem Text + Original-Attachments."""
    message = MIMEMultipart()
    message["to"] = to_addr
    message["subject"] = subject

    message.attach(MIMEText(body, "plain", "utf-8"))

    if original_attachments:
        for att in original_attachments:
            try:
                att_data = service.users().messages().attachments().get(
                    userId="me",
                    messageId=att["gmail_message_id"],
                    id=att["attachment_id"],
                ).execute()

                file_data = base64.urlsafe_b64decode(att_data["data"])
                part = MIMEBase("application", "octet-stream")
                part.set_payload(file_data)
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f'attachment; filename="{att["filename"]}"',
                )
                message.attach(part)
            except Exception as e:
                logger.warning(f"Could not attach {att['filename']}: {e}")

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")

    draft_body = {"message": {"raw": raw, "threadId": thread_id}}
    draft = service.users().drafts().create(userId="me", body=draft_body).execute()

    return draft["id"]


async def send_draft(draft_id: str) -> bool:
    """Freigegebenen Draft senden."""
    service = get_gmail_service()
    if not service:
        return False

    try:
        service.users().drafts().send(
            userId="me",
            body={"id": draft_id},
        ).execute()
        logger.info(f"Draft {draft_id} sent successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to send draft {draft_id}: {e}")
        return False


async def delete_draft(draft_id: str) -> bool:
    """Abgelehnten Draft loeschen."""
    service = get_gmail_service()
    if not service:
        return False

    try:
        service.users().drafts().delete(userId="me", id=draft_id).execute()
        logger.info(f"Draft {draft_id} deleted.")
        return True
    except Exception as e:
        logger.error(f"Failed to delete draft {draft_id}: {e}")
        return False
