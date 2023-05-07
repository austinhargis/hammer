import tkinter as tk
from tkinter import ttk


class PopupWindow(tk.Toplevel):

    def __init__(self, parent, title, message):
        super().__init__()

        self.attributes('-topmost', True)
        self.focus()
        self.title(title)

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(padx=self.parent.padding, pady=self.parent.padding)

        ttk.Label(main_frame,
                  text=message,
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        ttk.Button(main_frame, text=self.parent.get_region_text('prompt_exit'), command=lambda: self.destroy()).pack()

        self.mainloop()
