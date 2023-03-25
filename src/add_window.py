import tkinter as tk

from item_info import ItemInfo


class AddItem:

    def __init__(self, parent):
        super().__init__()

        self.template = ItemInfo(parent, 'add')

        self.template.bind('<Return>', lambda event: parent.add_entry([self.template.title_text.get(),
                                                                       self.template.author_text.get(),
                                                                       self.template.publish_date_text.get(),
                                                                       self.template.type_text.get(),
                                                                       self.template.location_text.get(),
                                                                       self.template.quantity_text.get()], self))

        button_frame = tk.Frame(self.template)
        button_frame.pack(expand=True, padx=parent.padding * 2, pady=(parent.padding, parent.padding * 2))
        tk.Button(button_frame, text='Add Item', command=lambda: parent.add_entry(
            [self.template.title_text.get(),
             self.template.author_text.get(),
             self.template.publish_date_text.get(),
             self.template.type_text.get(),
             self.template.location_text.get(),
             self.template.quantity_text.get()],
            self)) \
            .pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.template.destroy()).pack(side='right')

        self.template.bind('<Return>', lambda event: parent.add_entry([self.template.title_text.get(),
                                                                       self.template.author_text.get(),
                                                                       self.template.publish_date_text.get(),
                                                                       self.template.type_text.get(),
                                                                       self.template.location_text.get(),
                                                                       self.template.quantity_text.get()], self))
        self.template.mainloop()

