import streamlit as st
import random

st.set_page_config(
    page_title="Hangman Game",
    page_icon="🪢",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;600;700&family=Orbitron:wght@700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Fira Code', monospace;
}

.stApp {
    background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
    min-height: 100vh;
}

h1 {
    font-family: 'Orbitron', sans-serif;
    background: linear-gradient(90deg, #f72585, #7209b7, #4cc9f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    font-size: 3rem !important;
    letter-spacing: 4px;
    text-shadow: 0 0 40px rgba(247,37,133,0.5);
    margin-bottom: 0 !important;
}

.subtitle {
    text-align: center;
    color: #4cc9f0;
    font-size: 0.9rem;
    letter-spacing: 2px;
    margin-bottom: 2rem;
}

.hangman-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(76,201,240,0.3);
    border-radius: 16px;
    padding: 20px 30px;
    margin: 1rem 0;
    box-shadow: 0 0 30px rgba(114,9,183,0.2);
}

.hangman-art {
    font-family: 'Fira Code', monospace;
    font-size: 1.1rem;
    line-height: 1.4;
    color: #f72585;
    white-space: pre;
    text-align: center;
}

.word-display {
    font-family: 'Orbitron', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 12px;
    text-align: center;
    color: #4cc9f0;
    padding: 1rem;
    text-shadow: 0 0 20px rgba(76,201,240,0.6);
}

.wrong-letters {
    color: #f72585;
    font-size: 1.1rem;
    text-align: center;
    letter-spacing: 4px;
}

