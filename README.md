<h1 align="center">AI Chatbot Platform with Multi-Model Support and Email Integration</h1>

<p align="center">
  A Streamlit-based AI system supporting Gemini and OpenAI models, complete user authentication, persistent chat history, image analysis, dual-model comparison mode, and integrated email composition and delivery.
</p>

<hr/>

<h2>Project Overview</h2>

<p>
This application is a full-featured conversational AI platform built on Streamlit. It enables authenticated users to interact with AI models, manage multi-session chat histories, analyze images, generate professional emails, and compare outputs from two AI models in a structured debate mode.
</p>

<hr/>

<h2>Key Features</h2>

<h3>1. User Authentication</h3>
<p>
The system supports user registration and login with local JSON-based credential storage. Optional email credentials can be saved to enable outbound email functionality.
</p>

<h3>2. Persistent Chat History</h3>
<p>
Each authenticated user maintains individual chat sessions stored locally in <code>chat_history.json</code>. Users can create, switch, and delete chats.
</p>

<h3>3. AI Model Switching</h3>
<p>
The platform provides real-time selection between different AI engines:
</p>
<ul>
  <li>Gemini (Google Generative AI)</li>
  <li>OpenAI (GPT-4o-mini with fallback to GPT-3.5)</li>
</ul>

<h3>4. Response Style Customization</h3>
<p>
Users may select one of multiple communication styles:
</p>
<ul>
  <li>Professional</li>
  <li>Humorous</li>
  <li>Child-friendly</li>
</ul>

<h3>5. Image Analysis</h3>
<p>
Users may upload images (JPG/PNG). For Gemini mode, the system processes the image using a vision-enabled model and generates descriptive insights.
</p>

<h3>6. Email Composition and Delivery</h3>
<p>
The integrated Mail Mode enables:
</p>
<ul>
  <li>Generating email content using AI</li>
  <li>Editing the generated text</li>
  <li>Saving a reusable signature</li>
  <li>Sending emails through Gmail SMTP using App Passwords</li>
</ul>

<h3>7. AI Duo (Model Comparison Mode)</h3>
<p>
This feature allows the user to run the same prompt through Gemini and OpenAI and view:
</p>
<ul>
  <li>Individual responses</li>
  <li>A synthesized, neutral conclusion generated via Gemini</li>
  <li>A one-click option to save the debate into the active chat session</li>
</ul>

<hr/>

<h2>Project Structure</h2>

<pre>
├── app.py
├── users.json
├── chat_history.json
├── requirements.txt
└── README.md
</pre>

<hr/>

<h2>Installation</h2>

<h3>1. Clone the repository</h3>
<pre>
git clone &lt;your-repository-url&gt;
cd &lt;your-project&gt;
</pre>

<h3>2. Install dependencies</h3>
<pre>
pip install -r requirements.txt
</pre>

<h3>3. Configure API Keys</h3>
<p>Create the file:</p>

<pre>
.streamlit/secrets.toml
</pre>

<p>Add your API credentials:</p>

<pre>
GEMINI_API_KEY="your_key"
OPENAI_API_KEY="your_key"
</pre>

<p>Email credentials are collected during user signup and do not need to be added here.</p>

<hr/>

<h2>Running the Application</h2>

<pre>
streamlit run app.py
</pre>

<hr/>

<h2>Usage Instructions</h2>

<h3>Authentication</h3>
<p>
Register a new account or log in with existing credentials. Email-related fields at signup are optional.
</p>

<h3>Chat Interface</h3>
<ul>
  <li>Select an AI model</li>
  <li>Choose a response style</li>
  <li>Initiate conversations</li>
  <li>Switch or delete chat sessions</li>
</ul>

<h3>Image Upload</h3>
<p>
Upload an image to obtain a Gemini-generated description. OpenAI vision support is not activated in this version.
</p>

<h3>AI Duo Mode</h3>
<p>
Enter a prompt, run both models, compare outputs, and generate synthesized conclusions.
</p>

<h3>Mail Mode</h3>
<ol>
  <li>Enable Mail Mode from the sidebar</li>
  <li>Enter recipient, subject, and greeting</li>
  <li>Generate email content via the Compose tab</li>
  <li>Edit the email in the Edit &amp; Send tab</li>
  <li>Send using Gmail SMTP (App Password required)</li>
</ol>

<hr/>

<h2>Security Considerations</h2>
<ul>
  <li>Use Gmail App Passwords, not your actual email password</li>
  <li>JSON file storage is intended for development use only</li>
  <li>Do not expose API keys or upload secrets to public repositories</li>
</ul>

<hr/>

<h2>License</h2>
<p>
This project is intended for educational and evaluation purposes.
</p>

<hr/>

<h2>Author</h2>
<p>
Developed by Supriya  
VIT-AP University  
</p>
