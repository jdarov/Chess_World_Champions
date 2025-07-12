import os
from tkinter import Tk, Frame, Button, messagebox, simpledialog
from board import Board
from PIL import Image, ImageTk
from card import PawnBoostCard, BishopGhostCard, DestroyOpponentPieceCard

class ChessGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess World Champions")

        self.board = Board()
        self.turn = 'white'
        self.selected = None
        self.valid_moves = []
        self.square_size = 64

        self.board_frame = Frame(self.root)
        self.board_frame.pack()

        self.buttons = [[None for _ in range(8)] for _ in range(8)]

        # Card system
        self.hands = {
            'white': [PawnBoostCard(), BishopGhostCard(), DestroyOpponentPieceCard()],
            'black': [PawnBoostCard(), BishopGhostCard(), DestroyOpponentPieceCard()]
        }
        self.bishop_ghost_active = {'white': False, 'black': False}

        self.load_piece_images()
        self.draw_board()
        self.show_turn()

    def load_piece_images(self):
        base_path = os.path.join("assets", "pieces")
        piece_types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
        colors = ["white", "black"]

        self.images = {}

        for color in colors:
            for piece in piece_types:
                filename = f"{color}_{piece}.png"
                path = os.path.join(base_path, filename)
                try:
                    pil_img = Image.open(path).convert("RGBA")
                    datas = pil_img.getdata()
                    newData = []
                    for item in datas:
                        if item[:3] == (255, 255, 255):
                            newData.append((255, 255, 255, 0))
                        else:
                            newData.append(item)
                    pil_img.putdata(newData)
                    pil_img = pil_img.resize((self.square_size, self.square_size), Image.LANCZOS)
                    tk_img = ImageTk.PhotoImage(pil_img)
                    self.images[f"{color}_{piece}"] = tk_img
                except Exception as e:
                    print(f"Failed to load {filename}: {e}")

        empty = Image.new("RGBA", (self.square_size, self.square_size), (255, 255, 255, 0))
        self.empty_image = ImageTk.PhotoImage(empty)

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                default_color = "#e3e3e3" if (row + col) % 2 == 0 else "#888888"

                bg_color = default_color
                if self.selected == (row, col):
                    bg_color = "lightblue"
                elif (row, col) in self.valid_moves:
                    target_piece = self.board.board[row][col]
                    if target_piece and target_piece.color != self.turn:
                        bg_color = "#ff5555"
                    else:
                        bg_color = "lightgreen"

                if piece:
                    piece_type = piece.__class__.__name__.lower()
                    image_key = f"{piece.color}_{piece_type}"
                    image = self.images.get(image_key)
                else:
                    image = self.empty_image

                if self.buttons[row][col] is None:
                    btn = Button(
                        self.board_frame,
                        image=image,
                        text="",
                        bg=bg_color,
                        bd=0,
                        highlightthickness=0,
                        command=lambda r=row, c=col: self.on_click(r, c)
                    )
                    btn.grid(row=row, column=col)
                    self.buttons[row][col] = btn
                else:
                    self.buttons[row][col].config(image=image, text="", bg=bg_color)
                self.buttons[row][col].image = image

    def show_turn(self):
        hand = self.hands[self.turn]
        card_options = "\n".join([f"{i+1}. {card.name} ({card.description})" for i, card in enumerate(hand)])
        move_or_card = simpledialog.askstring(
            "Your Move",
            f"{self.turn.capitalize()}'s turn!\n\nType 'move' to move a piece, or:\n{card_options}\nType the number to play a card."
        )
        if move_or_card and move_or_card.strip().lower() == "move":
            # Wait for board click as usual
            return
        elif move_or_card and move_or_card.strip().isdigit():
            idx = int(move_or_card.strip()) - 1
            if 0 <= idx < len(hand):
                card = hand[idx]
                if card.can_play(self):
                    card.play(self)
                    # Remove card from hand after play
                    del hand[idx]
                    self.end_turn()
                    return
                else:
                    messagebox.showinfo("Card", "This card cannot be played at this time!")
                    self.show_turn()
            else:
                self.show_turn()
        else:
            self.show_turn()

    def end_turn(self):
        # Reset bishop ghost effect if it was active
        self.bishop_ghost_active[self.turn] = False
        self.turn = 'black' if self.turn == 'white' else 'white'
        self.selected = None
        self.valid_moves = []
        self.draw_board()
        self.show_turn()

    def on_click(self, row, col):
        piece = self.board.board[row][col]
        if self.selected:
            from_row, from_col = self.selected
            moving_piece = self.board.board[from_row][from_col]

            if (row, col) in self.valid_moves:
                self.board.move_piece(from_row, from_col, row, col)
                if self.board.is_checkmate('black' if self.turn == 'white' else 'white'):
                    self.draw_board()
                    messagebox.showinfo("Checkmate", f"{self.turn.capitalize()} wins by checkmate!")
                    self.root.quit()
                    return
                elif self.board.is_stalemate('black' if self.turn == 'white' else 'white'):
                    self.draw_board()
                    messagebox.showinfo("Stalemate", "Stalemate! The game is a draw.")
                    self.root.quit()
                    return
                elif self.board.is_in_check('black' if self.turn == 'white' else 'white'):
                    messagebox.showinfo("Check", f"{('Black' if self.turn == 'white' else 'White')} is in check!")
                self.end_turn()
                return

            self.selected = None
            self.valid_moves = []
            self.draw_board()

        elif piece and piece.color == self.turn:
            self.selected = (row, col)
            all_moves = piece.get_valid_moves(self.board, row, col, self)
            self.valid_moves = []
            for (r, c) in all_moves:
                board_copy = self.board.copy()
                board_copy.move_piece(row, col, r, c)
                if not board_copy.is_in_check(self.turn):
                    self.valid_moves.append((r, c))
            self.draw_board()