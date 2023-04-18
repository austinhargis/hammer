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
            'show_checkout_menu': 'allowed',
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
            data_in = open(f'{self.parent.data_path}/settings.pkl', 'rb')
            self.data = pickle.load(data_in)
            data_in.close()
        except EOFError:
            self.settings_enabled = 'disabled'
        except FileNotFoundError:
            self.push_save()

    def push_save(self):
        """
            saves the current settings dictionary to a pickle file
            :return:
        """

        data_out = open(f'{self.parent.data_path}/settings.pkl', 'wb')
        pickle.dump(self.data, data_out)
        data_out.close()
