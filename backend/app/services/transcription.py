from pathlib import Path


class TranscriptionService:
    """Transcribes audio files with deterministic local fallback output."""

    async def transcribe(self, file_path: str) -> dict:
        filename = Path(file_path).name
        transcript = (
            f"Rep: Thanks for joining, let's discuss priorities for {filename}. "
            "Prospect: Budget and timeline are my biggest concerns."
        )
        return {
            "transcript": transcript,
            "talk_ratio_rep": 0.42,
            "talk_ratio_prospect": 0.58,
        }
