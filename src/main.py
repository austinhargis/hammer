"""

    hammer: an inventory management system developed in 
    python with mysql

    version: v0.2.0a

"""
import logging
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import ttk
import _tkinter

from database import Database
from login import Login
from menu_bar import MenuBar
from save_manager import SaveManager

if not os.path.isdir(f'{Path.home()}/hammer'):
    os.mkdir(f'{Path.home()}/hammer')

logging.basicConfig(filename=f'{Path.home()}/hammer/hammer.log', format='%(asctime)s %(message)s', encoding='utf-8',
                    level=logging.INFO,
                    filemode='w')


class Hammer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title(f"hammer")
        self.minsize(800, 600)
        # self.state('zoomed')

        self.data_path = f'{Path.home()}/hammer'
        self.heading_font = ('Arial', 20, 'bold')
        self.manage_check_delay = 250
        self.padding = 10
        self.user_barcode = None
        self.user_permissions = None
        self.wraplength = 200

        self.save_m = SaveManager(self)
        self.menu_bar = MenuBar(self)
        self.tab_controller = ttk.Notebook(self)
        self.db = Database(self)
        self.db.start()

        self.tab_controller.pack(expand=1, fill='both')

        self.create_tab(Login, 'Login')

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
            self.tab_controller.add(window(self, values), text=title[0:10])
        else:
            self.tab_controller.add(window(self), text=title[0:10])
        tabs = self.tab_controller.tabs()
        self.tab_controller.select(len(tabs) - 1)

        logging.info(f'Created ExpandedInfo tab for {title}')

    def get_user_permissions(self):
        self.db.dbCursor.execute("""
            SELECT is_admin, can_check_out, can_modify_users, can_manage_records
            FROM users
            WHERE barcode=%s
        """, (self.user_barcode,))
        user_permissions_row = self.db.dbCursor.fetchone()

        self.user_permissions = {
            'is_admin': user_permissions_row[0],
            'can_check_out': user_permissions_row[1],
            'can_modify_users': user_permissions_row[2],
            'can_manage_records': user_permissions_row[3]
        }


if __name__ == "__main__":
    try:
        root = Hammer()
        root.mainloop()
    except _tkinter.TclError:
        pass
