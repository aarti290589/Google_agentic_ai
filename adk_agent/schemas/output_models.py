# adk_agent/schemas/output_models.py

from typing import List, Dict

class ReviewAnalysisResult:
    def __init__(self, review_text: str, sentiment: str, aspect: str, recommendation: List[str]):
        self.review_text = review_text
        self.sentiment = sentiment
        self.aspect = aspect
        self.recommendation = recommendation

    def to_dict(self):
        return {
            'review_text': self.review_text,
            'sentiment': self.sentiment,
            'aspect': self.aspect,
            'recommendation': self.recommendation
        }
