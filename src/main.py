"""

    hammer: an inventory management system developed in 
    python with mysql

    version: v0.2.0a

"""
import logging
import os
import tkinter as tk
from pathlib import Path
from tkinter import ttk
import _tkinter
import mysql.connector.errors

from configure_env_window import ConfigureEnvWindow
from database import Database
from languages import *
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
        self.db = Database(self)
        self.db.start()

        tk.Tk.__init__(self, *args, **kwargs)
        self.title(f"hammer")
        self.minsize(800, 600)

        self.data_path = f'{Path.home()}/hammer'
        self.heading_font = ('Arial', 20, 'bold')
        self.manage_check_delay = 250
        self.padding = 10
        self.user_barcode = None
        self.user_permissions = None
        self.wraplength = 200

        self.tab_controller = ttk.Notebook(self)
        self.save_m = SaveManager(self)
        self.menu_bar = MenuBar(self)

        self.tab_controller.pack(expand=1, fill='both')

        self.logout()

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

    def get_region_text(self, required_key):
        for key in languages[self.save_m.data['language']]:
            if required_key in languages[self.save_m.data['language']][key]:
                return languages[self.save_m.data['language']][key][required_key]
            else:
                continue
        print(f'Could not find key {required_key}')
        return required_key

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

    def logout(self):

        self.configure(menu=tk.Menu(self))
        for child_tab in self.tab_controller.tabs():
            self.tab_controller.forget(child_tab)

        self.create_tab(Login, self.get_region_text('login_heading'))


if __name__ == "__main__":
    try:
        root = Hammer()
        root.mainloop()
    except _tkinter.TclError:
        pass
    except mysql.connector.errors.ProgrammingError:
        app = tk.Toplevel()
        app.attributes('-topmost')
        ConfigureEnvWindow().pack()
        app.mainloop()
