import pathlib


class TranscriptionService:
    """Transcription adapter using text passthrough for manual testing."""

    @staticmethod
    async def transcribe(file_path: str) -> str:
        path = pathlib.Path(file_path)
        if path.suffix.lower() in {'.txt'}:
            return path.read_text(encoding='utf-8')
        return (
            'Transcript unavailable for binary media in local mode. '
            'Upload a .txt transcript for deterministic analysis.'
        )
