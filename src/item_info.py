import tkinter as tk
from tkinter import ttk

from languages import *


class ItemInfo(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # self.attributes('-topmost', True)
        # self.resizable(False, False)
        # self.title(f'{process.capitalize()} Item')

        self.barcode_frame = tk.Frame(self)
        self.barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding * 2,
                                                                                              self.parent.padding))
        ttk.Label(self.barcode_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_barcode']).pack(side='left')
        self.barcode_text = tk.Entry(self.barcode_frame)
        self.barcode_text.pack(side='right')

        self.title_frame = tk.Frame(self)
        self.title_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.title_frame, text=languages[self.parent.save_m.data['language']]['iteminfo']['item_title']).pack(
            side='left')
        self.title_text = tk.Entry(self.title_frame)
        self.title_text.pack(side='right')

        self.author_frame = tk.Frame(self)
        self.author_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.author_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_author']).pack(side='left')
        self.author_text = tk.Entry(self.author_frame)
        self.author_text.pack(side='right')

        self.description_frame = tk.Frame(self)
        self.description_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.description_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_description']).pack(side='left',
                                                                                                            anchor='nw')
        self.description_text_frame = tk.Frame(self.description_frame)
        self.description_text_frame.pack()
        self.description_text = tk.Text(self.description_text_frame, width=26, height=5)
        self.description_text.pack(side='right')

        self.publish_frame = tk.Frame(self)
        self.publish_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.publish_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_publish_date']).pack(
            side='left')
        self.publish_date_text = tk.Entry(self.publish_frame)
        self.publish_date_text.pack(side='right')

        self.type_frame = tk.Frame(self)
        self.type_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.type_frame, text=languages[self.parent.save_m.data['language']]['iteminfo']['item_type']).pack(
            side='left')
        self.type_text = tk.Entry(self.type_frame)
        self.type_text.pack(side='right')

        self.location_frame = tk.Frame(self)
        self.location_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.location_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_location']).pack(side='left')
        self.location_text = tk.Entry(self.location_frame)
        self.location_text.pack(side='right')

        self.quantity_frame = tk.Frame(self)
        self.quantity_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(self.quantity_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_quantity']).pack(side='left')
        self.quantity_text = tk.Entry(self.quantity_frame)
        self.quantity_text.pack(side='right')

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(expand=True,
                               padx=self.parent.padding,
                               pady=self.parent.padding)

        ttk.Button(self.button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='right')

    def get_item_info(self):
        return [self.barcode_text.get(),
                self.title_text.get(),
                self.author_text.get(),
                self.description_text.get('1.0', tk.END),
                self.publish_date_text.get(),
                self.type_text.get(),
                self.location_text.get(),
                self.quantity_text.get()]
