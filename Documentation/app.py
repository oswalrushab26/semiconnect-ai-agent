import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ddgs import DDGS
import os
from prompts import MARKET_INTEL_PROMPT, VLSI_TUTOR_PROMPT, BUSINESS_OPS_PROMPT

load_dotenv()

def web_search(query: str) -> str:
    """Searches the web and returns a summary of top results."""
    results = DDGS().text(query, max_results=5)
    return "\n\n".join([f"{r['title']}: {r['body']}" for r in results])

st.set_page_config(page_title="SemiConnect", page_icon="🔌", layout="centered")

st.title("🔌 SemiConnect")
st.caption("AI agent for the semiconductor industry — Market Intelligence · VLSI Tutor · Business Ops")

st.sidebar.header("SemiConnect")
st.sidebar.write("Built by Rushab Oswal")
mode = st.sidebar.radio("Choose a mode:", ["Market Intelligence", "VLSI Tutor", "Business Ops"])
st.sidebar.divider()

mode_descriptions = {
    "Market Intelligence": "📊 Live OSAT, fab, and supply chain news",
    "VLSI Tutor": "📚 Step-by-step Verilog & digital electronics",
    "Business Ops": "💼 Vendor, sourcing & supply chain analysis"
}
st.sidebar.info(mode_descriptions[mode])

prompts = {
    "Market Intelligence": MARKET_INTEL_PROMPT,
    "VLSI Tutor": VLSI_TUTOR_PROMPT,
    "Business Ops": BUSINESS_OPS_PROMPT
}

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

if len(st.session_state.messages) == 0:
    st.info(f"👋 You're in **{mode}** mode. Ask me anything to get started.")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask something...")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)
    response = st.session_state.chat.send_message(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    with st.chat_message("assistant"):
        st.write(response.text)

        st.sidebar.divider()
if st.sidebar.button("🔄 Clear conversation"):
    st.session_state.messages = []
    st.session_state.pop("chat", None)
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("Built with Python, Gemini API & DuckDuckGo search — 100% free tools")
st.sidebar.caption("[GitHub](https://github.com/oswalrushab26/semiconnect-ai-agent)")