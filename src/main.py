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
from expanded_info import ExpandedInformation
from manage_window import ManageItem
from database import Database
from menu_bar import MenuBar
from save_manager import SaveManager
from item_info import ItemInfo

if not os.path.isdir('./data'):
    os.mkdir('./data')

logging.basicConfig(filename='./data/hammer.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO,
                    filemode='w')


class Hammer(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f"hammer")
        self.minsize(400, 300)
        # self.state('zoomed')

        self.manage_check_delay = 250

        # self.style = ttk.Style(self)
        # self.style.theme_use('clam')
        # self.style.configure('Treeview', background='#26242f', fieldbackground='#26242f', fontcolor='white')

        self.save_m = SaveManager()
        self.db = Database("hammer.db", self)
        self.menu_bar = MenuBar(self)
        self.tab_controller = ttk.Notebook(self)

        self.padding = 10
        self.wraplength = 200

        self.window()
        self.config(menu=self.menu_bar)
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
            self.delete_button.configure(state='disabled')
            self.after(self.manage_check_delay, self.check_focus)
        else:
            self.manage_button.configure(state='normal')
            self.delete_button.configure(state='normal')
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
        popup = tk.Toplevel(padx=self.padding, pady=self.padding)
        popup.title('Confirm Delete?')

        ttk.Label(popup,
                  text='Are you sure you would like to delete this?',
                  wraplength=self.wraplength,
                  justify='center').pack()
        ttk.Label(popup,
                  text=f'Item: {self.tree.item(self.tree.focus())["values"][2]}').pack()

        button_frame = tk.Frame(popup)
        button_frame.pack(expand=True)

        ttk.Button(button_frame,
                   text='Confirm',
                   command=lambda: [self.delete_entry(), popup.destroy()]).pack(side='left')
        ttk.Button(button_frame,
                   text='Cancel',
                   command=lambda: popup.destroy()).pack(side='right')

        popup.mainloop()

        logging.info('Initialized delete confirmation')

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
            self.tree.insert('', tk.END, values=current_table[y])

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

        screen_frame = tk.Frame(self.tab_controller, padx=self.padding, pady=self.padding)
        screen_frame.pack()

        self.tab_controller.add(screen_frame, text='Home')
        self.tab_controller.pack(expand=1, fill='both')
        self.tab_controller.bind('<Button-2>', lambda event: self.delete_tab())

        manage_frame = tk.Frame(screen_frame, padx=self.padding, pady=self.padding)
        manage_frame.pack(side='left', anchor='nw')
        ttk.Button(manage_frame, text='Add', command=lambda: self.tab_controller.add(AddItem(self), text='Add')).pack()
        self.manage_button = ttk.Button(manage_frame,
                                        text='Manage',
                                        command=lambda: self.tab_controller.add(ManageItem(self), text='Manage'))
        self.manage_button.pack()
        self.manage_button.configure(state='disabled')

        self.delete_button = ttk.Button(manage_frame, text='Delete', command=lambda: self.delete_popup_window())
        self.delete_button.pack()
        self.delete_button.configure(state='disabled')

        # creates the TreeView which will handle displaying all schema in the database
        tree_frame = tk.Frame(screen_frame)
        tree_frame.pack(side='right', anchor='ne')
        self.tree = ttk.Treeview(tree_frame,
                                 columns=(
                                     'id', 'barcode', 'title', 'author', 'publish_date', 'type', 'location',
                                     'quantity'))
        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('barcode', 'title', 'author', 'publish_date', 'location', 'quantity')

        self.treeScroll = ttk.Scrollbar(tree_frame)
        self.treeScroll.configure(command=self.tree.yview_scroll)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='both')

        self.tree.heading('id', text='ID')
        self.tree.heading('barcode', text='Barcode')
        self.tree.column('barcode', stretch=False, width=150)
        self.tree.heading('title', text='Title')
        self.tree.column('title', stretch=False, width=150)
        self.tree.heading('author', text='Author')
        self.tree.column('author', stretch=False, width=150)
        self.tree.heading('publish_date', text='Publish Date')
        self.tree.heading('location', text='Location')
        self.tree.heading('quantity', text='Quantity')
        self.tree.pack(expand=True, fill='y')

        search_frame = tk.Frame(tree_frame)
        search_frame.pack(fill='both', expand=True, pady=self.padding)
        search_box = tk.Entry(search_frame)
        search_box.pack(side='left', padx=self.padding)
        ttk.Button(search_frame, text='Search', command=lambda: self.search_table(search_box)).pack(side='left')

        self.bind('<Return>', lambda event: self.search_table(search_box))
        self.tree.bind('<Double-1>', lambda event: self.tree_double_click())

    def tree_double_click(self):
        current_item = self.tree.focus()

        entry_values = self.tree.item(current_item)['values']
        entry_title = self.tree.item(current_item)['values'][2]

        self.tab_controller.add(ExpandedInformation(self, entry_values), text=f'{entry_title}')

    def delete_tab(self):
        pass


if __name__ == "__main__":
    root = Hammer()
    root.after(root.manage_check_delay, root.check_focus)
    root.mainloop()
