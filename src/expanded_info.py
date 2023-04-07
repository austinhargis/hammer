import tkinter as tk
from tkinter import ttk

from languages import *


class ExpandedInformation(tk.Frame):

    def __init__(self, parent, entry_values):
        super().__init__()

        self.parent = parent

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
        main_frame.pack(expand=True, side='left', anchor='nw')

        top_frame = ttk.Frame(main_frame)
        top_frame.pack(side='top', fill='x', padx=self.parent.padding, pady=self.parent.padding)

        left_frame = ttk.Frame(top_frame)
        left_frame.pack(side='left', anchor='nw')

        right_frame = ttk.Frame(top_frame)
        right_frame.pack(side='right', anchor='ne')

        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.pack(side='bottom', fill='x', padx=self.parent.padding, pady=self.parent.padding)

        title_frame = ttk.Frame(left_frame)
        title_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(title_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_title']}: {self.title}") \
            .pack(side='left')

        author_frame = ttk.Frame(left_frame)
        author_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(author_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_author']}: {self.author}") \
            .pack(side='left')

        description_frame = ttk.Frame(left_frame)
        description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(description_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_description']}: "
                       f"{self.description}").pack(side='left')

        publish_date_frame = ttk.Frame(right_frame)
        publish_date_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(publish_date_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['iteminfo']['item_publish_date']}: "
                       f"{self.publish_date}").pack(side='left')

        type_frame = ttk.Frame(right_frame)
        type_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(type_frame, text=f'Type: {self.type}').pack(side='left')

        tree_frame = ttk.Frame(bottom_frame)
        tree_frame.pack(side='left')

        self.tree = ttk.Treeview(tree_frame, columns=('barcode', 'location', 'status'))

        # hide the initial blank column that comes with TreeViews
        self.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.tree['displaycolumns'] = ('barcode', 'location', 'status')

        self.treeScroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.treeScroll.set)
        self.treeScroll.pack(side='right', fill='both')

        self.tree.heading('barcode', text='Barcode')
        self.tree.heading('location', text='Location')
        self.tree.heading('status', text='Status')
        self.tree.pack(expand=True, fill='y')

        ttk.Button(bottom_frame, text='Delete Item', command=lambda: self.delete_item()).pack()

        ttk.Button(tree_frame, text='Close', command=lambda: self.destroy()).pack(side='bottom',
                                                                                  pady=self.parent.padding)

    def get_record_items(self):
        items = self.parent.db.dbCursor.execute(f"""
            SELECT * 
            FROM items
            WHERE id=?
        """, (self.id,)).fetchall()

        for item in items:
            item = list(item)
            del item[0]
            item.append(self.parent.get_item_status(item[0]))
            self.tree.insert('', tk.END, values=item)

    def delete_item(self):
        selected = self.tree.item(self.parent.tree.focus())
        barcode = selected['values'][0]

        barcode_checkouts = self.parent.db.dbCursor.execute(f"""
            SELECT *
            FROM checkouts
            WHERE item_barcode=?    
        """, (barcode,)).fetchall()

        if len(barcode_checkouts) == 0:
            self.parent.db.dbCursor.execute(f"""
                DELETE FROM items
                WHERE barcode=?
            """, (barcode,))
            self.parent.db.dbConnection.commit()
