"""
Konfiguration via Environment Variables.
Lokal: .env Datei, Railway: Service Variables.
"""

import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    # --- Server ---
    PORT: int = int(os.getenv("PORT", "8000"))

    # --- Database ---
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@localhost:5432/clara_bridge",
    )

    # --- Gmail API ---
    GMAIL_CREDENTIALS_JSON: str = os.getenv("GMAIL_CREDENTIALS_JSON", "")
    GMAIL_TOKEN_JSON: str = os.getenv("GMAIL_TOKEN_JSON", "")
    GMAIL_ADDRESS: str = os.getenv("GMAIL_ADDRESS", "frank.eulen.weischer@gmail.com")
    POLL_INTERVAL_SECONDS: int = int(os.getenv("POLL_INTERVAL_SECONDS", "300"))

    # --- Anthropic ---
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

    # --- Telegram ---
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID", "")

    # --- Supplier (Pilot: ekookna) ---
    SUPPLIER_EMAIL: str = os.getenv("SUPPLIER_EMAIL", "judyta.klima@ekookna.pl")
    SUPPLIER_NAME: str = os.getenv("SUPPLIER_NAME", "Judyta Klima")

    # --- E&W ---
    EW_EMAIL: str = os.getenv("EW_EMAIL", "info@eulen-weischer.de")
    EW_NAME: str = os.getenv("EW_NAME", "Tilmann Weischer")


settings = Settings()
