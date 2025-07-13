import os
from tkinter import Tk, Frame, Button, messagebox, simpledialog
from board import Board
from PIL import Image, ImageTk
from card import PawnBoostCard, BishopGhostCard, DestroyOpponentPieceCard, KnightmareLoopCard

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
            'white': [PawnBoostCard(), BishopGhostCard(), DestroyOpponentPieceCard(), KnightmareLoopCard()],
            'black': [PawnBoostCard(), BishopGhostCard(), DestroyOpponentPieceCard(), KnightmareLoopCard()]
        }
        self.bishop_ghost_active = {'white': False, 'black': False}
        self.pawn_boost_active = {'white': False, 'black': False}
        self.knightmare_active = {'white': False, 'black': False}
        self.knightmare_state = None  # Track knight pos, capture, moves for this turn
        self.knightmare_doing_second_move = False

        self.active_card = None  # Track the card being played
        self.game_over = False

        self.root.protocol("WM_DELETE_WINDOW", self.quit_game)

        self.load_piece_images()
        self.draw_board()
        self.show_turn()

    def quit_game(self):
        self.game_over = True
        try:
            self.root.destroy()
        except Exception:
            pass

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
        # Don't prompt if game over
        if self.game_over:
            return

        hand = self.hands[self.turn]

        # If hand is empty, skip prompt and allow direct board interaction
        if not hand:
            return

        card_options = "\n".join([f"{i+1}. {card.name} ({card.description})" for i, card in enumerate(hand)])
        move_or_card = simpledialog.askstring(
            "Your Move",
            f"{self.turn.capitalize()}'s turn!\n\nType 'move' to move a piece, or:\n{card_options}\nType the number to play a card."
        )
        if move_or_card is None:
            self.quit_game()
            return

        if move_or_card.strip().lower() == "move":
            return
        elif move_or_card.strip().isdigit():
            idx = int(move_or_card.strip()) - 1
            if 0 <= idx < len(hand):
                card = hand[idx]
                if card.can_play(self):
                    self.active_card = card
                    if isinstance(card, BishopGhostCard):
                        self.bishop_ghost_active[self.turn] = True
                    elif isinstance(card, PawnBoostCard):
                        self.pawn_boost_active[self.turn] = True
                    elif isinstance(card, KnightmareLoopCard):
                        self.knightmare_active[self.turn] = True
                        self.knightmare_state = {
                            "knight_pos": None,
                            "capture_done": False,
                            "first_move_done": False
                        }
                        self.knightmare_doing_second_move = False
                        messagebox.showinfo("Card Activated", f"{card.name} is active! Select your knight to move twice this turn.")
                        self.selected = None
                        self.valid_moves = []
                        self.draw_board()
                        return
                    if isinstance(card, DestroyOpponentPieceCard):
                        self.handle_destroy_card()
                        if card in self.hands[self.turn]:
                            self.hands[self.turn].remove(card)
                        self.active_card = None
                        self.end_turn()
                        return
                    else:
                        messagebox.showinfo("Card Activated", f"{card.name} is active. Make your move using the card's effect.")
                        self.selected = None
                        self.valid_moves = []
                        self.draw_board()
                        return
                else:
                    messagebox.showinfo("Card", "This card cannot be played at this time!")
                    self.show_turn()
            else:
                self.show_turn()
        else:
            self.show_turn()

    def handle_destroy_card(self):
        opponent = 'black' if self.turn == 'white' else 'white'
        valid_targets = []
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if (piece and piece.color == opponent and
                    piece.__class__.__name__.lower() not in ("king", "queen")):
                    valid_targets.append((row, col))
        if not valid_targets:
            messagebox.showinfo("Destroy", "No valid opponent pieces to destroy.")
            return
        coord_str = "\n".join([f"{i+1}: {self.coord_to_alg(row, col)}" for i, (row, col) in enumerate(valid_targets)])
        pick = simpledialog.askstring(
            "Destroy Opponent Piece",
            f"Select one opponent piece to destroy:\n{coord_str}\nType the number."
        )
        if pick is None:
            self.quit_game()
            return
        if pick.strip().isdigit():
            idx = int(pick.strip()) - 1
            if 0 <= idx < len(valid_targets):
                row, col = valid_targets[idx]
                self.board.board[row][col] = None
                self.draw_board()
                messagebox.showinfo("Destroyed", f"Piece at {self.coord_to_alg(row, col)} destroyed.")

    def coord_to_alg(self, row, col):
        return f"{chr(ord('a')+col)}{8-row}"

    def end_turn(self):
        self.bishop_ghost_active[self.turn] = False
        self.pawn_boost_active[self.turn] = False
        self.knightmare_active[self.turn] = False
        self.knightmare_state = None
        self.knightmare_doing_second_move = False
        self.active_card = None
        self.selected = None
        self.valid_moves = []

        opponent = 'black' if self.turn == 'white' else 'white'
        if self.board.is_checkmate(opponent):
            self.draw_board()
            messagebox.showinfo("Checkmate", f"{self.turn.capitalize()} wins by checkmate!")
            self.game_over = True
            self.quit_game()
            return
        elif self.board.is_stalemate(opponent):
            self.draw_board()
            messagebox.showinfo("Stalemate", "Stalemate! The game is a draw.")
            self.game_over = True
            self.quit_game()
            return

        self.turn = opponent
        self.draw_board()
        self.show_turn()

    def on_click(self, row, col):
        if self.game_over:
            return

        # Knightmare Loop logic
        if self.knightmare_active[self.turn]:
            # First selection: select knight to use
            if not self.knightmare_state["first_move_done"]:
                piece = self.board.board[row][col]
                if piece and piece.color == self.turn and piece.__class__.__name__.lower() == "knight":
                    self.selected = (row, col)
                    all_moves = piece.get_valid_moves(self.board, row, col, self)
                    self.valid_moves = []
                    for (r, c) in all_moves:
                        board_copy = self.board.copy()
                        board_copy.move_piece(row, col, r, c)
                        if not board_copy.is_in_check(self.turn):
                            self.valid_moves.append((r, c))
                    self.draw_board()
                elif self.selected and (row, col) in self.valid_moves:
                    from_row, from_col = self.selected
                    moving_piece = self.board.board[from_row][from_col]
                    target = self.board.board[row][col]
                    capture = target is not None
                    self.board.move_piece(from_row, from_col, row, col)
                    # Save which knight is moving, and whether capture occurred
                    self.knightmare_state["knight_pos"] = (row, col)
                    self.knightmare_state["capture_done"] = capture
                    self.knightmare_state["first_move_done"] = True
                    self.knightmare_doing_second_move = True
                    # Now highlight the same knight for its second move
                    self.selected = (row, col)
                    all_moves = moving_piece.get_valid_moves(self.board, row, col, self)
                    self.valid_moves = []
                    for (r, c) in all_moves:
                        # On second move, restrict captures if already captured
                        if capture:
                            if self.board.board[r][c] is None:
                                board_copy = self.board.copy()
                                board_copy.move_piece(row, col, r, c)
                                if not board_copy.is_in_check(self.turn):
                                    self.valid_moves.append((r, c))
                        else:
                            board_copy = self.board.copy()
                            board_copy.move_piece(row, col, r, c)
                            if not board_copy.is_in_check(self.turn):
                                self.valid_moves.append((r, c))
                    self.draw_board()
                else:
                    self.selected = None
                    self.valid_moves = []
                    self.draw_board()
            # Second move
            elif self.knightmare_doing_second_move and self.selected:
                from_row, from_col = self.selected
                knight_pos = self.knightmare_state["knight_pos"]
                if (from_row, from_col) != knight_pos:
                    self.selected = knight_pos
                    from_row, from_col = knight_pos
                piece = self.board.board[from_row][from_col]
                if piece is None or piece.__class__.__name__.lower() != "knight":
                    self.end_turn()
                    return
                if (row, col) in self.valid_moves:
                    target = self.board.board[row][col]
                    # On second move, can only capture if no capture yet
                    if self.knightmare_state["capture_done"]:
                        if target is not None:
                            # Invalid, can't capture again
                            return
                    self.board.move_piece(from_row, from_col, row, col)
                    # Clean up
                    if self.active_card and self.active_card in self.hands[self.turn]:
                        self.hands[self.turn].remove(self.active_card)
                    self.active_card = None
                    self.knightmare_active[self.turn] = False
                    self.knightmare_state = None
                    self.knightmare_doing_second_move = False
                    self.selected = None
                    self.valid_moves = []
                    self.draw_board()
                    # Check checkmate/stalemate
                    opponent = 'black' if self.turn == 'white' else 'white'
                    if self.board.is_checkmate(opponent):
                        self.draw_board()
                        messagebox.showinfo("Checkmate", f"{self.turn.capitalize()} wins by checkmate!")
                        self.game_over = True
                        self.quit_game()
                        return
                    elif self.board.is_stalemate(opponent):
                        self.draw_board()
                        messagebox.showinfo("Stalemate", "Stalemate! The game is a draw.")
                        self.game_over = True
                        self.quit_game()
                        return
                    elif self.board.is_in_check(opponent):
                        messagebox.showinfo("Check", f"{('Black' if self.turn == 'white' else 'White')} is in check!")
                    self.end_turn()
                    return
                else:
                    # Did not pick valid move, stay on knight
                    self.selected = (from_row, from_col)
                    self.draw_board()
            return

        piece = self.board.board[row][col]
        if self.selected:
            from_row, from_col = self.selected
            moving_piece = self.board.board[from_row][from_col]
            if (row, col) in self.valid_moves:
                self.board.move_piece(from_row, from_col, row, col)
                # Remove card if active
                if self.active_card:
                    if self.active_card in self.hands[self.turn]:
                        self.hands[self.turn].remove(self.active_card)
                    self.active_card = None
                    self.bishop_ghost_active[self.turn] = False
                    self.pawn_boost_active[self.turn] = False

                # Check for check after move
                opponent = 'black' if self.turn == 'white' else 'white'
                if self.board.is_checkmate(opponent):
                    self.draw_board()
                    messagebox.showinfo("Checkmate", f"{self.turn.capitalize()} wins by checkmate!")
                    self.game_over = True
                    self.quit_game()
                    return
                elif self.board.is_stalemate(opponent):
                    self.draw_board()
                    messagebox.showinfo("Stalemate", "Stalemate! The game is a draw.")
                    self.game_over = True
                    self.quit_game()
                    return
                elif self.board.is_in_check(opponent):
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