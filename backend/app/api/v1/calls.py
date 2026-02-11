from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.db.session import get_db
from app.models.entities import Call, CallStatus, User
from app.schemas.calls import CallOut
from app.services.analysis import AnalysisService
from app.services.dependencies import get_current_user
from app.services.transcription import TranscriptionService

router = APIRouter(prefix='/calls', tags=['calls'])


@router.get('', response_model=list[CallOut])
async def list_calls(
    current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)
) -> list[CallOut]:
    result = await db.execute(
        select(Call)
        .where(Call.organization_id == current_user.organization_id)
        .order_by(Call.created_at.desc())
    )
    return [CallOut.model_validate(item) for item in result.scalars().all()]


@router.post('/upload', response_model=CallOut)
async def upload_call(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallOut:
    settings = get_settings()
    content = await file.read()
    max_size = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail='File exceeds maximum upload size')

    storage_dir = Path(settings.storage_path)
    storage_dir.mkdir(parents=True, exist_ok=True)
    file_path = storage_dir / f'{current_user.organization_id}_{file.filename}'
    with file_path.open('wb') as handle:
        handle.write(content)

    call = Call(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        file_name=file.filename,
        file_path=str(file_path),
        status=CallStatus.UPLOADED,
    )
    db.add(call)
    await db.flush()

    transcript = await TranscriptionService.transcribe(str(file_path))
    analysis = AnalysisService.analyze(transcript)
    call.transcript = transcript
    call.analysis = analysis
    call.status = CallStatus.ANALYZED

    await db.commit()
    await db.refresh(call)
    return CallOut.model_validate(call)


@router.get('/{call_id}', response_model=CallOut)
async def get_call(
    call_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> CallOut:
    result = await db.execute(
        select(Call).where(
            Call.id == call_id, Call.organization_id == current_user.organization_id
        )
    )
    call = result.scalar_one_or_none()
    if not call:
        raise HTTPException(status_code=404, detail='Call not found')
    return CallOut.model_validate(call)
