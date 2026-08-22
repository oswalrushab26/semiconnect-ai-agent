import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ddgs import DDGS
import pandas as pd
import os
from prompts import MARKET_INTEL_PROMPT, VLSI_TUTOR_PROMPT, BUSINESS_OPS_PROMPT, LEARNING_PATH_PROMPT

load_dotenv()
if "GEMINI_API_KEY" not in os.environ and "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

_search_cache = {}

def web_search(query: str) -> str:
    """Searches the web and returns a summary of top results."""
    if query in _search_cache:
        return _search_cache[query]
    results = DDGS().text(query, max_results=5)
    combined = "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    _search_cache[query] = combined
    return combined

st.set_page_config(page_title="SemiConnect", page_icon="🔌", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
    }
    .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp label {
        color: #1a1a2e !important;
    }
    section[data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    .stButton button {
        background-color: #f0f2f6 !important;
        color: #1a1a2e !important;
        border: 1px solid #d0d0d0 !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
    }
    .stButton button:hover {
        background-color: #e0e2e6 !important;
        border-color: #b0b0b0 !important;
    }
    .stChatMessage {
        background-color: #ffffff !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        margin: 8px 0 !important;
        border: 1px solid #e8e8e8 !important;
    }
    .stChatMessage:has([data-testid="chat-avatar-user"]) {
        background-color: #f0f2f6 !important;
    }
    .stChatInput input {
        background-color: #ffffff !important;
        border-radius: 25px !important;
        border: 2px solid #d0d0d0 !important;
        padding: 10px 20px !important;
        color: #1a1a2e !important;
    }
    .stChatInput input:focus {
        border-color: #4a6cf7 !important;
        outline: none !important;
        box-shadow: none !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f5 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 8px 20px !important;
        color: #555 !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
        border-bottom: 3px solid #4a6cf7 !important;
    }
    section[data-testid="stSidebar"] .stButton button {
        background-color: #f0f2f6 !important;
        color: #1a1a2e !important;
        border: 1px solid #d0d0d0 !important;
    }
    section[data-testid="stSidebar"] .stButton button:hover {
        background-color: #e0e2e6 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔌 SemiConnect")
st.caption("AI agent for the semiconductor industry — Market Intelligence · VLSI Tutor · Business Ops · Learning Path")

tab_chat, tab_tracker, tab_about = st.tabs(["💬 Chat", "📈 Tracker", "ℹ️ About"])

with tab_about:
    st.subheader("What is SemiConnect?")
    st.write("""
    SemiConnect is an AI agent built for the semiconductor industry, with four specialist modes:

    - **Market Intelligence** — live news on OSAT, fab investments, and supply chain shifts
    - **VLSI Tutor** — step-by-step teaching of Verilog and digital electronics
    - **Business Ops** — vendor, sourcing, and supply chain strategy analysis, with support for uploading your own CSV/Excel data for direct analysis
    - **Learning Path** — guides complete beginners through semiconductor/VLSI fundamentals, step by step, with progress tracking

    Built by Rushab Oswal using free tools: Python, Gemini API, and DuckDuckGo search.
    """)
    st.link_button("View source on GitHub", "https://github.com/oswalrushab26/semiconnect-ai-agent")

with tab_tracker:
    st.subheader("📈 Supply Chain Watchlist")
    st.write("Track specific companies and check for the latest news on demand.")

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    new_company = st.text_input("Add a company to track (e.g. Tata Electronics, Kaynes Semicon)")
    if st.button("➕ Add to watchlist"):
        if new_company and new_company not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_company)
            st.rerun()

    st.divider()

    for company in st.session_state.watchlist:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{company}**")
        check = col2.button("🔍 Check latest", key=f"check_{company}")
        remove = col3.button("🗑️", key=f"remove_{company}")

        if check:
            with st.spinner(f"Checking news for {company}..."):
                result = web_search(f"{company} semiconductor news")
            st.write(f"📰 {result}")

        if remove:
            st.session_state.watchlist.remove(company)
            st.rerun()

st.sidebar.header("SemiConnect")
st.sidebar.write("Built by Rushab Oswal")
mode = st.sidebar.radio("Choose a mode:", ["Market Intelligence", "VLSI Tutor", "Business Ops", "Learning Path"])
st.sidebar.divider()

learning_topics = [
    "What is a semiconductor?",
    "Basic electronics: voltage, current, transistors",
    "Digital logic: gates and boolean logic",
    "Sequential logic: flip-flops and memory",
    "Introduction to Verilog",
    "Semiconductor industry overview: fab, OSAT, packaging"
]

mode_descriptions = {
    "Market Intelligence": "📊 Live OSAT, fab, and supply chain news",
    "VLSI Tutor": "📚 Step-by-step Verilog & digital electronics",
    "Business Ops": "💼 Vendor, sourcing & supply chain analysis",
    "Learning Path": "🎓 Zero to pro: guided semiconductor learning"
}

st.sidebar.write(mode_descriptions[mode])

uploaded_file = None
if mode == "Business Ops":
    st.sidebar.divider()
    st.sidebar.subheader("📎 Analyze a file")
    uploaded_file = st.sidebar.file_uploader("Upload vendor/supply data (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.write(f"✅ Loaded {len(df)} rows")
            st.session_state.file_summary = df.describe(include="all").to_string()
            st.session_state.file_preview = df.head(10).to_string()
        except Exception:
            st.sidebar.write("❌ Couldn't read that file. Try a CSV or Excel file.")

if mode == "Learning Path":
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = 0
    st.sidebar.write("**Your progress:**")
    for i, topic in enumerate(learning_topics):
        if i < st.session_state.learning_progress:
            st.sidebar.write(f"✅ {topic}")
        elif i == st.session_state.learning_progress:
            st.sidebar.write(f"👉 {topic}")
        else:
            st.sidebar.write(f"⬜ {topic}")
    if st.sidebar.button("Mark current topic complete"):
        st.session_state.learning_progress = min(st.session_state.learning_progress + 1, len(learning_topics))
        st.rerun()

prompts = {
    "Market Intelligence": MARKET_INTEL_PROMPT,
    "VLSI Tutor": VLSI_TUTOR_PROMPT,
    "Business Ops": BUSINESS_OPS_PROMPT,
    "Learning Path": LEARNING_PATH_PROMPT
}

if "chat" not in st.session_state or st.session_state.get("mode") != mode:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    system_instruction = prompts[mode]
    if mode == "Business Ops" and "file_summary" in st.session_state:
        system_instruction += f"""

The user has uploaded a data file. Here is a preview of the first 10 rows:
{st.session_state.file_preview}

Here are summary statistics for the file:
{st.session_state.file_summary}

When the user asks about this data, analyze it using the information above."""

    st.session_state.chat = client.chats.create(
        model="gemini-flash-latest",
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[web_search]
        )
    )
    st.session_state.mode = mode
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_friendly_error(e):
    err = str(e)
    if "429" in err or "RESOURCE_EXHAUSTED" in err:
        return "⏳ SemiConnect is getting a lot of use right now and has hit its free-tier limit. Please try again in a few minutes, or come back tomorrow — thanks for your patience!"
    elif "503" in err or "UNAVAILABLE" in err:
        return "⏳ The AI service is experiencing high demand right now. Please try again in a moment."
    else:
        return "⚠️ Something went wrong on my end. Please try rephrasing your question or try again shortly."

with tab_chat:
    if len(st.session_state.messages) == 0:
        st.info(f"👋 You're in **{mode}** mode. Ask me anything to get started.")

        examples = {
            "Market Intelligence": ["Latest news on Tata Electronics", "What's happening with Kaynes Semicon?", "Recent OSAT investments in India"],
            "VLSI Tutor": ["Explain what a flip-flop is", "Difference between combinational and sequential logic", "Teach me Verilog basics"],
            "Business Ops": ["OSAT India vs Taiwan comparison", "How to evaluate a vendor's reliability?", "Key risks in semiconductor supply chains"],
            "Learning Path": ["I'm a complete beginner, where do I start?", "What is a semiconductor?", "Guide me from basics to VLSI"]
        }
        st.write("Try asking:")
        cols = st.columns(len(examples[mode]))
        for col, ex in zip(cols, examples[mode]):
            if col.button(ex, use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": ex})
                with st.spinner("Thinking..."):
                    try:
                        response = st.session_state.chat.send_message(ex)
                        answer = response.text
                    except Exception as e:
                        answer = get_friendly_error(e)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

    avatars = {"user": "🧑", "assistant": "🔌"}
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask something...")
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=avatars["user"]):
            st.write(user_input)

        with st.chat_message("assistant", avatar=avatars["assistant"]):
            with st.spinner("Thinking..."):
                try:
                    response = st.session_state.chat.send_message(user_input)
                    answer = response.text
                except Exception as e:
                    answer = get_friendly_error(e)
            st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})

st.sidebar.divider()
if st.sidebar.button("🔄 Clear conversation"):
    st.session_state.messages = []
    st.session_state.pop("chat", None)
    st.rerun()

st.sidebar.divider()
st.sidebar.subheader("💬 Feedback")
st.sidebar.write("Help shape what SemiConnect becomes next:")
st.sidebar.link_button("Share your feedback", "https://docs.google.com/forms/d/e/1FAIpQLSdsaegorN8MwUMLLjgehV7ddzwr5oTGIK6xH3BauSvz3bSGww/viewform?usp=publish-editor")

st.sidebar.divider()
st.sidebar.caption("Built with Python, Gemini API & DuckDuckGo search — 100% free tools")
st.sidebar.caption("[GitHub](https://github.com/oswalrushab26/semiconnect-ai-agent)")
