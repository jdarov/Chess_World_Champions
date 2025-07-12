from pieces import King, Queen, Rook, Bishop, Knight, Pawn
import copy

class Board:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.reset_board()

    def reset_board(self):
        # Place pieces for both colors
        for col, piece in enumerate([Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]):
            self.board[0][col] = piece('black')
            self.board[7][col] = piece('white')
        for col in range(8):
            self.board[1][col] = Pawn('black')
            self.board[6][col] = Pawn('white')
        for row in range(2,6):
            for col in range(8):
                self.board[row][col] = None

    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None

    def copy(self):
        return copy.deepcopy(self)

    def find_king(self, color):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and isinstance(piece, King) and piece.color == color:
                    return (row, col)
        return None

    def is_in_check(self, color):
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    moves = piece.get_valid_moves(self, row, col)
                    if king_pos in moves:
                        return True
        return False

    def all_legal_moves(self, color):
        moves = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    for move in piece.get_valid_moves(self, row, col):
                        b_copy = self.copy()
                        b_copy.move_piece(row, col, move[0], move[1])
                        if not b_copy.is_in_check(color):
                            moves.append(((row, col), move))
        return moves

    def is_checkmate(self, color):
        return self.is_in_check(color) and not self.all_legal_moves(color)

    def is_stalemate(self, color):
        return not self.is_in_check(color) and not self.all_legal_moves(color)