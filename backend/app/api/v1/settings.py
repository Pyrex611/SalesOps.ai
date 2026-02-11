from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.entities import Organization, Role, User
from app.schemas.settings import TemplatesOut, TemplatesUpdate
from app.services.dependencies import get_current_user

router = APIRouter(prefix='/settings', tags=['settings'])


def _ensure_manager_or_admin(user: User) -> None:
    if user.role not in {Role.MANAGER, Role.ADMIN}:
        raise HTTPException(status_code=403, detail='Manager or admin role required')


@router.get('/templates', response_model=TemplatesOut)
async def get_templates(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> TemplatesOut:
    _ensure_manager_or_admin(current_user)

    result = await db.execute(
        select(Organization).where(Organization.id == current_user.organization_id)
    )
    org = result.scalar_one()
    settings = org.settings or {}

    return TemplatesOut(
        crm_field_mapping=settings.get('crm_field_mapping', {}),
        call_analysis_template=settings.get('call_analysis_template', {}),
    )


@router.put('/templates', response_model=TemplatesOut)
async def update_templates(
    payload: TemplatesUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> TemplatesOut:
    _ensure_manager_or_admin(current_user)

    result = await db.execute(
        select(Organization).where(Organization.id == current_user.organization_id)
    )
    org = result.scalar_one()

    settings = dict(org.settings or {})
    settings['crm_field_mapping'] = payload.crm_field_mapping
    settings['call_analysis_template'] = payload.call_analysis_template
    org.settings = settings

    await db.commit()
    await db.refresh(org)

    return TemplatesOut(
        crm_field_mapping=org.settings.get('crm_field_mapping', {}),
        call_analysis_template=org.settings.get('call_analysis_template', {}),
    )
