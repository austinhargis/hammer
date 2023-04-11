from tkinter import ttk


class LocationTemplate(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both')
        self.heading_label = ttk.Label(heading_frame, font=self.parent.heading_font)
        self.heading_label.pack(side='left')

        name_frame = ttk.Frame(main_frame)
        name_frame.pack(fill='both')
        ttk.Label(name_frame, text='Location Name').pack(side='left')
        self.name_entry = ttk.Entry(name_frame)
        self.name_entry.pack(side='right')

        barcode_frame = ttk.Frame(main_frame)
        barcode_frame.pack(fill='both')
        ttk.Label(barcode_frame, text='Barcode').pack(side='left')
        self.barcode_entry = ttk.Entry(barcode_frame)
        self.barcode_entry.pack(side='right')

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='both')
        self.func_button = ttk.Button(button_frame)
        self.func_button.pack(side='left')
        ttk.Button(button_frame, text='Close', command=lambda: [self.parent.tab_controller.select(0),
                                                                self.destroy()]).pack(side='left')

        self.name_entry.focus()
        self.name_entry.bind('<Return>', lambda event: self.barcode_entry.focus())

    def get_all_entries(self):
        return [
            self.barcode_entry.get(),
            self.name_entry.get()
        ]
