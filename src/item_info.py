import tkinter as tk


class ItemInfo(tk.Toplevel):

    def __init__(self, parent, process):
        super().__init__()

        self.parent = parent

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title(f'{process.capitalize()} Item')

        barcode_frame = tk.Frame(self)
        barcode_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding * 2,
                                                                                         self.parent.padding))
        ttk.Label(barcode_frame, text='Barcode').pack(side='left')
        self.barcode_text = tk.Entry(barcode_frame)
        self.barcode_text.pack(side='right')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(title_frame, text='Title').pack(side='left')
        self.title_text = tk.Entry(title_frame)
        self.title_text.pack(side='right')

        author_frame = tk.Frame(self)
        author_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(author_frame, text='Author').pack(side='left')
        self.author_text = tk.Entry(author_frame)
        self.author_text.pack(side='right')

        description_frame = tk.Frame(self)
        description_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(description_frame, text='Item Description').pack(side='left', anchor='nw')
        description_text_frame = tk.Frame(description_frame)
        description_text_frame.pack()
        self.description_text = tk.Text(description_text_frame, width=26, height=5)
        self.description_text.pack(side='right')

        publish_frame = tk.Frame(self)
        publish_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(publish_frame, text='Publish Date').pack(side='left')
        self.publish_date_text = tk.Entry(publish_frame)
        self.publish_date_text.pack(side='right')

        type_frame = tk.Frame(self)
        type_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(type_frame, text='Item Type').pack(side='left')
        self.type_text = tk.Entry(type_frame)
        self.type_text.pack(side='right')

        location_frame = tk.Frame(self)
        location_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(location_frame, text='Location').pack(side='left')
        self.location_text = tk.Entry(location_frame)
        self.location_text.pack(side='right')

        quantity_frame = tk.Frame(self)
        quantity_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        ttk.Label(quantity_frame, text='Item Quantity').pack(side='left')
        self.quantity_text = tk.Entry(quantity_frame)
        self.quantity_text.pack(side='right')

    def get_item_info(self):
        return [self.barcode_text.get(),
                self.title_text.get(),
                self.author_text.get(),
                self.description_text.get('1.0', tk.END),
                self.publish_date_text.get(),
                self.type_text.get(),
                self.location_text.get(),
                self.quantity_text.get()]
