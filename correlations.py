from transformers import pipeline
import spacy
from typing import Optional
import re

class TextAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = None
        self.nlp = None
        
    def load_models(self):
        if self.sentiment_analyzer is None:
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                return_all_scores=True
            )
        
        if self.nlp is None:
            try:
                self.nlp = spacy.load("en_core_web_sm")
            except OSError:
                self.nlp = spacy.blank("en")
    
    def analyze_sentiment(self, text: str) -> float:
        self.load_models()
        
        if not text.strip():
            return 0.0
            
        try:
            results = self.sentiment_analyzer(text[:512])
            if results and len(results) > 0:
                scores = results[0]
                positive_score = next((s['score'] for s in scores if s['label'] == 'positive'), 0)
                negative_score = next((s['score'] for s in scores if s['label'] == 'negative'), 0)
                sentiment = positive_score - negative_score
                return max(-1.0, min(1.0, sentiment))
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
        return 0.0

text_analyzer = TextAnalyzer()
