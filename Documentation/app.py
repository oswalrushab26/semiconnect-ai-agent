import re
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv
from ddgs import DDGS
import pandas as pd
import os
from prompts import MARKET_INTEL_PROMPT, VLSI_TUTOR_PROMPT, BUSINESS_OPS_PROMPT, LEARNING_PATH_PROMPT
from home import render_home

def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "styles.css")
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_dotenv()
if "GEMINI_API_KEY" not in os.environ and "GEMINI_API_KEY" in st.secrets:
    os.environ["GEMINI_API_KEY"] = st.secrets["GEMINI_API_KEY"]

_search_cache = {}

def web_search(query: str) -> str:
    """Searches the web and returns a summary of top results."""
    if query in _search_cache:
        return _search_cache[query]
    results = DDGS().text(query, max_results=5)
    combined = "\n\n".join([f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}" for r in results])
    _search_cache[query] = combined
    return combined

st.set_page_config(page_title="SemiConnect", page_icon=chr(0x1F50C), layout="centered")
load_css()

st.title(chr(0x1F50C) + " SemiConnect")
st.caption("AI agent for the semiconductor industry " + chr(0x2014) + " Market Intelligence " + chr(0x00B7) + " VLSI Tutor " + chr(0x00B7) + " Business Ops " + chr(0x00B7) + " Learning Path")

tab_chat, tab_tracker, tab_about = st.tabs(["\U0001F4AC Chat", "\U0001F4C8 Tracker", "\u2139\uFE0F About"])

with tab_about:
    render_home()
    st.write("""
    SemiConnect is an AI agent built for the semiconductor industry, with four specialist modes:

    - **Market Intelligence** — live news on OSAT, fab investments, and supply chain shifts
    - **VLSI Tutor** — step-by-step teaching of Verilog and digital electronics
    - **Business Ops** — vendor, sourcing and semiconductor supply chain strategy analysis, with support for uploading your own CSV/Excel data for direct analysis
    - **Learning Path** — guides complete beginners through semiconductor/VLSI fundamentals, step by step, with progress tracking

    Built by Rushab Oswal using free tools: Python, Gemini API, and DuckDuckGo search.
    """)
    st.link_button("View source on GitHub", "https://github.com/oswalrushab26/semiconnect-ai-agent")

with tab_tracker:
    st.subheader(chr(0x1F4E6) + " Supply Chain Watchlist")
    st.write("Track specific companies and check for the latest news on demand.")

    if "watchlist" not in st.session_state:
        st.session_state.watchlist = []

    new_company = st.text_input("Add a company to track (e.g. Tata Electronics, Kaynes Semicon)")
    if st.button(chr(0x2795) + " Add to watchlist"):
        if new_company and new_company not in st.session_state.watchlist:
            st.session_state.watchlist.append(new_company)
            st.rerun()

    st.divider()

    for company in st.session_state.watchlist:
        col1, col2, col3 = st.columns([3, 2, 1])
        col1.write(f"**{company}**")
        check = col2.button(chr(0x1F50D) + " Check latest", key=f"check_{company}")
        remove = col3.button(chr(0x1F5D1) + chr(0xFE0F), key=f"remove_{company}")

        if check:
            with st.spinner(f"Checking news for {company}..."):
                result = web_search(f"{company} semiconductor news")
            st.write(f"{chr(0x1F4F0)} {result}")

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

learning_objectives = {
    "What is a semiconductor?": [
        "Understand what a semiconductor is",
        "Learn why silicon is commonly used",
        "Compare conductors, insulators, and semiconductors",
        "Understand the basic idea of doping"
    ],
    "Basic electronics: voltage, current, transistors": [
        "Understand voltage, current, and resistance",
        "Learn how a transistor works at a basic level",
        "Understand the transistor as a switch",
        "Connect basic electronics to digital circuits"
    ],
    "Digital logic: gates and boolean logic": [
        "Understand basic logic gates",
        "Learn Boolean expressions",
        "Read and build truth tables",
        "Understand how gates form digital circuits"
    ],
    "Sequential logic: flip-flops and memory": [
        "Understand the difference between combinational and sequential logic",
        "Learn how flip-flops store information",
        "Understand registers and counters",
        "Build intuition for clocked digital systems"
    ],
    "Introduction to Verilog": [
        "Understand what Verilog is used for",
        "Learn basic Verilog syntax",
        "Write simple combinational and sequential RTL",
        "Understand how RTL describes hardware"
    ],
    "Semiconductor industry overview: fab, OSAT, packaging": [
        "Understand the semiconductor manufacturing flow",
        "Learn what a fab does",
        "Understand the role of OSAT companies",
        "Learn the basics of semiconductor packaging"
    ]
}

mode_descriptions = {
    "Market Intelligence": chr(0x1F4CA) + " Live OSAT, fab, and supply chain news",
    "VLSI Tutor": chr(0x1F4DA) + " Step-by-step Verilog & digital electronics",
    "Business Ops": chr(0x1F4BC) + " Vendor, sourcing & supply chain analysis",
    "Learning Path": chr(0x1F393) + " Zero to pro: guided semiconductor learning"
}

st.sidebar.write(mode_descriptions[mode])

uploaded_file = None
if mode == "Business Ops":
    st.sidebar.divider()
    st.sidebar.subheader(chr(0x1F4CE) + " Analyze a file")
    uploaded_file = st.sidebar.file_uploader("Upload vendor/supply data (CSV or Excel)", type=["csv", "xlsx"])

    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.write(f"{chr(0x2705)} Loaded {len(df)} rows")
            st.session_state.file_summary = df.describe(include="all").to_string()
            st.session_state.file_preview = df.head(10).to_string()
        except Exception:
            st.sidebar.write("Couldn't read that file. Try a CSV or Excel file.")

if mode == "Learning Path":
    if "learning_progress" not in st.session_state:
        st.session_state.learning_progress = 0

    completed = st.session_state.learning_progress
    total = len(learning_topics)

    st.sidebar.write("**Your progress:**")
    st.sidebar.progress(completed / total)
    st.sidebar.caption(f"{completed} of {total} topics completed")

    if completed < total:
        current_topic = learning_topics[completed]
        st.sidebar.info(
            f"{chr(0x1F449)} **Current topic**\n\n{current_topic}"
        )

        st.sidebar.write("**By the end of this topic, you should understand:**")
        for objective in learning_objectives[current_topic]:
            st.sidebar.write(f"{chr(0x2022)} {objective}")

        st.sidebar.caption("Ask the VLSI Tutor about this topic to learn it step by step.")
    else:
        st.sidebar.success(
            f"{chr(0x1F389)} **Learning path completed!**\n\nYou have covered all {total} topics."
        )

    for i, topic in enumerate(learning_topics):
        if i < completed:
            st.sidebar.write(f"{chr(0x2705)} {topic}")
        elif i == completed:
            st.sidebar.write(f"{chr(0x1F449)} **{topic}**")
        else:
            st.sidebar.write(f"{chr(0x2B1C)} {topic}")

    if completed < total:
        if st.sidebar.button("Mark current topic complete"):
            st.session_state.learning_progress = completed + 1
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
        model="gemini-flash-lite-latest",
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
        return "SemiConnect is getting a lot of use right now and has hit its free-tier limit. Please try again in a few minutes, or come back tomorrow " + chr(0x2014) + " thanks for your patience!"
    elif "503" in err or "UNAVAILABLE" in err:
        return "The AI service is experiencing high demand right now. Please try again in a moment."
    else:
        return "Something went wrong on my end. Please try rephrasing your question or try again shortly."

with tab_chat:
    if len(st.session_state.messages) == 0:
        st.info(chr(0x1F44B) + f" You're in **{mode}** mode. Ask me anything to get started.")

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
                        answer = re.sub(r'\[svg\]\([^)]*\)', '', answer)
                        answer = re.sub(r'\n{3,}', '\n\n', answer)
                        print(f"DEBUG: Gemini response characters = {len(answer)}")
                    except Exception as e:
                        answer = get_friendly_error(e)
                st.session_state.messages.append({"role": "assistant", "content": re.sub(r'\[svg\]\([^)]*\)', '', re.sub(r'\n{3,}', '\n\n', answer))})
                st.rerun()

    avatars = {"user": "user", "assistant": "assistant"}
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar=avatars[msg["role"]]):
            content = msg["content"]
            content = re.sub(
                r'\[svg\]\([^)]*\)',
                '',
                content,
            )
            st.markdown(content)

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
                    answer = re.sub(r'\[svg\]\([^)]*\)', '', answer)
                    answer = re.sub(r'\n{3,}', '\n\n', answer)
                    print(f"DEBUG: Gemini response characters = {len(answer)}")
                except Exception as e:
                    answer = get_friendly_error(e)
            answer_display = re.sub(
                r'\[svg\]\([^)]*\)',
                '',
                answer,
            )
            st.markdown(answer_display)

        st.session_state.messages.append({"role": "assistant", "content": re.sub(r'\[svg\]\([^)]*\)', '', re.sub(r'\n{3,}', '\n\n', answer))})

if st.sidebar.button(chr(0x1F5D1) + chr(0xFE0F) + " Clear conversation"):
    st.session_state.messages = []
    st.session_state.pop("chat", None)
    st.rerun()
st.sidebar.subheader(chr(0x1F4AC) + " Feedback")
st.sidebar.divider()
st.sidebar.write("Help shape what SemiConnect becomes next:")
st.sidebar.link_button("Share your feedback", "https://docs.google.com/forms/d/e/1FAIpQLSdsaegorN8MwUMLLjgehV7ddzwr5oTGIK6xH3BauSvz3bSGww/viewform?usp=publish-editor")

st.sidebar.divider()
st.sidebar.caption("Built with Python, Gemini API & DuckDuckGo search " + chr(0x2014) + " 100% free tools")
st.sidebar.caption("[GitHub](https://github.com/oswalrushab26/semiconnect-ai-agent)")
