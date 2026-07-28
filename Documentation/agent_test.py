from dotenv import load_dotenv
import os
from google import genai
from google.genai import types
from prompts import MARKET_INTEL_PROMPT, VLSI_TUTOR_PROMPT, BUSINESS_OPS_PROMPT
from ddgs import DDGS

def web_search(query: str) -> str:
    """Searches the web and returns a summary of top results."""
    results = DDGS().text(query, max_results=5)
    combined = "\n\n".join([f"{r['title']}: {r['body']}" for r in results])
    return combined

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
print("1. Market News mode")
print("2. VLSI Tutor mode")
print("3. Business Ops mode")
choice = input("Pick 1, 2, or 3: ")

if choice == "2":
    system_instruction = VLSI_TUTOR_PROMPT
elif choice == "3":
    system_instruction = BUSINESS_OPS_PROMPT
else:
    system_instruction = MARKET_INTEL_PROMPT

chat = client.chats.create(
    model="gemini-flash-latest",
    config=types.GenerateContentConfig(
        system_instruction=system_instruction,
        tools=[web_search]
    )
)

print("SemiConnect is ready. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    response = chat.send_message(user_input)
    print("\nSemiConnect:", response.text, "\n")