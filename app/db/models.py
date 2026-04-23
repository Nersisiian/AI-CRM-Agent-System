import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    company = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    leads = relationship("Lead", back_populates="customer")
    deals = relationship("Deal", back_populates="customer")

class Lead(Base):
    __tablename__ = "leads"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    source = Column(String(100))
    status = Column(String(50), default="new")
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="leads")

class Deal(Base):
    __tablename__ = "deals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column(UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False)
    amount = Column(Float, nullable=False)
    stage = Column(String(50), default="qualification")
    closed_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="deals")