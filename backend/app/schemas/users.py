from datetime import datetime

from pydantic import BaseModel, EmailStr

from app.models.entities import Role


class UserOut(BaseModel):
    id: int
    organization_id: int
    email: EmailStr
    full_name: str
    role: Role
    is_active: bool
    created_at: datetime

    model_config = {'from_attributes': True}
