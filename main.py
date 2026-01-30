from tkinter import *
from rules import *


# -------------------- CONSTANTS --------------------
LIGHT = "#d6ebd5"
DARK = "#528234"
SELECTED = "#9fd3e6"
LEGAL = "#b9ca4a"
LAST = "#016845"
FONT = ("DejaVu Sans", 60)

# -------------------- GAME STATE --------------------
selected_square = None
highlighted_moves = []
last_move = None
selected_square = None
game_over = False

# -------------------- BOARD SETUP --------------------
def new_board():
    board = {}
    ranks = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
    white = ["♖", "♘", "♗", "♕", "♔", "♗", "♘", "♖"]
    black = ["♜", "♞", "♝", "♛", "♚", "♝", "♞", "♜"]

    for i in range(8):
        board[(0, i)] = ranks[i]("black", black[i])
        board[(1, i)] = Pawn("black", "♟")
        board[(6, i)] = Pawn("white", "♙")
        board[(7, i)] = ranks[i]("white", white[i])

    return board

board_state = new_board()


# -------------------- CLICK HANDLER --------------------
def on_click(event, r, c):
    global selected_square, last_move, highlighted_moves
    
    if game_over:
        return
    
    clicked = (r, c)

    # First click: select a piece
    if selected_square is None:
        piece = board_state.get(clicked)
        if not piece:
            return
        selected_square = clicked
        highlighted_moves = get_legal_moves(piece, clicked, board_state)
        update_board()
        return


    # Second click: try to move
    if clicked not in highlighted_moves:
        print("Invalid move")
        selected_square = None
        highlighted_moves = []
        update_board()
        return

    start = selected_square
    piece = board_state.pop(start)
    board_state[clicked] = piece
    last_move = (start, clicked)

    selected_square = None
    highlighted_moves = []
    update_board()


# -------------------- UI --------------------
def update_board():
    for (r, c), lbl in grid.items():
        base = LIGHT if (r + c) % 2 == 0 else DARK
        color = base

        if last_move and (r, c) in last_move:
            color = LAST
        if (r, c) in highlighted_moves:
            color = LEGAL
        if selected_square == (r, c):
            color = SELECTED
        
        lbl.config(bg=color)
        piece = board_state.get((r, c))
        lbl.config(text=piece.symbol if piece else "")



# -------------------- TKINTER --------------------
root = Tk()
root.title("Chess")
root.configure(bg="gray20")  #  <---- choose background color from "https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html"

frame = Frame(root)
frame.pack(padx=20, pady=20)   

grid = {}

for r in range(8):
    for c in range(8):
        lbl = Label(frame, width=2, height=1, font=FONT, relief="solid", bd=1)
        lbl.grid(row=r, column=c)
        lbl.bind("<Button-1>", lambda e, r=r, c=c: on_click(e, r, c))
        grid[(r, c)] = lbl

update_board()
root.mainloop()