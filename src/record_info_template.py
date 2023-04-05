import tkinter as tk
from tkinter import ttk

from languages import *


class RecordInfoTemplate(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        # self.attributes('-topmost', True)
        # self.resizable(False, False)
        # self.title(f'{process.capitalize()} Item')

        main_frame = tk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        self.heading_frame = ttk.Frame(main_frame)
        self.heading_frame.pack(fill='both', padx=self.parent.padding, pady=self.parent.padding)
        self.heading_label = ttk.Label(self.heading_frame, font=self.parent.heading_font)
        self.heading_label.pack(side='left')

        self.title_frame = ttk.Frame(main_frame)
        self.title_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(self.title_frame, text=languages[self.parent.save_m.data['language']]['iteminfo']['item_title']).pack(
            side='left')
        self.title_text = ttk.Entry(self.title_frame)
        self.title_text.pack(side='right')

        self.author_frame = ttk.Frame(main_frame)
        self.author_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(self.author_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_author']).pack(side='left')
        self.author_text = ttk.Entry(self.author_frame)
        self.author_text.pack(side='right')

        self.description_frame = ttk.Frame(main_frame)
        self.description_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(self.description_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_description']).pack(side='left',
                                                                                                            anchor='nw')
        self.description_text_frame = ttk.Frame(self.description_frame)
        self.description_text_frame.pack()
        self.description_text = tk.Text(self.description_text_frame, width=26, height=5)
        self.description_text.pack(side='right')

        self.publish_frame = ttk.Frame(main_frame)
        self.publish_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(self.publish_frame,
                  text=languages[self.parent.save_m.data['language']]['iteminfo']['item_publish_date']).pack(
            side='left')
        self.publish_date_text = ttk.Entry(self.publish_frame)
        self.publish_date_text.pack(side='right')

        self.type_frame = ttk.Frame(main_frame)
        self.type_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(self.type_frame, text=languages[self.parent.save_m.data['language']]['iteminfo']['item_type']).pack(
            side='left')
        self.type_text = ttk.Entry(self.type_frame)
        self.type_text.pack(side='right')

        self.button_frame = ttk.Frame(main_frame)
        self.button_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(self.button_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_deny'],
                   command=lambda: [self.parent.tab_controller.select(0),
                                    self.destroy()]).pack(side='left')

    def get_item_info(self):
        return [self.title_text.get(),
                self.author_text.get(),
                self.description_text.get('1.0', tk.END),
                self.publish_date_text.get(),
                self.type_text.get()]
