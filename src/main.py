"""

    hammer: an inventory management system developed in 
    python with sqlite3

    version: v0.1.0a

"""
import logging
import os

import tkinter as tk
from tkinter import ttk

from add_window import AddItem
from manage_window import ManageItem
from database import Database
from menu_bar import MenuBar
from save_manager import SaveManager

if not os.path.isdir('./data'):
    os.mkdir('./data')

logging.basicConfig(filename='./data/hammer.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO,
                    filemode='w')


class Hammer(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f"hammer")
        self.minsize(400, 300)

        self.manage_check_delay = 250

        # self.style = ttk.Style(self)
        # self.style.theme_use('clam')
        # self.style.configure('Treeview', background='#26242f', fieldbackground='#26242f', fontcolor='white')

        self.save_m = SaveManager()
        self.db = Database("hammer.db")
        self.menu_bar = MenuBar(self)

        # creates the TreeView which will handle displaying all schema in the database
        self.tree = ttk.Treeview(self,
                                 columns=(
                                     'id', 'barcode', 'title', 'author', 'publish_date', 'type', 'location',
                                     'quantity'))
        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('barcode', 'title', 'author', 'publish_date', 'type', 'location', 'quantity')

        self.treeScroll = tk.Scrollbar(self)
        self.treeScroll.configure(command=self.tree.yview_scroll)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='both')

        self.padding = 10

        self.config(menu=self.menu_bar)
        self.window()
        self.populate_table()

        self.tree.bind("<Delete>", lambda event: self.delete_popup_window())
        self.bind("<Escape>", lambda event: self.destroy())

    def add_entry(self, data, window):
        """
            add_entry takes the input from the TopLevel window for
            inserting data into the database and passes it to the
            database handler, before refreshing the table and destroying
            the TopLevel window

            :param data: a list of user inputted data
            :param window: a TopLevel item
            :return:
        """
        self.db.insert_query(data)
        self.refresh_table()
        window.template.destroy()

        logging.info('Added item into database')

    def update_entry(self, data, window, entry_id):
        self.db.update_query(data, entry_id)
        self.refresh_table()
        window.template.destroy()

    def test_add_item(self):
        self.db.test_add_query()
        self.refresh_table()

    def check_focus(self):
        if self.tree.focus() == '':
            self.manage_button.configure(state='disabled')
            self.after(self.manage_check_delay, self.check_focus)
        else:
            self.manage_button.configure(state='normal')
            self.after(self.manage_check_delay, self.check_focus)

    def clear_table(self):
        """
            clear_table purges the TreeView of all of its children
            :return:
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def delete_entry(self):
        """
            delete_entry takes the currently selected/focused item in
            the TreeView and performs a SQL query to remove it from the
            database, before finally refreshing the table
            :return:
        """
        current_item = self.tree.focus()
        if current_item != '':
            self.db.delete_query(self.tree.item(current_item)['values'])
            self.refresh_table()

            logging.info('Deleted item from database')

    def delete_popup_window(self):
        """
            delete_popup_window creates a popup window that allows the user to ensure that they
            intended on deleting the focused item
            :return:
        """
        delete_popup = tk.Toplevel()
        delete_popup.title('Confirm Delete?')
        tk.Label(delete_popup, text='Are you sure you would like to delete this?').pack(padx=self.padding * 2,
                                                                                        pady=(self.padding * 2,
                                                                                              self.padding))
        tk.Label(delete_popup, text=f'Item: {self.tree.item(self.tree.focus())["values"][2]}').pack(
            padx=self.padding * 2,
            pady=self.padding)
        button_frame = tk.Frame(delete_popup)
        button_frame.pack(expand=True, padx=self.padding * 2, pady=(self.padding, self.padding * 2))
        tk.Button(button_frame, text='Confirm', command=lambda: [self.delete_entry(), delete_popup.destroy()]).pack(
            side='left',
            padx=self.padding)
        tk.Button(button_frame, text='Cancel', command=lambda: delete_popup.destroy()).pack(side='right',
                                                                                            padx=self.padding)

        delete_popup.mainloop()

    def drop_table(self):
        """
            drop_table will delete all data within the table
            :return:
        """
        self.db.drop_table()
        self.refresh_table()

        logging.info('Dropped table')

    def populate_table(self, current_table=None):
        """
            populate_table takes the return value of self.db.get_all_query()
            and builds a "table" of tk.Entry with the database
            :param current_table: determines the necessary table (for searches)
            :return:
        """
        if current_table is None:
            current_table = self.db.get_all_query()

        for y in range(len(current_table)):
            self.tree.insert('', tk.END, values=current_table[y], tags=('item',))

        if len(self.tree.get_children()) > 0:
            child = self.tree.get_children()[0]
            self.tree.focus(child)
            self.tree.selection_set(child)

        logging.info('Populated the table')

    def refresh_table(self):
        """
            refresh_table iterates through all elements in the TreeView
            and then for each element, deletes it from the TreeView before
            repopulating the table
            :return:
        """

        self.clear_table()
        self.populate_table()

        logging.info('Refreshed the table')

    def search_table(self, entry_box):
        """
            the search table function gets the currently entered text from the passed
            entry_box and executes a SQL query with it
            :param entry_box:
            :return:
        """
        search_term = entry_box.get()

        current_table = self.db.dbCursor.execute(f"""SELECT * 
                                                     FROM inventory 
                                                     WHERE barcode LIKE \'%{search_term}%\'
                                                     OR title LIKE \'%{search_term}%\' 
                                                     OR author LIKE \'%{search_term}%\'
                                                     OR publish_date LIKE \'%{search_term}%\'
                                                     OR type LIKE \'%{search_term}%\'
                                                     OR location LIKE \'%{search_term}%\'
                                                     OR quantity LIKE \'%{search_term}%\'""").fetchall()
        self.clear_table()
        self.populate_table(current_table)

    def window(self):
        self.tree.heading('id', text='ID')
        self.tree.heading('barcode', text='Barcode')
        self.tree.heading('title', text='Title')
        self.tree.heading('author', text='Author')
        self.tree.heading('publish_date', text='Publish Date')
        self.tree.heading('type', text='Type')
        self.tree.heading('location', text='Location')
        self.tree.heading('quantity', text='Quantity')
        self.tree.pack(fill='both', expand=True, padx=self.padding * 2, pady=(self.padding * 2, 0))

        manage_frame = tk.Frame(self)
        manage_frame.pack(fill='both', expand=True, padx=(0, self.padding))
        tk.Button(manage_frame, text='Add', command=lambda: AddItem(self)).pack(side='left', padx=(self.padding * 2,
                                                                                                   self.padding),
                                                                                pady=self.padding * 2)
        self.manage_button = tk.Button(manage_frame, text='Manage', command=lambda: ManageItem(self))
        self.manage_button.pack(side='left', padx=self.padding, pady=self.padding * 2)
        self.manage_button.configure(state='disabled')
        tk.Button(manage_frame, text='Delete', command=lambda: self.delete_popup_window()).pack(side='left',
                                                                                                padx=self.padding,
                                                                                                pady=self.padding * 2)

        search_frame = tk.Frame(self)
        search_frame.pack(fill='both', expand=True, padx=self.padding, pady=(0, self.padding * 2))
        search_box = tk.Entry(search_frame)
        search_box.pack(side='left', padx=self.padding)
        tk.Button(search_frame, text='Search', command=lambda: self.search_table(search_box)).pack(side='left')

        self.bind('<Return>', lambda event: self.search_table(search_box))


if __name__ == "__main__":
    root = Hammer()
    root.after(root.manage_check_delay, root.check_focus)
    root.mainloop()
