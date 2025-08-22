import webview
import sqlite3

DB_FILE = 'products.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS products (
            name TEXT PRIMARY KEY,
            quantity INTEGER,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

class API:
    def get_inventory(self):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT name, quantity, price FROM products")
        rows = c.fetchall()
        conn.close()
        return [{"name": r[0], "quantity": r[1], "price": r[2]} for r in rows]

    def add_or_update_product(self, data):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
            INSERT INTO products (name, quantity, price)
            VALUES (?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                quantity=excluded.quantity,
                price=excluded.price
        """, (data['name'], int(data['quantity']), float(data['price'])))
        conn.commit()
        conn.close()

    def delete_product(self, name):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("DELETE FROM products WHERE name=?", (name,))
        conn.commit()
        conn.close()

if __name__ == '__main__':
    init_db()
    api = API()
    window = webview.create_window("Inventory Manager", "index.html", js_api=api, width=1000, height=700)
    webview.start()

