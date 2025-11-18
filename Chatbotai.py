import streamlit as st
import google.generativeai as genai
import openai
import requests
import json
import os
import imghdr
from PIL import Image
import io
import base64
import smtplib
import ssl
from email.message import EmailMessage
import traceback

# -------------------- API KEY SETUP -------------------- #
GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY")
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# -------------------- FILE STORAGE -------------------- #
history_file = "chat_history.json"
users_file = "users.json"

# -------------------- LOAD USERS & HISTORY -------------------- #
if os.path.exists(users_file):
    with open(users_file, "r") as file:
        users = json.load(file)
else:
    users = {}

if os.path.exists(history_file):
    with open(history_file, "r") as f:
        chat_history = json.load(f)
else:
    chat_history = {}

# -------------------- SESSION STATE INIT -------------------- #
for key, val in {
    "logged_in": False, "username": None,
    "current_chat": None, "new_chat_pending": False,
    "ai_mode": "Gemini"
}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -------------------- AUTHENTICATION -------------------- #
if not st.session_state.logged_in:
    st.title("Welcome to ChatBot")
    option = st.radio("Login or Sign Up", ["Login", "Sign Up"], horizontal=True)

    # --- SIGN UP ---
    if option == "Sign Up":
        new_username = st.text_input("Create Username")
        new_password = st.text_input("Create Password", type="password")

        st.markdown("### 📧 Optional Mail Mode Setup")
        email_user = st.text_input("Your Gmail Address (for sending mails)")
        email_pass = st.text_input("App Password (not your normal password)", type="password")

        if st.button("Sign Up"):
            if new_username in users:
                st.error("Username already exists. Try another.")
            elif not new_username or not new_password:
                st.warning("Please fill in both username and password.")
            else:
                users[new_username] = {
                    "password": new_password,
                    "email": email_user,
                    "email_password": email_pass
                }
                with open(users_file, "w") as file:
                    json.dump(users, file, indent=4)
                st.success("Account created successfully! You can now log in.")
                st.rerun()

    # --- LOGIN ---
    elif option == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username]["password"] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome back, {username}!")
                st.rerun()
            else:
                st.error("Invalid username or password.")

    st.stop()

# -------------------- SIDEBAR -------------------- #
st.sidebar.success(f"Logged in as: {st.session_state.username}")
if st.sidebar.button("Logout"):
    for key in ["logged_in", "username", "current_chat"]:
        st.session_state[key] = None
    st.rerun()

st.sidebar.subheader("😊 AI Mode")
st.session_state.ai_mode = st.sidebar.radio("Choose AI Model", ["Gemini", "OpenAI"], horizontal=True)

st.sidebar.subheader("🎨 Response Style")
style = st.sidebar.radio("Choose Style", ["Professional", "Funnier", "Kid"], horizontal=True)

# --- AI Duo toggle ---
st.sidebar.markdown("---")
st.sidebar.header("🤖 AI Duo (optional)")
if "duo_mode" not in st.session_state:
    st.session_state.duo_mode = False
st.session_state.duo_mode = st.sidebar.checkbox("Enable AI Duo Mode (Gemini vs OpenAI)", value=st.session_state.duo_mode)

# -------------------- TITLE -------------------- #
st.title("💬 AI Chatbot with Image, Mail & Mode Switch")

# -------------------- CHAT HISTORY UI -------------------- #
user_chats = chat_history.get(st.session_state.username, {})

st.sidebar.header("Chat Options")
if st.sidebar.button("➕ Create New Chat"):
    new_chat_name = f"Chat {len(user_chats) + 1}"
    user_chats[new_chat_name] = []
    st.session_state.current_chat = new_chat_name
    chat_history[st.session_state.username] = user_chats
    with open(history_file, "w") as f:
        json.dump(chat_history, f)
    st.rerun()

if user_chats:
    selected = st.sidebar.radio("Select Chat", list(user_chats.keys()), index=0)
    st.session_state.current_chat = selected
    if st.sidebar.button(f"🗑️ Delete '{selected}'"):
        del user_chats[selected]
        st.session_state.current_chat = list(user_chats.keys())[0] if user_chats else None
        chat_history[st.session_state.username] = user_chats
        with open(history_file, "w") as f:
            json.dump(chat_history, f)
        st.sidebar.warning(f"Chat '{selected}' deleted!")
        st.rerun()

