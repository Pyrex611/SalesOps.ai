from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.session import get_db
from app.models.entities import Organization, Role, User
from app.schemas.auth import TokenResponse, UserLogin, UserRegister
from app.schemas.users import UserOut
from app.services.dependencies import get_current_user

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)) -> UserOut:
    existing = await db.execute(select(User).where(User.email == payload.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail='Email already registered')

    org = Organization(name=payload.organization_name)
    db.add(org)
    await db.flush()

    user = User(
        organization_id=org.id,
        email=payload.email,
        full_name=payload.full_name,
        role=Role.ADMIN,
        hashed_password=get_password_hash(payload.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return UserOut.model_validate(user)


@router.post('/login', response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)) -> TokenResponse:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    token = create_access_token(user.email)
    return TokenResponse(access_token=token)


@router.get('/me', response_model=UserOut)
async def me(user: User = Depends(get_current_user)) -> UserOut:
    return UserOut.model_validate(user)
