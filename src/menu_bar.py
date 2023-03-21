import sys
import tkinter as tk
from webbrowser import open_new_tab

from add_window import AddItem


class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="File", underline=0, menu=self.file_menu)
        self.file_menu.add_command(label='Settings')
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator='Escape')

        self.database_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Database", underline=0, menu=self.database_menu)
        self.database_menu.add_command(label='Add Item', underline=1, command=lambda: AddItem(parent))
        self.database_menu.add_command(label='Delete Selected', underline=1, command=lambda: parent.delete_entry(None),
                                       accelerator='Delete')
        self.database_menu.add_command(label='Refresh Table', underline=1, command=lambda: parent.refresh_table(),
                                       accelerator='F5')

        self.bind('F5', parent.refresh_table)

        self.developer_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label='Developer', underline=0, menu=self.developer_menu)
        self.developer_menu.add_command(label='Add Test Item', underline=1, command=lambda: parent.add_item())
        self.developer_menu.add_command(label='Drop Table', underline=1, command=lambda: parent.drop_table())

        self.help_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label="Help", underline=0, menu=self.help_menu)
        self.help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
            'https://github.com/austinhargis/hammer'))

    def quit(self):
        sys.exit()
