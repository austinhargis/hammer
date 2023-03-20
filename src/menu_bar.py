import sys
import tkinter as tk
from webbrowser import open_new_tab


class MenuBar(tk.Menu):

	def __init__(self, parent):
		tk.Menu.__init__(self, parent)

		self.file_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="File", underline=0, menu=self.file_menu)
		self.file_menu.add_command(label="Exit", underline=1, command=self.quit)

		self.database_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="Database", underline=0, menu=self.database_menu)

		self.help_menu = tk.Menu(self, tearoff=False)
		self.add_cascade(label="Help", underline=0, menu=self.help_menu)
		self.help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
			'https://github.com/austinhargis/hammer'))

	def quit(self):
		sys.exit()
