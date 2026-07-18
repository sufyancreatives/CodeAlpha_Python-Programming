import streamlit as st
import re
import os

st.set_page_config(
    page_title="CodeAlpha Python Project Suite",
    page_icon="🚀",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #0f0c1b, #0c1a1f, #0d0f14);
    min-height: 100vh;
}

h1.suite-title {
    font-family: 'Outfit', sans-serif;
    font-weight: 800;
    background: linear-gradient(90deg, #ff007f, #7f00ff, #00f2fe, #00ff87);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 3rem !important;
    letter-spacing: 2px;
    margin-bottom: 0.1rem !important;
}

.suite-subtitle {
    text-align: center;
    color: #00f2fe;
    font-size: 1rem;
    letter-spacing: 2px;
    margin-bottom: 2.5rem;
}

.welcome-card {
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 0, 127, 0.2);
    border-radius: 16px;
    padding: 30px;
    text-align: center;
    max-width: 800px;
    margin: 0 auto;
    box-shadow: 0 8px 32px 0 rgba(127, 0, 255, 0.1);
}

.card-feature {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    transition: all 0.3s ease;
}

.card-feature:hover {
    border-color: #00f2fe;
    box-shadow: 0 0 15px rgba(0, 242, 254, 0.15);
    transform: translateY(-2px);
}
</style>
""", unsafe_allow_html=True)

def run_app_file(filepath):
    if not os.path.exists(filepath):
        st.error(f"File not found: {filepath}")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
        
    # Remove st.set_page_config to avoid errors in the multi-page hub
    code_clean = re.sub(r'st\.set_page_config\s*\([^)]*\)', '', code)
    
    # Run the cleaned python file
    exec(code_clean, globals())

# Sidebar Navigation Hub
st.sidebar.markdown("### 🚀 Project Selection")
selection = st.sidebar.selectbox(
    "Choose Application:",
    [
        "🏠 Main Dashboard",
        "🎮 Task 1: Hangman Game",
        "📈 Task 2: Stock Portfolio Tracker",
        "🤖 Task 3: Task Automation Hub",
        "💬 Task 4: AlphaBot Chatbot"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 This portal bundles all 4 CodeAlpha programming assignments into a single deployed app."
)

if selection == "🏠 Main Dashboard":
    st.markdown('<h1 class="suite-title">CODEALPHA ASSIGNMENT SUITE</h1>', unsafe_allow_html=True)
    st.markdown('<p class="suite-subtitle">INTERACTIVE PYTHON PORTAL</p>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="welcome-card">
        <h3>Welcome to the Python Programming Suite!</h3>
        <p style="color: #9ab4c5;">Use the sidebar navigation to choose and run any of the four applications instantly. The system dynamically imports and executes each environment container on the fly.</p>
    </div>
    <br>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="card-feature">
            <h4 style="color: #ff007f; margin: 0;">🎮 Task 1: Hangman Game</h4>
            <p style="font-size: 0.85rem; color: #9ab4c5; margin: 5px 0 0 0;">Test your word-guessing skills in this classic game. Includes a neon theme, live gallows ASCII drawing, and a one-time letter reveal hint system.</p>
        </div>
        <div class="card-feature">
            <h4 style="color: #00ff87; margin: 0;">📈 Task 2: Stock Portfolio Tracker</h4>
            <p style="font-size: 0.85rem; color: #9ab4c5; margin: 5px 0 0 0;">Add and manage stock quantities. The tracker automatically calculates your current values against a pre-loaded database. Exports reports to CSV & TXT.</p>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        <div class="card-feature">
            <h4 style="color: #00f2fe; margin: 0;">🤖 Task 3: Task Automation Hub</h4>
            <p style="font-size: 0.85rem; color: #9ab4c5; margin: 5px 0 0 0;">Run real-life automation workflows: batch move/copy/zip files, parse emails and phone numbers with regex, or scrape web page content dynamically.</p>
        </div>
        <div class="card-feature">
            <h4 style="color: #a100ff; margin: 0;">💬 Task 4: AlphaBot Chatbot</h4>
            <p style="font-size: 0.85rem; color: #9ab4c5; margin: 5px 0 0 0;">Interact with a rule-based virtual assistant. Includes interactive suggestion buttons and specialized modules for Python, Git, and tech facts.</p>
        </div>
        """, unsafe_allow_html=True)

elif selection == "🎮 Task 1: Hangman Game":
    run_app_file("task1_hungman game/app.py")
    
elif selection == "📈 Task 2: Stock Portfolio Tracker":
    run_app_file("task2_stock portfolio/stock.py")
    
elif selection == "🤖 Task 3: Task Automation Hub":
    run_app_file("task3_Automation/automation.py")
    
elif selection == "💬 Task 4: AlphaBot Chatbot":
    run_app_file("task4_Chatbot/chatbot.py")
