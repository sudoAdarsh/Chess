from tkinter import *
from rules import *
import copy


# -------------------- CONSTANTS --------------------
LIGHT = "#d6ebd5"
DARK = "#528234"
SELECTED = "#9fd3e6"
LEGAL = "#b9ca4a"
LAST = "#016845"
FONT = ("DejaVu Sans", 60)
en_passant_target = None 
en_passant_pawn = None  

# -------------------- GAME STATE --------------------
current_turn = "white"
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

# -------------------- CHECK LOGIC --------------------
def find_king(color, board):
    for pos, piece in board.items():
        if isinstance(piece, King) and piece.color == color:
            return pos
    return None

def is_in_check(color, board):
    king_pos = find_king(color, board)
    if king_pos is None:
        return False
    for pos, piece in board.items():
        if piece.color != color:
            if piece.is_valid_move(pos, king_pos, board):
                return True
    return False


# -------------------- SIMULATION --------------------
def simulate_move(board, start, end):
    new_board = copy.deepcopy(board)
    piece = new_board.pop(start)
    if isinstance(piece, Pawn) and end == en_passant_target and end not in new_board:
        if en_passant_pawn in new_board:
            new_board.pop(en_passant_pawn)
    new_board[end] = piece
    return new_board



# -------------------- MOVE VALIDATION --------------------
def is_legal_move(piece, start, end, board):
    if start == end:
        return False
    target = board.get(end)
    if target and target.color == piece.color:
        return False
    
    if isinstance(piece, King) and abs(end[1] - start[1]) == 2 and start[0] == end[0]:
        return can_castle(piece, start, end, board)

    if isinstance(piece, Pawn) and end == en_passant_target and end not in board:
        sr, sc = start
        er, ec = end
        direction = -1 if piece.color == "white" else 1

        if er == sr + direction and abs(ec - sc) == 1:
            victim = board.get(en_passant_pawn)
            if victim and isinstance(victim, Pawn) and victim.color != piece.color:
                test = simulate_move(board, start, end)
                return not is_in_check(piece.color, test)
        return False
    
    if not piece.is_valid_move(start, end, board):
        return False
    test = simulate_move(board, start, end)
    return not is_in_check(piece.color, test)


def get_legal_moves(piece, pos, board):
    moves = []
    for r in range(8):
        for c in range(8):
            end = (r, c)
            if is_legal_move(piece, pos, end, board):
                moves.append((r, c))
    return moves


def can_castle(king, start, end, board):
    if king.has_moved or is_in_check(king.color, board):
        return False
    
    sr, sc = start
    er, ec = end

    direction = 1 if ec > sc else -1
    rook_col = 7 if direction == 1 else 0
    rook_pos = (sr, rook_col)

    rook = board.get(rook_pos)
    if not rook or not isinstance(rook, Rook) or rook.has_moved:
        return False
    
    for c in range(sc + direction, rook_col, direction):
        if (sr, c) in board:
            return False
        
    for c in [sc + direction, sc + 2 * direction]:
        temp = simulate_move(board, start, (sr, c))
        if is_in_check(king.color, temp):
            return False
    return True

# -------------------- PAWN PROMOTION --------------------
def choose_promotion(color):
    choice = {"piece": None}

    win = Toplevel(root)
    win.title("Pawn Promotion")
    win.configure(bg="gray20")
    win.update_idletasks()
    win.grab_set()
    win.resizable(False, False)

    Label(
        win,
        text="Choose Promotion",
        font=("DejaVu Sans", 14),
        bg="gray20",
        fg="white"
    ).pack(padx=10, pady=10)

    pieces = [
        ("Queen", Queen, "♕" if color == "white" else "♛"),
        ("Rook", Rook,  "♖" if color == "white" else "♜"),
        ("Bishop", Bishop, "♗" if color == "white" else "♝"),
        ("Knight", Knight, "♘" if color == "white" else "♞"),
    ]

    frame = Frame(win, bg="gray20")
    frame.pack(padx=10, pady=10)

    def select(piece_class, symbol):
        choice["piece"] = (piece_class, symbol)
        try:
            win.grab_release()
        except TclError: 
            pass
        win.destroy()

    for name, cls, sym in pieces:
        Button(
            frame,
            text=sym,
            font=FONT,
            width=2,
            command=lambda c=cls, s=sym: select(c, s)
        ).pack(side=LEFT, padx=5)

    win.wait_window()
    return choice["piece"]

# -------------------- CLICK HANDLER --------------------
def on_click(event, r, c):
    global selected_square, last_move, highlighted_moves, current_turn, en_passant_pawn, en_passant_target
    
    if game_over:
        return
    
    clicked = (r, c)

    # First click: select a piece
    if selected_square is None:
        piece = board_state.get(clicked)
        if not piece or piece.color != current_turn:
            return
        selected_square = clicked
        highlighted_moves = get_legal_moves(piece, clicked, board_state)
        update_board()
        return


    # Second click: try to move
    if clicked == selected_square:   # Same color
        selected_square = None
        highlighted_moves = []
        update_board()
        return
    
    if selected_square is not None:  # Safety check
        clicked_piece = board_state.get(clicked)
        if clicked_piece and clicked_piece.color == current_turn:
            selected_square = clicked
            highlighted_moves = get_legal_moves(clicked_piece, clicked, board_state)
            update_board()
            return
        
    if clicked not in highlighted_moves:  # Illegal move
        selected_square = None
        highlighted_moves = []
        update_board()
        return

    start = selected_square
    piece = board_state.get(start)

    if not is_legal_move(piece, start, clicked, board_state):
        print("Illegal move")
        selected_square = None
        highlighted_moves = []
        update_board
        return
    
    if isinstance(piece, King) and abs(clicked[1] - start[1]) == 2:
        row = start[0]
        if clicked[1] > start[1]:
            # King-side: rook h -> f
            rook_start = (row, 7)
            rook_end = (row, 5)
        else:
            # Queen-side: rook a -> d
            rook_start = (row, 0)
            rook_end = (row, 3)

        rook = board_state.pop(rook_start)
        board_state[rook_end] = rook
        rook.has_moved = True

    if isinstance(piece, Pawn) and clicked == en_passant_target and clicked not in board_state:
        if en_passant_pawn in board_state:
            board_state.pop(en_passant_pawn)

    piece = board_state.pop(start)
    board_state[clicked] = piece

    en_passant_target = None
    en_passant_pawn = None

    if isinstance(piece, Pawn) and abs(clicked[0] - start[0]) == 2:
        mid_row = (clicked[0] + start[0]) // 2
        en_passant_target = (mid_row, clicked[1])
        en_passant_pawn = clicked

    # Pawn Promotion
    if isinstance(piece, Pawn):
        if (piece.color == "white" and clicked[0] == 0) or (piece.color == "black" and clicked[0] == 7):
            promo = choose_promotion(piece.color)
            if promo:
                cls, sym = promo
                board_state[clicked] = cls(piece.color, sym)
            else:
                board_state[clicked] = piece


    last_move = (start, clicked)
    piece.has_moved = True

    selected_square = None
    highlighted_moves = []
    current_turn = "black" if current_turn == "white" else "white"
    flip_board()
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


def flip_board():
    for (r, c), lbl in grid.items():
        lbl.grid(
            row=r if current_turn == "white" else 7 - r,
            column=c if current_turn == "white" else 7 - c
        )


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