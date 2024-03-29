import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    database='destination_db',
)
cursor = conn.cursor()

# Create Category table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE
)
''')
conn.commit()

class Category:
    def __init__(self, name):
        self.name = name

    def save_to_db(self):
        cursor.execute('INSERT INTO Category (name) VALUES (%s)', (self.name,))
        conn.commit()

def add_category():
    name = input("Enter category name: ")
    new_category = Category(name)
    new_category.save_to_db()

def get_categories():
    cursor.execute('SELECT COUNT(*) FROM Category')
    num_categories = cursor.fetchone()[0]

    if num_categories == 0:
        print("There are no categories available. Please consider adding some.")
    else:
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        print("Available Categories:")
        for cat in categories:
            print(cat)
                
# Close the connection when done
def close_connection():
    conn.close()
