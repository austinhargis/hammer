import tkinter as tk
from tkinter import ttk


class RecordChildTemplate(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        selected = self.parent.tree.item(self.parent.tree.focus())
        self.id = selected['values'][0]

        self.get_item_record()

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        self.heading_label = ttk.Label(heading_frame, font=self.parent.heading_font)
        self.heading_label.pack(side='left')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame, text='Item Barcode').pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        location_frame = ttk.Frame(main_frame)
        location_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(location_frame, text='Item Location').pack(side='left')
        self.location_entry = ttk.Entry(location_frame)
        self.location_entry.pack(side='right')

        description_frame = ttk.Frame(main_frame)
        description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(description_frame, text='Descriptor').pack(side='left')
        self.description_entry = ttk.Entry(description_frame)
        self.description_entry.pack(side='right')

        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.func_button = ttk.Button(self.button_frame)
        self.func_button.pack(side='left')
        ttk.Button(self.button_frame,
                   text='Cancel',
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='left')

    def get_item_info(self):
        return [
            self.id,
            self.barcode_entry.get(),
            self.location_entry.get(),
            self.description_entry.get()
        ]

    def get_item_record(self):
        self.record = self.parent.db.dbCursor.execute(f"""
            SELECT *
            FROM item_record
            WHERE id=?
        """, (self.id,)).fetchall()
