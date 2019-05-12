import tkinter as tk
from tkinter import ttk
import mainWindow as ui
import logging

logging.basicConfig(level=logging.DEBUG)

root=tk.Tk()
root.title("Led Controller")

test = ui.MainWindow(root, borderwidth=5)

def onClose():
    test.disconnectDevice(True)
    root.desroy()

root.protocol("WM_DELTE_WINDOW", onClose)
root.mainloop()