# -------------------- DISPLAY CHAT -------------------- #
if st.session_state.current_chat:
    for msg in user_chats[st.session_state.current_chat]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# -------------------- IMAGE UPLOAD -------------------- #
image_file = st.file_uploader("Upload an image", type=["jpg", "png"])

def process_image(image):
    image_bytes = image.read()
    image.seek(0)

    if st.session_state.ai_mode == "OpenAI":
        return "🖼️ OpenAI image input not supported yet."

    elif st.session_state.ai_mode == "Gemini":
        mime_type = f"image/{imghdr.what(None, h=image_bytes)}"
        gemini_input = {
            "inline_data": {
                "mime_type": mime_type,
                "data": base64.b64encode(image_bytes).decode("utf-8")
            }
        }
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content([gemini_input, "Describe this image."], stream=False)
            return response.text
        except Exception as e:
            return f"❌ Gemini Error: {e}"

if image_file:
    st.image(image_file, caption="Uploaded Image", use_column_width=True)
    st.markdown(f"**Image Result:** {process_image(image_file)}")

# -------------------- CHAT INPUT -------------------- #
prompt = st.chat_input("Say something...")

# -------------------- AI RESPONSE -------------------- #
def generate_response(prompt_text, style_choice):
    if style_choice == "Funnier":
        prompt_text = f"Respond in a humorous and witty tone:\n{prompt_text}"
    elif style_choice == "Kid":
        prompt_text = f"Explain in a very simple, friendly, and playful way for a 7-year-old:\n{prompt_text}"
    elif style_choice == "Professional":
        prompt_text = f"Respond in a formal, polished, and professional tone:\n{prompt_text}"

    if st.session_state.ai_mode == "Gemini":
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            return model.generate_content(prompt_text).text
        except Exception as e:
            return f"❌ Gemini Error: {e}"

    elif st.session_state.ai_mode == "OpenAI":
        openai_models_to_try = ["gpt-4o-mini", "gpt-3.5-turbo"]
        last_exc = None
        for m in openai_models_to_try:
            try:
                res = openai.chat.completions.create(
                    model=m,
                    messages=[{"role": "user", "content": prompt_text}]
                )
                return res.choices[0].message.content
            except Exception as e:
                last_exc = e
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")
            return model.generate_content(prompt_text).text
        except Exception as ge:
            return f"❌ OpenAI error: {last_exc}\n❌ Gemini fallback error: {ge}"

    return "⚠️ Unsupported AI mode selected."

# -------------------- PROCESS CHAT -------------------- #
if prompt and st.session_state.current_chat:
    response_text = generate_response(prompt, style)

    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Save conversation
    user_chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
    user_chats[st.session_state.current_chat].append({"role": "assistant", "content": response_text})
    chat_history[st.session_state.username] = user_chats

    with open(history_file, "w") as f:
        json.dump(chat_history, f)

# -------------------- AI DUO MODE (Debate) - Read-only outputs ----------
# (Only one Duo block; toggle is in sidebar)
for k in ["duo_last_prompt", "duo_gemini", "duo_openai", "duo_synthesis"]:
    if k not in st.session_state:
        st.session_state[k] = ""

