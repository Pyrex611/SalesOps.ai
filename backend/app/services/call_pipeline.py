from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.entities import Call, CallAnalysis, CallStatus
from app.services.analysis import AnalysisService
from app.services.transcription import TranscriptionService


class CallPipelineService:
    def __init__(self) -> None:
        self.transcription = TranscriptionService()
        self.analysis = AnalysisService()

    async def process_call(self, db: AsyncSession, call_id: str) -> None:
        result = await db.execute(select(Call).where(Call.id == call_id))
        call = result.scalar_one_or_none()
        if not call:
            return

        tx = await self.transcription.transcribe(call.storage_url)
        call.transcript = tx["transcript"]
        call.talk_ratio_rep = tx["talk_ratio_rep"]
        call.talk_ratio_prospect = tx["talk_ratio_prospect"]
        call.status = CallStatus.transcribed

        analysis = await self.analysis.analyze(call.transcript)
        db.add(
            CallAnalysis(
                call_id=call.id,
                executive_summary=analysis["executive_summary"],
                sentiment_score=analysis["sentiment_score"],
                buying_intent_score=analysis["buying_intent_score"],
                objections=analysis["objections"],
                action_items=analysis["action_items"],
            )
        )
        call.status = CallStatus.analyzed
        await db.commit()
