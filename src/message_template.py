import tkinter as tk
from tkinter import ttk


class MessageTemplate(ttk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.configure(padding=self.parent.padding)

        self.confirm_button = None
        self.heading_label = None
        self.message_text = None

        self.window()

    def get_data(self):
        return [self.message_text.get('1.0', 'end-1c')]

    def window(self):
        heading_frame = ttk.Frame(self)
        heading_frame.pack(anchor='nw', side='top')
        self.heading_label = ttk.Label(heading_frame, font=self.parent.heading_font)
        self.heading_label.pack(anchor='nw', side='top')

        message_frame = ttk.Frame(self)
        message_frame.pack(anchor='nw', side='top')
        self.message_text = tk.Text(message_frame, height=10)
        self.message_text.pack(anchor='nw', side='top')

        button_frame = ttk.Frame(self)
        button_frame.pack(anchor='nw', side='top')
        self.confirm_button = ttk.Button(button_frame)
        self.confirm_button.pack(side='left')
        ttk.Button(button_frame, text=self.parent.get_region_text('prompt_deny'),
                   command=lambda: self.destroy()).pack(side='left')


