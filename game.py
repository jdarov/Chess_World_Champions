# game.py
from board import Board

class ChessGame:
    def __init__(self):
        self.board = Board()
        self.turn = 'white'

    def start(self):
        while True:
            self.board.display()

            if self.board.is_checkmate(self.turn):
                winner = 'black' if self.turn == 'white' else 'white'
                print("\n" + "=" * 35)
                print(f"|       CHECKMATE! {winner.upper()} WINS!    |")
                print("=" * 35 + "\n")
                play_again = input("Would you like to play again? (Y/N): ").strip().lower()
                if play_again.startswith('y'):
                    self.__init__()  # reinitialize the game
                    continue
                else:
                    print("Thanks for playing!")
                    break

            elif self.board.is_in_check(self.turn):
                print("CHECK!")

            print(f"{self.turn.capitalize()}'s move")
            move = input("Enter move (e.g., e2 e4 or 'quit'): ").strip().lower()

            if move == 'quit':
                print("Thanks for playing!")
                break

            try:
                start_pos, end_pos = move.split()
                from_row, from_col = self.convert_to_coords(start_pos)
                to_row, to_col = self.convert_to_coords(end_pos)

                piece = self.board.board[from_row][from_col]

                if not piece or piece.color != self.turn:
                    print("Invalid piece. Try again.")
                    continue

                valid_moves = piece.get_valid_moves(self.board)
                if (to_row, to_col) not in valid_moves:
                    print("Invalid move. Try again.")
                    continue

                self.board.move_piece(from_row, from_col, to_row, to_col)
                self.turn = 'black' if self.turn == 'white' else 'white'

            except ValueError:
                print("Invalid input format. Use e.g., e2 e4")

    def convert_to_coords(self, pos):
        col = ord(pos[0]) - ord('a')
        row = 8 - int(pos[1])
        return (row, col)
