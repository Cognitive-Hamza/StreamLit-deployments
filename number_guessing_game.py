import streamlit as st
import random
import time

# Page configuration
st.set_page_config(
    page_title="🎯 Number Guesser Game",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for attractive UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Card-like container */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Title styling */
    h1 {
        color: white;
        text-align: center;
        font-size: 3rem !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin-bottom: 0.5rem !important;
    }
    
    /* Subtitle styling */
    .subtitle {
        text-align: center;
        color: #f0f0f0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    
    /* Game stats box */
    .stats-box {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 20px 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Score display */
    .score-item {
        text-align: center;
        padding: 10px;
    }
    
    .score-label {
        color: #f0f0f0;
        font-size: 0.9rem;
        margin-bottom: 5px;
    }
    
    .score-value {
        color: white;
        font-size: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    /* Feedback messages */
    .feedback {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        padding: 15px;
        border-radius: 10px;
        margin: 20px 0;
        animation: fadeIn 0.5s;
    }
    
    .feedback-high {
        background: rgba(255, 107, 107, 0.2);
        color: #ff6b6b;
        border: 2px solid #ff6b6b;
    }
    
    .feedback-low {
        background: rgba(78, 205, 196, 0.2);
        color: #4ecdc4;
        border: 2px solid #4ecdc4;
    }
    
    .feedback-correct {
        background: rgba(85, 239, 196, 0.2);
        color: #55efc4;
        border: 2px solid #55efc4;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Button styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        font-size: 1.1rem;
        font-weight: bold;
        border-radius: 10px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Input field styling */
    .stNumberInput>div>div>input {
        background: rgba(255, 255, 255, 0.9);
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        font-size: 1.2rem;
        padding: 10px;
        text-align: center;
    }
    
    /* Range display */
    .range-display {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        color: white;
        font-size: 1.1rem;
        margin: 15px 0;
        border: 2px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Progress bar styling */
    .stProgress>div>div>div {
        background: linear-gradient(90deg, #f093fb 0%, #f5576c 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.feedback = ""
    st.session_state.game_over = False
    st.session_state.min_range = 1
    st.session_state.max_range = 100
    st.session_state.best_score = None
    st.session_state.guess_history = []

def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.feedback = ""
    st.session_state.game_over = False
    st.session_state.min_range = 1
    st.session_state.max_range = 100
    st.session_state.guess_history = []

def make_guess(guess):
    if st.session_state.game_over:
        return
    
    st.session_state.attempts += 1
    st.session_state.guess_history.append(guess)
    
    if guess > st.session_state.secret_number:
        st.session_state.feedback = "high"
        st.session_state.max_range = min(guess - 1, st.session_state.max_range)
    elif guess < st.session_state.secret_number:
        st.session_state.feedback = "low"
        st.session_state.min_range = max(guess + 1, st.session_state.min_range)
    else:
        st.session_state.feedback = "correct"
        st.session_state.game_over = True
        if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
            st.session_state.best_score = st.session_state.attempts

# Header
st.markdown("# 🎯 Number Guesser")
st.markdown('<p class="subtitle">Can you guess the secret number?</p>', unsafe_allow_html=True)

# Game stats
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stats-box">
        <div class="score-item">
            <div class="score-label">Attempts</div>
            <div class="score-value">{st.session_state.attempts}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stats-box">
        <div class="score-item">
            <div class="score-label">Range</div>
            <div class="score-value">{st.session_state.max_range - st.session_state.min_range + 1}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    best = st.session_state.best_score if st.session_state.best_score else "-"
    st.markdown(f"""
    <div class="stats-box">
        <div class="score-item">
            <div class="score-label">Best Score</div>
            <div class="score-value">{best}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Current range display
if not st.session_state.game_over:
    st.markdown(f"""
    <div class="range-display">
        🎲 Current Range: <strong>{st.session_state.min_range} - {st.session_state.max_range}</strong>
    </div>
    """, unsafe_allow_html=True)

# Feedback messages
if st.session_state.feedback == "high":
    st.markdown('<div class="feedback feedback-high">📉 Too High! Try a lower number.</div>', unsafe_allow_html=True)
elif st.session_state.feedback == "low":
    st.markdown('<div class="feedback feedback-low">📈 Too Low! Try a higher number.</div>', unsafe_allow_html=True)
elif st.session_state.feedback == "correct":
    st.markdown(f'<div class="feedback feedback-correct">🎉 Correct! You won in {st.session_state.attempts} attempts!</div>', unsafe_allow_html=True)
    st.balloons()

# Game interface
if not st.session_state.game_over:
    # Input and guess button
    col1, col2 = st.columns([3, 1])
    
    with col1:
        guess = st.number_input(
            "Enter your guess",
            min_value=1,
            max_value=100,
            value=50,
            step=1,
            key="guess_input",
            label_visibility="collapsed"
        )
    
    with col2:
        if st.button("🎯 Guess", use_container_width=True):
            if 1 <= guess <= 100:
                make_guess(guess)
                st.rerun()
            else:
                st.error("Please enter a number between 1 and 100!")
    
    # Progress hint
    if st.session_state.attempts > 0:
        progress = (100 - (st.session_state.max_range - st.session_state.min_range + 1)) / 100
        st.progress(progress, text="Getting closer...")
else:
    # Game over - show reset button
    if st.button("🔄 Play Again", use_container_width=True):
        reset_game()
        st.rerun()

# Guess history (in sidebar or expander)
if st.session_state.guess_history:
    with st.expander("📊 Guess History"):
        for i, g in enumerate(reversed(st.session_state.guess_history), 1):
            if g > st.session_state.secret_number:
                emoji = "📉"
                result = "Too High"
            elif g < st.session_state.secret_number:
                emoji = "📈"
                result = "Too Low"
            else:
                emoji = "🎯"
                result = "CORRECT!"
            
            st.write(f"{emoji} Attempt {len(st.session_state.guess_history) - i + 1}: **{g}** - {result}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: rgba(255,255,255,0.7); padding: 20px;'>
    <p>💡 <strong>Tip:</strong> Use binary search strategy for optimal results!</p>
</div>
""", unsafe_allow_html=True)