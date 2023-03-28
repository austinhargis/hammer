import tkinter as tk
import urllib.request


class UpdateChecker(tk.Toplevel):

    def __init__(self, parent):
        super().__init__()

        self.current_version = None
        self.parent = parent
        self.server_version = None
        self.version = '0.1.0'

        self.attributes('-topmost', True)
        self.resizable(False, False)
        self.title('Updater')

        title_frame = tk.Frame(self)
        title_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2,
                         pady=(self.parent.padding * 2, self.parent.padding))
        tk.Label(title_frame, text='Update').pack()

        auto_update_frame = tk.Frame(self)
        auto_update_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(auto_update_frame, text=f'Automatic Updates {self.parent.save_m.data["automatic_updates"]}').pack()

        subtitle_frame = tk.Frame(self)
        subtitle_frame.pack(fill='both', expand=True, padx=self.parent.padding * 2, pady=self.parent.padding)
        tk.Label(subtitle_frame, text=f'Last Checked {self.parent.save_m.data["last_update_check"]}').pack()

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
        urllib.request.urlretrieve('https://raw.githubusercontent.com/austinhargis/hammer/main/version.txt',
                                   '../version.txt')

        if self.server_version is None:
            file = open('../version.txt', 'r')
            self.server_version_text = file.read()
            self.server_version = tuple(self.server_version_text.split('.'))
            self.current_version = tuple(self.version.split('.'))
            file.close()

        self.server_label['text'] = f'Server Version: {self.server_version_text}'

        if self.server_version > self.current_version:
            print(f'update needed')
