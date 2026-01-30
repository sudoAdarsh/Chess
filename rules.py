class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.has_moved = False

class Knight(Piece):
    def is_valid_move(self):
        pass

class King(Piece):
    def is_valid_move(self):
        pass

class Rook(Piece):
    def is_valid_move(self):
        pass

class Bishop(Piece):
    def is_valid_move(self):
        pass

class Queen(Piece):
    def is_valid_move(self):
        pass

class Pawn(Piece):
    def is_valid_move(self):
        pass