import sys
import tkinter as tk
from webbrowser import open_new_tab

from user_view_specific import ViewSpecificUser
from user_create import CreateUser
from settings import SettingsWindow
from update_checker import UpdateChecker
from view_checkouts import ViewCheckouts
from view_users import ViewUsers

from login import Login


class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        self.checkout_menu = None
        self.users_menu = None
        self.parent = parent

        self.help_menu = None
        self.database_menu = None
        self.file_menu = None
        self.developer_menu = None

        self.counter = 0

        self.generate()

    def generate(self):
        self.delete(0, 'end')

        self.file()
        self.users()
        self.developer()
        self.help()

    def file(self):
        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label=self.parent.get_region_text('file_menu'), underline=0,
                         menu=self.file_menu)
        self.file_menu.add_command(label=self.parent.get_region_text('update_check_for'),
                                   underline=1,
                                   command=lambda: self.parent.create_tab(UpdateChecker, self.parent.get_region_text('update_check_for')))
        self.file_menu.add_command(label=self.parent.get_region_text('settings'),
                                   underline=1,
                                   command=lambda: self.parent.create_tab(SettingsWindow,
                                                                          self.parent.get_region_text('settings')))
        self.file_menu.add_command(label=self.parent.get_region_text('logout'),
                                   underline=1,
                                   command=lambda: self.parent.logout())
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator='Escape')

    def developer(self):
        if self.parent.save_m.data['show_developer_menu'] == 'allowed':
            self.developer_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=self.parent.get_region_text('developer_menu'),
                             underline=0, menu=self.developer_menu)
            self.developer_menu.add_command(label='View All Checkouts', underline=1,
                                            command=lambda: self.parent.create_tab(ViewCheckouts, 'View All Checkouts'))

    def help(self):
        if self.parent.save_m.data['show_help_menu'] == 'allowed':
            self.help_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=self.parent.get_region_text('help_menu'), underline=0,
                             menu=self.help_menu)
            self.help_menu.add_command(label=self.parent.get_region_text('github'), underline=1, command=lambda: open_new_tab(
                'https://github.com/austinhargis/hammer'))

    def users(self):
        if self.parent.save_m.data['show_users_menu'] == 'allowed':
            self.users_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=self.parent.get_region_text('users_menu'), underline=0,
                             menu=self.users_menu)
            self.users_menu.add_command(label=self.parent.get_region_text('user_add'),
                                        underline=1,
                                        command=lambda: self.parent.create_tab(CreateUser,
                                                                               self.parent.get_region_text('user_add')))
            self.users_menu.add_command(label=self.parent.get_region_text('user_specific'),
                                        underline=1,
                                        command=lambda: self.parent.create_tab(ViewSpecificUser,
                                                                               self.parent.get_region_text('user_specific')))
            self.users_menu.add_command(label=self.parent.get_region_text('user_view'),
                                        underline=1,
                                        command=lambda: self.parent.create_tab(ViewUsers,
                                                                               self.parent.get_region_text('user_view')))

    def quit(self):
        sys.exit()
