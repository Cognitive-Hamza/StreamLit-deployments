import streamlit as st
import random
from PIL import Image
import base64

# Page configuration
st.set_page_config(
    page_title="Rock Paper Scissors",
    page_icon="✊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
def local_css():
    st.markdown("""
    <style>
        .main {
            padding: 0rem 1rem;
        }
        
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            height: 3em;
            font-size: 1.2em;
            font-weight: bold;
            transition: all 0.3s ease;
            border: none;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        
        .player-choice-btn {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        
        .computer-choice-display {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            font-size: 1.5em;
            margin: 20px 0;
        }
        
        .result-display {
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            font-size: 2em;
            font-weight: bold;
            margin: 20px 0;
            animation: fadeIn 1s;
        }
        
        .tie-result {
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            color: #333;
        }
        
        .win-result {
            background: linear-gradient(135deg, #d4fc79 0%, #96e6a1 100%);
            color: #2c5530;
        }
        
        .lose-result {
            background: linear-gradient(135deg, #ff9a9e 0%, #fad0c4 100%);
            color: #7a1c1c;
        }
        
        .score-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .game-title {
            text-align: center;
            font-size: 3.5em;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5em;
            font-weight: 800;
        }
        
        .choice-emoji {
            font-size: 5em;
            display: block;
            text-align: center;
        }
        
        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 2em;
            font-size: 1.2em;
        }
        
        @keyframes fadeIn {
            from {opacity: 0;}
            to {opacity: 1;}
        }
        
        @keyframes pulse {
            0% {transform: scale(1);}
            50% {transform: scale(1.05);}
            100% {transform: scale(1);}
        }
        
        .pulse-animation {
            animation: pulse 0.5s ease-in-out;
        }
        
        .footer {
            text-align: center;
            margin-top: 3em;
            color: #888;
            font-size: 0.9em;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state variables
def init_session_state():
    if 'player_score' not in st.session_state:
        st.session_state.player_score = 0
    if 'computer_score' not in st.session_state:
        st.session_state.computer_score = 0
    if 'ties' not in st.session_state:
        st.session_state.ties = 0
    if 'last_result' not in st.session_state:
        st.session_state.last_result = ""
    if 'computer_choice' not in st.session_state:
        st.session_state.computer_choice = ""
    if 'player_choice' not in st.session_state:
        st.session_state.player_choice = ""
    if 'game_history' not in st.session_state:
        st.session_state.game_history = []

# Determine the winner
def determine_winner(player, computer):
    if player == computer:
        return "tie"
    elif (player == "rock" and computer == "scissors") or \
         (player == "paper" and computer == "rock") or \
         (player == "scissors" and computer == "paper"):
        return "player"
    else:
        return "computer"

# Get emoji for choice
def get_emoji(choice):
    emojis = {
        "rock": "✊",
        "paper": "✋",
        "scissors": "✌️"
    }
    return emojis.get(choice, "❓")

# Update scores based on result
def update_scores(result):
    if result == "player":
        st.session_state.player_score += 1
    elif result == "computer":
        st.session_state.computer_score += 1
    else:
        st.session_state.ties += 1

# Main game function
def play_game(player_choice):
    # Computer makes a random choice
    computer_choice = random.choice(["rock", "paper", "scissors"])
    
    # Store choices
    st.session_state.player_choice = player_choice
    st.session_state.computer_choice = computer_choice
    
    # Determine the winner
    result = determine_winner(player_choice, computer_choice)
    
    # Update scores
    update_scores(result)
    
    # Store result
    st.session_state.last_result = result
    
    # Add to game history
    st.session_state.game_history.append({
        "player": player_choice,
        "computer": computer_choice,
        "result": result
    })
    
    # Keep only last 10 games in history
    if len(st.session_state.game_history) > 10:
        st.session_state.game_history = st.session_state.game_history[-10:]

# Main app
def main():
    # Apply custom CSS
    local_css()
    
    # Initialize session state
    init_session_state()
    
    # Header section
    st.markdown('<h1 class="game-title">Rock Paper Scissors</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Choose your weapon and see if you can beat the computer!</p>', unsafe_allow_html=True)
    
    # Display score cards in columns
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="score-card">
            <h3>Player</h3>
            <h1 style="color: #667eea;">{st.session_state.player_score}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="score-card">
            <h3>Ties</h3>
            <h1 style="color: #888;">{st.session_state.ties}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="score-card">
            <h3>Computer</h3>
            <h1 style="color: #f5576c;">{st.session_state.computer_score}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Game controls section
    st.markdown("<h2 style='text-align: center;'>Choose Your Move</h2>", unsafe_allow_html=True)
    
    # Create three columns for the choice buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("✊ Rock", key="rock", help="Click to choose Rock"):
            play_game("rock")
            st.rerun()
    
    with col2:
        if st.button("✋ Paper", key="paper", help="Click to choose Paper"):
            play_game("paper")
            st.rerun()
    
    with col3:
        if st.button("✌️ Scissors", key="scissors", help="Click to choose Scissors"):
            play_game("scissors")
            st.rerun()
    
    # Display game result if a choice has been made
    if st.session_state.last_result:
        st.markdown("---")
        
        # Display choices
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            st.markdown(f"<h3 style='text-align: center;'>Your Choice</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='choice-emoji'>{get_emoji(st.session_state.player_choice)}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{st.session_state.player_choice.title()}</h4>", unsafe_allow_html=True)
        
        with col2:
            st.markdown("<h3 style='text-align: center;'>VS</h3>", unsafe_allow_html=True)
            st.markdown("<div class='choice-emoji'>⚔️</div>", unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"<h3 style='text-align: center;'>Computer's Choice</h3>", unsafe_allow_html=True)
            st.markdown(f"<div class='choice-emoji'>{get_emoji(st.session_state.computer_choice)}</div>", unsafe_allow_html=True)
            st.markdown(f"<h4 style='text-align: center;'>{st.session_state.computer_choice.title()}</h4>", unsafe_allow_html=True)
        
        # Display result with appropriate styling
        if st.session_state.last_result == "tie":
            st.markdown('<div class="result-display tie-result">🤝 It\'s a Tie!</div>', unsafe_allow_html=True)
        elif st.session_state.last_result == "player":
            st.markdown('<div class="result-display win-result">🏆 You Win!</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="result-display lose-result">💻 Computer Wins!</div>', unsafe_allow_html=True)
    
    # Game history section
    if st.session_state.game_history:
        st.markdown("---")
        st.markdown("<h3>Recent Games</h3>", unsafe_allow_html=True)
        
        # Create a table of recent games
        history_data = []
        for i, game in enumerate(reversed(st.session_state.game_history)):
            result_emoji = "🤝" if game["result"] == "tie" else "🏆" if game["result"] == "player" else "💻"
            history_data.append({
                "Game": len(st.session_state.game_history) - i,
                "Player": f"{get_emoji(game['player'])} {game['player'].title()}",
                "Computer": f"{get_emoji(game['computer'])} {game['computer'].title()}",
                "Result": result_emoji
            })
        
        st.table(history_data)
    
    # Game rules section in sidebar
    with st.sidebar:
        st.markdown("## 📖 Game Rules")
        st.markdown("""
        - **Rock** beats Scissors (✊ crushes ✌️)
        - **Scissors** beats Paper (✌️ cuts ✋)
        - **Paper** beats Rock (✋ covers ✊)
        - Same choice results in a **Tie**
        """)
        
        st.markdown("## 🎮 How to Play")
        st.markdown("""
        1. Click on your choice: Rock, Paper, or Scissors
        2. The computer will randomly select its choice
        3. See who wins based on the rules
        4. Track your score and game history
        """)
        
        # Reset button in sidebar
        st.markdown("---")
        if st.button("🔄 Reset Game", use_container_width=True):
            st.session_state.player_score = 0
            st.session_state.computer_score = 0
            st.session_state.ties = 0
            st.session_state.last_result = ""
            st.session_state.computer_choice = ""
            st.session_state.player_choice = ""
            st.session_state.game_history = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown('<div class="footer">Rock Paper Scissors Game</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()