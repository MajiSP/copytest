import tkinter as tk
from tkinter import filedialog
import shutil
import os
import subprocess
import sys
import ctypes

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def copy_boot_device_with_admin():
    source_path = source_entry.get()
    dest_path = dest_entry.get()

    if not os.path.exists(source_path):
        status_label.config(text="Error: Source path does not exist.")
        return

    if not os.path.isdir(source_path):
        status_label.config(text="Error: Source path is not a directory.")
        return

    try:
        if os.path.isdir(os.path.join(source_path, "Windows")):
            subprocess.run(["robocopy", source_path, dest_path, "/MIR", "/COPYALL", "/R:3", "/W:5", "/NFL", "/NDL", "/NJH", "/NJS", "/nc", "/ns", "/np"])
        else:
            shutil.copytree(source_path, dest_path)
        status_label.config(text="Copy successful!")
    except Exception as e:
        status_label.config(text=f"Error: {str(e)}")

def copy_boot_device():
    copy_boot_device_with_admin()

def browse_source():
    source_path = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, source_path)

def browse_dest():
    dest_path = filedialog.askdirectory()
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, dest_path)

def main():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit(0)

    root = tk.Tk()
    root.title("Boot Device Copier Test for Thijmen")
    root.geometry("400x150")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True)

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
else:
    root = tk.Tk()
    root.title("Boot Device Copier Test for Thijmen")
    root.geometry("400x150")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(expand=True)

    source_label = tk.Label(frame, text="Source Boot Device:")
    source_label.grid(row=0, column=0, sticky="w")
    source_entry = tk.Entry(frame, width=30)
    source_entry.grid(row=0, column=1)
    source_browse_button = tk.Button(frame, text="Browse", command=browse_source)
    source_browse_button.grid(row=0, column=2)

    dest_label = tk.Label(frame, text="Destination Device:")
    dest_label.grid(row=1, column=0, sticky="w")
    dest_entry = tk.Entry(frame, width=30)
    dest_entry.grid(row=1, column=1)
    dest_browse_button = tk.Button(frame, text="Browse", command=browse_dest)
    dest_browse_button.grid(row=1, column=2)

    copy_button = tk.Button(frame, text="Copy", command=copy_boot_device)
    copy_button.grid(row=2, column=1, pady=10)

    status_label = tk.Label(frame, text="")
    status_label.grid(row=3, column=0, columnspan=3)

    root.mainloop()
