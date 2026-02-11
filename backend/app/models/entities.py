from __future__ import annotations

from datetime import datetime
from enum import Enum as PyEnum
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, DateTime, Enum as SAEnum, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class UserRole(str, PyEnum):
    admin = "admin"
    manager = "manager"
    rep = "rep"


class CallStatus(str, PyEnum):
    uploaded = "uploaded"
    transcribed = "transcribed"
    analyzed = "analyzed"
    failed = "failed"


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    subscription_tier: Mapped[str] = mapped_column(String(30), default="professional")
    settings: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    users: Mapped[list[User]] = relationship(back_populates="organization")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(200))
    role: Mapped[UserRole] = mapped_column(SAEnum(UserRole), default=UserRole.rep)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    organization: Mapped[Organization] = relationship(back_populates="users")


class Call(Base):
    __tablename__ = "calls"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    organization_id: Mapped[str] = mapped_column(ForeignKey("organizations.id"), index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), index=True)
    file_name: Mapped[str] = mapped_column(String(255))
    storage_url: Mapped[str] = mapped_column(String(500))
    transcript: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[CallStatus] = mapped_column(SAEnum(CallStatus), default=CallStatus.uploaded)
    talk_ratio_rep: Mapped[float] = mapped_column(Float, default=0.0)
    talk_ratio_prospect: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class CallAnalysis(Base):
    __tablename__ = "call_analysis"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    call_id: Mapped[str] = mapped_column(ForeignKey("calls.id"), unique=True, index=True)
    executive_summary: Mapped[str] = mapped_column(Text)
    sentiment_score: Mapped[float] = mapped_column(Float)
    buying_intent_score: Mapped[float] = mapped_column(Float)
    objections: Mapped[list[str]] = mapped_column(JSON, default=list)
    action_items: Mapped[list[dict[str, str]]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
