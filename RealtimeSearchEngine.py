import os
import datetime
from json import load, dump
from dotenv import load_dotenv
from googlesearch import search
from groq import Groq

# Load environment variables
load_dotenv()
Username = os.getenv("Username", "User")
Assistantname = os.getenv("Assistantname", "AI Assistant")
GroqAPIKey = os.getenv("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# Ensure Data directory exists
os.makedirs("Data", exist_ok=True)
chatlog_path = os.path.join("Data", "ChatLog.json")

# Initial system prompt
System = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
*** Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

def Information():
    now = datetime.datetime.now()
    return (
        f"Use This Real-time Information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours, {now.strftime('%M')} minutes, {now.strftime('%S')} seconds.\n"
    )

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    return '\n'.join([line for line in lines if line.strip()])

def GoogleSearch(query):
    try:
        results = list(search(query, advanced=True, num_results=5))
    except Exception as e:
        return f"Search failed: {e}"

    Answer = f"The search results for '{query}' are:\n[start]\n"
    for i in results:
        Answer += f"Title: {i.title}\nDescription: {i.description}\n\n"
    Answer += "[end]"
    return Answer

def RealtimeSearchEngine(prompt):
    # Load past chat log
    try:
        with open(chatlog_path, "r", encoding="utf-8") as f:
            messages = load(f)
    except (FileNotFoundError, ValueError):
        messages = []

    messages.append({"role": "user", "content": prompt})

    # Dynamic context with each run
    system_messages = [
        {"role": "system", "content": System},
        {"role": "user", "content": "Hi"},
        {"role": "assistant", "content": "Hello, how can I help you?"},
        {"role": "system", "content": GoogleSearch(prompt)},
        {"role": "system", "content": Information()}
    ]

    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=system_messages + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
        stop=None
    )

    Answer = ""
    for chunk in completion:
        content = getattr(chunk.choices[0].delta, "content", "")
        if content:
            Answer += content

    Answer = Answer.replace("</s>", "").strip()
    messages.append({"role": "assistant", "content": Answer})

    with open(chatlog_path, "w", encoding="utf-8") as f:
        dump(messages, f, indent=4)

    return AnswerModifier(Answer)

# Command-line interface
if __name__ == "__main__":
    while True:
        prompt = input("Enter your query: ")
        print(RealtimeSearchEngine(prompt))
