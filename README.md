ChatMail-Fusion-AI
Dual-AI Chat & Mail Assistant — powered by Gemini and OpenAI

A Streamlit-based multimodal AI assistant that combines Gemini and OpenAI for intelligent chatting, image analysis, debate mode, and automated email composition/sending. The app includes user authentication, chat history management, model switching, and a complete Mail Mode for drafting and sending professional emails.

Features
• Dual AI Model Switching: Choose between Gemini and OpenAI with dynamic style modes (Professional, Funnier, Kid).
• AI Duo Debate Mode: Compare Gemini and OpenAI side-by-side, generate a synthesis, and save outputs to chat history.
• Multimodal Chat: Supports text input, image upload, and styled responses.
• Mail Mode: Generate, edit, and send professional emails directly via Gmail App Password.
• User Login System: Signup/login with secure local storage and personalized chat sessions.
• Persistent Chat History: Create, delete, and switch between multiple chats per user.
• Image Analysis: Upload an image and get descriptive insights powered by Gemini Vision.
• Clean Streamlit Interface: Sidebar controls, expandable sections, and polished UI flow.

Tech Stack
• Streamlit
• Gemini 2.5 Flash
• OpenAI GPT-4o-mini / GPT-3.5
• Python
• SMTP for Email
• PIL (Image Processing)
• Local JSON Storage (users.json, chat_history.json)

Installation
Clone the repository

Create a virtual environment

Install dependencies using pip

Add API keys in .streamlit/secrets.toml

Run the app with: streamlit run app.py

API Key Setup
File: .streamlit/secrets.toml

GEMINI_API_KEY = "your_gemini_key"
OPENAI_API_KEY = "your_openai_key"

Gmail Setup for Mail Mode
• Enable 2-step verification
• Generate a Gmail App Password
• Enter Gmail + App Password during Signup

Run the Application
streamlit run app.py

Project Structure
app.py
users.json (local only — do not commit)
chat_history.json (local only — do not commit)
requirements.txt
README.md

Security Notes
• Add chat_history.json and users.json to .gitignore
• Never commit real chat logs, personal email data, or credentials
• Users must use Gmail App Passwords (not real Gmail passwords)

License
This project is for educational and personal use.
