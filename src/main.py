"""

    hammer: an inventory management system developed in 
    python with sqlite3

    version: v0.1.0a

"""

import tkinter as tk
from tkinter import ttk

from database import Database
from menu_bar import MenuBar

version = 'v0.1.0a'


class Hammer(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f"hammer - {version}")
        menu_bar = MenuBar(self)
        self.config(menu=menu_bar)


if __name__ == "__main__":
    root = Hammer()
    root.mainloop()
    
    db = Database("hammer.db")
