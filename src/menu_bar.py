import sys
import tkinter as tk
from webbrowser import open_new_tab

from checkin_screen import CheckinScreen
from checkout_screen import CheckoutScreen
from src.user_view_specific import ViewSpecificUser
from user_create import CreateUser
from languages import *
from settings import SettingsWindow
from update_checker import UpdateChecker
from view_checkouts import ViewCheckouts
from view_users import ViewUsers


class MenuBar(tk.Menu):

    def __init__(self, parent):
        tk.Menu.__init__(self, parent)

        self.checkout_menu = None
        self.users_menu = None
        self.parent = parent

        self.help_menu = None
        self.database_menu = None
        self.file_menu = None
        self.developer_menu = None

        self.counter = 0

        self.generate()

    def generate(self):
        self.delete(0, 'end')

        self.file()
        self.checkout()
        self.users()
        self.developer()
        self.help()

    def checkout(self):
        if self.parent.save_m.data['show_checkout_menu'] == 'allowed':
            self.checkout_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label='Checkout', underline=0, menu=self.checkout_menu)
            self.checkout_menu.add_command(label='Checkout to User', underline=1,
                                           command=lambda: self.parent.create_tab(CheckoutScreen, 'Checkout Item'))
            self.checkout_menu.add_command(label='Check Item In', underline=1,
                                           command=lambda: self.parent.create_tab(CheckinScreen, 'Check In Item'))
            self.checkout_menu.add_command(label='View All Checkouts', underline=1,
                                           command=lambda: self.parent.create_tab(ViewCheckouts, 'View All Checkouts'))

    def file(self):
        self.file_menu = tk.Menu(self, tearoff=False)
        self.add_cascade(label=languages[self.parent.save_m.data['language']]['menubar']['file_menu'], underline=0,
                         menu=self.file_menu)
        self.file_menu.add_command(label=languages[self.parent.save_m.data['language']]['update']['update_check_for'],
                                   underline=1,
                                   command=lambda: self.parent.create_tab(UpdateChecker, languages[
                                       self.parent.save_m.data['language']]['update']['update_check_for']))
        self.file_menu.add_command(label=languages[self.parent.save_m.data['language']]['settings']['settings'],
                                   underline=1,
                                   command=lambda: self.parent.create_tab(SettingsWindow, languages[
                                       self.parent.save_m.data['language']]['settings']['settings']))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", underline=1, command=self.quit, accelerator='Escape')

    def developer(self):
        if self.parent.save_m.data['show_developer_menu'] == 'allowed':
            self.developer_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=languages[self.parent.save_m.data['language']]['menubar']['developer_menu'],
                             underline=0, menu=self.developer_menu)
            self.developer_menu.add_command(
                label=languages[self.parent.save_m.data['language']]['developer']['table_drop'], underline=1,
                command=lambda: self.parent.drop_table())

    def help(self):
        if self.parent.save_m.data['show_help_menu'] == 'allowed':
            self.help_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=languages[self.parent.save_m.data['language']]['menubar']['help_menu'], underline=0,
                             menu=self.help_menu)
            self.help_menu.add_command(label="GitHub", underline=1, command=lambda: open_new_tab(
                'https://github.com/austinhargis/hammer'))

    def users(self):
        if self.parent.save_m.data['show_users_menu'] == 'allowed':
            self.users_menu = tk.Menu(self, tearoff=False)
            self.add_cascade(label=languages[self.parent.save_m.data['language']]['menubar']['users_menu'], underline=0,
                             menu=self.users_menu)
            self.users_menu.add_command(label=languages[self.parent.save_m.data['language']]['users']['user_add'],
                                        underline=1,
                                        command=lambda: self.parent.create_tab(CreateUser, languages[
                                            self.parent.save_m.data['language']]['users']['user_add']))
            self.users_menu.add_command(label=languages[self.parent.save_m.data['language']]['users']['user_specific'],
                                        underline=1,
                                        command=lambda: self.parent.create_tab(ViewSpecificUser, languages[
                                            self.parent.save_m.data['language']]['users']['user_specific']))
            self.users_menu.add_command(label=languages[self.parent.save_m.data['language']]['users']['user_view'],
                                        underline=1,
                                        command=lambda: self.parent.create_tab(ViewUsers, languages[
                                            self.parent.save_m.data['language']]['users']['user_view']))

    def quit(self):
        sys.exit()
