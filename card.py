class Card:
    name = "Base Card"
    description = "No effect."

    def can_play(self, gui):
        return True

class PawnBoostCard(Card):
    name = "Pawn Boost"
    description = "Any pawn on its starting square may move 1, 2, or 3 spaces for this turn."

    def can_play(self, gui):
        # Only if player has at least one pawn on its starting square
        board = gui.board.board
        color = gui.turn
        row = 6 if color == "white" else 1
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color == color and piece.__class__.__name__.lower() == "pawn":
                return True
        return False

class BishopGhostCard(Card):
    name = "Bishop Ghost"
    description = "Your bishops can move through your own pieces, but cannot capture this turn."

    def can_play(self, gui):
        # Only restrict if the player is currently in check
        if gui.board.is_in_check(gui.turn):
            return False
        return True

class DestroyOpponentPieceCard(Card):
    name = "Destroy Opponent Piece"
    description = "Destroy any one opponent piece except King or Queen."

    def can_play(self, gui):
        opponent = 'black' if gui.turn == 'white' else 'white'
        for row in range(8):
            for col in range(8):
                piece = gui.board.board[row][col]
                if (piece and piece.color == opponent
                    and piece.__class__.__name__.lower() not in ("king", "queen")):
                    return True
        return False

class KnightmareLoopCard(Card):
    name = "Knightmare Loop"
    description = "Move the same knight twice this turn. Only one capture allowed."

    def can_play(self, gui):
        # Can play if player has a knight that can move at least once
        board = gui.board.board
        color = gui.turn
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece and piece.color == color and piece.__class__.__name__.lower() == "knight":
                    moves = piece.get_valid_moves(gui.board, row, col, gui)
                    if moves:
                        return True
        return False