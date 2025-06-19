import streamlit as st
from TicTacToe import T3Game

# Initialize session state variables once
if "game" not in st.session_state:
    st.session_state.game = None
if "mode" not in st.session_state:
    st.session_state.mode = "PvC"  # default mode
if "message" not in st.session_state:
    st.session_state.message = ""
if "game_over" not in st.session_state:
    st.session_state.game_over = False

def start_new_game():
    st.session_state.game = T3Game(game_mode=st.session_state.mode)
    st.session_state.message = "New game started in mode: " + st.session_state.mode
    st.session_state.game_over = False

st.title("Tic Tac Toe")

# Game mode selection & New Game button
mode = st.radio("Select Game Mode", options=["PvC", "PvP"], index=0, key="mode")
if st.button("New Game"):
    start_new_game()

if st.session_state.game is None:
    start_new_game()

game = st.session_state.game

# Automatically let computer play if in PvC mode and it's machine's turn and game not over.
if game.game_mode == "PvC" and game.current_player == "O" and not st.session_state.game_over:
    result = game.play_turn()  # computer makes move
    st.session_state.message = result["status"]
    if "wins" in result["status"] or "draw" in result["status"]:
        st.session_state.game_over = True
    # Force a rerun to update board after computer move.
    st.rerun()

st.subheader("Current Board")

# Display board as a 3x3 grid of buttons
cols = st.columns(3)
for i in range(3):
    row_cols = st.columns(3)
    for j in range(3):
        cell_value = game.board[i][j]
        # Display cell mark if exists or show a space; if cell is empty and game is not over, make it clickable.
        if cell_value != "":
            btn_label = cell_value
            disabled = True
        else:
            btn_label = " "
            disabled = st.session_state.game_over
        # Use unique key for each button.
        if row_cols[j].button(btn_label, key=f"cell_{i}_{j}", disabled=disabled):
            # Only allow move if cell empty and game not over.
            if not st.session_state.game_over:
                result = game.play_turn(i, j)
                st.session_state.message = result["status"]
                if "wins" in result["status"] or "draw" in result["status"]:
                    st.session_state.game_over = True
                # In PvC mode, if human played and game is not over, then machine auto move on next rerun
                st.rerun()

st.write(st.session_state.message)

# If game is over, provide a reset option.
if st.session_state.game_over:
    if st.button("Restart Game"):
        start_new_game()
        st.rerun()