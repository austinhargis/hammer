import sv_ttk
import tkinter as tk
from tkinter import ttk


class AddItem(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()
        self.attributes('-topmost', True)
        self.title('Add Item')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=(parent.padding*2, parent.padding))
        tk.Label(title_frame, text='Title').pack(side='left')
        title_text = tk.Entry(title_frame)
        title_text.pack(side='right')

        author_frame = tk.Frame(self)
        author_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=parent.padding)
        tk.Label(author_frame, text='Author').pack(side='left')
        author_text = tk.Entry(author_frame)
        author_text.pack(side='right')

        publish_frame = tk.Frame(self)
        publish_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=parent.padding)
        tk.Label(publish_frame, text='Publish Date').pack(side='left')
        publish_date_text = tk.Entry(publish_frame)
        publish_date_text.pack(side='right')

        type_frame = tk.Frame(self)
        type_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=parent.padding)
        tk.Label(type_frame, text='Item Type').pack(side='left')
        type_text = tk.Entry(type_frame)
        type_text.pack(side='right')

        location_frame = tk.Frame(self)
        location_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=parent.padding)
        tk.Label(location_frame, text='Location').pack(side='left')
        location_text = tk.Entry(location_frame)
        location_text.pack(side='right')

        quantity_frame = tk.Frame(self)
        quantity_frame.pack(fill='both', expand=True, padx=parent.padding*2, pady=parent.padding)
        tk.Label(quantity_frame, text='Item Quantity').pack(side='left')
        quantity_text = tk.Entry(quantity_frame)
        quantity_text.pack(side='right')

        button_frame = tk.Frame(self)
        button_frame.pack(expand=True, padx=parent.padding*2, pady=(parent.padding, parent.padding*2))
        tk.Button(button_frame, text='Add Item', command=lambda: parent.add_entry([title_text.get(),
                                                                                   author_text.get(),
                                                                                   publish_date_text.get(),
                                                                                   type_text.get(),
                                                                                   location_text.get(),
                                                                                   quantity_text.get()], self)) \
            .pack(side='left')

        self.bind('<Return>', lambda event: parent.add_entry([title_text.get(),
                                                              author_text.get(),
                                                              publish_date_text.get(),
                                                              type_text.get(),
                                                              location_text.get(),
                                                              quantity_text.get()], self))

        tk.Button(button_frame, text='Cancel', command=lambda: self.destroy()).pack(side='right')

        self.mainloop()
