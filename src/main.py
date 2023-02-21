"""

    hammer: an inventory management system developed in 
    python with sqlite3

    version: v0.1.0a

"""

import os, sys
from tkinter import *
from tkinter import ttk

from database import Database

version = 'v0.1.0a'

class Hammer:

    def __init__(self, root):
        root.title(f"hammer - {version}")

if __name__ == "__main__":
    root = Tk()
    Hammer(root)
    root.mainloop()
    
    db = Database("hammer.db")
