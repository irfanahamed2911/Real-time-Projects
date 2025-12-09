import sqlite3
import os

DB_NAME = "normal_invoice.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        address TEXT,
        phone TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER,
        date TEXT,
        due_date TEXT,
        tax_rate REAL,
        subtotal REAL,
        tax REAL,
        total REAL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        description TEXT,
        quantity REAL,
        rate REAL,
        amount REAL
    )""")
    conn.commit()
    conn.close()

def get_customer_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM customers WHERE name = ?", (name,))
    customer = c.fetchone()
    conn.close()
    return customer

def save_customer_if_not_exists(name, address, phone):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM customers WHERE name = ?", (name,))
    if not c.fetchone():
        c.execute("INSERT INTO customers (name, address, phone) VALUES (?, ?, ?)", (name, address, phone))
    conn.commit()
    conn.close()

def insert_invoice(customer, date, due_date, tax_rate, subtotal, tax, total):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id FROM customers WHERE name = ?", (customer[0],))
    customer_id = c.fetchone()[0]
    c.execute("INSERT INTO invoices (customer_id, date, due_date, tax_rate, subtotal, tax, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (customer_id, date, due_date, tax_rate, subtotal, tax, total))
    invoice_id = c.lastrowid
    conn.commit()
    conn.close()
    return invoice_id

def insert_invoice_item(invoice_id, item):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    desc, qty, rate, amount = item
    c.execute("INSERT INTO invoice_items (invoice_id, description, quantity, rate, amount) VALUES (?, ?, ?, ?, ?)",
              (invoice_id, desc, qty, rate, amount))
    conn.commit()
    conn.close()
