# features/analytics.py
import plotly.graph_objects as go
from datetime import datetime, timedelta
from typing import Dict, List
from database.models import ChatHistory

class AnalyticsDashboard:
    def __init__(self):
        pass
    
    def get_market_sentiment(self, watchlist: List[str]) -> Dict:
        sentiment_data = {}
        for company in watchlist:
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
        """Get user statistics - simplified version"""
        history = ChatHistory.get_history(user_id, limit=1000)
        
        if not history:
            return {"total_messages": 0, "most_used_mode": "None", "last_7_days": 0}
        
        total_messages = len(history)
        
        # Count modes
        modes = {}
        for item in history:
            mode = item.get('mode', 'Unknown')
            modes[mode] = modes.get(mode, 0) + 1
        
        # Get most used mode
        most_used_mode = "None"
        if modes:
            most_used_mode = max(modes, key=modes.get)
        
        # Count last 7 days
        last_7_days = 0
        seven_days_ago = datetime.now() - timedelta(days=7)
        
        for item in history:
            timestamp_str = item.get('timestamp', '')
            if timestamp_str:
                try:
                    # Parse timestamp string to datetime
                    if isinstance(timestamp_str, str):
                        # Handle different timestamp formats
                        if 'T' in timestamp_str:
                            ts = datetime.fromisoformat(timestamp_str.replace('Z', ''))
                        elif ' ' in timestamp_str:
                            ts = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                        else:
                            ts = datetime.strptime(timestamp_str, '%Y-%m-%d')
                        
                        if ts > seven_days_ago:
                            last_7_days += 1
                except:
                    pass
        
        return {
            "total_messages": total_messages,
            "most_used_mode": most_used_mode,
            "last_7_days": last_7_days
        }
    