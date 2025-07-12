import tkinter as tk
from board import Board

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess World Champions")

        self.board = Board()
        self.turn = 'white'
        self.selected = None
        self.valid_moves = []

        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(8)] for _ in range(8)]
        self.draw_board()

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                text = str(piece) if piece else ""
                default_color = "white" if (row + col) % 2 == 0 else "gray"

                # Highlighting logic
                bg_color = default_color
                if self.selected == (row, col):
                    bg_color = "lightblue"  # Selected square
                elif (row, col) in self.valid_moves:
                    bg_color = "lightgreen"  # Valid move

                if self.buttons[row][col] is None:
                    btn = tk.Button(
                        self.board_frame,
                        text=text,
                        bg=bg_color,
                        width=6,
                        height=3,
                        command=lambda r=row, c=col: self.on_click(r, c)
                    )
                    btn.grid(row=row, column=col)
                    self.buttons[row][col] = btn
                else:
                    self.buttons[row][col].config(text=text, bg=bg_color)

    def on_click(self, row, col):
        piece = self.board.board[row][col]

        if self.selected:
            from_row, from_col = self.selected
            moving_piece = self.board.board[from_row][from_col]

            if (row, col) in self.valid_moves:
                self.board.move_piece(from_row, from_col, row, col)
                self.turn = 'black' if self.turn == 'white' else 'white'

            self.selected = None
            self.valid_moves = []
            self.draw_board()

        elif piece and piece.color == self.turn:
            self.selected = (row, col)
            self.valid_moves = piece.get_valid_moves(self.board)
            self.draw_board()
