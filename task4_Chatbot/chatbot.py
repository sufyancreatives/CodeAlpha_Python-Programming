import streamlit as st
import random
import time

st.set_page_config(
    page_title="AlphaBot - Knowledge Hub",
    page_icon="💬",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600&family=Outfit:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0e0b16, #1b0a2a, #0a1128);
    min-height: 100vh;
}

h1 {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(90deg, #a100ff, #f200ff, #00f2fe);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 2.8rem !important;
    letter-spacing: 2px;
    margin-bottom: 0.2rem !important;
}

.subtitle {
    text-align: center;
    color: #f200ff;
    font-size: 0.95rem;
    letter-spacing: 1.5px;
    margin-bottom: 2rem;
    font-family: 'Fira Code', monospace;
}

div[data-testid="stChatMessage"] {
    background-color: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(242, 0, 255, 0.15) !important;
    border-radius: 12px !important;
    margin-bottom: 10px !important;
    padding: 15px !important;
}

div[data-testid="stChatMessage"] div[data-testid="stMarkdownContainer"] p {
    color: #e0e0e0 !important;
}

div[data-testid="stChatInput"] textarea {
    background-color: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(0, 242, 254, 0.3) !important;
    color: #ffffff !important;
    border-radius: 10px !important;
}

div[data-testid="stChatInput"] textarea:focus {
    border-color: #f200ff !important;
    box-shadow: 0 0 10px rgba(242, 0, 255, 0.4) !important;
}

div[data-testid="stChatInput"] button {
    background-color: #f200ff !important;
    color: white !important;
    border-radius: 8px !important;
}

.info-badge {
    background: rgba(0, 242, 254, 0.1);
    border: 1px solid #00f2fe;
    color: #00f2fe;
    padding: 4px 10px;
    border-radius: 15px;
    font-size: 0.75rem;
    display: inline-block;
    margin: 3px;
    font-family: 'Fira Code', monospace;
}

footer {
    display: none !important;
}
</style>
""", unsafe_allow_html=True)

# ─── KNOWLEDGE BASE DATABASE ─────────────────────────────────────────────────────
KNOWLEDGE_BASE = {
    "python": {
        "title": "🐍 Python Programming",
        "keywords": ["python", "programming", "code", "script", "lists", "dictionary"],
        "content": """**Python** is an interpreted, high-level programming language designed for readability.
        
**Key Structures:**
- **Lists**: Ordered collections of items: `my_list = [1, 2, 3]`. Mutable (can be modified).
- **Dictionaries**: Store data in key-value pairs: `my_dict = {"name": "Alice", "age": 25}`.
- **Functions**: Blocks of reusable code defined with `def` syntax:
  ```python
  def greet(name):
      return f"Hello, {name}!"
  ```"""
    },
    "streamlit": {
        "title": "💻 Streamlit Framework",
        "keywords": ["streamlit", "framework", "web app", "ui", "session state"],
        "content": """**Streamlit** is an open-source Python framework that enables developers to build custom web applications for data science and AI in minutes.
        
**Core Principles:**
- **Script runs top-to-bottom**: Every interaction reruns the entire python script.
- **Interactive widgets**: Variables are assigned directly from inputs: `age = st.slider("Age", 0, 100)`.
- **Session State**: Preserves variables and data across script reruns via `st.session_state`."""
    },
    "automation": {
        "title": "🤖 Task Automation",
        "keywords": ["automation", "automate", "shutil", "os", "file organization", "scraper"],
        "content": """**Automation** with Python allows you to write scripts that run boring, repetitive system tasks instantly.
        
**Essential Libraries:**
- `os` & `shutil`: Create/delete folders, list file hierarchies, move or copy files.
- `re` (Regular Expressions): Search and parse strings for specific patterns (e.g. emails, phone formats).
- `requests` & `bs4` (BeautifulSoup): Scrape webpages and gather remote structure or title metadata."""
    },
    "api": {
        "title": "🔌 What is an API?",
        "keywords": ["api", "application programming interface", "endpoint", "url", "json"],
        "content": """**API** stands for *Application Programming Interface*. It is a software intermediary that allows two applications to talk to each other.
        
**How it works:**
1. A **Request** is sent from a client (like your app) to a server endpoint.
2. The server processes the request and responds with a data payload (typically formatted in **JSON**).
3. The client parses this data to display live information, such as weather feeds, stock prices, or bank transactions."""
    },
    "git": {
        "title": "🌿 Git Version Control",
        "keywords": ["git", "github", "version control", "repository", "commit", "push"],
        "content": """**Git** is a distributed version control system that tracks modifications to code files, making it easy to collaborate with other developers.
        
**Core CLI commands:**
- `git init`: Setup a new local git repository.
- `git add .`: Track files and stage all current changes.
- `git commit -m "Message"`: Save the snapshot of staged changes.
- `git push`: Upload local commits to a remote hosting platform like **GitHub**."""
    },
    "facts": {
        "title": "🌌 Space & Tech Trivia",
        "keywords": ["fact", "facts", "trivia", "science", "space", "fun fact"],
        "content": """Here are some fascinating tech and space facts:
- **First Bug**: The term "bug" originated in 1947 when Grace Hopper discovered a physical moth stuck inside the Harvard Mark II computer.
- **Python's Name**: Guido van Rossum named Python after the BBC comedy series *"Monty Python's Flying Circus"*, not the snake.
- **Space Silence**: Sound waves need a medium like air to travel. Since space is a vacuum, it is completely silent!"""
    }
}

# Predefined responses function
def get_bot_response(user_message: str) -> str:
    msg = user_message.lower().strip()
    
    if not msg:
        return "I can't hear you! Feel free to type something."
        
    # Check Greetings
    if any(greet == msg for greet in ["hello", "hi", "hey", "yo"]):
        return "Hi!"
    elif any(greet in msg for greet in ["hello", "hi", "hey", "greetings", "yo"]):
        return "Hi there! I am AlphaBot. I've been updated with an advanced **Knowledge Hub**. Ask me about *Python*, *Streamlit*, *Git*, *APIs*, or *Trivia*! 👋"
        
    # Check Status
    elif "how are you" in msg:
        return "I'm fine, thanks!"
    elif any(q in msg for q in ["how's it going", "how are you doing", "how do you do"]):
        return "I am doing great! My knowledge modules are loaded and ready. Let me know what you want to learn about! 😊"
        
    # Check Identity
    elif any(q in msg for q in ["who are you", "what is your name", "what's your name"]):
        return "I am **AlphaBot**, your Python-powered knowledge assistant. 🤖"
        
    # Check Joke
    elif any(q in msg for q in ["joke", "tell me a joke", "make me laugh"]):
        jokes = [
            "Why do programmers wear glasses? Because they can't C#! 🤓",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem! 💡",
            "Why did the database administrator leave the restaurant? There were too many joins! 🗄️",
            "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?' 🍺",
            "['hip', 'hip'] (hip hip array!) 💻"
        ]
        return random.choice(jokes)
        
    # Check Farewell
    elif "bye" in msg or "goodbye" in msg:
        return "Goodbye!"
    elif any(q in msg for q in ["exit", "quit", "see you"]):
        return "Goodbye! Keep learning and building! See you soon! 🌟"
        
    # Scan Knowledge Base matching keywords
    matched_topic = None
    for key, data in KNOWLEDGE_BASE.items():
        if any(keyword in msg for keyword in data["keywords"]) or key in msg:
            matched_topic = data
            break
            
    if matched_topic:
        return f"### {matched_topic['title']}\n\n{matched_topic['content']}"
        
    # Help / Fallback
    return ("I'm not sure how to answer that. I have specialized info modules! "
            "Try typing one of these keywords: **Python, Streamlit, API, Git, Automation, Facts,** or **Joke**! 💡")


# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am AlphaBot. I have loaded several informational guides for you. Ask me about *Python*, *Streamlit*, *Git*, *APIs*, or *Automation*! 📚"}
    ]

st.markdown("<h1>💬 ALPHABOT KNOWLEDGE HUB</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">INTERACTIVE RULE-BASED TECHNICAL ASSISTANT</p>', unsafe_allow_html=True)

# Helper Guide Expander
with st.expander("ℹ️ Chatbot Guide & Available Topics"):
    st.markdown("""
    AlphaBot maps keywords to full educational content blocks. Try asking:
    - **Python**: *What is python?*, *Tell me about lists*
    - **Streamlit**: *How does streamlit work?*, *Explain session state*
    - **API**: *What is an API?*, *Tell me about endpoints*
    - **Git**: *How to use git?*, *Git commands*
    - **Automation**: *What is task automation?*
    - **Trivia**: *Give me a fun fact*
    """)
    
    st.markdown("**Active Knowledge Tags:**")
    tags_html = ""
    for data in KNOWLEDGE_BASE.values():
        tags_html += f'<span class="info-badge">{data["title"]}</span>'
    st.markdown(tags_html, unsafe_allow_html=True)

st.markdown("<p style='font-size:0.8rem; color:#f200ff; text-align:center; margin-bottom:5px;'>💡 Quick Knowledge Inquiries:</p>", unsafe_allow_html=True)
s_col1, s_col2, s_col3, s_col4 = st.columns(4)
clicked_suggestion = None

with s_col1:
    if st.button("🐍 Python Info", key="s_py", use_container_width=True):
        clicked_suggestion = "Tell me about Python"
with s_col2:
    if st.button("💻 Streamlit Info", key="s_st", use_container_width=True):
        clicked_suggestion = "Streamlit session state"
with s_col3:
    if st.button("🔌 API Basics", key="s_api", use_container_width=True):
        clicked_suggestion = "What is an API"
with s_col4:
    if st.button("🌌 Space/Tech Facts", key="s_facts", use_container_width=True):
        clicked_suggestion = "Fun facts"

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input handling
chat_input_val = st.chat_input("Ask AlphaBot something...")
user_prompt = clicked_suggestion if clicked_suggestion else chat_input_val

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)
        
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = get_bot_response(user_prompt)
        
        # Simulated typing effect
        typing_speed = 0.015
        temp_response = ""
        for char in full_response:
            temp_response += char
            message_placeholder.markdown(temp_response + "▌")
            time.sleep(typing_speed)
        message_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    if any(q in user_prompt.lower() for q in ["bye", "goodbye", "exit"]):
        st.info("💡 To restart the conversation, refresh the browser page!")
