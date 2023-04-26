import tkinter as tk
from tkinter import ttk

from add_item_from_record_window import AddItemFromRecordWindow
from languages import *
from popup_window import PopupWindow


class ExpandedInformation(tk.Frame):

    def __init__(self, parent, entry_values):
        super().__init__()

        self.parent = parent
        self.entry_id = self.parent.tree.item(self.parent.tree.focus())
        self.entry_id = self.entry_id['values'][0]

        self.id = entry_values[0]
        self.title = entry_values[1]
        self.author = entry_values[2]
        self.publish_date = entry_values[3]
        self.type = entry_values[4]
        self.description = entry_values[7]

        self.window()
        self.get_record_items()

    def window(self):

        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', side='left', anchor='nw')

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side='top', fill='x', padx=self.parent.padding, pady=self.parent.padding)

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(fill='x', side='left', anchor='nw')

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(fill='x', expand=True, side='right', anchor='ne', padx=self.parent.padding)

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', expand=True, fill='both', padx=self.parent.padding, pady=self.parent.padding)

        title_frame = ttk.Frame(left_frame)
        title_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(title_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['item_info']['item_title']}: {self.title}") \
            .pack(side='left')

        author_frame = ttk.Frame(left_frame)
        author_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(author_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['item_info']['item_author']}: {self.author}") \
            .pack(side='left')

        description_frame = ttk.Frame(left_frame)
        description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(description_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['item_info']['item_description']}: "
                       f"\n{self.description}",
                  wraplength=500).pack(side='left')

        publish_date_frame = ttk.Frame(right_frame)
        publish_date_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(publish_date_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['item_info']['item_publish_date']}: "
                       f"{self.publish_date}").pack(side='left')

        type_frame = ttk.Frame(right_frame)
        type_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(type_frame, text=f'Type: {self.type}').pack(side='left')

        tree_frame = ttk.Frame(bottom_frame)
        tree_frame.pack(expand=True, fill='both', side='top')

        self.tree = ttk.Treeview(tree_frame, columns=('barcode', 'location', 'description', 'status'))

        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('barcode', 'location', 'description', 'status')

        treeScroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=treeScroll.set)
        treeScroll.pack(side='right', fill='both')

        self.tree.heading('barcode', text='Barcode')
        self.tree.heading('location', text='Location')
        self.tree.heading('description', text='Description')
        self.tree.heading('status', text='Status')
        self.tree.pack(fill='both', expand=True)

        button_frame = ttk.Frame(bottom_frame)
        button_frame.pack(fill='both', side='bottom')

        ttk.Button(button_frame, text='Close',
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='right',
                                                          pady=self.parent.padding,
                                                          fill='x')

        ttk.Button(button_frame, text='Delete Item',
                   command=lambda: [self.delete_item(), self.refresh_table()]).pack(side='right',
                                                                                    fill='x')

        ttk.Button(button_frame, text='Manage Item',
                   command=lambda: None).pack(side='right',
                                              fill='x')

        ttk.Button(button_frame, text='Create Item',
                   command=lambda: [self.parent.create_tab(AddItemFromRecordWindow, 'Create Item',
                                                           self.entry_id)]).pack(side='right',
                                                                                 fill='x')

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.get_record_items()

    def get_record_items(self):
        self.parent.db.dbCursor.execute(f"""
            SELECT * 
            FROM items
            WHERE id=%s
        """, (self.id,))
        items = self.parent.db.dbCursor.fetchall()

        for item in items:
            item = list(item)
            del item[0]
            item.append(self.parent.home_tab.get_item_status(item[0]))
            self.tree.insert('', tk.END, values=item)

    def delete_item(self):
        selected = self.tree.item(self.tree.focus())
        barcode = selected['values'][0]

        self.parent.db.dbCursor.execute(f"""
            SELECT *
            FROM checkouts
            WHERE item_barcode=%s    
        """, (barcode,))
        barcode_checkouts = self.parent.db.dbCursor.fetchall()

        if len(barcode_checkouts) == 0:
            self.parent.db.dbCursor.execute(f"""
                DELETE FROM items
                WHERE barcode=%s
            """, (barcode,))
            self.parent.db.dbConnection.commit()
        else:
            PopupWindow(self.parent,
                        'Barcode Checked Out',
                        'This item cannot be deleted at this time because it is currently checked out.')
