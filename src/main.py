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
        self.menu_bar = MenuBar(self)
        self.tree = ttk.Treeview(self, columns=('id', 'title', 'author', 'publish_date', 'type', 'location', 'quantity'))

        self.config(menu=self.menu_bar)
        self.window()
        self.populate_table()

    """
        populate_table takes the return value of self.db.get_all_query()
        and builds a "table" of tk.Entry with the database
    """

    def add_item(self):
        self.db.add_query()
        self.refresh_table()

    def drop_table(self):
        self.db.delete_query()
        self.refresh_table()

    def populate_table(self):
        current_table = self.db.get_all_query()

        for y in range(len(current_table)):
            self.tree.insert('', tk.END, values=current_table[y])

    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.populate_table()

    def window(self):
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('author', text='Author')
        self.tree.heading('publish_date', text='Publish Date')
        self.tree.heading('type', text='Type')
        self.tree.heading('location', text='Location')
        self.tree.heading('quantity', text='Quantity')
        self.tree.pack(fill='both', expand=True)

        self.menu_bar.database_menu.add_command(label='Add 1 Item', underline=1, command=lambda: self.add_item())
        self.menu_bar.database_menu.add_command(label='Drop Table', underline=1, command=lambda: self.drop_table())
        self.menu_bar.database_menu.add_command(label='Refresh', underline=1, command=lambda: self.refresh_table())


if __name__ == "__main__":
    root = Hammer()
    root.mainloop()
