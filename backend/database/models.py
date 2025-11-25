#Defining Tables inside database
import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, TIMESTAMP, Float, Boolean,
    ForeignKey, func
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship, declarative_base
from pgvector.sqlalchemy import Vector

Base = declarative_base()

# Sessions Table
class SessionModel(Base):
    __tablename__ = "sessions"

    session_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    current_sector = Column(String, nullable=False)
    summary_text = Column(Text, default="")
    summary_last_updated_at = Column(TIMESTAMP(timezone=True))
    missing_fields = Column(JSONB, default=list)
    sector_completion = Column(Boolean)
    company_profile = Column(JSONB, default={})
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationships -> Won't have to write JOINS manually
    qa_messages = relationship("QAMessage", back_populates="session", cascade="all, delete-orphan")
    structured_fields = relationship("StructuredField", back_populates="session", cascade="all, delete-orphan")
    emissions = relationship("EmissionsSnapshot", back_populates="session", cascade="all, delete-orphan")
    vectors = relationship("VectorMemory", back_populates="session", cascade="all, delete-orphan")

# QA Messages Table
class QAMessage(Base):
    __tablename__ = "qa_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)

    sector = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    answer_text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="qa_messages")

# Structured Fields
class StructuredField(Base):
    __tablename__ = "structured_fields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)

    sector = Column(String, nullable=False)
    entity_id = Column(String, nullable=False)
    field_name = Column(String, nullable=False)
    field_value_float = Column(Float)
    field_value_text = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="structured_fields")

# Emissions Snapshots Table
class EmissionsSnapshot(Base):
    __tablename__ = "emissions_snapshots"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)

    sector = Column(String, nullable=False)
    raw_emissions = Column(JSONB, default={})
    steps = Column(Text, nullable=False)
    missing_fields = Column(JSONB, default=list)
    confidence_model = Column(Float)
    confidence_data = Column(Float)
    confidence_final = Column(Float)
    calculation_valid = Column(Boolean)
    top_sources = Column(JSONB, default=list)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="emissions")

# Vector Memory Table
class VectorMemory(Base):
    __tablename__ = "vector_memory"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("sessions.session_id", ondelete="CASCADE"), nullable=False)

    content = Column(Text, nullable=False)
    sector = Column(String, nullable=False)
    embedding = Column(Vector(1536), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    session = relationship("SessionModel", back_populates="vectors")