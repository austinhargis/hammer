import logging
import tkinter as tk
from tkinter import ttk

from add_item_from_record_window import AddItemFromRecordWindow
from add_record_window import AddRecordWindow
from checkin_screen import CheckinScreen
from checkout_screen import CheckoutScreen
from expanded_info import ExpandedInformation
from user_create import CreateUser
from languages import *
from location_create import LocationCreate
from location_view import LocationView
from manage_record_window import ManageRecordWindow
from user_view_specific import ViewSpecificUser


class HomeTab(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.delete_button = None
        self.manage_button = None
        self.parent = parent

        self.window()
        self.populate_table()
        self.after(self.parent.manage_check_delay, self.check_focus)
        self.parent.tree.bind("<Delete>", lambda event: self.delete_popup_window())
        self.parent.config(menu=self.parent.menu_bar)

    def check_focus(self):
        if self.parent.tree.focus() == '':
            self.manage_button.configure(state='disabled')
            self.delete_button.configure(state='disabled')
            self.after(self.parent.manage_check_delay, self.check_focus)
        else:
            self.manage_button.configure(state='normal')
            self.delete_button.configure(state='normal')
            self.after(self.parent.manage_check_delay, self.check_focus)

    def clear_table(self):
        """
            clear_table purges the TreeView of all of its children
            :return:
        """
        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)

    def delete_entry(self):
        """
            delete_entry takes the currently selected/focused item in
            the TreeView and performs a SQL query to remove it from the
            database, before finally refreshing the table
            :return:
        """
        current_item = self.parent.tree.focus()
        if current_item != '':
            self.parent.db.delete_query(self.parent.tree.item(current_item)['values'])
            self.refresh_table()

            logging.info('Deleted item from database')

    def delete_popup_window(self):
        """
            delete_popup_window creates a popup window that allows the user to ensure that they
            intended on deleting the focused item
            :return:
        """
        popup = tk.Toplevel(padx=self.parent.padding, pady=self.parent.padding)
        popup.title('Confirm Delete?')

        ttk.Label(popup,
                  text=languages[self.parent.save_m.data['language']]['prompts']['prompt_delete'],
                  wraplength=self.parent.wraplength,
                  justify='center').pack()
        ttk.Label(popup,
                  text=f'Item: {self.parent.tree.item(self.parent.tree.focus())["values"][1]}').pack()

        button_frame = ttk.Frame(popup)
        button_frame.pack(expand=True)

        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_confirm'],
                   command=lambda: [self.delete_entry(), popup.destroy()]).pack(side='left')
        ttk.Button(button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: popup.destroy()).pack(side='right')

        popup.mainloop()

        logging.info('Initialized delete confirmation')

    def populate_table(self, current_table=None):
        """
            populate_table takes the return value of self.db.get_all_query()
            and builds a "table" of tk.Entry with the database
            :param current_table: determines the necessary table (for searches)
            :return:
        """
        if current_table is None:
            current_table = self.parent.db.get_all_query()

        for row in current_table:
            self.parent.tree.insert('', tk.END, values=row)

        if len(self.parent.tree.get_children()) > 0:
            child = self.parent.tree.get_children()[0]
            self.parent.tree.focus(child)
            self.parent.tree.selection_set(child)

        logging.info('Populated the table')

    def get_item_status(self, barcode):
        self.parent.db.dbCursor.execute(f"""
            SELECT *
            FROM checkouts
            WHERE item_barcode=%s
        """, (barcode,))
        check_status = self.parent.db.dbCursor.fetchall()

        logging.info(f'Got item status for item {barcode}')

        if len(check_status) == 0:
            return languages[self.parent.save_m.data['language']]['item_info']['item_available']
        else:
            return languages[self.parent.save_m.data['language']]['item_info']['item_unavailable']

    def refresh_table(self):
        """
            refresh_table iterates through all elements in the TreeView
            and then for each element, deletes it from the TreeView before
            repopulating the table
            :return:
        """

        self.clear_table()
        self.populate_table()

        logging.info('Refreshed the table')

    def search_table(self, entry_box):
        """
            the search table function gets the currently entered text from the passed
            entry_box and executes a SQL query with it
            :param entry_box:
            :return:
        """
        search_term = entry_box.get()

        self.parent.db.dbCursor.execute(f"""SELECT * 
                                     FROM item_record 
                                     WHERE title LIKE \'%{search_term}%\' 
                                     OR author LIKE \'%{search_term}%\'
                                     OR publish_date LIKE \'%{search_term}%\'
                                     OR type LIKE \'%{search_term}%\'""")
        current_table = self.parent.db.dbCursor.fetchall()
        self.clear_table()
        self.populate_table(current_table)

        logging.info(f'Performed search query "{search_term}"')

    def sort_tree(self):
        for item in self.parent.tree.get_children():
            self.parent.tree.delete(item)

        sorts_names = {
            'Ascending': 'asc',
            'Descending': 'desc',
            'Title': 'title',
            'Author': 'author',
            'Publish Date': 'publish_date',
            'Type': 'type'
        }

        column = sorts_names[self.sort_col_var.get()]
        direction = sorts_names[self.sort_type_var.get()]

        self.parent.db.dbCursor.execute(f"""
            SELECT * FROM item_record
            ORDER BY {column} {direction}
        """)
        sort_results = self.parent.db.dbCursor.fetchall()

        for item in sort_results:
            self.parent.tree.insert('', tk.END, values=item)

    def tree_double_click(self):
        current_item = self.parent.tree.focus()

        entry_values = self.parent.tree.item(current_item)['values']
        entry_title = self.parent.tree.item(current_item)['values'][1]

        self.parent.create_tab(ExpandedInformation, title=f'{entry_title}', values=entry_values)

    def window(self):
        main_frame = ttk.Frame(self)
        main_frame.pack(expand=True, fill='both', padx=self.parent.padding, pady=self.parent.padding)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side='left', anchor='nw', padx=self.parent.padding, pady=self.parent.padding)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(fill='both', expand=True, side='right', anchor='ne', padx=self.parent.padding)

        top_right_frame = ttk.Frame(right_frame)
        top_right_frame.pack(expand=True, fill='both', side='top')

        bottom_right_frame = ttk.Frame(right_frame)
        bottom_right_frame.pack(fill='both', side='bottom')

        checkout_frame = ttk.Frame(left_frame)
        checkout_frame.pack(fill='x', side='top', anchor='nw', padx=self.parent.padding, pady=(0, self.parent.padding))

        ttk.Label(checkout_frame,
                  text=languages[self.parent.save_m.data['language']]['item_info']['item_check_heading'],
                  font=self.parent.heading_font).pack(anchor='nw')
        ttk.Button(checkout_frame,
                   text=languages[self.parent.save_m.data['language']]['item_info']['item_action_check_in'],
                   command=lambda: self.parent.create_tab(CheckinScreen,
                                                          languages[self.parent.save_m.data['language']]['item_info'][
                                                              'item_action_check_in'])).pack(fill='x')
        ttk.Button(checkout_frame,
                   text=languages[self.parent.save_m.data['language']]['item_info']['item_action_check_out'],
                   command=lambda: self.parent.create_tab(CheckoutScreen,
                                                          languages[self.parent.save_m.data['language']]['item_info'][
                                                              'item_action_check_out'])).pack(fill='x')

        if bool(self.parent.user_permissions['can_manage_records']):
            manage_frame = ttk.Frame(left_frame)
            manage_frame.pack(fill='x', side='top', anchor='nw', padx=self.parent.padding,
                              pady=(0, self.parent.padding))

            ttk.Label(manage_frame, text=languages[self.parent.save_m.data['language']]['general']['records_heading'],
                      font=self.parent.heading_font).pack(anchor='nw')
            ttk.Button(manage_frame,
                       text=languages[self.parent.save_m.data['language']]['item_info']['item_record_add'],
                       command=lambda: self.parent.create_tab(AddRecordWindow,
                                                              languages[self.parent.save_m.data['language']][
                                                                  'item_info'][
                                                                  'item_record_add'])).pack(fill='x')
            self.manage_button = ttk.Button(manage_frame,
                                            text=languages[self.parent.save_m.data['language']]['item_info'][
                                                'item_record_manage'],
                                            command=lambda: self.parent.create_tab(ManageRecordWindow,
                                                                                   languages[self.parent.save_m.data[
                                                                                       'language']][
                                                                                       'item_info'][
                                                                                       'item_record_manage']))
            self.manage_button.pack(fill='x')
            self.manage_button.configure(state='disabled')

            self.delete_button = ttk.Button(manage_frame,
                                            text=languages[self.parent.save_m.data['language']]['item_info'][
                                                'item_delete_all'],
                                            command=lambda: self.delete_popup_window())
            self.delete_button.pack(fill='x')
            self.delete_button.configure(state='disabled')

            location_frame = ttk.Frame(left_frame)
            location_frame.pack(fill='x', side='top', padx=self.parent.padding, pady=(0, self.parent.padding))

            ttk.Label(location_frame, text=languages[self.parent.save_m.data['language']]['locations']['location_heading'],
                      font=self.parent.heading_font).pack(anchor='nw')
            ttk.Button(location_frame,
                       text=languages[self.parent.save_m.data['language']]['locations']['location_create'],
                       command=lambda: self.parent.create_tab(LocationCreate,
                                                              languages[self.parent.save_m.data['language']]['locations'][
                                                                  'location_create'])).pack(fill='x')
            ttk.Button(location_frame,
                       text=languages[self.parent.save_m.data['language']]['locations']['location_view'],
                       command=lambda: self.parent.create_tab(LocationView,
                                                              languages[self.parent.save_m.data['language']]['locations'][
                                                                  'location_view'])).pack(fill='x')

        users_frame = ttk.Frame(left_frame)
        users_frame.pack(fill='x', side='top', padx=self.parent.padding)

        ttk.Label(users_frame,
                  text=languages[self.parent.save_m.data['language']]['users']['users_home_heading'],
                  font=self.parent.heading_font).pack(anchor='nw')
        ttk.Button(users_frame,
                   text=languages[self.parent.save_m.data['language']]['users']['user_add'],
                   command=lambda: self.parent.create_tab(CreateUser,
                                                          languages[self.parent.save_m.data['language']]['users'][
                                                              'user_add'])).pack(
            fill='x')
        ttk.Button(users_frame,
                   text=languages[self.parent.save_m.data['language']]['users']['user_specific'],
                   command=lambda: self.parent.create_tab(ViewSpecificUser,
                                                          languages[self.parent.save_m.data['language']]['users'][
                                                              'user_specific'])).pack(fill='x')

        # creates the TreeView which will handle displaying all schema in the database
        self.parent.tree = ttk.Treeview(top_right_frame,
                                        columns=(
                                            'id', 'title', 'author', 'publish_date', 'type'))
        # hide the initial blank column that comes with TreeViews
        self.parent.tree['show'] = 'headings'
        # show only the desired columns (hiding the id)
        self.parent.tree['displaycolumns'] = ('title', 'author', 'publish_date', 'type',)

        self.parent.tree_scroll_bar = ttk.Scrollbar(top_right_frame, command=self.parent.tree.yview)
        self.parent.tree.configure(yscrollcommand=self.parent.tree_scroll_bar.set)
        self.parent.tree_scroll_bar.pack(side='right', fill='both', pady=self.parent.padding)

        self.parent.tree.heading('id', text='ID')
        self.parent.tree.heading('title', text='Title')
        self.parent.tree.column('title', stretch=False, width=150)
        self.parent.tree.heading('author', text='Author')
        self.parent.tree.column('author', stretch=False, width=150)
        self.parent.tree.heading('publish_date', text='Publish Date')
        self.parent.tree.heading('type', text='Type')
        self.parent.tree.pack(expand=True, fill='both', padx=(self.parent.padding, 0), pady=self.parent.padding)

        search_frame = ttk.Frame(bottom_right_frame)
        search_frame.pack(side='left', fill='both', pady=self.parent.padding)
        ttk.Label(search_frame, text='Search', font=self.parent.heading_font).pack(side='left',
                                                                                   padx=self.parent.padding)
        search_box = ttk.Entry(search_frame)
        search_box.pack(side='left', padx=(0, self.parent.padding), pady=self.parent.padding)
        ttk.Button(search_frame, text='Search', command=lambda: self.search_table(search_box)).pack(side='left')

        sort_frame = ttk.Frame(bottom_right_frame)
        sort_frame.pack(side='left')
        self.sort_col_var = tk.StringVar(sort_frame)
        sort_column = ttk.OptionMenu(sort_frame, self.sort_col_var, 'Title', *[
            'Title', 'Author', 'Publish Date', 'Type'
        ])
        sort_column.pack(side='left', padx=(self.parent.padding, 0))

        self.sort_type_var = tk.StringVar(sort_frame)
        sort_type = ttk.OptionMenu(sort_frame, self.sort_type_var, 'Ascending', *[
            'Ascending', 'Descending'
        ])
        sort_type.pack(side='left')
        ttk.Button(sort_frame, text='Sort', command=lambda: self.sort_tree()).pack(side='left')

        self.bind('<Return>', lambda event: self.search_table(search_box))
        self.parent.tree.bind('<Double-1>', lambda event: self.tree_double_click())
