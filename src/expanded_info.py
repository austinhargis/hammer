import tkinter as tk
from tkinter import ttk


class ExpandedInformation(tk.Frame):

    def __init__(self, parent, entry_values):
        super().__init__()

        self.parent = parent

        self.id = entry_values[0]
        self.barcode = entry_values[1]
        self.title = entry_values[2]
        self.author = entry_values[3]
        self.description = entry_values[8]
        self.publish_date = entry_values[4]
        self.type = entry_values[5]
        self.location = entry_values[6]
        self.quantity = entry_values[7]

        self.tab()

    def tab(self):

        ttk.Label(self, text=f'ID: {self.id}').pack()
        ttk.Label(self, text=f'Barcode {self.barcode}').pack()
        ttk.Label(self, text=f'Title: {self.title}').pack()
        ttk.Label(self, text=f'Author: {self.author}').pack()
        ttk.Label(self, text=f'Description: {self.description}').pack()
        ttk.Label(self, text=f'Publish Date: {self.publish_date}').pack()
        ttk.Label(self, text=f'Type: {self.type}').pack()
        ttk.Label(self, text=f'Quantity: {self.quantity}').pack()
        ttk.Label(self, text=f'Location: {self.location}').pack()
