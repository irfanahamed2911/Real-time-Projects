import sqlite3

DB_NAME = "flange_stock.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Create bolts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bolts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            size TEXT,
            unit TEXT NOT NULL,
            price REAL,
            grade TEXT,
            thread TEXT NOT NULL,
            place TEXT
        )
    ''')

    # Create nuts table
    c.execute('''
        CREATE TABLE IF NOT EXISTS nuts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            size TEXT,
            unit TEXT NOT NULL,
            price REAL,
            grade TEXT,
            thread TEXT NOT NULL,
            place TEXT
        )
    ''')

    conn.commit()
    conn.close()

def get_table(type_):
    type_ = type_.lower()
    if type_ == "bolt":
        return "bolts"
    elif type_ == "nut":
        return "nuts"
    else:
        raise ValueError("Invalid type")

def add_product(name, type_, size, unit, price, grade, thread, place):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = get_table(type_)
    c.execute(f'''
        INSERT INTO {table} (name, type, size, unit, price, grade, thread, place)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (name, type_, size, unit, price, grade, thread, place))
    conn.commit()
    conn.close()

def get_products_by_type(type_):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = get_table(type_)
    c.execute(f"SELECT * FROM {table}")
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_products():
    return (
        get_products_by_type("bolt") +
        get_products_by_type("nut")
    )

def update_product(id_, name, type_, size, unit, price, grade, thread, place):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = get_table(type_)
    c.execute(f'''
        UPDATE {table}
        SET name=?, type=?, size=?, unit=?, price=?, grade=?, thread=?, place=?
        WHERE id=?
    ''', (name, type_, size, unit, price, grade, thread, place, id_))
    conn.commit()
    conn.close()

def delete_product(id_, type_):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    table = get_table(type_)
    c.execute(f"DELETE FROM {table} WHERE id=?", (id_,))
    conn.commit()
    conn.close()
