import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import mtranslate as mt

# Load environment variables
load_dotenv()
InputLanguage = os.getenv("InputLanguage", "en-US")

# Ensure required folders exist
os.makedirs("Data", exist_ok=True)
os.makedirs(os.path.join("Frontend", "Files"), exist_ok=True)

# Write Voice.html for browser-based speech recognition
HtmlCode = '''<!DOCTYPE html>
<html lang="en">
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <p id="output"></p>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new webkitSpeechRecognition() || new SpeechRecognition();
            recognition.lang = '';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>'''

# Save HTML to Data folder
voice_html_path = os.path.join("Data", "Voice.html")
with open(voice_html_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Chrome browser setup (not headless!)
chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# DO NOT use headless mode — WebSpeech API won't work
# chrome_options.add_argument("--headless=new")  # <-- Commented out

# Initialize driver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

TempDirPath = os.path.join("Frontend", "Files")
voice_html_url = "file://" + os.path.abspath(voice_html_path)

def SetAssistantStatus(status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as f:
        f.write(status)

def QueryModifier(query):
    query = query.strip().lower()
    query_words = query.split()
    question_keywords = ["how", "what", "where", "when", "why", "which", "whose", "whom", "can you", "what's", "where's", "how's"]

    if not query:
        return ""

    ends_with_punct = query[-1]
    if any(query.startswith(word) for word in question_keywords):
        if ends_with_punct not in ["?", ".", "!"]:
            query += "?"
    else:
        if ends_with_punct not in ["?", ".", "!"]:
            query += "."

    return query.capitalize()

def UniversalTranslator(text):
    try:
        translated = mt.translate(text, "en", "auto")
        return translated.capitalize()
    except Exception:
        return text.capitalize()

def SpeechRecognition():
    print("[INFO] Launching browser and starting voice recognition...")
    driver.get(voice_html_url)
    sleep(1)  # Allow HTML/JS to load
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            text = driver.find_element(By.ID, "output").text.strip()
            if text:
                print(f"[INFO] Recognized text: {text}")
                driver.find_element(By.ID, "end").click()
                sleep(0.5)
                if "en" in InputLanguage.lower():
                    return QueryModifier(text)
                else:
                    SetAssistantStatus("Translating ...")
                    return QueryModifier(UniversalTranslator(text))
        except Exception:
            pass
        sleep(0.5)

# Manual
