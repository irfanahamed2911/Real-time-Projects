import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_script(script_name):
    python = sys.executable
    subprocess.Popen([python, script_name])

def open_gst_bill():
    run_script("custombill.py")  # Runs GST Bill

def open_normal_bill():
    run_script("normal.py")  # Runs Normal Bill

def open_stock_hex():
    run_script("stockhex.py")  # Runs Hex Stock app

def open_stock_flange():
    run_script("stockflange.py")  # Runs Flange Stock app

def open_calculator1():
    run_script("calculator1.py")

def open_calculator2():
    run_script("calculator2.py")

# --- Main Window ---
root = tk.Tk()
root.title("Dashboard")
root.geometry("400x600")
root.configure(bg="#f1f3f4")

# Title
title = tk.Label(root, text="Dashboard", font=("Segoe UI", 20, "bold"), bg="#f1f3f4", fg="#202124")
title.pack(pady=30)

# Button style
btn_style = {
    "font": ("Segoe UI", 14),
    "width": 20,
    "height": 2,
    "bg": "#0077cc",
    "fg": "white",
    "bd": 0,
    "activebackground": "#005fa3",
    "cursor": "hand2"
}

# Buttons
tk.Button(root, text="GST Bill", command=open_gst_bill, **btn_style).pack(pady=10)
tk.Button(root, text="Normal Bill", command=open_normal_bill, **btn_style).pack(pady=10)
tk.Button(root, text="Stocks Hex", command=open_stock_hex, **btn_style).pack(pady=10)
tk.Button(root, text="Stocks Flange", command=open_stock_flange, **btn_style).pack(pady=10)
tk.Button(root, text="Calculator 1", command=open_calculator1, **btn_style).pack(pady=10)
tk.Button(root, text="Calculator 2", command=open_calculator2, **btn_style).pack(pady=10)

root.mainloop()
