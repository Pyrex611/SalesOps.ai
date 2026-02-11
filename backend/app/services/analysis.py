from __future__ import annotations

from collections import Counter
import re
from typing import Any

POSITIVE_TERMS = {
    'great',
    'excellent',
    'love',
    'excited',
    'amazing',
    'helpful',
    'confident',
    'progress',
}
NEGATIVE_TERMS = {
    'issue',
    'concern',
    'problem',
    'frustrated',
    'expensive',
    'slow',
    'risk',
}


class AnalysisService:
    """Deterministic analysis engine that mirrors production AI contract shape."""

    @staticmethod
    def analyze(transcript: str) -> dict[str, Any]:
        normalized = transcript.lower()
        words = re.findall(r"[a-z']+", normalized)
        counts = Counter(words)

        positive = sum(counts[t] for t in POSITIVE_TERMS)
        negative = sum(counts[t] for t in NEGATIVE_TERMS)
        sentiment = max(1, min(10, 5 + positive - negative))
        buying_intent = max(
            1,
            min(
                10,
                counts['budget'] + counts['timeline'] + counts['decision'] + counts['next'] + 2,
            ),
        )

        closing_probability = max(1, min(100, 42 + positive * 8 - negative * 9 + buying_intent * 4))
        summary = ' '.join(transcript.split()[:48])
        pain_points = [term for term in sorted(NEGATIVE_TERMS) if term in counts]

        return {
            'executive_summary': {
                'overview': summary,
                'call_type': AnalysisService._infer_call_type(normalized),
                'outcome': AnalysisService._infer_outcome(normalized),
            },
            'scores': {
                'sentiment_score': sentiment,
                'buying_intent_score': buying_intent,
                'closing_probability': closing_probability,
                'engagement_score': max(1, min(10, sentiment + 1)),
            },
            'bant': AnalysisService._extract_bant(normalized),
            'pain_points': pain_points,
            'objections': [term for term in ('expensive', 'concern', 'risk') if term in counts],
            'key_moments': AnalysisService._key_moments(normalized),
            'methodology_insights': {
                'mugica_keuilian': AnalysisService._detect_framework_cues(normalized),
                'bill_walsh': AnalysisService._detect_competitive_cues(normalized),
            },
            'next_steps': AnalysisService.extract_next_steps(transcript),
            'follow_up': AnalysisService._generate_follow_up(transcript, summary),
            'structured_payload': {
                'schema_version': 'v1',
                'crm_ready': True,
                'conversation_state': AnalysisService._conversation_state(closing_probability),
            },
        }

    @staticmethod
    def extract_next_steps(transcript: str) -> list[dict[str, str]]:
        lines = [line.strip() for line in transcript.split('.') if line.strip()]
        tasks: list[dict[str, str]] = []
        for line in lines:
            lowered = line.lower()
            if any(trigger in lowered for trigger in ('will', 'next', 'send', 'schedule', 'follow')):
                owner = 'prospect' if 'you will' in lowered else 'rep'
                tasks.append({'description': line, 'owner': owner, 'status': 'open'})
        return tasks[:10]

    @staticmethod
    def _infer_call_type(normalized: str) -> str:
        if 'demo' in normalized:
            return 'demo'
        if 'proposal' in normalized or 'pricing' in normalized:
            return 'negotiation'
        return 'discovery'

    @staticmethod
    def _infer_outcome(normalized: str) -> str:
        if 'next week' in normalized or 'schedule' in normalized:
            return 'next_step_confirmed'
        if 'follow up' in normalized:
            return 'follow_up_needed'
        return 'open'

    @staticmethod
    def _extract_bant(normalized: str) -> dict[str, str]:
        def status(keyword_set: set[str]) -> str:
            return 'covered' if any(word in normalized for word in keyword_set) else 'missing'

        return {
            'budget': status({'budget', 'cost', 'price'}),
            'authority': status({'decision maker', 'vp', 'director', 'cfo'}),
            'need': status({'problem', 'need', 'challenge', 'pain'}),
            'timeline': status({'timeline', 'quarter', 'month', 'deadline'}),
        }

    @staticmethod
    def _key_moments(normalized: str) -> list[str]:
        checks = {
            'budget_discussion': 'budget',
            'timeline_mention': 'timeline',
            'decision_maker': 'decision maker',
            'pricing_conversation': 'price',
            'demo_request': 'demo',
            'contract_discussion': 'contract',
        }
        return [label for label, keyword in checks.items() if keyword in normalized]

    @staticmethod
    def _detect_framework_cues(normalized: str) -> dict[str, str]:
        return {
            'emotional_trigger': 'urgency' if 'urgent' in normalized else 'confidence',
            'deal_risk_moment': 'pricing_pushback' if 'expensive' in normalized else 'none_detected',
        }

    @staticmethod
    def _detect_competitive_cues(normalized: str) -> dict[str, str]:
        competitor_mentioned = 'competitor' in normalized or 'alternative' in normalized
        return {
            'competitive_pressure': 'high' if competitor_mentioned else 'low',
            'recommended_posture': 'differentiate_on_roi' if competitor_mentioned else 'consultative',
        }

    @staticmethod
    def _conversation_state(closing_probability: int) -> str:
        if closing_probability >= 75:
            return 'hot'
        if closing_probability >= 50:
            return 'warm'
        return 'nurture'

    @staticmethod
    def _generate_follow_up(transcript: str, summary: str) -> dict[str, Any]:
        preview_points = [line.strip() for line in transcript.split('.') if line.strip()][:2]
        email_body = (
            'Thanks again for the conversation today. '\
            f"Key themes we aligned on: {summary}. "
            'As a next step, I will send a tailored recommendation and timeline options. '\
            'If priorities shift, just reply and we can adapt quickly.\n\n'
            'Unsubscribe: {{dynamic_unsubscribe_link}}'
        )
        return {
            'subject': 'Next steps from our sales strategy call',
            'draft_body': email_body,
            'negative_reverse_sell_line': 'If this is not the right quarter, we can pause and revisit later.',
            'objection_neutralizer_line': 'If budget is tight, we can phase rollout to protect ROI early.',
            'drip_sequence': [
                {
                    'day': 2,
                    'goal': 'share value recap',
                    'message': 'Quick recap of agreed priorities and expected outcomes.',
                },
                {
                    'day': 5,
                    'goal': 'reduce friction',
                    'message': 'Happy to adapt scope if internal bandwidth is constrained.',
                },
            ],
            'referenced_moments': preview_points,
        }
