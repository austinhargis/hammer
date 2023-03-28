from datetime import datetime
import pickle


class SaveManager:

    def __init__(self):
        self.data = {
            'automatic_updates': 'disabled',
            'last_update_check': datetime.now(),
            'theme': 'system',
            'settings_version': 'v0.1.0a',
            'show_developer_menu': 'enabled',
        }
        self.settings_enabled = 'normal'

        self.load_save()

    def load_save(self):
        """
            attempts to load the settings pickle file
            :return:
        """

        try:
            data_in = open('./settings.pkl', 'rb')
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

        data_out = open('./settings.pkl', 'wb')
        pickle.dump(self.data, data_out)
        data_out.close()
