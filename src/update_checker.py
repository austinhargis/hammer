import tkinter as tk
import urllib.request
import webbrowser
from datetime import datetime
from tkinter import ttk

from languages import *


class UpdateChecker(tk.Frame):

    def __init__(self, parent):
        super().__init__()

        self.parent = parent
        self.server_version = None
        self.update_button = None
        self.version = '0.2.0'

        self.window()
        self.check_for_update()

    def check_for_update(self):
        self.parent.save_m.data['last_update_check'] = datetime.now().strftime('%I:%M%p %m/%d/%Y')
        self.last_check.configure(
            text=f"{languages[self.parent.save_m.data['language']]['update']['update_last_checked']} {self.parent.save_m.data['last_update_check']}")

        # Download the latest version file from the server
        urllib.request.urlretrieve('https://raw.githubusercontent.com/austinhargis/hammer/main/version.txt',
                                   f'{self.parent.data_path}/server_version.txt')

        # Convert the current and server version to information that is usable
        if self.server_version is None:
            with open(f'{self.parent.data_path}/server_version.txt') as s_ver:
                self.server_version_text = s_ver.read()
            self.server_version = tuple(self.server_version_text.replace('\n', '').split('.'))
            self.current_version = tuple(self.version.split('.'))

        self.server_label.configure(
            text=f"{languages[self.parent.save_m.data['language']]['update']['update_available_version']} {self.server_version_text}")

        # Determine whether the server version is newer than the current version
        if self.server_version > self.current_version:
            if self.update_button is None:
                self.update_button = ttk.Button(self.check_update_frame,
                                                text='Get Update',
                                                command=lambda: webbrowser.open_new_tab(
                                                    f'https://github.com/austinhargis/hammer/releases/tag/version_{self.server_version_text}')
                                                )
                self.update_button.pack(padx=self.parent.padding)

    def window(self):

        main_frame = tk.Frame(self)
        main_frame.pack(side='left', anchor='nw')

        title_frame = tk.Frame(main_frame)
        title_frame.pack(fill='both', padx=self.parent.padding,
                         pady=self.parent.padding)
        ttk.Label(title_frame,
                  text=languages[self.parent.save_m.data['language']]['update']['update_header'],
                  font=self.parent.heading_font).pack(side='left')

        subtitle_frame = tk.Frame(main_frame)
        subtitle_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.last_check = ttk.Label(subtitle_frame,
                                    text=f"{languages[self.parent.save_m.data['language']]['update']['update_last_checked']} {self.parent.save_m.data['last_update_check']}")
        self.last_check.pack(side='left')

        server_version_frame = tk.Frame(main_frame)
        server_version_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        self.server_label = ttk.Label(server_version_frame,
                                      text=languages[self.parent.save_m.data['language']]['update'][
                                          'update_available_version'])
        self.server_label.pack(side='left')

        current_version_frame = tk.Frame(main_frame)
        current_version_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Label(current_version_frame,
                  text=f"{languages[self.parent.save_m.data['language']]['update']['update_your_version']} {self.version}").pack(
            side='left')

        self.check_update_frame = tk.Frame(main_frame)
        self.check_update_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(self.check_update_frame,
                   text=languages[self.parent.save_m.data['language']]['update']['update_check_for'],
                   command=lambda: self.check_for_update()).pack(side='left')

        quit_frame = tk.Frame(main_frame)
        quit_frame.pack(fill='both', padx=self.parent.padding, pady=(0, self.parent.padding))
        ttk.Button(quit_frame,
                   text=languages[self.parent.save_m.data['language']]['prompts']['prompt_exit'],
                   command=lambda: [self.parent.tab_controller.select(0), self.destroy()]).pack(side='left')
