class Piece:
    def __init__(self, color):
        self.color = color

    def get_valid_moves(self, board, row, col):
        raise NotImplementedError("This method should be overridden by subclasses.")

class King(Piece):
    def get_valid_moves(self, board, row, col):
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
    def get_valid_moves(self, board, row, col):
        return Rook(self.color).get_valid_moves(board, row, col) + \
               Bishop(self.color).get_valid_moves(board, row, col)

class Rook(Piece):
    def get_valid_moves(self, board, row, col):
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
    def get_valid_moves(self, board, row, col):
        moves = []
        for dr, dc in [(-1,-1), (-1,1), (1,-1), (1,1)]:
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

class Knight(Piece):
    def get_valid_moves(self, board, row, col):
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
    def get_valid_moves(self, board, row, col):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        # Forward move
        if 0 <= row + direction < 8 and not board.board[row + direction][col]:
            moves.append((row + direction, col))
            # Double move from starting position
            if row == start_row and not board.board[row + 2 * direction][col]:
                moves.append((row + 2 * direction, col))
        # Captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target = board.board[r][c]
                if target and target.color != self.color:
                    moves.append((r, c))
        return moves