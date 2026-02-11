from datetime import datetime
from enum import Enum

from pydantic import BaseModel, EmailStr, Field


class UserRoleSchema(str, Enum):
    admin = "admin"
    manager = "manager"
    rep = "rep"


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)


class UserCreate(BaseModel):
    organization_id: str
    email: EmailStr
    full_name: str
    password: str = Field(min_length=8)
    role: UserRoleSchema = UserRoleSchema.rep


class UserRead(BaseModel):
    id: str
    organization_id: str
    email: EmailStr
    full_name: str
    role: UserRoleSchema


class CallRead(BaseModel):
    id: str
    file_name: str
    status: str
    transcript: str | None
    created_at: datetime


class AnalysisRead(BaseModel):
    call_id: str
    executive_summary: str
    sentiment_score: float
    buying_intent_score: float
    objections: list[str]
    action_items: list[dict[str, str]]
