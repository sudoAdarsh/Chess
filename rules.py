class Piece:
    def __init__(self, color, symbol):
        self.color = color
        self.symbol = symbol
        self.has_moved = False
    


class Knight(Piece):
    def is_valid_move(self, start, end, board_state):
        s_row, s_col = start
        e_row, e_col = end
        
        diff_row = abs(s_row - e_row)
        diff_col = abs(s_col - e_col)
        
        if diff_col  == 0 and diff_row == 0:
            return 1
        # Check for (2 and 1) or (1 and 2)
        return (diff_row == 2 and diff_col == 1) or (diff_row == 1 and diff_col == 2)
    


class Pawn(Piece):
    def is_valid_move(self, start, end, board_state):
        s_row, s_col = start
        e_row, e_col = end

        direction = -1 if self.color == "white" else 1

        if s_col == e_col:
            if e_row == s_row + direction:
                return (e_row, e_col) not in board_state
            if e_row == s_row + (2 * direction):
                if not self.has_moved:
                    middle_sq = (s_row + direction, s_col)
                    return (e_row, e_col) not in board_state and middle_sq not in board_state

        elif abs(e_col - s_col) == 1:
            if e_row == s_row + direction:
                return (e_row, e_col) in board_state
        
        return False

class King(Piece):
    def is_valid_move(self, start, end, board_state):
        s_row, s_col = start
        e_row, e_col = end
        
        diff_row = abs(s_row - e_row)
        diff_col = abs(s_col - e_col)
        
        if diff_col  == 0 and diff_row == 0:
            return False
        # Check for (2 and 1) or (1 and 2)
        return (diff_row <= 1 and diff_col <= 1)

class Queen(Piece):
    def is_valid_move(self, start, end, board_state):
        rook_logic = Rook(self.color, self.symbol)
        if rook_logic.is_valid_move(start, end, board_state):
            return True
        
        bishop_logic = Bishop(self.color, self.symbol)
        if bishop_logic.is_valid_move(start, end,board_state):
            return True
        return False

class Rook(Piece):
    def is_valid_move(self, start, end, board_state):
        s_row, s_col = start
        e_row, e_col = end

        # Check if move is in straight line 
        if not (s_row == e_row or s_col == e_col):
            return False
        
        # Determine direction of travel
        row_step = 0 if s_row == e_row else (1 if e_row > s_row else -1)
        col_step = 0 if s_col == e_col else (1 if e_col > s_col else -1)

        current_r, current_c = s_row + row_step, s_col + col_step

        while (current_r, current_c) != (e_row, e_col):
            if (current_r, current_c) in board_state:
                return False
            current_r += row_step
            current_c += col_step
        
        return True

class Bishop(Piece):
    def is_valid_move(self, start, end, board_state):
        s_row, s_col = start
        e_row, e_col = end
        
        # Check if the move is diagonal 
        if abs(s_row - e_row) != abs(s_col - e_col):
            return False

        # Determine direction of travel
        row_step = 1 if e_row > s_row else -1
        col_step = 1 if e_col > s_col else -1

        current_r, current_c = s_row + row_step, s_col + col_step

        while (current_r, current_c) != (e_row, e_col):
            if (current_r, current_c) in board_state:
                return False
            current_r += row_step
            current_c += col_step
        
        return True



