import tkinter as tk
from tkinter import ttk


class PopupWindow(tk.Toplevel):

    def __init__(self, parent, title, message):
        super().__init__()

        self.attributes('-topmost', True)
        self.title(title)

        self.parent = parent

        main_frame = tk.Frame(self)
        main_frame.pack(padx=self.parent.padding, pady=self.parent.padding)

        ttk.Label(main_frame,
                  text=message,
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        ttk.Button(main_frame, text='Close', command=lambda: self.destroy()).pack()

        self.mainloop()
