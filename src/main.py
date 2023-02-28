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

    """
        populate_table takes the return value of self.db.get_all_query()
        and builds a "table" of tk.Entry with the database
    """

    def populate_table(self):
        current_table = self.db.get_all_query()
        print(current_table)

        for y in range(len(current_table)):
            for x in range(len(current_table[y])):
                # if x > 0:
                entry = tk.Entry(self, width=16, font=('Arial', 14,))
                entry.grid(row=y, column=x)
                entry.insert(tk.END, current_table[y][x])

    def window(self):
        add_button = tk.Button(self, text="Add", command=lambda: self.db.add_query())
        add_button.grid()

        delete_button = tk.Button(self, text="Delete", command=lambda: self.db.delete_query())
        delete_button.grid()

        get_all_button = tk.Button(self, text="Get All", command=lambda: self.populate_table())
        get_all_button.grid()


if __name__ == "__main__":
    root = Hammer()
    root.mainloop()
