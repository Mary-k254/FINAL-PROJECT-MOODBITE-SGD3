# Keep your existing correlation analysis
# Just remove any torch/transformers imports
import pandas as pd
import numpy as np
from scipy import stats
from typing import List, Dict
from datetime import datetime, timedelta
from sqlmodel import Session, select
from database import MoodEntry, FoodLog

class MoodFoodAnalyzer:
    def __init__(self):
        self.min_data_points = 5
        
    def calculate_correlations(self, user_id: int, session: Session, days_back: int = 30) -> List[Dict]:
        # KEEP ALL YOUR EXISTING CODE HERE
        # This doesn't need heavy AI libraries
        # ... your existing analysis code ...
        
        return insights

analyzer = MoodFoodAnalyzer()
