# 🧠 Jarvis – AI Voice Assistant  

Jarvis is a Python-based **AI Voice Assistant** inspired by Iron Man’s J.A.R.V.I.S.  
It can talk with you in real-time, answer questions, search the web, open apps, and even generate images.  

---
🚀 Features

🎙️ Voice commands with speech recognition and text-to-speech

🤖 AI-powered answers (Groq LLaMA3, Cohere, Hugging Face models)

🔍 Real-time web search & summaries

🖼️ Image generation using Hugging Face Diffusion models

📂 PDF Question Answering (RAG with LangChain)

🖥️ Simple PyQt5 GUI with mic control

⚡ Runs multiple tasks at once (threading)

🌐 Agentic workflows with LangGraph (in progress)

---

## 🏗️ Tech Stack  
- **Python** – main language  
- **PyQt5, OpenCV, Selenium** – GUI & automation  
- **SpeechRecognition, Edge-TTS** – voice interaction  
- **Groq, Cohere, Hugging Face, LangChain** – AI models  
- **Hugging Face Diffusion models** – image generation  

---

## 📂 Project Structure  
Jarvis/
│── Frontend/ (GUI + Files)
│── Backend/ (Main, Model, Search, Automation)
│── README.md


---

## ⚡ How to Run  

1. Clone the repo:  

git clone https://github.com/yourusername/jarvis.git
cd jarvis


2. Install dependencies:

pip install -r requirements.txt


3. Add your API keys in a .env file:

GROQ_API_KEY=your_key
COHERE_API_KEY=your_key
HF_API_KEY=your_key


4. Run the assistant:

python Main.py


## 🎥 Demo Video  

Check out the live demo of **Jarvis – AI Voice Assistant** on YouTube:

[![Jarvis Demo](https://img.youtube.com/vi/FuxLB7d1xaQ/0.jpg)](https://www.youtube.com/watch?v=FuxLB7d1xaQ)

*(Click the thumbnail to watch the video)*



🔥 Currently Working On

📂 RAG (Retrieval-Augmented Generation) improvements

🔗 LangChain integration for better pipelines

🕸️ LangGraph workflows for multi-step reasoning

🤖 Agentic AI (autonomous decision-making agents)
