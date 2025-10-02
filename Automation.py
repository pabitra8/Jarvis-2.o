import os
import asyncio
import subprocess
import webbrowser
import requests
import keyboard
import logging

from dotenv import dotenv_values
from bs4 import BeautifulSoup
from AppOpener import close, open as appopen
from pywhatkit import search, playonyt
from rich import print
from groq import Groq

# ---------------------- Setup ----------------------
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
Username = env_vars.get("Username", "User")

client = Groq(api_key=GroqAPIKey)
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

messages = []
SystemChatBot = [{
    'role': "system",
    "content": f"Hello, I am {Username}. You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."
}]

# ---------------------- Core Functionalities ----------------------

def GoogleSearch(topic):
    search(topic)
    return True

def YouTubeSearch(topic):
    webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
    return True

def PlayYoutube(query):
    playonyt(query)
    return True

def OpenApp(app_name, sess=requests.session()):
    try:
        appopen(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        logging.warning(f"[WARNING] App open failed: {app_name.upper()} is not running. Trying web fallback...")
        def extract_links(html):
            soup = BeautifulSoup(html, 'html.parser')
            return [a.get('href') for a in soup.find_all('a', {'jsname': 'UWCkhb'})]

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response = sess.get(url, headers=headers)
            return response.text if response.status_code == 200 else None

        html = search_google(app_name)
        if html:
            links = extract_links(html)
            if links:
                webbrowser.open(links[0])
        return True

def CloseApp(app_name):
    if "chrome" in app_name.lower():
        return False
    try:
        close(app_name, match_closest=True, output=True, throw_error=True)
        return True
    except:
        return False

def System(command):
    actions = {
        "mute": lambda: keyboard.press_and_release("volume mute"),
        "unmute": lambda: keyboard.press_and_release("volume mute"),
        "volume up": lambda: keyboard.press_and_release("volume up"),
        "volume down": lambda: keyboard.press_and_release("volume down"),
    }
    action = actions.get(command)
    if action:
        action()
    return True

def Content(prompt):
    def open_notepad(file_path):
        subprocess.Popen(['notepad.exe', file_path])

    def content_writer_ai(prompt):
        try:
            messages.append({"role": "user", "content": prompt})
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=SystemChatBot + messages,
                max_tokens=2048,
                temperature=0.7,
                top_p=1,
                stream=True,
                stop=None
            )

            answer = ""
            for chunk in completion:
                content = getattr(chunk.choices[0].delta, "content", "")
                if content:
                    answer += content

            messages.append({"role": "assistant", "content": answer})
            return answer.strip()

        except Exception as e:
            logging.error(f"[ERROR] Content AI generation failed: {e}")
            return "Content generation failed."

    os.makedirs("Data", exist_ok=True)
    file_name = prompt.lower().replace(" ", "") + ".txt"
    file_path = os.path.join("Data", file_name)

    answer = content_writer_ai(prompt)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(answer)

    open_notepad(file_path)
    return True

# ---------------------- Async Logic ----------------------

async def TranslateAndExecute(commands: list[str]):
    tasks = []
    for command in commands:
        cmd = command.strip().lower()

        if cmd.startswith("open ") and cmd not in ["open it", "open file"]:
            tasks.append(asyncio.to_thread(OpenApp, cmd.removeprefix("open ")))

        elif cmd.startswith("close "):
            tasks.append(asyncio.to_thread(CloseApp, cmd.removeprefix("close ")))

        elif cmd.startswith("play "):
            tasks.append(asyncio.to_thread(PlayYoutube, cmd.removeprefix("play ")))

        elif cmd.startswith("content "):
            tasks.append(asyncio.to_thread(Content, cmd.removeprefix("content ")))

        elif cmd.startswith("google search "):
            tasks.append(asyncio.to_thread(GoogleSearch, cmd.removeprefix("google search ")))

        elif cmd.startswith("youtube search "):
            tasks.append(asyncio.to_thread(YouTubeSearch, cmd.removeprefix("youtube search ")))

        elif cmd.startswith("system "):
            tasks.append(asyncio.to_thread(System, cmd.removeprefix("system ")))

        else:
            logging.info(f"[SKIPPED] Unknown automation command: {command}")

    await asyncio.gather(*tasks)

async def Automation(commands: list[str]):
    await TranslateAndExecute(commands)
    return True

# ---------------------- Local Test Mode ----------------------

if __name__ == "__main__":
    print(">> Jarvis Automation CLI Test Mode\n→ Try: open notepad, play despacito, content my village essay")
    while True:
        cmd = input(">>> ")
        if cmd.lower() in ["exit", "quit"]:
            break
        asyncio.run(Automation([cmd]))
