# 🧠 Jarvis – AI Voice Assistant  

Jarvis is a Python-based **AI Voice Assistant** inspired by Iron Man’s J.A.R.V.I.S.  
It can talk with you in real-time, answer questions, search the web, open apps, and even generate images.  

---

## 🚀 Features  
- 🎙️ Voice commands with speech recognition and text-to-speech  
- 🤖 AI-powered answers (Groq LLaMA3, Cohere, Hugging Face models)  
- 🔍 Real-time web search & summaries  
- 🖼️ Image generation (Stable Diffusion XL)  
- 📂 PDF Question Answering (RAG)  
- 🖥️ Simple PyQt5 GUI with mic control  
- ⚡ Runs multiple tasks at once (threading)  
- 📊 Power BI dashboards for insights  
- 🛠️ System automation (open apps, send mails, etc.)  

---

## 🏗️ Tech Stack  
- **Python** – main language  
- **PyQt5, OpenCV, Selenium** – GUI & automation  
- **SpeechRecognition, Edge-TTS** – voice interaction  
- **Groq, Cohere, Hugging Face, LangChain** – AI models  
- **Stable Diffusion XL** – image generation  
- **SQL/MySQL, Power BI** – data & analytics  

---

## 📂 Project Structure  
Jarvis/
│── Frontend/ (GUI + Files)
│── Backend/ (Main, Model, Search, Automation)
│── README.md


---

## ⚡ How to Run  

1. Clone the repo:  
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis


Install dependencies:

pip install -r requirements.txt


Add your API keys in a .env file:

GROQ_API_KEY=your_key
COHERE_API_KEY=your_key
HF_API_KEY=your_key


Run the assistant:

python Main.py
