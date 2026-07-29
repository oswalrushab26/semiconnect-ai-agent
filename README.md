🔗 **Live demo:** https://semiconnect-ai-agent-ffgcjcy8kgxjhu9aqfhxei.streamlit.app/

# SemiConnect — Semiconductor Industry AI Agent

An AI agent built for the semiconductor industry, combining live market intelligence, 
a VLSI/Verilog learning tutor, and business operations analysis in one multi-mode 
Python agent.

## What it does

SemiConnect operates in three specialist modes:

- **Market Intelligence** — tracks live news on OSAT, fab investments, and 
  semiconductor supply chain developments using real-time web search
- **VLSI Tutor** — teaches digital electronics and Verilog concepts step by step, 
  breaking down topics with analogies and comprehension checks
- **Business Ops** — analyzes vendors, sourcing decisions, and supply chain strategy 
  from a practical operations standpoint

## How it works

- Built in Python using the Gemini API (`gemini-flash-latest`)
- Custom web search tool using DuckDuckGo (`ddgs`) — no paid search API required
- Mode-based system prompts route the agent's persona and focus area
- API key managed securely via environment variables (`.env`, excluded from repo)

## Tech stack

- Python
- Google Gemini API (`google-genai`)
- DuckDuckGo Search (`ddgs`)
- python-dotenv

## Why I built this

I'm building toward a career in semiconductor/OSAT business operations, and wanted 
hands-on experience with agentic AI applied directly to the industry I'm targeting — 
combining market awareness, technical (VLSI) fluency, and operational analysis in 
one tool.

## Setup

1. Clone the repo
2. pip install -r requirements.txt
3. Create a `.env` file with `GEMINI_API_KEY=your_key_here`
4. Run `agent_test.py`

## Web Interface

Run the Streamlit interface for a proper chat UI instead of the terminal:
```
py -m streamlit run app.py
```

## Author

Rushab Oswal — [www.linkedin.com/in/rushab-oswal-143776239]