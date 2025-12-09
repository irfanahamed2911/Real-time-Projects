import sqlite3

DB_NAME = "bolts_nuts.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        address TEXT,
        phone TEXT,
        gst_number TEXT
    )""")
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        date TEXT,
        due_date TEXT,
        tax_rate REAL,
        subtotal REAL,
        tax REAL,
        total REAL
    )""")

    cur.execute("""
    CREATE TABLE IF NOT EXISTS invoice_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_id INTEGER,
        description TEXT,
        quantity REAL,
        rate REAL,
        amount REAL,
        FOREIGN KEY(invoice_id) REFERENCES invoices(id)
    )""")
    conn.commit()
    conn.close()

def get_customer_by_name(name):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE name=?", (name,))
    customer = cur.fetchone()
    conn.close()
    return customer

def save_customer_if_not_exists(name, address, phone, gst_number):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers WHERE name=?", (name,))
    if not cur.fetchone():
        cur.execute("INSERT INTO customers (name, address, phone, gst_number) VALUES (?, ?, ?, ?)", 
                    (name, address, phone, gst_number))
    conn.commit()
    conn.close()

def insert_invoice(customer, date, due_date, tax_rate, subtotal, tax, total):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO invoices (customer_name, date, due_date, tax_rate, subtotal, tax, total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (customer[0], date, due_date, tax_rate, subtotal, tax, total))
    invoice_id = cur.lastrowid
    conn.commit()
    conn.close()
    return invoice_id

def insert_invoice_item(invoice_id, item):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO invoice_items (invoice_id, description, quantity, rate, amount)
        VALUES (?, ?, ?, ?, ?)
    """, (invoice_id, item[0], item[1], item[2], item[3]))
    conn.commit()
    conn.close()
