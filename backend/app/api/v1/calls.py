from pathlib import Path

from fastapi import APIRouter, BackgroundTasks, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.session import AsyncSessionLocal, get_db
from app.models.entities import Call, CallAnalysis, User
from app.schemas.core import AnalysisRead, CallRead
from app.services.call_pipeline import CallPipelineService

router = APIRouter(prefix="/calls", tags=["calls"])
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def run_pipeline(call_id: str) -> None:
    async with AsyncSessionLocal() as db:
        service = CallPipelineService()
        await service.process_call(db, call_id)


@router.post("/upload", response_model=CallRead)
async def upload_call(
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    file: UploadFile = File(...),
) -> CallRead:
    if file.content_type not in {"audio/mpeg", "audio/wav", "audio/mp4", "video/mp4"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported media type")

    destination = UPLOAD_DIR / file.filename
    with destination.open("wb") as out:
        out.write(await file.read())

    call = Call(
        organization_id=current_user.organization_id,
        user_id=current_user.id,
        file_name=file.filename,
        storage_url=str(destination),
    )
    db.add(call)
    await db.commit()
    await db.refresh(call)

    background_tasks.add_task(run_pipeline, call.id)
    return CallRead(
        id=call.id,
        file_name=call.file_name,
        status=call.status.value,
        transcript=call.transcript,
        created_at=call.created_at,
    )


@router.get("", response_model=list[CallRead])
async def list_calls(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)) -> list[CallRead]:
    result = await db.execute(
        select(Call).where(Call.organization_id == current_user.organization_id).order_by(Call.created_at.desc())
    )
    items = result.scalars().all()
    return [
        CallRead(
            id=item.id,
            file_name=item.file_name,
            status=item.status.value,
            transcript=item.transcript,
            created_at=item.created_at,
        )
        for item in items
    ]


@router.get("/{call_id}/analysis", response_model=AnalysisRead)
async def get_analysis(
    call_id: str, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)
) -> AnalysisRead:
    call_result = await db.execute(
        select(Call).where(Call.id == call_id, Call.organization_id == current_user.organization_id)
    )
    if not call_result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Call not found")
    result = await db.execute(select(CallAnalysis).where(CallAnalysis.call_id == call_id))
    analysis = result.scalar_one_or_none()
    if not analysis:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis not ready")
    return AnalysisRead(
        call_id=call_id,
        executive_summary=analysis.executive_summary,
        sentiment_score=analysis.sentiment_score,
        buying_intent_score=analysis.buying_intent_score,
        objections=analysis.objections,
        action_items=analysis.action_items,
    )
