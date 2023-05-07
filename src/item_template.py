from tkinter import ttk


class ItemTemplate(ttk.Frame):

    def __init__(self, parent, entry_id):
        super().__init__()

        self.entry_id = entry_id
        self.parent = parent

        self.get_item_record()

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        self.heading_label = ttk.Label(heading_frame, font=self.parent.heading_font)
        self.heading_label.pack(side='left')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(barcode_frame, text=self.parent.get_region_text('checkout_item_barcode')).pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        location_frame = ttk.Frame(main_frame)
        location_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(location_frame, text=self.parent.get_region_text('location_barcode')).pack(side='left')
        self.location_entry = ttk.Entry(location_frame)
        self.location_entry.pack(side='right')

        description_frame = ttk.Frame(main_frame)
        description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(description_frame, text=self.parent.get_region_text('item_description')).pack(side='left')
        self.description_entry = ttk.Entry(description_frame)
        self.description_entry.pack(side='right')

        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.func_button = ttk.Button(self.button_frame)
        self.func_button.pack(side='left')
        ttk.Button(self.button_frame,
                   text=self.parent.get_region_text('prompt_deny'),
                   command=lambda: [self.destroy()]).pack(side='left')

        self.barcode_entry.focus()
        self.barcode_entry.bind('<Return>', lambda event: self.location_entry.focus())
        self.location_entry.bind('<Return>', lambda event: self.description_entry.focus())

    def get_item_info(self):
        return [
            self.entry_id,
            self.barcode_entry.get(),
            self.location_entry.get(),
            self.description_entry.get()
        ]

    def get_item_record(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT *
            FROM item_record
            WHERE id=%s
        """, (self.entry_id,))
        self.record = self.parent.db.dbCursor.fetchall()
