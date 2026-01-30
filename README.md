# ♟️ Chess 

A **fully functional chess game** built from scratch in Python using Tkinter.  
All core chess rules are implemented manually, with a clear separation between **game logic** and **UI**.

This project focuses on correctness, state management, and clean architecture rather than visual effects or external libraries.

---

## ✨ Highlights

- Complete chess ruleset implemented **without using any chess libraries**
- Rule validation via move simulation (prevents illegal king exposure)
- Clean separation of concerns:
  - UI & game flow → `main.py`
  - Piece rules & movement → `rules.py`

---

## ♜ Game Features

### Core Gameplay
- Two-player (local) chess
- Click-to-select, click-to-move interface
- Automatic board flip after each turn
- Legal move highlighting

### Chess Rules (All Implemented)
- Correct movement for all pieces
- Captures
- Pawn double move (first move only)
- Pawn promotion (player choice: Queen, Rook, Bishop, Knight)
- Castling (king-side & queen-side)
- En passant
- Check detection
- Checkmate
- Stalemate
- King safety (cannot move into or remain in check)
- Pinned pieces handled correctly

### User Feedback & UI
- Popup messages for:
  - Checkmate
  - Stalemate
- King square highlighted in **red** when in check
- Last move highlighting

---

## 🧠 How It Works (Design Overview)

- The board is stored as a dictionary:  
  `(row, col) → Piece`
- Each piece defines its own movement logic
- Legal moves are determined by:
  1. Valid piece movement
  2. Simulating the move
  3. Rejecting moves that leave the king in check
- Special rules (castling, en passant, promotion) are layered on top of this system

This approach mirrors how real chess engines validate moves at a basic level.

---

## 📁 Project Structure
```
.
├── main.py     # Game loop, UI, state management
└── rules.py    # Piece movement rules and logic
```
---

## ▶️ Running the Game

### Requirements
- Python 3.x
- Tkinter (included with standard Python)

### Run
```python
python main.py
```
---
## 👤 Author
Built as a personal project to deeply understand chess rules, stateful systems, and UI-driven applications in Python.

The primary motivation behind this project was to implement chess rules manually.
Future versions may explore integration with `python-chess` for engine support and advanced features.
#### ⚠️ Known Limitations
- Closing the pawn promotion dialog without selecting a piece may cause unexpected behavior
- Board size depends on font size and can be adjusted in `main.py`
