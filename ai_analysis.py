import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Dict
from datetime import datetime, timedelta
from sqlmodel import Session, select
from app.models.database import MoodEntry, FoodLog

class MoodFoodAnalyzer:
    def __init__(self):
        self.min_data_points = 5
        
    def calculate_correlations(self, user_id: int, session: Session, days_back: int = 30) -> List[Dict]:
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days_back)
        
        mood_statement = select(MoodEntry).where(
            MoodEntry.user_id == user_id,
            MoodEntry.date >= start_date
        )
        mood_data = session.exec(mood_statement).all()
        
        food_statement = select(FoodLog).where(
            FoodLog.user_id == user_id,
            FoodLog.date >= start_date
        )
        food_data = session.exec(food_statement).all()
        
        if len(mood_data) < self.min_data_points:
            return [{
                "type": "insufficient_data",
                "message": "Need more mood entries to generate insights",
                "confidence": 0.0
            }]
        
        analysis_data = self._prepare_analysis_data(mood_data, food_data)
        insights = self._generate_insights(analysis_data)
        return insights
    
    def _prepare_analysis_data(self, mood_data: List[MoodEntry], food_data: List[FoodLog]) -> pd.DataFrame:
        mood_df = pd.DataFrame([{
            'date': entry.date,
            'mood_score': entry.mood_score
        } for entry in mood_data])
        
        unique_foods = list(set([entry.food_name for entry in food_data]))
        food_presence = []
        
        for entry in food_data:
            food_presence.append({
                'date': entry.date,
                'food': entry.food_name,
                'present': True
            })
        
        food_df = pd.DataFrame(food_presence)
        if not food_df.empty:
            food_pivot = food_df.pivot_table(
                index='date', 
                columns='food', 
                values='present', 
                fill_value=False
            ).astype(bool)
            
            analysis_df = mood_df.merge(food_pivot, on='date', how='left')
            analysis_df[unique_foods] = analysis_df[unique_foods].fillna(False)
        else:
            analysis_df = mood_df
            for food in unique_foods:
                analysis_df[food] = False
        
        return analysis_df
    
    def _generate_insights(self, analysis_df: pd.DataFrame) -> List[Dict]:
        insights = []
        mood_scores = analysis_df['mood_score']
        
        food_columns = [col for col in analysis_df.columns if col not in ['date', 'mood_score']]
        
        for food in food_columns:
            if food in analysis_df.columns:
                food_days = analysis_df[analysis_df[food] == True]
                non_food_days = analysis_df[analysis_df[food] == False]
                
                if len(food_days) >= 3:
                    avg_mood_with = food_days['mood_score'].mean()
                    avg_mood_without = non_food_days['mood_score'].mean()
                    
                    if len(food_days) > 1 and len(non_food_days) > 1:
                        t_stat, p_value = stats.ttest_ind(
                            food_days['mood_score'], 
                            non_food_days['mood_score'],
                            equal_var=False
                        )
                    else:
                        p_value = 1.0
                    
                    mood_diff = avg_mood_with - avg_mood_without
                    if abs(mood_diff) >= 0.5 and p_value < 0.2:
                        confidence = max(0.1, 1 - p_value)
                        
                        if mood_diff > 0:
                            insight_type = "positive_correlation"
                            message = f"When you ate {food}, your mood was {mood_diff:.1f} points higher on average"
                        else:
                            insight_type = "negative_correlation" 
                            message = f"When you ate {food}, your mood was {abs(mood_diff):.1f} points lower on average"
                        
                        insights.append({
                            "type": insight_type,
                            "food": food,
                            "message": message,
                            "mood_difference": round(mood_diff, 2),
                            "confidence": round(confidence, 2),
                            "days_analyzed": len(food_days)
                        })
        
        insights.sort(key=lambda x: x['confidence'], reverse=True)
        
        if not insights:
            insights.append({
                "type": "no_strong_patterns",
                "message": "No strong food-mood patterns detected yet. Keep tracking!",
                "confidence": 0.0
            })
        
        return insights

analyzer = MoodFoodAnalyzer()
