class Piece:
    def __init__(self, color):
        self.color = color

    def get_valid_moves(self, board, row, col, gui=None):
        raise NotImplementedError("This method should be overridden by subclasses.")

class King(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),          (0, 1),
                      (1, -1),  (1, 0), (1, 1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if not target or target.color != self.color:
                    moves.append((r, c))
        return moves

class Queen(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        return Rook(self.color).get_valid_moves(board, row, col, gui) + \
               Bishop(self.color).get_valid_moves(board, row, col, gui)

class Rook(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        moves = []
        for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if not target:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

class Bishop(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        moves = []
        ghost = False
        if gui:
            ghost = gui.bishop_ghost_active.get(self.color, False)
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if not target:
                    moves.append((r, c))
                elif target.color == self.color:
                    if ghost:
                        moves.append((r, c))
                        r += dr
                        c += dc
                        continue
                    else:
                        break
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                r += dr
                c += dc
        return moves

class Knight(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        moves = []
        for dr, dc in [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                       (1, -2), (1, 2), (2, -1), (2, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if not target or target.color != self.color:
                    moves.append((r, c))
        return moves

class Pawn(Piece):
    def get_valid_moves(self, board, row, col, gui=None):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        max_steps = 1

        # Card: PawnBoostCard effect (stub)
        if gui:
            if hasattr(gui, "pawn_boost_active") and gui.pawn_boost_active.get((row, col), False):
                max_steps = 3
            elif row == start_row:
                max_steps = 2

        for step in range(1, max_steps + 1):
            r = row + direction * step
            if 0 <= r < 8 and not board.board[r][col]:
                moves.append((r, col))
            else:
                break
        # Captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if target and target.color != self.color:
                    moves.append((r, c))
        return moves
