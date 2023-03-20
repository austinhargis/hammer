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
        self.tree = ttk.Treeview(self,
                                 columns=('id', 'title', 'author', 'publish_date', 'type', 'location', 'quantity'))
        self.tree['show'] = 'headings'
        self.tree['displaycolumns'] = ('title', 'author', 'publish_date', 'type', 'location', 'quantity')

        self.config(menu=self.menu_bar)
        self.window()
        self.populate_table()

        self.tree.bind("<BackSpace>", self.delete_entry)

    def add_entry(self, data, window):
        self.db.insert_query(data)
        self.refresh_table()
        window.destroy()

    def add_item(self):
        self.db.test_add_query()
        self.refresh_table()

    def delete_entry(self, event):
        current_item = self.tree.focus()
        if current_item != '':
            self.db.delete_query(self.tree.item(current_item)['values'])
            self.refresh_table()

    """
        drop_table will delete all delete all data within the table
    """

    def drop_table(self):
        self.db.drop_table()
        self.refresh_table()

    """
        populate_table takes the return value of self.db.get_all_query()
        and builds a "table" of tk.Entry with the database
    """

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

        tk.Button(text='Add', command=lambda: self.create_item()).pack()
        tk.Button(text='Delete', command=lambda: self.delete_entry(None)).pack()

    def create_item(self):
        top = tk.Toplevel()
        top.attributes('-topmost', True)
        top.title('Add Item To Database')

        tk.Label(top, text='Title: ').grid(row=0, column=0)
        title_text = tk.Entry(top)
        title_text.grid(row=0, column=1)

        tk.Label(top, text='Author: ').grid(row=1, column=0)
        author_text = tk.Entry(top)
        author_text.grid(row=1, column=1)

        tk.Label(top, text='Publish Date: ').grid(row=2, column=0)
        publish_date_text = tk.Entry(top)
        publish_date_text.grid(row=2, column=1)

        tk.Label(top, text='Item Type: ').grid(row=3, column=0)
        type_text = tk.Entry(top)
        type_text.grid(row=3, column=1)

        tk.Label(top, text='Location: ').grid(row=4, column=0)
        location_text = tk.Entry(top)
        location_text.grid(row=4, column=1)

        tk.Label(top, text='Item Quantity: ').grid(row=5, column=0)
        quantity_text = tk.Entry(top)
        quantity_text.grid(row=5, column=1)

        tk.Button(top, text='Add Item', command=lambda: self.add_entry([title_text.get(),
                                                                        author_text.get(),
                                                                        publish_date_text.get(),
                                                                        type_text.get(),
                                                                        location_text.get(),
                                                                        quantity_text.get()], top))\
            .grid(row=6, column=0)

        tk.Button(top, text='Cancel', command=lambda: top.destroy()).grid(row=6, column=1)

        top.mainloop()


if __name__ == "__main__":
    root = Hammer()
    root.mainloop()
