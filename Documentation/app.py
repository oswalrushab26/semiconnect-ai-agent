import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ddgs import DDGS
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

st.title("🔌 SemiConnect")
st.caption("AI agent for the semiconductor industry — Market Intelligence · VLSI Tutor · Business Ops")

tab_chat, tab_about = st.tabs(["💬 Chat", "ℹ️ About"])

with tab_about:
    st.subheader("What is SemiConnect?")
    st.write("""
    SemiConnect is an AI agent built for the semiconductor industry, with three specialist modes:
    
    - **Market Intelligence** — live news on OSAT, fab investments, and supply chain shifts
    - **VLSI Tutor** — step-by-step teaching of Verilog and digital electronics
    - **Business Ops** — vendor, sourcing, and supply chain strategy analysis
    
    Built by Rushab Oswal using free tools: Python, Gemini API, and DuckDuckGo search.
    """)
    st.link_button("View source on GitHub", "https://github.com/oswalrushab26/semiconnect-ai-agent")


st.sidebar.header("SemiConnect")
st.sidebar.write("Built by Rushab Oswal")
mode = st.sidebar.radio("Choose a mode:", ["Market Intelligence", "VLSI Tutor", "Business Ops", "Learning Path"])
st.sidebar.divider()

mode_descriptions = {
    "Market Intelligence": "📊 Live OSAT, fab, and supply chain news",
    "VLSI Tutor": "📚 Step-by-step Verilog & digital electronics",
    "Business Ops": "💼 Vendor, sourcing & supply chain analysis",
    "Learning Path": "🎓 Zero to pro: guided semiconductor learning"
}

st.sidebar.info(mode_descriptions[mode])

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

learning_topics = [
    "What is a semiconductor?",
    "Basic electronics: voltage, current, transistors",
    "Digital logic: gates and boolean logic",
    "Sequential logic: flip-flops and memory",
    "Introduction to Verilog",
    "Semiconductor industry overview: fab, OSAT, packaging"
]


if "chat" not in st.session_state or st.session_state.get("mode") != mode:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    st.session_state.chat = client.chats.create(
        model="gemini-flash-latest",
        config=types.GenerateContentConfig(
            system_instruction=prompts[mode],
            tools=[web_search]
        )
    )
    st.session_state.mode = mode
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = []

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
                        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                            answer = "⏳ SemiConnect is getting a lot of use right now. Please try again shortly."
                        else:
                            answer = "⚠️ Something went wrong. Please try again."
                st.session_state.messages.append({"role": "assistant", "content": answer})
                st.rerun()

    avatars = {"user": "🧑", "assistant": "🔌"}
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
            st.write(msg["content"])

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
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        answer = "⏳ SemiConnect is getting a lot of use right now and has hit its free-tier limit. Please try again in a few minutes, or come back tomorrow — thanks for your patience!"
                    else:
                        answer = "⚠️ Something went wrong on my end. Please try rephrasing your question or try again shortly."
            st.write(answer)

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