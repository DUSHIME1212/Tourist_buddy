import os
from colorama import Fore, Style
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

def add_category():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"ADD CATEGORY".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)
    
    name = input('\n' + ' ' * 10 + "Enter category name: ".center(20))
    new_category = Category(name)
    new_category.save_to_db()

def get_categories():
    os.system('cls' if os.name == 'nt' else 'clear')

    cursor.execute('SELECT COUNT(*) FROM Category')
    num_categories = cursor.fetchone()[0]

    if num_categories == 0:
        print('\n' + Fore.LIGHTRED_EX + f"{'There are no categories available. Please consider adding some.'}".center(120) + Style.RESET_ALL)
    else:
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        
        print('\n' + ' ' * 10 + '=' * 100)
        print(Fore.BLUE + f"AVAILABLE CATEGORIES".center(120) + Style.RESET_ALL+ '\n')

        for cat in categories:
            print(' ' * 50 + f"Category {cat[0]}. {cat[1]}")

# Close the connection when done
def close_connection():
    conn.close()
