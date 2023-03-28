import sys
import tkinter as tk
from webbrowser import open_new_tab

from add_window import AddItem
from checkout_screen import CheckoutScreen
from create_user import CreateUser
from settings import SettingsWindow
from update_checker import UpdateChecker


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

        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=self.file_menu)
        self.file_menu.add_command(label='Check for Updates', underline=1, command=lambda: UpdateChecker(self.parent))
        self.file_menu.add_command(label='Settings', underline=1, command=lambda: SettingsWindow(self.parent))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator='Escape')

        self.checkout_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Checkout', underline=0, menu=self.checkout_menu)
        self.checkout_menu.add_command(label='Checkout to User', underline=1,
                                       command=lambda: CheckoutScreen(self.parent))
        self.checkout_menu.add_command(label='Check Item In', underline=1)

        self.users_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Users', underline=0, menu=self.users_menu)
        self.users_menu.add_command(label='Add User', underline=1, command=lambda: CreateUser(self.parent))

        self.database_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Database", underline=0, menu=self.database_menu)
        self.database_menu.add_command(label='Add Item', underline=1, command=lambda: AddItem(self.parent))
        self.database_menu.add_command(label='Delete Selected', underline=1,
                                       command=lambda: self.parent.delete_entry(None),
                                       accelerator='BackSpace')
        self.database_menu.add_command(label='Refresh Table', underline=1, command=lambda: self.refresh(),
                                       accelerator='F5')

        self.bind('F5', self.parent.refresh_table)

        self.help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=self.help_menu)
        self.help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
            'https://github.com/austinhargis/hammer'))

        if self.parent.save_m.data['show_developer_menu'] == 'enabled':
            self.developer_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label='Developer', underline=0, menu=self.developer_menu)
            self.developer_menu.add_command(label='Add Test Item', underline=1,
                                            command=lambda: self.parent.test_add_item())
            self.developer_menu.add_command(label='Drop Table', underline=1, command=lambda: self.parent.drop_table())


    def refresh(self):
        self.counter += 1

        if self.counter == 90:
            open_new_tab('https://youtu.be/otCpCn0l4Wo')
            self.counter = 0

        self.parent.refresh_table()

    def quit(self):
        sys.exit()
