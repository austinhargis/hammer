import sys
import tkinter as tk
from webbrowser import open_new_tab

from checkin_screen import CheckinScreen
from checkout_screen import CheckoutScreen
from create_user import CreateUser
from settings import SettingsWindow
from update_checker import UpdateChecker
from view_checkouts import ViewCheckouts
from view_users import ViewUsers


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
        self.checkout()
        self.users()
        self.developer()
        self.help()

    def checkout(self):
        self.checkout_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Checkout', underline=0, menu=self.checkout_menu)
        self.checkout_menu.add_command(label='Checkout to User', underline=1,
                                       command=lambda: self.parent.tab_controller.add(CheckoutScreen(self.parent),
                                                                                      text='Checkout Item'))
        self.checkout_menu.add_command(label='Check Item In', underline=1,
                                       command=lambda: self.parent.tab_controller.add(CheckinScreen(self.parent),
                                                                                      text='Check Item In'))
        self.checkout_menu.add_command(label='View Checkouts', underline=1,
                                       command=lambda: self.parent.tab_controller.add(ViewCheckouts(self.parent),
                                                                                      text='View Checkouts'))

    def file(self):
        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=self.file_menu)
        self.file_menu.add_command(label='Check for Updates', underline=1,
                                   command=lambda: self.parent.tab_controller.add(UpdateChecker(self.parent),
                                                                                  text='Check for Updates'))
        self.file_menu.add_command(label='Settings', underline=1,
                                   command=lambda: self.parent.tab_controller.add(SettingsWindow(self.parent),
                                                                                  text='Settings'))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator='Escape')

    def developer(self):
        if self.parent.save_m.data['show_developer_menu'] == 'enabled':
            self.developer_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label='Developer', underline=0, menu=self.developer_menu)
            self.developer_menu.add_command(label='Add Test Item', underline=1,
                                            command=lambda: self.parent.test_add_item())
            self.developer_menu.add_command(label='Drop Table', underline=1, command=lambda: self.parent.drop_table())

    def help(self):
        self.help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=self.help_menu)
        self.help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
            'https://github.com/austinhargis/hammer'))

    def users(self):
        self.users_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Users', underline=0, menu=self.users_menu)
        self.users_menu.add_command(label='Add User', underline=1,
                                    command=lambda: self.parent.tab_controller.add(CreateUser(self.parent),
                                                                                   text='Create User'))
        self.users_menu.add_command(label='View Users', underline=1,
                                    command=lambda: self.parent.tab_controller.add(ViewUsers(self.parent),
                                                                                   text='View Users'))

    def quit(self):
        sys.exit()