.status-win {
    background: linear-gradient(135deg, #06d6a0, #118ab2);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    color: white;
    box-shadow: 0 0 30px rgba(6,214,160,0.5);
    animation: pulse 1.5s infinite;
}

.status-lose {
    background: linear-gradient(135deg, #f72585, #7209b7);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    color: white;
    box-shadow: 0 0 30px rgba(247,37,133,0.5);
}

.tries-left {
    text-align: center;
    font-size: 1rem;
    color: #b5838d;
}

.tries-left span {
    color: #f72585;
    font-size: 1.4rem;
    font-weight: bold;
}

@keyframes pulse {
    0%  { box-shadow: 0 0 20px rgba(6,214,160,0.4); }
    50% { box-shadow: 0 0 50px rgba(6,214,160,0.9); }
    100%{ box-shadow: 0 0 20px rgba(6,214,160,0.4); }
}

.letter-pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 3px;
    font-weight: bold;
    font-size: 0.9rem;
}

.pill-correct {
    background: rgba(6,214,160,0.2);
    border: 1px solid #06d6a0;
    color: #06d6a0;
}

.pill-wrong {
    background: rgba(247,37,133,0.15);
    border: 1px solid #f72585;
    color: #f72585;
}

div[data-testid="stTextInput"] input,
div[data-testid="stTextInput"] input[type="text"],
.stTextInput input,
.stTextInput > div > div > input,
input[aria-label],
[data-baseweb="input"] input,
[data-baseweb="base-input"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(76,201,240,0.4) !important;
    color: #e0e0e0 !important;
    caret-color: #4cc9f0 !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 1.2rem !important;
    letter-spacing: 3px !important;
    border-radius: 10px !important;
    text-align: center !important;
    -webkit-text-fill-color: #e0e0e0 !important;
}

div[data-testid="stTextInput"] input:focus,
.stTextInput input:focus,
[data-baseweb="input"] input:focus {
    border-color: #7209b7 !important;
    box-shadow: 0 0 15px rgba(114,9,183,0.5) !important;
    color: #e0e0e0 !important;
    -webkit-text-fill-color: #e0e0e0 !important;
}

div[data-testid="stButton"] button {
    width: 100%;
    background: linear-gradient(135deg, #7209b7, #4361ee) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Orbitron', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 2px !important;
    padding: 0.6rem 1rem !important;
    transition: all 0.3s ease !important;
}

div[data-testid="stButton"] button:hover {
    background: linear-gradient(135deg, #f72585, #7209b7) !important;
    box-shadow: 0 0 20px rgba(247,37,133,0.5) !important;
    transform: translateY(-2px) !important;
}
</style>
""", unsafe_allow_html=True)

WORDS = ["python", "streamlit", "hangman", "keyboard", "galaxy"]
MAX_WRONG = 6

HANGMAN_STAGES = [
    r"",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]

def init_game():
    st.session_state.word = random.choice(WORDS)
    st.session_state.guessed = []
    st.session_state.wrong = []
    st.session_state.game_over = False
    st.session_state.won = False
    st.session_state.message = ""
    st.session_state.hint_used = False
    st.session_state.hint_letter = ""

if "word" not in st.session_state:
    init_game()

if "hint_used" not in st.session_state:
    st.session_state.hint_used = False
if "hint_letter" not in st.session_state:
    st.session_state.hint_letter = ""

def use_hint():
    word = st.session_state.word
    hidden = [c for c in set(word) if c not in st.session_state.guessed]
    if hidden:
        letter = random.choice(hidden)
        st.session_state.hint_letter = letter
        st.session_state.hint_used = True
        st.session_state.guessed.append(letter)
        st.session_state.message = f"💡 Hint revealed: **{letter.upper()}**"
        if all(c in st.session_state.guessed for c in word):
            st.session_state.won = True
            st.session_state.game_over = True

def get_display_word():
    return " ".join(
        letter if letter in st.session_state.guessed else "_"
        for letter in st.session_state.word
    )

def process_guess(letter: str):
    letter = letter.lower().strip()

    if not letter or not letter.isalpha() or len(letter) != 1:
        st.session_state.message = "⚠️ Please enter a single letter (a–z)."
        return

    if letter in st.session_state.guessed:
        st.session_state.message = f"🔄 You already guessed **{letter.upper()}**!"
        return

    st.session_state.guessed.append(letter)
    st.session_state.message = ""

    if letter in st.session_state.word:
        if all(c in st.session_state.guessed for c in st.session_state.word):
            st.session_state.won = True
            st.session_state.game_over = True
    else:
        st.session_state.wrong.append(letter)
        if len(st.session_state.wrong) >= MAX_WRONG:
            st.session_state.game_over = True

st.markdown("<h1>🪢 HANGMAN</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">GUESS THE WORD · 6 CHANCES</p>', unsafe_allow_html=True)

wrong_count = len(st.session_state.wrong)
if HANGMAN_STAGES[wrong_count].strip():
    art_html = HANGMAN_STAGES[wrong_count].replace("\n", "<br>").replace(" ", "&nbsp;")
    st.markdown(
        f'<div class="hangman-box"><div class="hangman-art">{art_html}</div></div>',
        unsafe_allow_html=True,
    )

st.markdown(
    f'<div class="word-display">{get_display_word()}</div>',
    unsafe_allow_html=True,
)

tries_left = MAX_WRONG - wrong_count
st.markdown(
    f'<p class="tries-left">Wrong guesses: <span>{wrong_count} / {MAX_WRONG}</span> &nbsp;|&nbsp; Chances left: <span>{tries_left}</span></p>',
    unsafe_allow_html=True,
)

if st.session_state.guessed:
    pills_html = "<div style='text-align:center; margin: 0.5rem 0;'>"
    for letter in sorted(st.session_state.guessed):
        cls = "pill-correct" if letter in st.session_state.word else "pill-wrong"
        pills_html += f'<span class="letter-pill {cls}">{letter.upper()}</span>'
    pills_html += "</div>"
    st.markdown(pills_html, unsafe_allow_html=True)

st.markdown("---")

if st.session_state.game_over:
    if st.session_state.won:
        st.markdown(
            '<div class="status-win">🎉 YOU WON! Brilliant!</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="status-lose">💀 GAME OVER — The word was <b>{st.session_state.word.upper()}</b></div>',
            unsafe_allow_html=True,
        )
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔄 Play Again", key="restart_btn"):
        init_game()
        st.rerun()

else:
    col1, col2 = st.columns([3, 1])
    with col1:
        guess_input = st.text_input(
            "Enter a letter:",
            max_chars=1,
            key="guess_input",
            label_visibility="collapsed",
            placeholder="Type a letter…",
        )
    with col2:
        guess_btn = st.button("GUESS →", key="guess_btn")

    if guess_btn and guess_input:
        process_guess(guess_input)
        st.rerun()

    hint_col, new_col = st.columns(2)
    with hint_col:
        hint_disabled = st.session_state.hint_used
        hint_label = (
            f"💡 Hint Used  ({st.session_state.hint_letter.upper()})"
            if hint_disabled
            else "💡 Use Hint  (1 per game)"
        )
        if st.button(hint_label, key="hint_btn", disabled=hint_disabled):
            use_hint()
            st.rerun()
    with new_col:
        if st.button("↩ New Game", key="new_game_btn"):
            init_game()
            st.rerun()

    if st.session_state.message:
        st.info(st.session_state.message)

st.markdown(
    "<p style='text-align:center; color:#4a4a6a; font-size:0.75rem; margin-top:2rem;'>"
    "Built with ❤️ using Python · Streamlit &nbsp;|&nbsp; "
    "Concepts: random · while loop · if-else · strings · lists"
    "</p>",
    unsafe_allow_html=True,
)
