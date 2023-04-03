import tkinter as tk
from tkinter import ttk

from item_info import ItemInfo


class ManageItem(ItemInfo):

    def __init__(self, parent):
        super().__init__(parent)

        self.parent = parent

        self.entry_id = None

        self.fill_entries()

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True,
                          padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        ttk.Button(button_frame, text='Save Changes',
                   command=lambda: [self.parent.update_entry(self.get_item_info(),
                                                             self.entry_id),
                                    self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='left')
        ttk.Button(button_frame,
                   text='Cancel',
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='right')

    def fill_entries(self):
        current_item = self.parent.tree.focus()
        self.entry_id = self.parent.tree.item(current_item)['values'][0]
        self.barcode_text.insert(0, self.parent.tree.item(current_item)['values'][1])
        self.title_text.insert(0, self.parent.tree.item(current_item)['values'][2])
        self.author_text.insert(0, self.parent.tree.item(current_item)['values'][3])
        self.description_text.insert('1.0', self.parent.tree.item(current_item)['values'][4])
        self.publish_date_text.insert(0, self.parent.tree.item(current_item)['values'][5])
        self.type_text.insert(0, self.parent.tree.item(current_item)['values'][6])
        self.location_text.insert(0, self.parent.tree.item(current_item)['values'][7])
        self.quantity_text.insert(0, self.parent.tree.item(current_item)['values'][8])