if st.session_state.duo_mode:
    st.markdown("## 🤼‍♂️ AI Duo — Gemini vs GPT-4o-mini (Debate Mode)")
    st.info("Enter a question or topic. Both models will respond. Use 'Synthesize' to create a final conclusion.")

    # Prompt input
    duo_prompt = st.text_area("Enter the debate prompt", value=st.session_state.duo_last_prompt, height=80, key="duo_prompt_area")

    # Actions row
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("🔥 Run Debate"):
            if not duo_prompt.strip():
                st.warning("Please enter a prompt to run the debate.")
            else:
                st.session_state.duo_last_prompt = duo_prompt

                # Gemini response
                try:
                    gem_model = genai.GenerativeModel("gemini-2.5-flash")
                    st.session_state.duo_gemini = gem_model.generate_content(duo_prompt).text
                except Exception as e:
                    st.session_state.duo_gemini = f"❌ Gemini error: {e}"

                # OpenAI response (GPT-4o-mini with fallback)
                try:
                    res = openai.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": duo_prompt}]
                    )
                    st.session_state.duo_openai = res.choices[0].message.content
                except Exception as e:
                    # try cheaper model before failing
                    try:
                        res = openai.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": duo_prompt}]
                        )
                        st.session_state.duo_openai = res.choices[0].message.content
                    except Exception as e2:
                        st.session_state.duo_openai = f"❌ OpenAI error: {e2}"

    with c2:
        if st.button("🔄 Clear Outputs"):
            st.session_state.duo_last_prompt = ""
            st.session_state.duo_gemini = ""
            st.session_state.duo_openai = ""
            st.session_state.duo_synthesis = ""
    with c3:
        if st.button("🗂 Save to Chat History"):
            if st.session_state.get("current_chat") and st.session_state.get("username"):
                chats = chat_history.get(st.session_state.username, {})
                cur = st.session_state.current_chat
                chats.setdefault(cur, [])
                chats[cur].append({"role": "user", "content": "[Duo Prompt] " + st.session_state.duo_last_prompt})
                chats[cur].append({"role": "assistant", "content": "[Gemini] " + st.session_state.duo_gemini})
                chats[cur].append({"role": "assistant", "content": "[OpenAI] " + st.session_state.duo_openai})
                chat_history[st.session_state.username] = chats
                with open(history_file, "w") as f:
                    json.dump(chat_history, f)
                st.success("✅ Debate saved to chat history.")
            else:
                st.warning("⚠️ No active chat or user session to save history.")

    # Read-only model outputs (use expanders)
    st.markdown("### 🔎 Model Responses (read-only)")
    left, right = st.columns(2)
    with left:
        st.subheader("Gemini")
        if st.session_state.duo_gemini:
            with st.expander("Show Gemini response", expanded=True):
                st.markdown(st.session_state.duo_gemini)
        else:
            st.info("No Gemini output yet.")
    with right:
        st.subheader("OpenAI (GPT-4o-mini)")
        if st.session_state.duo_openai:
            with st.expander("Show OpenAI response", expanded=True):
                st.markdown(st.session_state.duo_openai)
        else:
            st.info("No OpenAI output yet.")

    # Synthesis option
    st.markdown("### 🧩 Synthesize / Neutral Conclusion")
    st.caption("Synthesize both model outputs into a short, balanced conclusion using Gemini.")
    synth_col = st.columns([3, 1])
    with synth_col[0]:
        synth_instruction = st.text_area(
            "Synthesis instruction (optional)",
            value="Summarize the two responses in 2–4 sentences and provide a balanced conclusion.",
            height=80,
            key="synth_inst"
        )
    with synth_col[1]:
        if st.button("✅ Synthesize"):
            if not (st.session_state.duo_gemini or st.session_state.duo_openai):
                st.warning("Run the debate first to get both model outputs.")
            else:
                synth_prompt = (
                    "You are asked to synthesize two model responses. "
                    "Here is the Gemini output:\n\n"
                    f"{st.session_state.duo_gemini}\n\n"
                    "Here is the OpenAI output:\n\n"
                    f"{st.session_state.duo_openai}\n\n"
                    f"Instruction: {synth_instruction}\n\nProvide a short, balanced synthesis and final takeaway."
                )
                try:
                    synth_model = genai.GenerativeModel("gemini-2.5-flash")
                    st.session_state.duo_synthesis = synth_model.generate_content(synth_prompt).text
                except Exception as e:
                    st.session_state.duo_synthesis = f"❌ Synthesis error: {e}"

    if st.session_state.duo_synthesis:
        st.markdown("#### Synthesis")
        with st.expander("Show synthesis", expanded=True):
            st.markdown(st.session_state.duo_synthesis)

    st.markdown("---")
    st.info("Tip: Run the debate, compare styles, then synthesize for a final answer.")

# ============================================================
#                      📬 MAIL MODE
# ============================================================
# -------------------- MAIL MODE (fixed: removed st.stop so Edit tab renders) --------------------
if "mail_mode" not in st.session_state:
    st.session_state.mail_mode = False
if "editable_mail_body" not in st.session_state:
    st.session_state.editable_mail_body = ""
