"""
Clara Bridge - KI-Beschaffungsassistent
FastAPI Server fuer E-Mail Relay + Uebersetzung DE<>PL
"""

import asyncio
import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request

from backend.database import init_db
from backend.config import settings
from backend.email_service import poll_inbox
from backend.telegram_service import setup_telegram, handle_callback

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
)
logger = logging.getLogger("bridge")


async def polling_loop():
    """Gmail Inbox Polling alle 5 Minuten."""
    while True:
        try:
            await poll_inbox()
        except Exception as e:
            logger.error(f"Polling error: {e}")
        await asyncio.sleep(settings.POLL_INTERVAL_SECONDS)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Clara Bridge starting...")
    await init_db()
    await setup_telegram()
    polling_task = asyncio.create_task(polling_loop())
    logger.info("Clara Bridge ready. Polling active.")
    yield
    polling_task.cancel()
    logger.info("Clara Bridge shutting down.")


app = FastAPI(
    title="Clara Bridge",
    description="KI-Beschaffungsassistent - E-Mail Relay + Uebersetzung DE<>PL",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "clara-bridge"}


@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """Telegram Callback Queries empfangen (Button-Klicks von Till)."""
    body = await request.json()

    if "callback_query" in body:
        callback = body["callback_query"]
        callback_data = callback.get("data", "")
        callback_id = callback.get("id", "")

        result = await handle_callback(callback_data)

        async with httpx.AsyncClient() as client:
            await client.post(
                f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/answerCallbackQuery",
                json={"callback_query_id": callback_id},
            )

        return result

    return {"status": "ok"}


@app.get("/projects")
async def list_projects():
    """Phase 1: Einfache Projektliste (spaeter Dashboard)."""
    from backend.database import get_session
    from backend.models import Project
    from sqlalchemy import select

    async with get_session() as session:
        result = await session.execute(select(Project).order_by(Project.created_at.desc()))
        projects = result.scalars().all()
        return [
            {
                "id": p.id,
                "name": p.name,
                "status": p.status,
                "created_at": p.created_at.isoformat() if p.created_at else None,
            }
            for p in projects
        ]
