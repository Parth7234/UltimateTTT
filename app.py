import streamlit as st
import time
import sys
import os

# --- PATH SETUP ---
# Ensure we can import from 'src' regardless of how streamlit is launched
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.ultimate_ttt_engine import UltimateTTT, X, O, DRAW
from src import random_bot
from src import ai as medium_bot
from src import minimax_bot as hard_bot

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Ultimate Tic-Tac-Toe AI", page_icon="🎮", layout="centered")

# --- CUSTOM CSS FOR 3x3 GRID VISUALS ---
st.markdown("""
    <style>
    div.stButton > button {
        width: 100%;
        height: 50px;
        font-size: 20px;
        font-weight: bold;
        margin: 0px;
    }
    /* Visual separation for 3x3 Macro Boards */
    [data-testid="column"] {
        padding: 0px;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'game' not in st.session_state:
    st.session_state.game = UltimateTTT()
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Easy'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# --- HELPER FUNCTIONS ---

def reset_game():
    st.session_state.game = UltimateTTT()
    st.session_state.game_over = False

def bot_move():
    """Triggers the selected bot to make a move."""
    game = st.session_state.game
    
    if st.session_state.game_over:
        return

    # Select Bot Strategy
    diff = st.session_state.difficulty
    
    with st.spinner(f"🤖 AI ({diff}) is thinking..."):
        # Artificial delay for realism on Easy/Medium
        if diff != 'Hard': 
            time.sleep(0.5)
            
        try:
            if diff == 'Easy':
                move = random_bot.play(game.board, game.last, O)
            elif diff == 'Medium':
                move = medium_bot.play(game.board, game.last, O)
            elif diff == 'Hard':
                # Hard bot can take a few seconds
                move = hard_bot.play(game.board, game.last, O)
            
            if move:
                success = game.move(move[0], move[1])
                if not success:
                    st.error(f"Bot tried invalid move: {move}")
            else:
                st.error("Bot could not find a move (Draw?)")
                
        except Exception as e:
            st.error(f"Bot crashed: {e}")

def handle_click(r, c):
    """Handles the human player's click."""
    game = st.session_state.game
    if not st.session_state.game_over and game.curr_player == X:
        success = game.move(r, c)
        if success:
            # Check for win immediately after player move
            winner = game.get_winner()
            if winner:
                st.session_state.game_over = True
            else:
                # If game continues, Trigger Bot
                bot_move()
                # Check for win after bot move
                if game.get_winner():
                    st.session_state.game_over = True

# --- SIDEBAR ---
st.sidebar.title("🎮 Game Settings")
st.session_state.difficulty = st.sidebar.radio(
    "Select AI Level:",
    ('Easy', 'Medium', 'Hard'),
    index=['Easy', 'Medium', 'Hard'].index(st.session_state.difficulty)
)

st.sidebar.markdown("---")
if st.sidebar.button("🔄 New Game"):
    reset_game()
    st.rerun()

# --- MAIN GAME UI ---
st.title("Ultimate Tic-Tac-Toe")
st.markdown("You are **X** (Blue). AI is **O** (Red).")

game = st.session_state.game
valid_moves = game.get_valid_moves() if not st.session_state.game_over else []

# Display Game Status
winner = game.get_winner()
if winner:
    if winner == X:
        st.success("🏆 You Won! Congratulations!")
    elif winner == O:
        st.error("💀 The Bot Won! Better luck next time.")
    else:
        st.warning("🤝 It's a Draw!")
else:
    if game.curr_player == X:
        st.info(f"👉 Your Turn! (Play in highlighted cells)")
    else:
        st.info("⏳ Waiting for AI...")

# --- RENDER BOARD (9x9 Grid) ---
for macro_r in range(3):
    cols = st.columns([1, 0.1, 1, 0.1, 1]) # 3 boards + spacers
    macro_cols_indices = [0, 2, 4]
    
    for c_idx, macro_c in enumerate(macro_cols_indices):
        with cols[macro_c]:
            # Check macro board status
            macro_winner = game.mainboard[macro_r][c_idx]
            
            # Visual Header for Macro Board
            if macro_winner == X:
                st.markdown("<div style='text-align: center; color: blue; font-size: 24px;'>❌</div>", unsafe_allow_html=True)
            elif macro_winner == O:
                st.markdown("<div style='text-align: center; color: red; font-size: 24px;'>⭕</div>", unsafe_allow_html=True)
            elif macro_winner == DRAW:
                st.markdown("<div style='text-align: center; color: grey; font-size: 24px;'>➖</div>", unsafe_allow_html=True)
            else:
                # Render the 3x3 Micro Grid
                for micro_r in range(3):
                    micro_cols = st.columns(3)
                    for micro_c in range(3):
                        abs_r = macro_r * 3 + micro_r
                        abs_c = c_idx * 3 + micro_c
                        
                        val = game.board[abs_r][abs_c]
                        
                        # Label Logic
                        label = " "
                        if val == X: label = "X"
                        if val == O: label = "O"
                        
                        # --- HIGHLIGHTING LOGIC ---
                        is_valid = (abs_r, abs_c) in valid_moves
                        
                        # If valid, make it PRIMARY (Colored). Else SECONDARY (Grey).
                        btn_type = "primary" if is_valid else "secondary"
                        
                        # Disable if occupied or not valid
                        disabled = (val != 0) or (not is_valid) or st.session_state.game_over
                        
                        # Render Button
                        if micro_cols[micro_c].button(label, key=f"btn_{abs_r}_{abs_c}", type=btn_type, disabled=disabled):
                            handle_click(abs_r, abs_c)
                            st.rerun()
            
    if macro_r < 2:
        st.write("---")