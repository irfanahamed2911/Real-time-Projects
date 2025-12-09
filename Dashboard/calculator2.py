import tkinter as tk
from tkinter import messagebox
import sqlite3

DB_NAME = "bolts_nuts.db"

def init_weight_data():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Drop the old table if it exists and create a new one
    c.execute("DROP TABLE IF EXISTS weights")
    c.execute("""
        CREATE TABLE weights (
            product TEXT,
            size TEXT,
            pieces_per_kg REAL,
            UNIQUE(product, size)
        )
    """)

    # All values are now pieces per kg
    weights = [
        ("bolt", "6 x 10", 200), ("bolt", "6 x 15", 180), ("bolt", "6 x 20", 170), ("bolt", "6 x 25", 150), ("bolt", "6 x 30", 135),
        ("bolt", "6 x 35", 129), ("bolt", "6 x 40", 115), ("bolt", "6 x 45", 105), ("bolt", "6 x 50", 95),
        ("bolt", "6 x 55", 85), ("bolt", "6 x 60", 75), ("bolt", "6 x 65", 65), ("bolt", "6 x 70", 60),
        ("bolt", "6 x 75", 50), ("bolt", "6 x 80", 45), ("bolt", "6 x 85", 44), ("bolt", "6 x 90", 43),
        ("bolt", "6 x 95", 42), ("bolt", "6 x 100", 40), ("bolt", "6 x 110", 37), ("bolt", "6 x 125", 35),
        ("bolt", "6 x 150", 29),

        ("bolt", "8 x 10", 95), ("bolt", "8 x 15", 90), ("bolt", "8 x 20", 85), ("bolt", "8 x 25", 75), ("bolt", "8 x 30", 65), ("bolt", "8 x 35", 60), 
        ("bolt", "8 x 40", 55), ("bolt", "8 x 45 ", 50), ("bolt", "8 x 50", 47), ("bolt", "8 x 55", 45), ("bolt", "8 x 60", 40), ("bolt", "8 x 65", 38),
        ("bolt", "8 x 70", 37), ("bolt", "8 x 75", 35), ("bolt", "8 x 80", 33), ("bolt", "8 x 85", 30), ("bolt", "8 x 90", 31), ("bolt", "8 x 95", 30),
        ("bolt", "8 x 100", 30), ("bolt", "8 x 105", 28), ("bolt", "8 x 110", 27), ("bolt", "8 x 120", 26), ("bolt", "8 x 125", 25), ("bolt", "8 x 130", 24),
        ("bolt", "8 x 135", 23), ("bolt", "8 x 140", 22), ("bolt", "8 x 145", 21), ("bolt", "8 x 150", 20),

        ("bolt", "10 x 15", 55), ("bolt", "10 x 20", 47), ("bolt", "10 x 25", 41), ("bolt", "10 x 30", 39), ("bolt", "10 x 35", 36),
        ("bolt", "10 x 40", 32), ("bolt", "10 x 45", 30), ("bolt", "10 x 50", 28), ("bolt", "10 x 55", 26), ("bolt", "10 x 60", 24),
        ("bolt", "10 x 65", 23), ("bolt", "10 x 70", 21), ("bolt", "10 x 75", 19), ("bolt", "10 x 80", 18), ("bolt", "10 x 85", 17),
        ("bolt", "10 x 90", 17), ("bolt", "10 x 95 ", 16),("bolt", "10 x 100", 15), ("bolt", "10 x 105", 14), ("bolt", "10 x 110", 13),
        ("bolt", "10 x 115", 12), ("bolt", "10 x 120", 11),

        ("bolt", "12 x 20", 27), ("bolt", "12 x 25", 25), ("bolt", "12 x 30", 22),
        ("bolt", "12 x 35", 20), ("bolt", "12 x 40", 18), ("bolt", "12 x 45", 17),
        ("bolt", "12 x 50", 16), ("bolt", "12 x 55", 14), ("bolt", "12 x 60", 14),
        ("bolt", "12 x 65", 13), ("bolt", "12 x 70", 12), ("bolt", "12 x 75", 11),
        ("bolt", "12 x 80", 11), ("bolt", "12 x 85", 10), ("bolt", "12 x 90", 10),
        ("bolt", "12 x 95", 9), ("bolt", "12 x 100", 9), ("bolt", "12 x 105", 8),
        ("bolt", "12 x 110", 12), ("bolt", "12 x 120", 12),

        ("bolt", "14 x 10", 32), ("bolt", "14 x 20", 25), ("bolt", "14 x 30", 21),
        ("bolt", "14 x 40", 18), ("bolt", "14 x 50", 16), ("bolt", "14 x 60", 14),
        ("bolt", "14 x 70", 13), ("bolt", "14 x 80", 12), ("bolt", "14 x 90", 11),
        ("bolt", "14 x 100", 9),

        ("bolt", "16 x 10", 23), ("bolt", "16 x 20", 18), ("bolt", "16 x 30", 15),
        ("bolt", "16 x 40", 12), ("bolt", "16 x 50", 10), ("bolt", "16 x 60", 9),
        ("bolt", "16 x 70", 7), ("bolt", "16 x 80", 7), ("bolt", "16 x 90", 6),
        ("bolt", "16 x 100", 5),

        ("bolt", "18 x 10", 18), ("bolt", "18 x 20", 13), ("bolt", "18 x 30", 11),
        ("bolt", "18 x 40", 10), ("bolt", "18 x 50", 8), ("bolt", "18 x 60", 7),
        ("bolt", "18 x 70", 7), ("bolt", "18 x 80", 6), ("bolt", "18 x 90", 5),
        ("bolt", "18 x 100", 5),

        ("bolt", "20 x 10", 13), ("bolt", "20 x 20", 11), ("bolt", "20 x 30", 9),
        ("bolt", "20 x 40", 8), ("bolt", "20 x 50", 6), ("bolt", "20 x 60", 5),
        ("bolt", "20 x 70", 5), ("bolt", "20 x 80", 4), ("bolt", "20 x 90", 4),
        ("bolt", "20 x 100", 3),

        ("bolt", "22 x 10", 11), ("bolt", "22 x 20", 9), ("bolt", "22 x 30", 8),
        ("bolt", "22 x 40", 7), ("bolt", "22 x 50", 5), ("bolt", "22 x 60", 5),
        ("bolt", "22 x 70", 4), ("bolt", "22 x 80", 4), ("bolt", "22 x 90", 3),
        ("bolt", "22 x 100", 3),

        ("bolt", "24 x 10", 9), ("bolt", "24 x 20", 8), ("bolt", "24 x 30", 7),
        ("bolt", "24 x 40", 6), ("bolt", "24 x 50", 4), ("bolt", "24 x 60", 3),
        ("bolt", "24 x 70", 3), ("bolt", "24 x 80", 2), ("bolt", "24 x 90", 2),
        ("bolt", "24 x 100", 2),

        # Nuts - now in pieces per kg
        ("nut", "6mm", 380), ("nut", "8mm", 153), ("nut", "10mm", 167),
        ("nut", "12mm", 109), ("nut", "14mm", 80), ("nut", "16mm", 64),
        ("nut", "18mm", 55), ("nut", "20mm", 42), ("nut", "22mm", 33),
        ("nut", "24mm", 28),
    ]

    # Clear existing weights (optional)
    c.execute("DELETE FROM weights")

    for item in weights:
        product, size, pieces_per_kg = item
        c.execute("INSERT OR REPLACE INTO weights VALUES (?, ?, ?)", (product, size, pieces_per_kg))

    conn.commit()
    conn.close()

