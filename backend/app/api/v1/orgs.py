from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import Organization
from app.schemas.core import OrganizationCreate

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.post("")
async def create_org(payload: OrganizationCreate, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Organization).where(Organization.name == payload.name))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Organization already exists")
    org = Organization(name=payload.name)
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return {"id": org.id, "name": org.name, "subscription_tier": org.subscription_tier}
