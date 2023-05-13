import tkinter as tk
from tkinter import ttk


class PopupWindow(tk.Toplevel):

    def __init__(self, parent, title, message):
        super().__init__()

        self.attributes('-topmost', True)
        self.configure(padx=parent.padding, pady=parent.padding)
        self.focus()
        self.title(title)

        self.parent = parent

        ttk.Label(self,
                  text=message,
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        button = ttk.Button(self, text=self.parent.get_region_text('prompt_exit'), command=lambda: self.destroy())
        button.pack()

        self.bind('<Return>', lambda event: self.destroy())

        self.mainloop()
