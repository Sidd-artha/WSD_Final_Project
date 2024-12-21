import sqlite3
import json

def setup_database():
    connection = sqlite3.connect('db.sqlite')
    cursor = connection.cursor()

    # Remove existing tables if present
    cursor.execute('DROP TABLE IF EXISTS orders')
    cursor.execute('DROP TABLE IF EXISTS items')
    cursor.execute('DROP TABLE IF EXISTS customers')

    # Create customers table
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            UNIQUE (name, phone)
        )
    ''')

    # Create items table
    cursor.execute('''
        CREATE TABLE items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price REAL NOT NULL
        )
    ''')

    # Create orders table
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            notes TEXT,
            timestamp INTEGER NOT NULL,
            FOREIGN KEY (customer_id) REFERENCES customers(id),
            FOREIGN KEY (item_id) REFERENCES items(id)
        )
    ''')

    connection.commit()

    # Load orders data from JSON file
    with open('example_orders.json', 'r') as file:
        orders = json.load(file)

    # Insert data into tables
    for order in orders:
        cursor.execute('''
            INSERT OR IGNORE INTO customers (name, phone)
            VALUES (?, ?)
        ''', (order['name'], order['phone']))

        # Fetch the ID of the inserted or existing customer
        cursor.execute('''
            SELECT id FROM customers WHERE name = ? AND phone = ?
        ''', (order['name'], order['phone']))
        customer_id = cursor.fetchone()[0]

        for item in order['items']:
            cursor.execute('''
                INSERT OR IGNORE INTO items (name, price)
                VALUES (?, ?)
            ''', (item['name'], item['price']))

            # Fetch the ID of the inserted or existing item
            cursor.execute('''
                SELECT id FROM items WHERE name = ? AND price = ?
            ''', (item['name'], item['price']))
            item_id = cursor.fetchone()[0]

            # Insert into orders table
            cursor.execute('''
                INSERT INTO orders (customer_id, item_id, notes, timestamp)
                VALUES (?, ?, ?, ?)
            ''', (customer_id, item_id, order.get('notes', None), order['timestamp']))

    connection.commit()
    connection.close()

    print("Database setup and data insertion completed.")

if __name__ == "__main__":
    setup_database()
