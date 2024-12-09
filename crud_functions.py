import sqlite3

connection = sqlite3.connect('database14_4.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products
    (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    );
    """)
initiate_db()

# for i in range(1,5):
#     cursor.execute(f"INSERT INTO Products (title, description, price) VALUES(?, ?, ?)", (f'Product {i}', f'Описание {i}', f'{i*100}'))

def get_all_products():
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    return products

connection.commit()
# connection.close()