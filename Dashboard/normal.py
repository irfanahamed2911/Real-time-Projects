import tkinter as tk
from tkinter import messagebox, ttk
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime
import os
import webbrowser
import platform
import subprocess
from normal_db import (
    init_db, insert_invoice, insert_invoice_item,
    get_customer_by_name, save_customer_if_not_exists
)

init_db()

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("M.J.Traders N_B")
        self.root.geometry("950x600")
        self.root.configure(bg="#ffffff")

        self.cart = []
        self.last_invoice_path = None
        self.edit_index = None
        self.create_widgets()

        # Shortcut keys
        self.root.bind("<Control-Return>", lambda e: self.open_invoice_folder())
        self.root.bind("<Control-p>", lambda e: self.print_invoice())
        self.root.bind("<Control-P>", lambda e: self.print_invoice())
        self.root.bind("<Control-x>", lambda e: self.clear_cart())
        self.root.bind("<Delete>", lambda e: self.remove_selected_item())
        self.root.bind("<Control-i>", lambda e: self.generate_invoice())

    # ---------------------- GUI SETUP ----------------------
    def create_widgets(self):
        tk.Label(self.root, text="Customer Name:", bg="#ffffff").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.root, text="Address:", bg="#ffffff").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.root, text="Phone:", bg="#ffffff").grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.customer_name = tk.Entry(self.root, width=30)
        self.customer_address = tk.Entry(self.root, width=30)
        self.customer_phone = tk.Entry(self.root, width=30)

        self.customer_name.grid(row=0, column=1)
        self.customer_address.grid(row=1, column=1)
        self.customer_phone.grid(row=2, column=1)

        self.customer_name.bind("<FocusOut>", self.auto_fill_customer)

        tk.Label(self.root, text="Description:", bg="#ffffff").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        tk.Label(self.root, text="Quantity:", bg="#ffffff").grid(row=4, column=2, padx=10, pady=5, sticky="e")
        tk.Label(self.root, text="Rate:", bg="#ffffff").grid(row=4, column=4, padx=10, pady=5, sticky="e")

        self.desc = tk.Entry(self.root, width=25)
        self.qty = tk.Entry(self.root, width=10)
        self.rate = tk.Entry(self.root, width=10)

        self.desc.grid(row=4, column=1)
        self.qty.grid(row=4, column=3)
        self.rate.grid(row=4, column=5)

        self.rate.bind("<Return>", lambda e: self.add_to_cart())

        tk.Button(self.root, text="Add to Cart", command=self.add_to_cart,
                  bg="#1a73e8", fg="white").grid(row=4, column=6, padx=10)

        # Treeview for cart
        self.tree = ttk.Treeview(self.root, columns=("#1", "#2", "#3", "#4"), show="headings", height=10)
        self.tree.heading("#1", text="Description")
        self.tree.heading("#2", text="Quantity")
        self.tree.heading("#3", text="Rate")
        self.tree.heading("#4", text="Amount")
        self.tree.grid(row=5, column=0, columnspan=7, pady=10)

        # Buttons
        tk.Button(self.root, text="Edit Selected", command=self.edit_selected_item,
                  bg="#00bcd4", fg="white").grid(row=6, column=1)
        tk.Button(self.root, text="Update Item", command=self.update_item,
                  bg="#607d8b", fg="white").grid(row=6, column=0)
        tk.Button(self.root, text="Remove Selected", command=self.remove_selected_item,
                  bg="#ea4335", fg="white").grid(row=6, column=2)
        tk.Button(self.root, text="Clear Cart", command=self.clear_cart,
                  bg="#fbbc04", fg="black").grid(row=6, column=3)

        # Invoice control buttons
        tk.Button(self.root, text="Generate Invoice", command=self.generate_invoice,
                  bg="#1a73e8", fg="white").grid(row=8, column=3, pady=10)
        tk.Button(self.root, text="Open Invoice Folder", command=self.open_invoice_folder,
                  bg="#34a853", fg="white").grid(row=8, column=2, pady=10)
        tk.Button(self.root, text="Print Invoice", command=self.print_invoice,
                  bg="#673ab7", fg="white").grid(row=8, column=1, pady=10)

    # ---------------------- CUSTOMER HANDLING ----------------------
    def auto_fill_customer(self, event=None):
        name = self.customer_name.get().strip()
        if not name:
            return
        customer = get_customer_by_name(name)
        if customer:
            _, name, address, phone = customer
            self.customer_address.delete(0, tk.END)
            self.customer_phone.delete(0, tk.END)
            self.customer_address.insert(0, address)
            self.customer_phone.insert(0, phone)

    # ---------------------- CART OPERATIONS ----------------------
    def add_to_cart(self):
        desc = self.desc.get().strip()
        qty_text = self.qty.get().strip()
        rate_text = self.rate.get().strip()

        if not desc or not qty_text or not rate_text:
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            qty = float(qty_text)
            rate = float(rate_text)
        except ValueError:
            messagebox.showerror("Error", "Quantity and Rate must be numbers")
            return

        amount = qty * rate
        self.cart.append((desc, qty, rate, amount))
        self.tree.insert("", tk.END, values=(desc, f"{qty:.2f}", f"{rate:.2f}", f"{amount:.2f}"))
        self.clear_entry_fields()

    def edit_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Select an item to edit")
            return

        index = self.tree.index(selected[0])
        item = self.cart[index]

        self.edit_index = index
        self.desc.delete(0, tk.END)
        self.qty.delete(0, tk.END)
        self.rate.delete(0, tk.END)

        self.desc.insert(0, item[0])
        self.qty.insert(0, item[1])
        self.rate.insert(0, item[2])

    def update_item(self):
        if self.edit_index is None:
            messagebox.showwarning("Warning", "No item selected for update")
            return

        desc = self.desc.get().strip()
        qty_text = self.qty.get().strip()
        rate_text = self.rate.get().strip()

        try:
            qty = float(qty_text)
            rate = float(rate_text)
        except ValueError:
            messagebox.showerror("Error", "Quantity and Rate must be numbers")
            return

        amount = qty * rate
        self.cart[self.edit_index] = (desc, qty, rate, amount)

        # Refresh Treeview
        self.tree.delete(*self.tree.get_children())
        for item in self.cart:
            self.tree.insert("", tk.END, values=(item[0], f"{item[1]:.2f}", f"{item[2]:.2f}", f"{item[3]:.2f}"))

        self.edit_index = None
        self.clear_entry_fields()

    def remove_selected_item(self):
        selected = self.tree.selection()
        if not selected:
            return
        index = self.tree.index(selected[0])
        self.tree.delete(selected[0])
        del self.cart[index]

    def clear_cart(self):
        self.tree.delete(*self.tree.get_children())
        self.cart.clear()

    def clear_entry_fields(self):
        self.desc.delete(0, tk.END)
        self.qty.delete(0, tk.END)
        self.rate.delete(0, tk.END)

    # ---------------------- INVOICE GENERATION ----------------------
    def generate_invoice(self):
        if not self.cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        customer = [
            self.customer_name.get().strip(),
            self.customer_address.get().strip(),
            self.customer_phone.get().strip()
        ]

        save_customer_if_not_exists(*customer)

        date = datetime.now().strftime("%d-%m-%Y")
        subtotal = sum(item[3] for item in self.cart)
        total = subtotal

        invoice_id = insert_invoice(customer, date, date, 0, subtotal, 0, total)
        for item in self.cart:
            insert_invoice_item(invoice_id, item)

        self.last_invoice_path = self.generate_pdf(invoice_id, customer, date, subtotal, total)
        messagebox.showinfo("Success", "Invoice generated successfully!")
        self.clear_cart()

    def generate_pdf(self, invoice_id, customer, date, subtotal, total):
        safe_name = customer[0].strip().replace(" ", "_") or "Customer"
        folder = os.path.join("invoices", safe_name)
        os.makedirs(folder, exist_ok=True)
        filename = os.path.join(folder, f"invoice_{invoice_id}.pdf")

        c = canvas.Canvas(filename, pagesize=A4)
        width, height = A4

        # Header
        c.setFillColor(colors.HexColor("#15416b"))
        c.rect(0, height - 100, width, 100, fill=1)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 20)
        c.drawString(40, height - 60, "ESTIMATE")

        # Company info
        c.setFont("Helvetica-Bold", 16)
        c.drawRightString(width - 40, height - 20, "M J TRADERS")
        c.setFont("Helvetica", 11)
        c.drawRightString(width - 40, height - 35, "Dealers in all kinds of Bolts, Nuts and Washers")
        c.drawRightString(width - 40, height - 50, "No.10 Ellappan Naiken Street, Pudupet, Chennai-600002")
        c.drawRightString(width - 40, height - 65, "Phone: +91-9600159685 / +91-8778368148")
        c.drawRightString(width - 40, height - 80, "Email: mjtradersbnw@gmail.com")

        # Invoice details
        invoice_no = f"INV-{datetime.now().strftime('%Y%m%d')}-{str(invoice_id).zfill(6)}"
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(40, height - 130, f"Invoice No: {invoice_no}")
        c.drawString(40, height - 145, f"Date: {date}")
        c.drawString(40, height - 160, "NO RETURN")

        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(width - 40, height - 130, "Estimate To")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 40, height - 145, customer[0])
        c.drawRightString(width - 40, height - 160, customer[1])
        c.drawRightString(width - 40, height - 175, f"{customer[2]}")

        # Table Header
        c.setFillColor(colors.HexColor("#eeeeee"))
        c.rect(40, height - 220, width - 80, 20, fill=1)
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 10)
        headers = ["Item", "Description", "Qty", "Rate", "Amount"]
        x_positions = [50, 130, 330, 400, 480]
        for i, h in enumerate(headers):
            c.drawString(x_positions[i], height - 215, h)

        # Table Content
        y = height - 240
        c.setFont("Helvetica", 10)
        for idx, item in enumerate(self.cart, 1):
            c.drawString(50, y, str(idx))
            c.drawString(130, y, item[0])
            c.drawRightString(380, y, f"{item[1]:.2f}")
            c.drawRightString(460, y, f"Rs.{item[2]:.2f}")
            c.drawRightString(560, y, f"Rs.{item[3]:.2f}")
            y -= 20

        y -= 10
        c.setFont("Helvetica-Bold", 10)
        c.drawRightString(560, y, f"Total: Rs.{total:.2f}")

        # Footer
        c.setFillColor(colors.HexColor("#15416b"))
        c.rect(0, 0, width, 50, fill=True)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2, 15, "Thank you for your business!")
        c.setFont("Helvetica", 12)
        c.drawCentredString(width / 2, 35, "For any queries, please contact us at the above mentioned details.")

        c.save()
        return filename

    # ---------------------- FILE / PRINT HANDLERS ----------------------
    def open_invoice_folder(self):
        if self.last_invoice_path:
            webbrowser.open(os.path.dirname(self.last_invoice_path))

    def print_invoice(self):
        if not self.last_invoice_path:
            messagebox.showerror("Error", "No invoice to print")
            return
        if platform.system() == "Windows":
            os.startfile(self.last_invoice_path, "print")
        else:
            subprocess.run(["lp", self.last_invoice_path])


if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
