import tkinter as tk
from tkinter import ttk

from languages import *


class ExpandedInformation(tk.Frame):

    def __init__(self, parent, entry_values):
        super().__init__()

        self.parent = parent

        self.id = entry_values[0]
        self.barcode = entry_values[1]
        self.title = entry_values[2]
        self.author = entry_values[3]
        self.description = entry_values[8]
        self.publish_date = entry_values[4]
        self.type = entry_values[5]
        self.location = entry_values[6]
        self.quantity = entry_values[7]

        self.window()

    def window(self):

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(barcode_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_barcode']}: {self.barcode}")\
            .pack(side='left')

        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(title_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_title']}: {self.title}")\
            .pack(side='left')

        author_frame = ttk.Frame(main_frame)
        author_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(author_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_author']}: {self.author}")\
            .pack(side='left')

        item_status_frame = ttk.Frame(main_frame)
        item_status_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(item_status_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_status']}: "
                       f"{self.parent.get_item_status(self.barcode)}").pack(side='left')

        description_frame = ttk.Frame(main_frame)
        description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(description_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_description']}: "
                       f"{self.description}").pack(side='left')

        publish_date_frame = ttk.Frame(main_frame)
        publish_date_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(publish_date_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_publish_date']}: "
                       f"{self.publish_date}").pack(side='left')

        location_quantity_frame = ttk.Frame(main_frame)
        location_quantity_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(location_quantity_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_location']}: "
                       f"{self.location} / {languages[self.parent.save_m.data['language']]['iteminfo']['item_quantity']}"
                       f": {self.quantity}").pack(side='left')


        ttk.Label(main_frame, text=f'Type: {self.type}').pack(side='left')

