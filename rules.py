def get_legal_moves(piece, pos, board):
    moves = []
    for r in range(8):
        for c in range(8):
            if piece.is_valid_move(pos, (r, c), board):
                moves.append((r, c))
    return moves


class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.has_moved = False

class Knight(Piece):
    def is_valid_move(self, start, end, board):
        sr, sc = start
        er, ec = end

        dr = abs(sr - er)
        dc = abs(sc - ec)

        if dr == 0 and dc == 0:
            return False

        return (dr == 2 and dc == 1) or (dr == 1 and dc == 2)

class King(Piece):
    def is_valid_move(self, start, end, board):
        sr, sc = start
        er, ec = end

        dr = abs(sr - er)
        dc = abs(sc - ec)

        if dr == 0 and dc == 0:
            return False

        return dr <= 1 and dc <= 1

class Rook(Piece):
    def is_valid_move(self, start, end, board):
        sr, sc = start
        er, ec = end

        if sr != er and sc != ec:
            return False

        r_step = 0 if sr == er else (1 if er > sr else -1)
        c_step = 0 if sc == ec else (1 if ec > sc else -1)

        r, c = sr + r_step, sc + c_step
        while (r, c) != (er, ec):
            if (r, c) in board:
                return False
            r += r_step
            c += c_step

        return True

class Bishop(Piece):
    def is_valid_move(self, start, end, board):
        sr, sc = start
        er, ec = end

        if abs(sr - er) != abs(sc - ec):
            return False

        r_step = 1 if er > sr else -1
        c_step = 1 if ec > sc else -1

        r, c = sr + r_step, sc + c_step
        while (r, c) != (er, ec):
            if (r, c) in board:
                return False
            r += r_step
            c += c_step

        return True

class Queen(Piece):
    def is_valid_move(self, start, end, board):
        return (
            Rook(self.color, self.symbol).is_valid_move(start, end, board)
            or Bishop(self.color, self.symbol).is_valid_move(start, end, board)
        )

class Pawn(Piece):
    def is_valid_move(self, start, end, board):
        sr, sc = start
        er, ec = end

        direction = -1 if self.color == "white" else 1

        # Forward move
        if sc == ec:
            if er == sr + direction and (er, ec) not in board:
                return True

            if (
                er == sr + 2 * direction
                and not self.has_moved
                and (sr + direction, sc) not in board
                and (er, ec) not in board
            ):
                return True

        # Diagonal capture
        if abs(ec - sc) == 1 and er == sr + direction:
            target = board.get((er, ec))
            return target is not None and target.color != self.color

        return False