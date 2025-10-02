from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)

from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech

from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username")
Assistantname = env_vars.get("Assistantname")

# Default greeting message
DefaultMessage = f'''{Username} : Hello {Assistantname}, How are you?
{Assistantname} : Welcome {Username}. I am doing well. How may I help you?'''

# Background subprocesses (like image generation)
subprocesses = []

# Automation command types
Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

# -----------------------------------
# Initialization Functions
# -----------------------------------

def ShowDefaultChatIfNoChats():
    try:
        with open(r'Data\ChatLog.json', "r", encoding='utf-8') as f:
            if len(f.read().strip()) < 5:
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db:
                    db.write("")
                with open(TempDirectoryPath('Responses.data'), 'w', encoding='utf-8') as res:
                    res.write(DefaultMessage)
    except Exception as e:
        print(f"[ERROR] ShowDefaultChatIfNoChats: {e}")

def ReadChatLogJson():
    try:
        with open(r'Data\ChatLog.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def ChatLogIntegration():
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username} : {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname} : {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as f:
        f.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as f:
            data = f.read().strip()
            if data:
                with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as r:
                    r.write(data)
    except Exception as e:
        print(f"[ERROR] ShowChatsOnGUI: {e}")

def InitialExecution():
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

# -----------------------------------
# Main AI Logic
# -----------------------------------

def MainExecution():
    try:
        SetAssistantStatus("Listening ...")
        Query = SpeechRecognition()

        if not Query.strip():
            return

        ShowTextToScreen(f"{Username} : {Query}")
        SetAssistantStatus("Thinking ...")
        Decision = FirstLayerDMM(Query)

        print(f"\n[DEBUG] Decision: {Decision}\n")

        TaskExecution = False
        ImageExecution = False
        ImageGenerationQuery = ""

        # Classify decisions
        G = any(d.startswith("general") for d in Decision)
        R = any(d.startswith("realtime") for d in Decision)
        MergedQuery = " and ".join(
            ".".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")
        )

        # Trigger image generation
        for query in Decision:
            if "generate" in query:
                ImageGenerationQuery = query
                ImageExecution = True

        # Trigger automation
        for query in Decision:
            if not TaskExecution and any(query.startswith(func) for func in Functions):
                run(Automation(list(Decision)))
                TaskExecution = True

        # Start image generation script
        if ImageExecution:
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write(f"{ImageGenerationQuery},True")
            try:
                process = subprocess.Popen(
                    ['python', r'Backend\ImageGeneration.py'],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    stdin=subprocess.PIPE, shell=False
                )
                subprocesses.append(process)
            except Exception as e:
                print(f"[ERROR] Launching ImageGeneration.py: {e}")

        # Real-time or general response
        if G and R or R:
            SetAssistantStatus("Searching ...")
            Answer = RealtimeSearchEngine(QueryModifier(MergedQuery))
        elif G:
            QueryFinal = next((q.replace("general ", "") for q in Decision if q.startswith("general")), Query)
            Answer = ChatBot(QueryModifier(QueryFinal))
        else:
            return

        ShowTextToScreen(f"{Assistantname} : {Answer}")
        SetAssistantStatus("Answering ...")
        TextToSpeech(Answer)

    except Exception as e:
        print(f"[ERROR] in MainExecution: {e}")

# -----------------------------------
# Threaded Execution
# -----------------------------------

def FirstThread():
    while True:
        if GetMicrophoneStatus() == "True":
            MainExecution()
        else:
            if "Available ..." not in GetAssistantStatus():
                SetAssistantStatus("Available ...")
            sleep(0.1)

def SecondThread():
    GraphicalUserInterface()

# -----------------------------------
# Application Start
# -----------------------------------

if __name__ == "__main__":
    InitialExecution()
    threading.Thread(target=FirstThread, daemon=True).start()
    SecondThread()
