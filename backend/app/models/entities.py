from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(str, Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    REP = 'rep'


class CallStatus(str, Enum):
    UPLOADED = 'uploaded'
    TRANSCRIBED = 'transcribed'
    ANALYZED = 'analyzed'
    FAILED = 'failed'


class Organization(Base):
    __tablename__ = 'organizations'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    subscription_tier: Mapped[str] = mapped_column(String(50), default='professional', nullable=False)
    settings: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    users: Mapped[list['User']] = relationship(back_populates='organization')


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'), nullable=False)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(SAEnum(Role), nullable=False, default=Role.REP)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    organization: Mapped['Organization'] = relationship(back_populates='users')
    calls: Mapped[list['Call']] = relationship(back_populates='owner')


class Call(Base):
    __tablename__ = 'calls'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1024), nullable=False)
    transcript: Mapped[str] = mapped_column(Text, default='', nullable=False)
    status: Mapped[CallStatus] = mapped_column(SAEnum(CallStatus), default=CallStatus.UPLOADED, nullable=False)
    analysis: Mapped[dict] = mapped_column(JSON, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    owner: Mapped['User'] = relationship(back_populates='calls')