def open_calculator():
    init_weight_data()

    calc_win = tk.Tk()
    calc_win.title("Flange Product and Lock Nut")
    calc_win.geometry("460x420")
    calc_win.configure(bg="#f2f4f7")
    calc_win.resizable(False, False)

    def label(text, row):
        tk.Label(calc_win, text=text, bg="#f2f4f7", fg="#333", font=("Segoe UI", 11)).grid(row=row, column=0, padx=20, pady=10, sticky="w")

    type_var = tk.StringVar(value="Bolt")
    size_var = tk.StringVar(value=" ")
    qty_var = tk.DoubleVar()
    mode_var = tk.StringVar(value="count_to_kg")

    # Product type options
    product_types = ["Bolt", "Nut", "Washer"]
    current_product_index = 0

    label("Product Type:", 0)
    type_menu = tk.OptionMenu(calc_win, type_var, *product_types)
    type_menu.grid(row=0, column=1, pady=10, padx=5, sticky="w")

    label("Size :", 1)
    size_entry = tk.Entry(calc_win, textvariable=size_var, font=("Segoe UI", 11), bg="#fff", bd=0,
                          highlightthickness=1, relief="solid", width=25)
    size_entry.grid(row=1, column=1, pady=10)

    label("Quantity (pcs or kg):", 2)
    qty_entry = tk.Entry(calc_win, textvariable=qty_var, font=("Segoe UI", 11), bg="#fff", bd=0,
                         highlightthickness=1, relief="solid", width=25)
    qty_entry.grid(row=2, column=1, pady=10)

    label("Conversion Mode:", 3)
    pieces_to_kg_radio = tk.Radiobutton(calc_win, text="Pieces to KG", variable=mode_var, value="count_to_kg",
                                        bg="#f2f4f7", font=("Segoe UI", 10))
    pieces_to_kg_radio.grid(row=4, column=1, sticky="w", padx=5)
    
    kg_to_pieces_radio = tk.Radiobutton(calc_win, text="KG to Pieces", variable=mode_var, value="kg_to_count",
                                        bg="#f2f4f7", font=("Segoe UI", 10))
    kg_to_pieces_radio.grid(row=5, column=1, sticky="w", padx=5)

    result_label = tk.Label(calc_win, text="Result: ", bg="#f2f4f7", fg="#673AB7",
                            font=("Segoe UI", 12, "bold"))
    result_label.grid(row=6, column=0, columnspan=2, pady=30)

    def calculate(event=None):
        product_type = type_var.get().lower()
        size = size_var.get().strip().lower()
        qty = qty_var.get()
        mode = mode_var.get()

        if product_type == "bolt":
            if "x" not in size:
                messagebox.showerror("Error", "Bolt size must be like '6 x 20'")
                return
        else:
            if not size.endswith("mm"):
                messagebox.showerror("Error", "Nut/Washers size must be like '10mm'")
                return

        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT pieces_per_kg FROM weights WHERE product=? AND size=?", (product_type, size))
        result = c.fetchone()
        conn.close()

        if not result:
            result_label.config(text="❌ Size not found in database.")
            return

        pieces_per_kg = result[0]
        if mode == "count_to_kg":
            total_kg = qty / pieces_per_kg
            result_label.config(text=f"✅ {qty} pcs = {total_kg:.3f} kg")
        else:
            total_pieces = int(qty * pieces_per_kg)
            result_label.config(text=f"✅ {qty} kg ≈ {total_pieces} pcs")

    def handle_product_type_change(direction):
        nonlocal current_product_index
        if direction == "up":
            current_product_index = (current_product_index - 1) % len(product_types)
        else:  # down
            current_product_index = (current_product_index + 1) % len(product_types)
        type_var.set(product_types[current_product_index])

    def handle_mode_change():
        if mode_var.get() == "count_to_kg":
            mode_var.set("kg_to_count")
        else:
            mode_var.set("count_to_kg")

    def on_key_press(event):
        # Handle keyboard shortcuts
        if event.keysym == "Return":
            calculate()
        elif event.keysym == "Up":
            handle_product_type_change("up")
        elif event.keysym == "Down":
            handle_product_type_change("down")
        elif event.keysym == "Tab":
            handle_mode_change()
        elif event.keysym == "Escape":
            calc_win.quit()

    calc_btn = tk.Button(calc_win, text="Calculate", command=calculate,
                         bg="#673AB7", fg="white", font=("Segoe UI", 11, "bold"),
                         activebackground="#512DA8", relief="flat", padx=10, pady=6)
    calc_btn.grid(row=7, column=0, columnspan=2, pady=10)

    # Add keyboard shortcuts info
    shortcuts_label = tk.Label(calc_win, text="Shortcuts: Enter=Calculate | ↑↓=Product Type | Tab=Mode | Esc=Exit",
                               bg="#f2f4f7", fg="#666", font=("Segoe UI", 9))
    shortcuts_label.grid(row=8, column=0, columnspan=2, pady=5)

    # Bind keyboard events
    calc_win.bind("<Key>", on_key_press)
    calc_win.focus_set()  # Make sure window can receive key events

    # Also bind Enter key to entries for backward compatibility
    for widget in [size_entry, qty_entry]:
        widget.bind("<Return>", calculate)

    calc_win.mainloop()

if __name__ == "__main__":
    open_calculator()