"""

    hammer: an inventory management system developed in 
    python

    version: v0.1.0a

"""

import os, sys
from tkinter import *
from tkinter import ttk

version = 'v0.1.0a'

class Hammer:

    def __init__(self, root):
        root.title(f"hammer - {version}")

if __name__ == "__main__":
    root = Tk()
    Hammer(root)
    root.mainloop()
