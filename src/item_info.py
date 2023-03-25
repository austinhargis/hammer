import tkinter as tk


class ItemInfo(tk.Toplevel):

    def __init__(self, parent, process):
        super().__init__()

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title(f'{process.capitalize()} Item')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=(parent.padding * 2, parent.padding))
        tk.Label(title_frame, text='Title').pack(side='left')
        self.title_text = tk.Entry(title_frame)
        self.title_text.pack(side='right')

        author_frame = tk.Frame(self)
        author_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=parent.padding)
        tk.Label(author_frame, text='Author').pack(side='left')
        self.author_text = tk.Entry(author_frame)
        self.author_text.pack(side='right')

        publish_frame = tk.Frame(self)
        publish_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=parent.padding)
        tk.Label(publish_frame, text='Publish Date').pack(side='left')
        self.publish_date_text = tk.Entry(publish_frame)
        self.publish_date_text.pack(side='right')

        type_frame = tk.Frame(self)
        type_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=parent.padding)
        tk.Label(type_frame, text='Item Type').pack(side='left')
        self.type_text = tk.Entry(type_frame)
        self.type_text.pack(side='right')

        location_frame = tk.Frame(self)
        location_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=parent.padding)
        tk.Label(location_frame, text='Location').pack(side='left')
        self.location_text = tk.Entry(location_frame)
        self.location_text.pack(side='right')

        quantity_frame = tk.Frame(self)
        quantity_frame.pack(fill='both', expand=True, padx=parent.padding * 2, pady=parent.padding)
        tk.Label(quantity_frame, text='Item Quantity').pack(side='left')
        self.quantity_text = tk.Entry(quantity_frame)
        self.quantity_text.pack(side='right')
