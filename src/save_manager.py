import pickle
from datetime import datetime


class SaveManager:

    def __init__(self, parent):

        self.parent = parent

        self.data = {
            'automatic_update_check': 'allowed',
            'language': 'english',
            'last_update_check': datetime.now().strftime('%I:%M%p %m/%d/%Y'),
            'theme': 'system',
            'settings_version': 'v0.2.0a',
            'show_developer_menu': 'disallowed',
            'show_help_menu': 'allowed',
            'show_users_menu': 'allowed',
        }
        self.settings_enabled = 'normal'

        self.load_save()

    def load_save(self):
        """
            attempts to load the settings pickle file
            :return:
        """

        try:
            with open(f'{self.parent.data_path}/settings.pkl', 'rb') as file:
                self.data = pickle.load(file)
        except EOFError:
            self.settings_enabled = 'disabled'
        except FileNotFoundError:
            self.push_save()

    def push_save(self):
        """
            saves the current settings dictionary to a pickle file
            :return:
        """

        with open(f'{self.parent.data_path}/settings.pkl', 'wb') as file:
            pickle.dump(self.data, file)
