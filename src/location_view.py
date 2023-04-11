import logging
import tkinter as tk
from tkinter import ttk

from languages import *
from location_manage import LocationManage


class LocationView(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        main_frame = ttk.Frame(self)
        main_frame.pack(fill='both', expand=True)

        heading_frame = ttk.Frame(main_frame)
        heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        ttk.Label(heading_frame,
                  text='Locations',
                  font=self.parent.heading_font).pack()

        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill='both', expand=True, padx=self.parent.padding, pady=(0, self.parent.padding))
        self.tree = ttk.Treeview(tree_frame, columns=('location_id', 'barcode', 'name'))
        self.tree['show'] = 'headings'
        self.tree['displaycolumns'] = ('location_id', 'barcode', 'name')

        self.tree_scroll = ttk.Scrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)
        self.tree_scroll.pack(side='right', fill='both', pady=self.parent.padding)

        self.get_locations()

        self.tree.heading('location_id',
                          text='Location ID')
        self.tree.heading('barcode',
                          text='Location Barcode')
        self.tree.heading('name',
                          text='Location Name')
        self.tree.pack(fill='both', expand=True, padx=(self.parent.padding, 0), pady=(0, self.parent.padding))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(button_frame,
                   text='Manage Location',
                   command=lambda: self.parent.create_tab(LocationManage, 'Manage Location',
                                                          self.tree.item(self.tree.focus())['values'][0])).pack()
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_exit'],
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack()

    def get_locations(self):
        locations = self.parent.db.dbCursor.execute("""
            SELECT * FROM locations
        """).fetchall()

        for location_index in range(len(locations)):
            self.tree.insert('', tk.END, values=locations[location_index])

        logging.info('Got all locations')
