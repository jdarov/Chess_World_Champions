# main.py

from tkinter import Tk
from chessgui import ChessGUI

def main():
    root = Tk()
    app = ChessGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
