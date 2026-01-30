from tkinter import *
from rules import *


# -------------------- CONSTANTS --------------------
LIGHT = "#d6ebd5"
DARK = "#528234"
SELECTED = "#9fd3e6"
LEGAL = "#b9ca4a"
LAST = "#f5f682"
FONT = ("DejaVu Sans", 60)


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


# -------------------- UI --------------------
def update_board():
    for (r, c), lbl in grid.items():
        color = LIGHT if (r + c) % 2 == 0 else DARK
        
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
        grid[(r, c)] = lbl

update_board()
root.mainloop()