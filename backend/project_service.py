"""
Projekt-Service: Zuordnung, Anlage, Status-Management.
Thread-Zuordnung: 3-stufig (Gmail Thread-ID → Subject-Parsing → Telegram Fallback).
"""

import re
import logging

from sqlalchemy import select

from backend.database import get_session
from backend.models import Project, Email, ProjectStatus

logger = logging.getLogger("bridge.project")


async def assign_project(
    thread_id: str, subject: str, from_addr: str
) -> Project | None:
    """Projekt zuordnen. 3-stufig:
    1. Gmail Thread-ID: Gibt es bereits eine Mail mit dieser Thread-ID?
    2. Subject-Parsing: Kommission oder Adresse im Betreff?
    3. Fallback: None (wird via Telegram manuell zugeordnet)
    """
    project = await match_by_thread_id(thread_id)
    if project:
        logger.info(f"Project matched by thread_id: {project.name}")
        return project

    project = await match_by_subject(subject)
    if project:
        logger.info(f"Project matched by subject: {project.name}")
        return project

    project = await create_from_subject(subject, from_addr)
    if project:
        logger.info(f"New project created: {project.name}")
        return project

    logger.warning(f"Could not assign project for: {subject}")
    return None


async def match_by_thread_id(thread_id: str) -> Project | None:
    """Stufe 1: Projekt ueber Gmail Thread-ID finden."""
    if not thread_id:
        return None

    async with get_session() as session:
        result = await session.execute(
            select(Email.project_id)
            .where(Email.gmail_thread_id == thread_id)
            .where(Email.project_id.isnot(None))
            .limit(1)
        )
        row = result.first()
        if row and row[0]:
            project = await session.get(Project, row[0])
            return project
    return None


async def match_by_subject(subject: str) -> Project | None:
    """Stufe 2: Projekt ueber Betreff-Parsing finden.

    Sucht nach:
    - Kommissionsnamen: "Kom. Kern", "Kommission Polter"
    - Adressen: "Bellerstraße 31", "Bellerstr"
    """
    if not subject:
        return None

    keywords = extract_project_keywords(subject)
    if not keywords:
        return None

    async with get_session() as session:
        result = await session.execute(
            select(Project).order_by(Project.created_at.desc())
        )
        projects = result.scalars().all()

        for project in projects:
            project_name_lower = project.name.lower()
            address_lower = (project.property_address or "").lower()

            for keyword in keywords:
                if keyword in project_name_lower or keyword in address_lower:
                    return project

    return None


def extract_project_keywords(subject: str) -> list[str]:
    """Schluesselwoerter aus Betreff extrahieren.

    Patterns:
    - "Kom. NAME" / "Kommission NAME"
    - Strassennamen mit Hausnummer
    - "Angebot - ADRESSE"
    """
    keywords = []
    subject_lower = subject.lower()

    kom_patterns = [
        r"kom\.\s*(\w+)",
        r"kommission\s*(\w+)",
    ]
    for pattern in kom_patterns:
        match = re.search(pattern, subject_lower)
        if match:
            keywords.append(match.group(1))

    address_pattern = r"(\w+(?:stra[sß]e|str\.?)\s*\d+)"
    match = re.search(address_pattern, subject_lower)
    if match:
        keywords.append(match.group(1))

    return keywords


async def create_from_subject(subject: str, from_addr: str) -> Project | None:
    """Neues Projekt aus Betreff erstellen wenn moeglich."""
    keywords = extract_project_keywords(subject)
    if not keywords:
        return None

    name_parts = []
    address = ""

    for kw in keywords:
        if "str" in kw or "stra" in kw:
            address = kw
        else:
            name_parts.append(f"Kom. {kw.capitalize()}")

    if address and not name_parts:
        name_parts.append(address.capitalize())

    project_name = " - ".join(name_parts) if name_parts else f"Projekt ({subject[:50]})"
    if address and address not in project_name.lower():
        project_name += f" - {address}"

    architect_name = ""
    architect_email = ""
    if "ekookna" not in from_addr.lower() and "eulen" not in from_addr.lower():
        architect_email = from_addr

    async with get_session() as session:
        project = Project(
            name=project_name,
            architect_email=architect_email,
            property_address=address,
            status=ProjectStatus.RECEIVED,
        )
        session.add(project)
        await session.flush()
        return project
