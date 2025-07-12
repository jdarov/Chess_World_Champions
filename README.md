# ♛ Chess World Champions ♚  

> *Classic Chess. Card-Based Chaos. The Next Evolution.*

---

## 🎲 1. What is Chess World Champions?

**Chess World Champions** is a strategic, multiplayer chess game infused with collectible card mechanics.  
Outwit your opponent using both time-honored chess tactics and powerful, game-changing cards in a reimagined battle of wits!

---

## 🎯 2. Purpose of the Game

The purpose is simple:  
- **Win by checkmate** or outmaneuver your opponent using a unique set of cards that modify movement, trigger effects, or alter the board state.
- Experience chess like never before—every match is unpredictable, tactical, and full of surprises.
- This MVP (Minimum Viable Product) is the foundation for a future full-featured app, web version, and potential commercial release.

---

## 🔁 3. Game Logic & Flow

### **Turn Structure:**
1. **Player's Turn:**  
   - Choose to **move a piece** *or* **play/draw a card** from your hand.
2. **Card Play:**  
   - Cards are one-time use, with effects ranging from boosting pawns, allowing power moves, or removing opponent pieces (except the king/queen!).
   - Card effects last for the current turn only.
3. **Victory:**  
   - Standard chess victory (checkmate).
   - Optional: "First to 20 points" mode for fast games (see below).

### **Card System:**
- Each player starts with a hand of 3 cards.
- Decks and additional cards will be added in future versions.
- Card examples:  
  - Pawn Boost (move pawns up to 3 spaces)  
  - Bishop Ghost (bishop passes through friendly pieces)  
  - Destroy Opponent Piece (remove any non-king/queen enemy piece)

---

## 📁 4. Project Structure

```
Chess_World_Champions/
├── game_logic/           # Core chess rules and card engine
├── card_data/            # JSON files for card definitions
├── ui/                   # CLI for now, web UI in planning
├── nft_assets/           # Placeholder for NFT artwork
├── assets/               # Piece images, icons, and graphics
└── README.md             # This file!
```

---

## ⚙️ 5. Getting Started & Requirements

To run or contribute to this project, you'll need:

- **Python 3.8+**
- **Pillow** (`pip install Pillow`)
- **tkinter** (usually included with Python)
- (Optional) Other dependencies as features are added

**Quickstart:**
```bash
git clone https://github.com/jdarov/Chess_World_Champions.git
cd Chess_World_Champions
pip install Pillow
python main.py
```
*(Replace `main.py` with your entry-point script if different)*

---

## 🛡️ 6. Copyright & Contribution

This project is copyright © 2025  
**Joshua Darovitz (jdarov)**

- Forks, issues, and contributions are encouraged!
- Please **reference the original author** in your forks and derivative works.
- Commercial use or redistribution requires explicit permission.
- Card ideas, logic tweaks, and UI improvements are welcome—just open an issue or a pull request.

---

## 🚀 Roadmap

- ✅ Chess + card MVP (local multiplayer)
- ⏳ Web UI in React.js
- 🔜 Deck customization & more cards
- 🔜 NFT integration for unique piece skins, traits, and exclusive cards
- 🔜 Online play & ranking

---

## 💡 Philosophy

> "Chess is a war over the board. The object is to crush the opponent’s mind."  
> — Bobby Fischer

With Chess World Champions, the *battlefield just got a lot more unpredictable.*  
Play smart. Play bold. Play your cards right.

---

## 📫 Contact & Support

- Author: [Joshua Darovitz (jdarov)](https://github.com/jdarov)
- [YouTube: Jdarov | From Diesel to Debugging](https://www.youtube.com/@jdarov)

Have fun, and checkmate with style!