<h1 align="center">💬 AI Chatbot with Multi-Model Support, Image Understanding & Mail Mode</h1>

<p align="center">
  <strong>A fully-featured Streamlit-based AI platform supporting Gemini & OpenAI models, chat history, email generation, image analysis, and dual-model debate mode.</strong>
</p>
<hr/>

<h2>📌 Project Overview</h2>
<p>
This application is a robust AI-powered chatbot equipped with:
</p>

<ul>
  <li>🔐 <strong>User Authentication (Login + Signup)</strong></li>
  <li>💬 <strong>Persistent Chat History per User</strong></li>
  <li>🤖 <strong>AI Model Switching</strong> – Gemini or OpenAI</li>
  <li>🎭 <strong>Response Styles</strong> – Professional, Funnier, Kid Mode</li>
  <li>🖼️ <strong>Image Upload & Description (Gemini Vision)</strong></li>
  <li>📬 <strong>Mail Mode:</strong> Compose, Edit & Send Emails</li>
  <li>⚔️ <strong>AI Duo Debate Mode:</strong> Gemini vs OpenAI comparison</li>
  <li>💾 <strong>Local JSON-based Storage</strong> (users & chat history)</li>
</ul>

<hr/>

<h2>🚀 Features in Detail</h2>

<h3>1️⃣ Authentication System</h3>
<p>Users can create accounts, store email credentials (optional), and log in securely. User data is stored in <code>users.json</code>.</p>

<h3>2️⃣ Chat History</h3>
<p>Each user gets isolated chat sessions saved in <code>chat_history.json</code>. Users can:</p>
<ul>
  <li>Create new chats</li>
  <li>Switch between existing chats</li>
  <li>Delete chats</li>
</ul>

<h3>3️⃣ AI Model Switching</h3>
<p>Supports:</p>
<ul>
  <li><strong>Gemini 2.5 Flash</strong></li>
  <li><strong>OpenAI (GPT-4o-mini, 3.5-turbo fallback)</strong></li>
</ul>

<h3>4️⃣ Response Styles</h3>
<p>Dynamic tone modification:</p>
<ul>
  <li>Professional</li>
  <li>Funnier</li>
  <li>Kid-friendly</li>
</ul>

<h3>5️⃣ Image Analysis</h3>
<p>Users can upload images and get detailed descriptions using Gemini’s vision model.</p>

<h3>6️⃣ Mail Mode</h3>
<p>
A powerful integrated email workflow:
</p>
<ul>
  <li>Compose email ideas using AI</li>
  <li>Edit final email with a rich text area</li>
  <li>Save signatures</li>
  <li>Send mail using Gmail SMTP + App Password</li>
</ul>

<h3>7️⃣ AI Duo — Debate Mode</h3>
<p>
This mode runs both models (Gemini + OpenAI) on the same prompt and displays:
</p>
<ul>
  <li>Separate Gemini & OpenAI responses</li>
  <li>A synthesis generated via Gemini</li>
  <li>Optional save-to-chat</li>
</ul>

<hr/>

<h2>📂 Project Structure</h2>

<pre>
├── app.py (your Streamlit code)
├── users.json
├── chat_history.json
├── requirements.txt
└── README.md
</pre>

<hr/>

<h2>🔧 Installation & Setup</h2>

<h3>1️⃣ Clone the repository</h3>

<pre>
git clone &lt;your-repo-url&gt;
cd &lt;your-repo&gt;
</pre>

<h3>2️⃣ Install dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<h3>3️⃣ Setup Streamlit Secrets</h3>
<p>Create file:</p>

<pre>
.streamlit/secrets.toml
</pre>

<p>Add your API keys:</p>

<pre>
GEMINI_API_KEY="your_key"
OPENAI_API_KEY="your_key"
</pre>

<p>
Email credentials are stored when a user signs up, so they are not needed in secrets.
</p>

<hr/>

<h2>▶️ Run the Application</h2>

<pre>
streamlit run app.py
</pre>

<hr/>

<h2>✨ Usage Guide</h2>

<h3>🔐 Login / Signup</h3>
<p>Create an account and optionally add Gmail + App Password to enable Mail Mode.</p>

<h3>💬 Chat</h3>
<ul>
  <li>Choose Gemini or OpenAI</li>
  <li>Set response style</li>
  <li>Start chatting</li>
  <li>Chats are stored automatically</li>
</ul>

<h3>🖼️ Image Upload</h3>
<p>Upload a JPG/PNG and let Gemini describe it.</p>

<h3>🤖 AI Duo Mode</h3>
<p>Compare both models side-by-side with synthesis.</p>

<h3>📬 Mail Mode Workflow</h3>
<ol>
  <li>Enable Mail Mode in sidebar</li>
  <li>Enter recipient, subject & greeting</li>
  <li>Compose mail idea through chat</li>
  <li>Edit and send email in the "Edit & Send" tab</li>
</ol>

<hr/>

<h2>🛡️ Security Notes</h2>
<ul>
  <li>Never use your normal Gmail password — always use App Passwords.</li>
  <li>JSON storage is for prototype/testing only; use secure DBs in production.</li>
  <li>Do not expose your API keys.</li>
</ul>

<hr/>

<h2>📜 License</h2>
<p>This project is provided for learning and demonstration purposes.</p>

<hr/>

<h2>💡 Author</h2>
<p><strong>Developed by Supriya (VIT-AP)</strong></p>
<p>Streamlit • Gemini • OpenAI • Python</p>

<hr/>
<p align="center"><strong>🌟 If you like this project, consider starring the repository! 🌟</strong></p>
