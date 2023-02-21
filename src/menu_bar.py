import sys
import tkinter as tk
from webbrowser import open_new_tab


class MenuBar(tk.Menu):

	def __init__(self, parent):
		tk.Menu.__init__(self, parent)

		file_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="File", underline=0, menu=file_menu)
		file_menu.add_command(label="Exit", underline=1, command=self.quit)

		database_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="Database", underline=0, menu=database_menu)
		database_menu.add_command(label="Save DB", underline=1)
		database_menu.add_command(label="Open DB", underline=1)

		help_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="Help", underline=0, menu=help_menu)
		help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
			'https://github.com/austinhargis/hammer'))

	def quit(self):
		sys.exit()
