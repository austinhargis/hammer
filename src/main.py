"""

    hammer: an inventory management system developed in 
    python, with a rust backend, and a mongodb database

    version: v0.1.0a

"""

import os, sys
from tkinter import *
from tkinter import ttk

version = 'v0.1.0a'

class Hammer:

    def __init__(self, root):
        root.title(f"hammer - {version}")

    # TODO: implement add query 
    def addQuery():
        pass

    # TODO: implement delete query
    def deleteQuery():
        pass

    # TODO: implement update query
    def updateQuery():
        pass

if __name__ == "__main__":
    root = Tk()
    Hammer(root)
    root.mainloop()