import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='destinations_db',
    auth_plugin='mysql_native_password'
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

# Close the connection when done
def close_connection():
    conn.close()
