"""

    hammer: an inventory management system developed in 
    python with sqlite3

    version: v0.1.0a

"""
import logging
import os
from pathlib import Path

import tkinter as tk
from tkinter import ttk

from add_item_from_record_window import AddItemFromRecordWindow
from add_record_window import AddRecordWindow
from expanded_info import ExpandedInformation
from languages import *
from manage_record_window import ManageRecordWindow
from database import Database
from menu_bar import MenuBar
from save_manager import SaveManager

if not os.path.isdir(f'{Path.home()}/hammer'):
    os.mkdir(f'{Path.home()}/hammer')

logging.basicConfig(filename=f'{Path.home()}/hammer/hammer.log', format='%(asctime)s %(message)s', encoding='utf-8', level=logging.INFO,
                    filemode='w')


class Hammer(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title(f"hammer")
        self.minsize(400, 300)
        # self.state('zoomed')

        self.data_path = f'{Path.home()}/hammer'
        self.heading_font = ('Arial', 20, 'bold')
        self.manage_check_delay = 250
        self.padding = 10
        self.wraplength = 200

        # self.style = ttk.Style(self)
        # self.style.theme_use('clam')
        # self.style.configure('Treeview', background='#26242f', fieldbackground='#26242f', fontcolor='white')

        self.save_m = SaveManager(self)
        self.db = Database("hammer.db", self)
        self.menu_bar = MenuBar(self)
        self.tab_controller = ttk.Notebook(self)

        self.window()
        self.config(menu=self.menu_bar)
        self.populate_table()

        self.tree.bind("<Delete>", lambda event: self.delete_popup_window())
        self.bind("<Escape>", lambda event: self.destroy())

    def update_entry(self, data, entry_id):
        self.db.update_query(data, entry_id)
        self.refresh_table()

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

        logging.info('Reset tables')

    def populate_table(self, current_table=None):
        """
            populate_table takes the return value of self.db.get_all_query()
            and builds a "table" of tk.Entry with the database
            :param current_table: determines the necessary table (for searches)
            :return:
        """
        if current_table is None:
            current_table = self.db.get_all_query()

        for row in current_table:
            self.tree.insert('', tk.END, values=row)

        if len(self.tree.get_children()) > 0:
            child = self.tree.get_children()[0]
            self.tree.focus(child)
            self.tree.selection_set(child)

        logging.info('Populated the table')

    def get_item_status(self, barcode):
        check_status = self.db.dbCursor.execute(f"""
            SELECT *
            FROM checkouts
            WHERE item_barcode=?
        """, (barcode,)).fetchall()

        if len(check_status) == 0:
            return languages[self.save_m.data['language']]['iteminfo']['item_available']
        else:
            return languages[self.save_m.data['language']]['iteminfo']['item_unavailable']

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
                                                     FROM item_record 
                                                     OR title LIKE \'%{search_term}%\' 
                                                     OR author LIKE \'%{search_term}%\'
                                                     OR publish_date LIKE \'%{search_term}%\'
                                                     OR type LIKE \'%{search_term}%\'""").fetchall()
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
        ttk.Button(manage_frame, text='Add Record',
                   command=lambda: self.create_tab(AddRecordWindow, 'Add Record')).pack()
        self.manage_button = ttk.Button(manage_frame,
                                        text='Manage Record',
                                        command=lambda: self.create_tab(ManageRecordWindow, 'Manage Record'))
        self.manage_button.pack()
        self.manage_button.configure(state='disabled')

        ttk.Button(manage_frame, text='Create Item From Record',
                   command=lambda: self.create_tab(AddItemFromRecordWindow, 'Create Item From Record')).pack()

        # creates the TreeView which will handle displaying all schema in the database
        tree_frame = tk.Frame(screen_frame)
        tree_frame.pack(side='right', anchor='ne')
        self.tree = ttk.Treeview(tree_frame,
                                 columns=(
                                     'id', 'title', 'author', 'publish_date', 'type'))
        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('title', 'author', 'publish_date', 'type',)

        self.treeScroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='both')

        self.tree.heading('id', text='ID')
        self.tree.heading('title', text='Title')
        self.tree.column('title', stretch=False, width=150)
        self.tree.heading('author', text='Author')
        self.tree.column('author', stretch=False, width=150)
        self.tree.heading('publish_date', text='Publish Date')
        self.tree.heading('type', text='Type')
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

        print(entry_values)

        self.create_tab(ExpandedInformation, title=f'{entry_title}', values=entry_values)

    def create_tab(self, window, title, values=None):
        """
            Creates a new Notebook tab with the passed class and title,
            and automatically selects it.
            :param values:
            :param window:
            :param title:
            :return:
        """
        if values is not None:
            self.tab_controller.add(window(self, values), text=title)
        else:
            self.tab_controller.add(window(self), text=title)
        tabs = self.tab_controller.tabs()
        self.tab_controller.select(len(tabs) - 1)

    def delete_tab(self, event):
        pass


if __name__ == "__main__":
    root = Hammer()
    root.after(root.manage_check_delay, root.check_focus)
    root.mainloop()
