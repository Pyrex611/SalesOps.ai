import re


class AnalysisService:
    """Builds structured call analysis from transcript text."""

    async def analyze(self, transcript: str) -> dict:
        lowered = transcript.lower()
        objections = [
            token for token in ["budget", "timeline", "security", "integration"] if token in lowered
        ]
        action_items = [
            {"owner": "rep", "task": "Send tailored proposal", "deadline": "in 2 business days"},
            {"owner": "prospect", "task": "Confirm stakeholder attendees", "deadline": "this week"},
        ]
        sentiment = 8.0 if "thanks" in lowered else 6.0
        buying_intent = 7.5 if re.search(r"next step|proposal|demo", lowered) else 5.5
        return {
            "executive_summary": "Constructive discovery call with clear next actions and urgency signals.",
            "sentiment_score": sentiment,
            "buying_intent_score": buying_intent,
            "objections": objections,
            "action_items": action_items,
        }
