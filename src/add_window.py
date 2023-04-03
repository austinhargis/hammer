import tkinter as tk
from tkinter import ttk

from item_info import ItemInfo


class AddItem(ItemInfo):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # self.template.bind('<Return>', lambda event: parent.add_entry(self.template.get_item_info(), self))

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        ttk.Button(button_frame,
                   text='Add Item',
                   command=lambda: [self.parent.add_entry(self.get_item_info()), self.destroy()]).pack(side='left')
        ttk.Button(button_frame,
                   text='Cancel',
                   command=lambda: self.destroy()).pack(side='right')
