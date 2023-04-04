import tkinter as tk
from tkinter import ttk

from item_info import ItemInfo

from languages import *

class AddItem(ItemInfo):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        # self.template.bind('<Return>', lambda event: parent.add_entry(self.template.get_item_info(), self))

        ttk.Button(self.button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_add_item'],
                   command=lambda: [self.parent.add_entry(self.get_item_info()),
                                    self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='left')
