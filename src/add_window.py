import tkinter as tk

from item_info import ItemInfo


class AddItem:

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.template = ItemInfo(self.parent, 'add')

        self.template.bind('<Return>', lambda event: parent.add_entry(self.template.get_item_info(), self))

        button_frame = tk.Frame(self.template)
        button_frame.pack(expand=True, padx=self.parent.padding * 2,
                          pady=(self.parent.padding, self.parent.padding * 2))
        tk.Button(button_frame, text='Add Item', command=lambda: self.parent.add_entry(self.template.get_item_info(),
                                                                                       self)) \
            .pack(side='left')
        tk.Button(button_frame, text='Cancel', command=lambda: self.template.destroy()).pack(side='right')

        self.template.mainloop()
