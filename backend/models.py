"""
Datenmodell - SQLAlchemy ORM.
Phase 1: suppliers, projects, emails
Spaetere Phasen: requirements, supplier_offers, validations, ew_calculations
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    Enum,
    JSON,
)
from sqlalchemy.orm import DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


# --- Enums ---


class ProjectStatus(str, enum.Enum):
    RECEIVED = "RECEIVED"
    SENT_TO_SUPPLIER = "SENT_TO_SUPPLIER"
    IN_REVISION = "IN_REVISION"
    OFFER_RECEIVED = "OFFER_RECEIVED"
    OFFER_VALIDATED = "OFFER_VALIDATED"
    EW_OFFER_DRAFTED = "EW_OFFER_DRAFTED"
    EW_OFFER_SENT = "EW_OFFER_SENT"
    COMPLETED = "COMPLETED"


class EmailStatus(str, enum.Enum):
    RECEIVED = "RECEIVED"
    DRAFT = "DRAFT"
    APPROVED_BY_EW = "APPROVED_BY_EW"
    SENT = "SENT"
    REJECTED = "REJECTED"


class EmailDirection(str, enum.Enum):
    INBOUND = "INBOUND"
    OUTBOUND = "OUTBOUND"


# --- Phase 1 Tabellen ---


class Supplier(Base):
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    contact_name = Column(String(200))
    email = Column(String(200), nullable=False)
    language = Column(String(10), default="pl")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    projects = relationship("Project", back_populates="supplier")


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String(300), nullable=False)
    architect_name = Column(String(200))
    architect_email = Column(String(200))
    supplier_id = Column(Integer, ForeignKey("suppliers.id"))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.RECEIVED)
    property_address = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    supplier = relationship("Supplier", back_populates="projects")
    emails = relationship("Email", back_populates="project")


class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    direction = Column(Enum(EmailDirection), nullable=False)
    from_addr = Column(String(200))
    to_addr = Column(String(200))
    subject = Column(String(500))
    body_original = Column(Text)
    body_translated = Column(Text)
    original_language = Column(String(10))
    translated_language = Column(String(10))
    attachments = Column(JSON, default=list)
    gmail_thread_id = Column(String(100))
    gmail_message_id = Column(String(100), unique=True)
    gmail_draft_id = Column(String(100))
    status = Column(Enum(EmailStatus), default=EmailStatus.RECEIVED)
    sent_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="emails")


# --- Phase 2+ Tabellen (Stubs, werden spaeter aktiviert) ---


class Requirement(Base):
    """Phase 2: Extrahierte Anforderungen aus Architekten-PDF."""

    __tablename__ = "requirements"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    position = Column(String(20))
    room = Column(String(100))
    qty = Column(Integer, default=1)
    width = Column(Float)
    height = Column(Float)
    opening_direction = Column(String(50))
    brh = Column(Float)
    wall_thickness = Column(Float)
    u_value = Column(Float)
    security_class = Column(String(20))
    glazing_type = Column(String(50))
    frame_color_inside = Column(String(100))
    frame_color_outside = Column(String(100))
    window_sill_depth = Column(Float)
    roller_shutter_type = Column(String(100))
    special_notes = Column(Text)
    drawing_image_path = Column(String(500))


class SupplierOffer(Base):
    """Phase 3: Angebote vom Lieferanten."""

    __tablename__ = "supplier_offers"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    version = Column(Integer, default=1)
    position = Column(String(20))
    offered_u_value = Column(Float)
    offered_security_class = Column(String(20))
    offered_glazing = Column(String(50))
    unit_price = Column(Float)
    total_price = Column(Float)
    raw_pdf_path = Column(String(500))


class Validation(Base):
    """Phase 3: Abgleich Anforderung vs. Angebot."""

    __tablename__ = "validations"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    offer_version = Column(Integer)
    position = Column(String(20))
    field_name = Column(String(100))
    required_value = Column(String(200))
    offered_value = Column(String(200))
    status = Column(String(20), default="UNCHECKED")
    confidence_score = Column(Float)


class EWCalculation(Base):
    """Phase 4: E&W-Aufschlag pro Position."""

    __tablename__ = "ew_calculations"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    position = Column(String(20))
    supplier_price = Column(Float)
    markup_percent = Column(Float)
    markup_fixed = Column(Float)
    labor_hours = Column(Float)
    labor_rate = Column(Float)
    total_ew_price = Column(Float)


class CalculationTemplate(Base):
    """Phase 4: Wiederverwendbare Kalkulationsregeln."""

    __tablename__ = "calculation_templates"

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    is_default = Column(Boolean, default=False)
    default_markup_percent = Column(Float)
    default_labor_rate_per_hour = Column(Float)
    labor_hours_per_window_type = Column(JSON)
    travel_cost_flat = Column(Float)
