from collections import Counter
import re


POSITIVE_TERMS = {'great', 'excellent', 'love', 'excited', 'amazing', 'helpful'}
NEGATIVE_TERMS = {'issue', 'concern', 'problem', 'frustrated', 'expensive', 'slow'}


class AnalysisService:
    """Lightweight analysis engine for transcript-derived insights."""

    @staticmethod
    def analyze(transcript: str) -> dict:
        normalized = transcript.lower()
        words = re.findall(r"[a-z']+", normalized)
        counts = Counter(words)
        positive = sum(counts[t] for t in POSITIVE_TERMS)
        negative = sum(counts[t] for t in NEGATIVE_TERMS)
        sentiment = max(1, min(10, 5 + positive - negative))
        buying_intent = max(1, min(10, counts['budget'] + counts['timeline'] + 3))
        summary = ' '.join(transcript.split()[:40])
        key_moments = [
            label
            for label, keyword in {
                'budget_discussion': 'budget',
                'timeline_mention': 'timeline',
                'decision_maker': 'decision maker',
                'pricing_conversation': 'price',
            }.items()
            if keyword in normalized
        ]
        return {
            'summary': summary,
            'sentiment_score': sentiment,
            'buying_intent_score': buying_intent,
            'pain_points': [term for term in NEGATIVE_TERMS if term in counts],
            'objections': [term for term in ('expensive', 'concern') if term in counts],
            'key_moments': key_moments,
            'next_steps': AnalysisService.extract_next_steps(transcript),
        }

    @staticmethod
    def extract_next_steps(transcript: str) -> list[dict]:
        lines = [line.strip() for line in transcript.split('.') if line.strip()]
        tasks: list[dict] = []
        for line in lines:
            if any(trigger in line.lower() for trigger in ('will', 'next', 'send', 'schedule')):
                tasks.append({'description': line, 'owner': 'rep'})
        return tasks[:10]
