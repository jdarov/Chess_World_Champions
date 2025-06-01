class Piece:
    def __init__(self, color, position):
        self.color = color  # 'white' or 'black'
        self.position = position  # (row, col)

    def __str__(self):
        return self.symbol

    def get_valid_moves(self, board):
        raise NotImplementedError("This method should be implemented by subclasses")


class Pawn(Piece):
    @property
    def symbol(self):
        return 'P' if self.color == 'white' else 'p'

    def get_valid_moves(self, board):
        direction = -1 if self.color == 'white' else 1
        row, col = self.position
        moves = []

        # Move forward 1 square
        if board.is_within_bounds(row + direction, col) and board.board[row + direction][col] is None:
            moves.append((row + direction, col))

            # Double move from starting row
            start_row = 6 if self.color == 'white' else 1
            if row == start_row and board.board[row + 2 * direction][col] is None:
                moves.append((row + 2 * direction, col))

        # Diagonal captures
        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target and target.color != self.color:
                    moves.append((r, c))

        return moves


class Rook(Piece):
    @property
    def symbol(self):
        return 'R' if self.color == 'white' else 'r'

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Vertical and horizontal

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target is None:
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
    @property
    def symbol(self):
        return 'N' if self.color == 'white' else 'n'

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        knight_moves = [
            (row + 2, col + 1), (row + 2, col - 1),
            (row - 2, col + 1), (row - 2, col - 1),
            (row + 1, col + 2), (row + 1, col - 2),
            (row - 1, col + 2), (row - 1, col - 2)
        ]

        for r, c in knight_moves:
            if board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves


class Bishop(Piece):
    @property
    def symbol(self):
        return 'B' if self.color == 'white' else 'b'

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # Diagonals

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        return moves


class Queen(Piece):
    @property
    def symbol(self):
        return 'Q' if self.color == 'white' else 'q'

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),      # Rook moves
            (-1, -1), (-1, 1), (1, -1), (1, 1)     # Bishop moves
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            while board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target is None:
                    moves.append((r, c))
                elif target.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc

        return moves


class King(Piece):
    @property
    def symbol(self):
        return 'K' if self.color == 'white' else 'k'

    def get_valid_moves(self, board):
        moves = []
        row, col = self.position
        king_moves = [
            (row + 1, col), (row - 1, col),
            (row, col + 1), (row, col - 1),
            (row + 1, col + 1), (row + 1, col - 1),
            (row - 1, col + 1), (row - 1, col - 1)
        ]

        for r, c in king_moves:
            if board.is_within_bounds(r, c):
                target = board.board[r][c]
                if target is None or target.color != self.color:
                    moves.append((r, c))

        return moves
