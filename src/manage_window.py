import tkinter as tk

from item_info import ItemInfo


class ManageItem:

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.entry_id = None
        self.template = ItemInfo(parent, 'manage')
        self.template.bind('<Return>', lambda event: parent.add_entry([self.template.title_text.get(),
                                                                       self.template.author_text.get(),
                                                                       self.template.publish_date_text.get(),
                                                                       self.template.type_text.get(),
                                                                       self.template.location_text.get(),
                                                                       self.template.quantity_text.get()], self))

        self.fill_entries()

        button_frame = tk.Frame(self.template)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Save Changes',
                  command=lambda: self.parent.update_entry([self.template.title_text.get(),
                                                            self.template.author_text.get(),
                                                            self.template.publish_date_text.get(),
                                                            self.template.type_text.get(),
                                                            self.template.location_text.get(),
                                                            self.template.quantity_text.get()],
                                                           self, self.entry_id)) \
            .pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.template.destroy()).pack(side='right')

        self.template.mainloop()

    def fill_entries(self):
        current_item = self.parent.tree.focus()
        self.entry_id = self.parent.tree.item(current_item)['values'][0]
        self.template.title_text.insert(0, self.parent.tree.item(current_item)['values'][1])
        self.template.author_text.insert(0, self.parent.tree.item(current_item)['values'][2])
        self.template.publish_date_text.insert(0, self.parent.tree.item(current_item)['values'][3])
        self.template.type_text.insert(0, self.parent.tree.item(current_item)['values'][4])
        self.template.location_text.insert(0, self.parent.tree.item(current_item)['values'][5])
        self.template.quantity_text.insert(0, self.parent.tree.item(current_item)['values'][6])
