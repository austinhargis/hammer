import tkinter as tk
import urllib.request
import webbrowser
from datetime import datetime


class UpdateChecker(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        # Passed parameters
        self.parent = parent

        # Initialize variables with default values
        self.server_version_text = None
        self.update_button = None
        self.current_version = None
        self.server_version = None
        self.version = '0.2.0'

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title('Check for Updates')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2,
                         pady=(self.parent.padding * 2, self.parent.padding))
        tk.Label(title_frame, text='Update Checker').pack()

        subtitle_frame = tk.Frame(self)
        subtitle_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        self.last_check = tk.Label(subtitle_frame, text=f'Last Checked {self.parent.save_m.data["last_update_check"]}')
        self.last_check.pack()

        self.server_label = tk.Label(self, text='Server Version: ')
        self.server_label.pack()

        tk.Label(self, text=f'Current Version: {self.version}').pack()

        check_update_theme = tk.Frame(self)
        check_update_theme.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=(self.parent.padding,
                                                                                              self.parent.padding * 2))
        tk.Button(check_update_theme, text='Check for Updates', command=lambda: self.check_for_update()).pack()

        self.check_for_update()

        self.mainloop()

    def check_for_update(self):
        self.parent.save_m.data['last_update_check'] = datetime.now().strftime('%I:%M%p %m/%d/%Y')
        self.last_check.configure(text=f'Last Checked {self.parent.save_m.data["last_update_check"]}')

        # Download the latest version file from the server
        urllib.request.urlretrieve('https://raw.githubusercontent.com/austinhargis/hammer/main/version.txt',
                                   './data/version.txt')

        # Convert the current and server version to information that is usable
        if self.server_version is None:
            file = open('./data/version.txt', 'r')
            self.server_version_text = file.read()
            self.server_version = tuple(self.server_version_text.replace('\n', '').split('.'))
            self.current_version = tuple(self.version.split('.'))
            file.close()

        self.server_label['text'] = f'Server Version: {self.server_version_text}'

        # Determine whether the server version is newer than the current version
        if self.server_version > self.current_version:
            if self.update_button is None:
                self.update_button = tk.Button(self,
                                               text='Get Update',
                                               command=lambda: webbrowser.open_new_tab(
                                                   'https://github.com/austinhargis/hammer/releases')
                                               )
                self.update_button.pack(padx=self.parent.padding * 2,
                                        pady=(self.parent.padding, self.parent.padding * 2))
