from pieces import (
    Pawn, Rook, Knight, Bishop, Queen, King
)
from copy import deepcopy

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

    def move_piece(self, from_row, from_col, to_row, to_col, silent=False):
        if not self.is_within_bounds(from_row, from_col) or not self.is_within_bounds(to_row, to_col):
            if not silent:
                print("Move is out of bounds.")
            return

        piece = self.board[from_row][from_col]
        if not piece:
            if not silent:
                print("No piece at the starting position.")
            return

        target = self.board[to_row][to_col]
        if target and target.color == piece.color:
            if not silent:
                print("Cannot capture your own piece.")
            return

        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        piece.position = (to_row, to_col)

        if not silent:
            move_info = f"{chr(from_col + ord('a'))}{8 - from_row} to {chr(to_col + ord('a'))}{8 - to_row}"
            if target:
                print(f"{piece.color.capitalize()} {piece} captures {target} at {move_info}.")
            else:
                print(f"{piece.color.capitalize()} {piece} moves to {move_info}.")


# board.py

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        for row in self.board:
            for piece in row:
                if piece and piece.color != color:
                    if king_pos in piece.get_valid_moves(self):  # <- FIXED
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False

        for row in self.board:
            for piece in row:
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self):  # <- FIXED
                        temp_board = deepcopy(self)
                        from_row, from_col = piece.position
                        to_row, to_col = move
                        temp_board.move_piece(from_row, from_col, to_row, to_col, silent=True)

                        if not temp_board.is_in_check(color):
                            return False
        return True

    def find_king(self, color):
        for row in self.board:
            for piece in row:
                if piece and isinstance(piece, King) and piece.color == color:
                    return piece.position
