"""

    hammer: an inventory management system developed in 
    python with sqlite3

    version: v0.1.0a

"""
import logging

import sv_ttk
import tkinter as tk
from tkinter import ttk

from add_window import AddItem
from database import Database
from menu_bar import MenuBar

logging.basicConfig(filename='hammer.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO,
                    filemode='w')
version = 'v0.1.0a'


class Hammer(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f"hammer - {version}")
        self.minsize(400, 300)
        self.config(background='#26242f')

        self.db = Database("hammer.db")
        self.menu_bar = MenuBar(self)

        # creates the TreeView which will handle displaying all schema in the database
        self.tree = ttk.Treeview(self,
                                 columns=('id', 'title', 'author', 'publish_date', 'type', 'location', 'quantity'))
        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('title', 'author', 'publish_date', 'type', 'location', 'quantity')

        self.config(menu=self.menu_bar)
        self.window()
        self.populate_table()

        self.tree.bind("<BackSpace>", self.delete_entry)
        self.bind("<Escape>", lambda event: self.destroy())

    """
        add_entry takes the input from the TopLevel window for
        inserting data into the database and passes it to the 
        database handler, before refreshing the table and destroying
        the TopLevel window
    """
    def add_entry(self, data, window):
        self.db.insert_query(data)
        self.refresh_table()
        window.destroy()

        logging.info('Added item into database')

    def add_item(self):
        self.db.test_add_query()
        self.refresh_table()

    """
        delete_entry takes the currently selected/focused item in
        the TreeView and performs a SQL query to remove it from the
        database, before finally refreshing the table
    """
    def delete_entry(self, event):
        current_item = self.tree.focus()
        if current_item != '':
            self.db.delete_query(self.tree.item(current_item)['values'])
            self.refresh_table()

            logging.info('Deleted item from database')

    """
        drop_table will delete all delete all data within the table
    """
    def drop_table(self):
        self.db.drop_table()
        self.refresh_table()

        logging.info('Dropped table')

    """
        populate_table takes the return value of self.db.get_all_query()
        and builds a "table" of tk.Entry with the database
    """
    def populate_table(self):
        current_table = self.db.get_all_query()

        for y in range(len(current_table)):
            self.tree.insert('', tk.END, values=current_table[y])

        logging.info('Populated the table')

    """
        refresh_table iterates through all elements in the TreeView
        and then for each element, deletes it from the TreeView before
        repopulating the table
    """
    def refresh_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.populate_table()

        logging.info('Refreshed the table')

    def window(self):
        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.heading('author', text='Author')
        self.tree.heading('publish_date', text='Publish Date')
        self.tree.heading('type', text='Type')
        self.tree.heading('location', text='Location')
        self.tree.heading('quantity', text='Quantity')
        self.tree.pack(fill='both', expand=True)

        tk.Button(text='Add', command=lambda: AddItem(self)).pack()
        tk.Button(text='Delete', command=lambda: self.delete_entry(None)).pack()


if __name__ == "__main__":
    root = Hammer()
    sv_ttk.use_dark_theme()
    root.mainloop()
