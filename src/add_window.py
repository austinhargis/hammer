import sv_ttk
import tkinter as tk
from tkinter import ttk


class AddItem(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()
        self.attributes('-topmost', True)
        self.title('Add Item')

        tk.Label(self, text='Title: ').grid(row=0, column=0)
        title_text = tk.Entry(self)
        title_text.grid(row=0, column=1)

        tk.Label(self, text='Author: ').grid(row=1, column=0)
        author_text = tk.Entry(self)
        author_text.grid(row=1, column=1)

        tk.Label(self, text='Publish Date: ').grid(row=2, column=0)
        publish_date_text = tk.Entry(self)
        publish_date_text.grid(row=2, column=1)

        tk.Label(self, text='Item Type: ').grid(row=3, column=0)
        type_text = tk.Entry(self)
        type_text.grid(row=3, column=1)

        tk.Label(self, text='Location: ').grid(row=4, column=0)
        location_text = tk.Entry(self)
        location_text.grid(row=4, column=1)

        tk.Label(self, text='Item Quantity: ').grid(row=5, column=0)
        quantity_text = tk.Entry(self)
        quantity_text.grid(row=5, column=1)

        tk.Button(self, text='Add Item', command=lambda: parent.add_entry([title_text.get(),
                                                                           author_text.get(),
                                                                           publish_date_text.get(),
                                                                           type_text.get(),
                                                                           location_text.get(),
                                                                           quantity_text.get()], self)) \
            .grid(row=6, column=0)

        tk.Button(self, text='Cancel', command=lambda: self.destroy()).grid(row=6, column=1)

        self.mainloop()
