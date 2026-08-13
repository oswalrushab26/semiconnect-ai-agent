# features/analytics.py
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List
import pandas as pd
from database.models import ChatHistory

class AnalyticsDashboard:
    def __init__(self):
        pass
    
    def get_market_sentiment(self, watchlist: List[str]) -> Dict:
        sentiment_data = {}
        for company in watchlist:
            # Simple sentiment simulation
            sentiment_data[company] = {
                "score": 0.5 + (hash(company) % 100) / 200,
                "trend": "up" if hash(company) % 2 == 0 else "down"
            }
        return sentiment_data
    
    def create_sentiment_chart(self, sentiment_data: Dict) -> go.Figure:
        companies = list(sentiment_data.keys())
        scores = [data['score'] for data in sentiment_data.values()]
        
        fig = go.Figure(data=[
            go.Bar(
                x=companies,
                y=scores,
                marker_color=['green' if s > 0.5 else 'red' for s in scores],
                text=[f"{s:.1%}" for s in scores],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Market Sentiment Score",
            yaxis_title="Sentiment Score",
            yaxis_range=[0, 1],
            height=400,
            showlegend=False
        )
        return fig
    
    def get_user_stats(self, user_id: int) -> Dict:
        history = ChatHistory.get_history(user_id, limit=1000)
        if not history:
            return {"total_messages": 0, "most_used_mode": "None", "last_7_days": 0}
        
        df = pd.DataFrame(history)
        return {
            "total_messages": len(df),
            "most_used_mode": df['mode'].mode().iloc[0] if not df.empty else "None",
            "last_7_days": len(df[df['timestamp'] > (datetime.now() - timedelta(days=7))])
        }
    