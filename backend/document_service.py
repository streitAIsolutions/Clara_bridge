"""
Dokument-Service: PDF-Parsing, Anforderungs-Extraktion.
Phase 2 - Stub.
"""

import logging

logger = logging.getLogger("bridge.document")


async def parse_window_list(pdf_path: str) -> list:
    """Phase 2: Fensterliste aus PDF extrahieren."""
    raise NotImplementedError("Phase 2: PDF-Parsing noch nicht implementiert")


async def extract_drawings(pdf_path: str) -> list:
    """Phase 2: Zeichnungen aus PDF extrahieren."""
    raise NotImplementedError("Phase 2: Zeichnungs-Extraktion noch nicht implementiert")