if "email_signature" not in st.session_state:
    st.session_state.email_signature = ""
if "mail_tab" not in st.session_state:
    st.session_state.mail_tab = "Compose"

st.sidebar.markdown("---")
st.sidebar.header("📬 Mail Mode")
st.session_state.mail_mode = st.sidebar.checkbox("Enable Mail Mode", value=st.session_state.mail_mode)

if st.session_state.mail_mode:
    st.sidebar.info("Mail Mode Active — compose and edit emails easily.")
    recipient = st.sidebar.text_input("Recipient Email Address", key="mail_recipient")
    subject = st.sidebar.text_input("Subject", key="mail_subject")
    dear_name = st.sidebar.text_input("Dear (Greeting Name)", key="mail_dear")

    st.sidebar.markdown("### ✍️ Signature")
    signature_input = st.sidebar.text_area(
        "Your Email Signature:",
        value=st.session_state.email_signature,
        height=100,
        key="signature_editor"
    )

    if st.sidebar.button("💾 Save Signature"):
        st.session_state.email_signature = signature_input
        st.sidebar.success("✅ Signature saved successfully!")

    tabs = st.tabs(["✉️ Compose", "📝 Edit & Send"])

    # ---------------- Compose tab: generate body from prompt (prompt is the chat input) ----------------
    with tabs[0]:
        st.markdown("### ✉️ Compose Your Mail Idea")
        st.info("Type what your mail should say in the main chat box. The generated body will appear here (without greeting/signature).")

        # Only generate when there's a prompt; DO NOT stop the script afterwards.
        if prompt:
            with st.chat_message("user"):
                st.markdown(prompt)

            mail_prompt = (
                "Write a professional email body for the following request. "
                "Do NOT include greetings (like 'Dear', 'Hi') or signature.\n\n"
                f"Request: {prompt}"
            )
            with st.chat_message("assistant"):
                try:
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    response = model.generate_content(mail_prompt)
                    mail_body = (response.text or "").strip()
                    st.session_state.editable_mail_body = mail_body
                    st.success("✅ Email body generated. Switch to '📝 Edit & Send' to review or modify it.")
                    st.markdown(mail_body if mail_body else "_(No text returned by the model.)_")
                except Exception as e:
                    st.error(f"❌ Gemini error: {str(e)}")

    # ---------------- Edit & Send tab: editable field and send button ----------------
    with tabs[1]:
        st.markdown("### 📝 Review, Edit, and Send")
        st.session_state.editable_mail_body = st.text_area(
            "Edit your email body before sending:",
            value=st.session_state.editable_mail_body,
            height=300,
            key="editable_mail_body_area"
        )

        if st.button("📤 Send Email Now"):
            body_to_send = st.session_state.editable_mail_body.strip()
            if not body_to_send:
                st.warning("⚠️ Please generate or edit your email body first.")
            else:
                username = st.session_state.username
                user_data = users.get(username, {})
                EMAIL_USER = user_data.get("email", "")
                EMAIL_PASSWORD = user_data.get("email_password", "")


                if not EMAIL_USER or not EMAIL_PASSWORD:
                    st.error("❌ Missing EMAIL_USER or EMAIL_PASSWORD in .streamlit/secrets.toml")
                elif not recipient:
                    st.error("❌ Please enter a recipient email address in the sidebar.")
                else:
                    try:
                        greeting = f"Dear {dear_name},\n\n" if dear_name else ""
                        final_mail = f"{greeting}{body_to_send}\n\n{st.session_state.email_signature}"

                        msg = EmailMessage()
                        msg["From"] = EMAIL_USER
                        msg["To"] = recipient
                        msg["Subject"] = subject
                        msg.set_content(final_mail)

                        context = ssl.create_default_context()
                        with smtplib.SMTP("smtp.gmail.com", 587) as server:
                            server.starttls(context=context)
                            server.login(EMAIL_USER, EMAIL_PASSWORD)
                            server.send_message(msg)

                        st.success(f"✅ Email sent successfully to {recipient}")
                        st.session_state.editable_mail_body = ""
                    except Exception as e:
                        st.error(f"❌ Failed to send email: {str(e)}")
                        st.text(traceback.format_exc())
# -------------------- END MAIL MODE --------------------
