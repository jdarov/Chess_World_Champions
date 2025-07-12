from abc import ABC, abstractmethod

class Card(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description

    @abstractmethod
    def can_play(self, gui):
        """Returns True if the card can be played in the current state."""
        return True

    @abstractmethod
    def play(self, gui):
        """Apply the card effect to the board."""
        pass

class PawnBoostCard(Card):
    def __init__(self):
        super().__init__(
            name="Pawn Boost",
            description="Move any pawn forward up to 3 spaces instead of the usual 1 or 2 (if still unmoved)."
        )

    def can_play(self, gui):
        # Can play if at least one pawn that can move forward 3 spaces
        board = gui.board
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.__class__.__name__.lower() == 'pawn' and piece.color == gui.turn:
                    # Check if pawn is at starting row
                    if (piece.color == 'white' and row == 6) or (piece.color == 'black' and row == 1):
                        # Check if 1, 2, or 3 spaces ahead are empty
                        direction = -1 if piece.color == 'white' else 1
                        for dist in range(1, 4):
                            r = row + dist * direction
                            if 0 <= r < 8 and not board.board[r][col]:
                                return True
                            if 0 <= r < 8 and board.board[r][col]:
                                break  # blocked
        return False

    def play(self, gui):
        # Prompt user to pick a pawn and a target square up to 3 spaces forward (implement with a GUI dialog or in cli, for now just print)
        print("Select a pawn to move up to 3 spaces forward.")
        # You'd need to implement UI to select which pawn and where to move.
        # For now, this is just a stub.

class BishopGhostCard(Card):
    def __init__(self):
        super().__init__(
            name="Bishop Ghost",
            description="For this turn, your bishops can move diagonally through your own pieces."
        )

    def can_play(self, gui):
        # Can always play if the player has a bishop
        board = gui.board
        for row in range(8):
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.__class__.__name__.lower() == 'bishop' and piece.color == gui.turn:
                    return True
        return False

    def play(self, gui):
        # Set a flag on the board or GUI for this player for this turn
        print("Your bishops can pass through your own pieces this turn.")
        gui.bishop_ghost_active = True

class DestroyOpponentPieceCard(Card):
    def __init__(self):
        super().__init__(
            name="Destroy",
            description="Pick one piece on opponent's side of the field and destroy it."
        )

    def can_play(self, gui):
        # Can play if opponent has at least one piece on your side
        board = gui.board
        opponent = 'black' if gui.turn == 'white' else 'white'
        your_side = range(0, 4) if gui.turn == 'white' else range(4, 8)
        for row in your_side:
            for col in range(8):
                piece = board.board[row][col]
                if piece and piece.color == opponent:
                    return True
        return False

    def play(self, gui):
        # Prompt user to pick an opponent piece on your side to destroy
        print("Select an opponent's piece on your side of the board to destroy.")
        # You'd need to implement UI to select which piece to destroy
        # For now, this is just a stub.
