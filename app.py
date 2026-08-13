# app.py
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ddgs import DDGS
import pandas as pd
import os
import hashlib
from datetime import datetime

# Import our modules
from database.models import init_database, User, ChatHistory, Watchlist, Usage, get_db_connection
from features.auth import AuthManager
from features.analytics import AnalyticsDashboard
from features.reporting import ReportGenerator
from utils.rate_limiter import TieredRateLimiter
from utils.cache import CacheManager
from utils.security import SecurityManager
from config import config
from prompts import MARKET_INTEL_PROMPT, VLSI_TUTOR_PROMPT, BUSINESS_OPS_PROMPT, LEARNING_PATH_PROMPT

load_dotenv()

# Initialize
auth_manager = AuthManager()
analytics_dashboard = AnalyticsDashboard()
report_generator = ReportGenerator()
rate_limiter = TieredRateLimiter()
cache_manager = CacheManager()
security_manager = SecurityManager()
init_database()

# Page config
st.set_page_config(
    page_title="SemiConnect",
    page_icon="🔌",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.metric-card {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    border-left: 4px solid #667eea;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "user_email" not in st.session_state:
    st.session_state.user_email = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Market Intelligence"
if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# Cache for search
_search_cache = {}

def web_search(query: str) -> str:
    cache_key = hashlib.md5(query.encode()).hexdigest()
    if cache_key in _search_cache:
        return _search_cache[cache_key]
    
    try:
        results = DDGS().text(query, max_results=5)
        combined = "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
        _search_cache[cache_key] = combined
        return combined
    except Exception as e:
        return f"⚠️ Search error: {str(e)}"

# Authentication functions
def login_form():
    st.sidebar.markdown("### 🔐 Sign In")
    email = st.sidebar.text_input("Email")
    password = st.sidebar.text_input("Password", type="password")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("Sign In", use_container_width=True):
            user = auth_manager.authenticate_user(email, password)
            if user:
                st.session_state.authenticated = True
                st.session_state.user_id = user['id']
                st.session_state.user_email = email
                st.rerun()
            else:
                st.sidebar.error("Invalid credentials")
    
    with col2:
        if st.button("Sign Up", use_container_width=True):
            if security_manager.validate_email(email):
                valid, errors = security_manager.validate_password(password)
                if valid:
                    if auth_manager.create_user(email, password):
                        st.sidebar.success("Account created! Please sign in.")
                    else:
                        st.sidebar.error("User already exists")
                else:
                    st.sidebar.error("\n".join(errors))
            else:
                st.sidebar.error("Invalid email")

# Main app
def main():
    # Sidebar
    with st.sidebar:
        st.markdown("### 🔌 SemiConnect")
        
        if not st.session_state.authenticated:
            login_form()
            st.stop()
        
        # User info
        user = User.get_by_email(st.session_state.user_email)
        tier = user['tier'].upper() if user else "FREE"
        st.markdown(f"""
        **👤 User:** {st.session_state.user_email}
        **💎 Tier:** {tier}
        """)
        
        # Check daily limit
        if not auth_manager.check_usage_limit(st.session_state.user_email):
            st.warning("⚠️ Daily limit reached. Upgrade to Pro!")
        
        st.divider()
        
        # Mode selection
        mode = st.radio(
            "Choose a mode:",
            ["Market Intelligence", "VLSI Tutor", "Business Ops", "Learning Path"]
        )
        st.session_state.mode = mode
        
        st.divider()
        
        # Watchlist
        st.markdown("### 📋 Watchlist")
        new_company = st.text_input("Add company", key="watchlist_input")
        if st.button("➕ Add", use_container_width=True):
            if new_company:
                Watchlist.add(st.session_state.user_id, new_company)
                st.rerun()
        
        # Display watchlist
        watchlist = Watchlist.get_all(st.session_state.user_id)
        for item in watchlist:
            col1, col2 = st.columns([3, 1])
            col1.write(f"• {item['company_name']}")
            if col2.button("🗑️", key=f"remove_{item['id']}"):
                Watchlist.remove(st.session_state.user_id, item['id'])
                st.rerun()
        
        st.divider()
        
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_id = None
            st.session_state.user_email = None
            st.rerun()
    
    # Main content
    # Stats
    col1, col2, col3 = st.columns(3)
    with col1:
        usage = Usage.get_today_usage(st.session_state.user_id)
        st.metric("💬 Today's Messages", usage['messages_used'])
    with col2:
        watchlist_count = len(Watchlist.get_all(st.session_state.user_id))
        st.metric("🏢 Watchlist", watchlist_count)
    with col3:
        tier_name = user['tier'].upper() if user else "FREE"
        st.metric("💎 Tier", tier_name)
    
    st.divider()
    
    # Tabs
    tab_chat, tab_analytics, tab_reports = st.tabs(["💬 Chat", "📊 Analytics", "📄 Reports"])
    
    with tab_chat:
        render_chat()
    
    with tab_analytics:
        render_analytics()
    
    with tab_reports:
        render_reports()

def render_chat():
    mode = st.session_state.mode
    mode_descriptions = {
        "Market Intelligence": "📊 Live OSAT, fab, and supply chain news",
        "VLSI Tutor": "📚 Step-by-step Verilog & digital electronics",
        "Business Ops": "💼 Vendor, sourcing & supply chain analysis",
        "Learning Path": "🎓 Zero to pro: guided semiconductor learning"
    }
    st.caption(mode_descriptions[mode])
    
    # Check limit before processing
    if not auth_manager.check_usage_limit(st.session_state.user_email):
        st.warning("⚠️ Daily message limit reached. Upgrade to Pro for unlimited access!")
        st.info("💎 Pro plan: $49/month - Unlimited messages, advanced analytics, and more!")
        return
    
    # Get Gemini client
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("❌ Gemini API key not found! Please check your .env file.")
        return
    
    client = genai.Client(api_key=api_key)
    
    # Build prompts
    prompts = {
        "Market Intelligence": MARKET_INTEL_PROMPT,
        "VLSI Tutor": VLSI_TUTOR_PROMPT,
        "Business Ops": BUSINESS_OPS_PROMPT,
        "Learning Path": LEARNING_PATH_PROMPT
    }
    
    # Initialize chat
    if "chat_obj" not in st.session_state or st.session_state.get("current_mode") != mode:
        try:
            st.session_state.chat_obj = client.chats.create(
                model="gemini-flash-latest",
                config=types.GenerateContentConfig(
                    system_instruction=prompts[mode],
                    tools=[web_search]
                )
            )
            st.session_state.current_mode = mode
        except Exception as e:
            st.error(f"Failed to initialize chat: {str(e)}")
            return
    
    # Display messages
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🔌"):
            st.write(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Ask something...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar="🧑"):
            st.write(user_input)
        
        with st.chat_message("assistant", avatar="🔌"):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat_obj.send_message(user_input)
                    answer = response.text
                except Exception as e:
                    if "429" in str(e):
                        answer = "⏳ Too many requests. Please try again in a few minutes."
                    else:
                        answer = f"⚠️ Error: {str(e)}"
                st.write(answer)
        
        st.session_state.messages.append({"role": "assistant", "content": answer})
        
        # Save to database and increment usage
        ChatHistory.save(st.session_state.user_id, mode, user_input, "user", answer)
        Usage.increment(st.session_state.user_id, "message")

def render_analytics():
    st.subheader("📊 Analytics Dashboard")
    
    # Check if user is Pro or Enterprise
    user = User.get_by_email(st.session_state.user_email)
    is_premium = user and user['tier'] in ["pro", "enterprise"]
    
    if is_premium:
        watchlist = Watchlist.get_all(st.session_state.user_id)
        company_names = [item['company_name'] for item in watchlist]
        
        if company_names:
            sentiment_data = analytics_dashboard.get_market_sentiment(company_names)
            fig = analytics_dashboard.create_sentiment_chart(sentiment_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Add companies to your watchlist to see sentiment analysis.")
        
        # User stats
        stats = analytics_dashboard.get_user_stats(st.session_state.user_id)
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Messages", stats['total_messages'])
        col2.metric("Most Used Mode", stats['most_used_mode'])
        col3.metric("Last 7 Days", stats['last_7_days'])
    else:
        st.info("🔒 Analytics Dashboard is a Pro feature")
        st.markdown("""
        Upgrade to Pro to access:
        - Market sentiment analysis
        - Usage analytics
        - Advanced visualizations
        - Export capabilities
        
        💎 **Pro Plan: $49/month**
        """)
        if st.button("💼 Upgrade to Pro"):
            st.success("Payment integration coming soon!")

def render_reports():
    st.subheader("📄 Report Generation")
    
    # Check if user is Pro or Enterprise
    user = User.get_by_email(st.session_state.user_email)
    is_premium = user and user['tier'] in ["pro", "enterprise"]
    
    if is_premium:
        report_type = st.selectbox(
            "Select report type",
            ["Weekly Market Brief", "Competitor Analysis", "Supply Chain Report"]
        )
        
        watchlist = Watchlist.get_all(st.session_state.user_id)
        company_names = [item['company_name'] for item in watchlist]
        
        if st.button("Generate Report", use_container_width=True):
            with st.spinner("Generating report..."):
                if report_type == "Weekly Market Brief":
                    report = report_generator.generate_weekly_brief(company_names)
                else:
                    report = "Report generation coming soon..."
                
                st.markdown(report)
                
                # Download option
                st.download_button(
                    label="📥 Download Report",
                    data=report,
                    file_name=f"report_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown"
                )
    else:
        st.info("🔒 Report Generation is a Pro feature")
        st.markdown("""
        Upgrade to Pro to generate:
        - Weekly market briefs
        - Competitor analysis
        - Supply chain reports
        - Custom reports
        
        💎 **Pro Plan: $49/month**
        """)

if __name__ == "__main__":
    main()
    