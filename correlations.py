from __future__ import annotations  # ← ADD THIS
# SIMPLE sentiment analysis without transformers
import re
from typing import Optional

class TextAnalyzer:
    def analyze_sentiment(self, text: str) -> float:
        """Simple rule-based sentiment analysis"""
        if not text.strip():
            return 0.0
            
        positive_words = {'good', 'great', 'happy', 'awesome', 'amazing', 'excellent', 'joy', 'love', 'nice', 'better', 'best'}
        negative_words = {'bad', 'terrible', 'awful', 'sad', 'angry', 'hate', 'worst', 'horrible', 'upset', 'annoying'}
        
        words = set(re.findall(r'\b\w+\b', text.lower()))
        
        positive_count = len(words & positive_words)
        negative_count = len(words & negative_words)
        
        if positive_count + negative_count == 0:
            return 0.0
            
        sentiment = (positive_count - negative_count) / (positive_count + negative_count)
        return max(-1.0, min(1.0, sentiment))

text_analyzer = TextAnalyzer()
