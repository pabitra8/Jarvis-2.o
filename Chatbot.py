import os
import datetime
from json import load, dump
from dotenv import dotenv_values
from groq import Groq

# ------------------------ Environment ------------------------
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Assistant")
GroqAPIKey = env_vars.get("GroqAPIKey")

client = Groq(api_key=GroqAPIKey)

# ------------------------ Paths ------------------------
os.makedirs("Data", exist_ok=True)
CHAT_LOG_PATH = os.path.join("Data", "ChatLog.json")

# ------------------------ System Message ------------------------
SystemPrompt = f"""Hello, I am {Username}, You are a very accurate and advanced AI chatbot named {Assistantname} which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

SystemChatBot = [
    {"role": "system", "content": SystemPrompt}
]

# ------------------------ Utilities ------------------------

def RealtimeInformation():
    now = datetime.datetime.now()
    return (
        f"Please use this real-time information if needed,\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H')} hours : {now.strftime('%M')} minutes : {now.strftime('%S')} seconds.\n"
    )

def AnswerModifier(answer):
    return '\n'.join(line for line in answer.split('\n') if line.strip())

def LoadChatLog():
    try:
        with open(CHAT_LOG_PATH, "r", encoding="utf-8") as f:
            return load(f)
    except (FileNotFoundError, ValueError):
        return []

def SaveChatLog(messages):
    with open(CHAT_LOG_PATH, "w", encoding="utf-8") as f:
        dump(messages, f, indent=4)

# ------------------------ ChatBot Function ------------------------

def ChatBot(query):
    try:
        messages = LoadChatLog()
        messages.append({"role": "user", "content": query})

        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=SystemChatBot + [{"role": "system", "content": RealtimeInformation()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True
        )

        Answer = ""
        for chunk in response:
            content = getattr(chunk.choices[0].delta, "content", "")
            if content:
                Answer += content

        Answer = Answer.replace("</s>", "").strip()
        messages.append({"role": "assistant", "content": Answer})
        SaveChatLog(messages)

        return AnswerModifier(Answer)

    except Exception as e:
        print(f"[ERROR] ChatBot failed: {e}")
        return "Sorry, something went wrong while processing your request."

# ------------------------ Manual Test (Optional) ------------------------

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print(f"{Assistantname}:", ChatBot(user_input))
