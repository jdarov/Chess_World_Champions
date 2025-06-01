from pieces import (
    Pawn, Rook, Knight, Bishop, Queen, King
)

class Board:
    def __init__(self):
        self.board = self.create_starting_board()

    def create_starting_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]

        # Back ranks
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]

        # Black pieces
        for col, piece_class in enumerate(piece_order):
            board[0][col] = piece_class('black', (0, col))
        for col in range(8):
            board[1][col] = Pawn('black', (1, col))

        # White pieces
        for col in range(8):
            board[6][col] = Pawn('white', (6, col))
        for col, piece_class in enumerate(piece_order):
            board[7][col] = piece_class('white', (7, col))

        return board

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def is_empty(self, row, col):
        return self.is_within_bounds(row, col) and self.board[row][col] is None

    def display(self):
        print("  a b c d e f g h")
        print(" +-----------------+")
        for row_idx, row in enumerate(self.board):
            row_display = []
            for cell in row:
                row_display.append(str(cell) if cell else '.')
            print(f"{8 - row_idx}|{' '.join(row_display)}|")
        print(" +-----------------+")
        print("  a b c d e f g h")

    def move_piece(self, from_row, from_col, to_row, to_col):
        if not self.is_within_bounds(from_row, from_col) or not self.is_within_bounds(to_row, to_col):
            print("Move is out of bounds.")
            return

        piece = self.board[from_row][from_col]
        if not piece:
            print("No piece at the starting position.")
            return

        target = self.board[to_row][to_col]
        if target and target.color == piece.color:
            print("Cannot capture your own piece.")
            return

        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.position = (to_row, to_col)

        move_info = f"{chr(from_col + ord('a'))}{8 - from_row} to {chr(to_col + ord('a'))}{8 - to_row}"
        if target:
            print(f"{piece.color.capitalize()} {piece} captures {target} at {move_info}.")
        else:
            print(f"{piece.color.capitalize()} {piece} moves to {move_info}.")
