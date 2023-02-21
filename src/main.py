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
        self.minsize(400, 300)
        self.db = Database("hammer.db")
        menu_bar = MenuBar(self)
        self.config(menu=menu_bar)
        self.window()

    def window(self):
        add_button = tk.Button(self, text="Add", command=self.db.addQuery)
        add_button.pack()

        delete_button = tk.Button(self, text="Delete", command=self.db.deleteQuery)
        delete_button.pack()


if __name__ == "__main__":
    root = Hammer()
    root.mainloop()
