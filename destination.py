import os
import textwrap
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

# Create Destination table if it doesn't exist
cursor.execute('''
CREATE TABLE IF NOT EXISTS Destination (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    background TEXT,
    operating_hours VARCHAR(100),
    exciting_facts TEXT,
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    rating FLOAT,
    key_nearby_places TEXT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES Category(id)
)
''')
conn.commit()

class Destination:
    def __init__(self, name, background, operating_hours, exciting_facts, latitude, longitude, rating, key_nearby_places, category_id):
        self.name = name
        self.background = background
        self.operating_hours = operating_hours
        self.exciting_facts = exciting_facts
        self.latitude = latitude
        self.longitude = longitude
        self.rating = rating
        self.key_nearby_places = key_nearby_places
        self.category_id = category_id

    def save_to_db(self):
        # Check if destination already exists based on name
        cursor.execute('SELECT id FROM Destination WHERE name = %s', (self.name,))
        existing_destination = cursor.fetchone()
        if existing_destination:
            print('\n' + Fore.LIGHTRED_EX + f"Destination already exists in the database.".center(120) + Style.RESET_ALL)
        else:
            cursor.execute('''
            INSERT INTO Destination 
            (name, background, operating_hours, exciting_facts, latitude, longitude, rating, key_nearby_places, category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.name, self.background, self.operating_hours, self.exciting_facts, self.latitude, self.longitude,
                self.rating, self.key_nearby_places, self.category_id))
            conn.commit()
            print('\n' + Fore.GREEN + f"{'Destination added successfully.'}".center(120) + Style.RESET_ALL)
    
    def update_destination_info(self):
        cursor.execute('''
            UPDATE Destination 
            SET background = %s, operating_hours = %s, exciting_facts = %s, latitude = %s, longitude = %s, rating = %s, key_nearby_places = %s, category_id = %s
            WHERE name = %s
        ''', (self.background, self.operating_hours, self.exciting_facts, self.latitude, self.longitude, self.rating, self.key_nearby_places, self.category_id, self.name))
        conn.commit()
        print('\n' + Fore.GREEN + f"{'Destination updated successfully.'}".center(120) + Style.RESET_ALL)

def rate_destination():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"RATE A DESTINATION BY CATEGORY".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)


    name = input('\n' + ' ' * 10 + "Enter destination name: ").center(20)
    rating = float(input('\n' + ' ' * 10 + "Enter rating (0-5): ").center(20))
    if rating < 0 or rating > 5:
        print('\n' + Fore.LIGHTRED_EX + f"{'Rating must be between 0 and 5.'}".center(120) + Style.RESET_ALL)
        return
    cursor.execute('SELECT id FROM Destination WHERE name = %s', (name,))
    existing_destination = cursor.fetchone()
    if not existing_destination:
        print('\n' + Fore.LIGHTRED_EX + f"{'Destination does not exist in the database.'}".center(120) + Style.RESET_ALL)
    else:
        cursor.execute('''
        UPDATE Destination
        SET rating = %s
        WHERE name = %s
        ''', (rating, name))
        conn.commit()
        print('\n' + Fore.GREEN + f"{'Destination rated successfully. Thank you for your feedback!'}".center(120) + Style.RESET_ALL)

def add_destination():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"ADD DESTINATION".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    name = input('\n' + ' ' * 10 + "Enter destination name: ".center(20))
    background = input('\n' + ' ' * 10 + "Enter description/background: ".center(20))
    operating_hours = input('\n' + ' ' * 10 + "Enter operating hours: ".center(20))
    exciting_facts = input('\n' + ' ' * 10 + "Enter exciting facts: ".center(20))
    location = input('\n' + ' ' * 10 + "Enter destination coordinates (latitude, longitude):".center(20))
    key_nearby_places = input('\n' + ' ' * 10 + "Enter key nearby places (hotel, restaurants, hospitals): ".center(20))
    category_id = int(input('\n' + ' ' * 10 + "Enter category ID: ".center(20)))
    # separate latitude and longitude
    location = location.split(',')
    latitude = location[0].strip()
    longitude = location[1].strip()

    new_destination = Destination(name, background, operating_hours, exciting_facts, latitude, longitude, 0, key_nearby_places, category_id)
    new_destination.save_to_db()

def search_by_category():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"FILTER DESTINATION BY CATEGORY".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    category_name = input('\n' + ' ' * 10 + "Enter category name to filter destinations: ".center(20))
    cursor.execute('''
    SELECT Destination.*
    FROM Destination JOIN Category
    ON Destination.category_id = Category.id
    WHERE Category.name = %s
    ''', (category_name,))
    results = cursor.fetchall()
    if results:
        print('\n' + f"DESTINATIONS in CATEGORY '{category_name}'".center(120) + '\n')
        for dest in results:
            print('\n' + f"{'=' * 100}".center(120))
            print(Fore.BLUE + f"Destination {dest[0]}. {dest[1]}\n".center(120) + Style.RESET_ALL)
            print(f"Category: {dest[9]}".center(120))
            print(f"Operating Hours: {dest[3]}".center(120))
            print(f"Location (lat, long): ({dest[5]}, {dest[6]})".center(120))
            print(f"Rating: {dest[7]}/5".center(120))
            print(f"Exciting Facts:\n".center(120))
            print(f"-> {dest[4]}".center(120))
            print(f"Key Nearby Places\n".center(120))
            print(f"-> {dest[8]}".center(120))
            print(f"Description\n".center(120))
            description_lines = textwrap.wrap(dest[2], width=100)
            for line in description_lines:
                print(line.center(120))
                print(f"{'=' * 100}".center(120))
    else:
        print('\n' + Fore.LIGHTRED_EX + f"NO DESTINATION FOUND IN CATEGORY '{category_name}'".center(120) + Style.RESET_ALL)

def search_by_query():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"SEARCH DESTINATION BY KEYWORD".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    query  = input('\n' + ' ' * 10 + "Enter keywords related to your destination: ".center(20))
    search_query = f"%{query}%"
    cursor.execute('''
        SELECT * FROM Destination 
        WHERE name LIKE %s 
        OR background LIKE %s 
        OR operating_hours LIKE %s 
        OR exciting_facts LIKE %s 
        OR key_nearby_places LIKE %s
    ''', (search_query, search_query, search_query, search_query, search_query))
    destinations = cursor.fetchall()
    if destinations:
        for destination in destinations:
            print('\n' + f"{'=' * 100}".center(120))
            print(Fore.BLUE + f"Destination {destination[0]}. {destination[1]}\n".center(120) + Style.RESET_ALL)
            print(f"Category: {destination[9]}".center(120))
            print(f"Operating Hours: {destination[3]}".center(120))
            print(f"Location (lat, long): ({destination[5]}, {destination[6]})".center(120))
            print(f"Rating: {destination[7]}/5".center(120))
            print(f"Exciting Facts:\n".center(120))
            print(f"-> {destination[4]}".center(120))
            print(f"Key Nearby Places\n".center(120))
            print(f"-> {destination[8]}".center(120))
            print(f"Description\n".center(120))
            description_lines = textwrap.wrap(destination[2], width=100)
            for line in description_lines:
                print(line.center(120))
                print(f"{'=' * 100}".center(120))
    else:
        print('\n' + Fore.LIGHTRED_EX + f"{'RESULT NOT FOUND'}".center(120) + Style.RESET_ALL)
    
# Close the connection when done
def close_connection():
    conn.close()

# Destination information dictionary
destinations = {}

def update_destination():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"UPDATE DESTINATION".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    name = input('\n' + ' ' * 10 + "Enter destination name: ".center(20))
    background = input('\n' + ' ' * 10 + "Enter description/background: ".center(20))
    operating_hours = input('\n' + ' ' * 10 + "Enter operating hours: ".center(20))
    exciting_facts = input('\n' + ' ' * 10 + "Enter exciting facts: ".center(20))
    location = input('\n' + ' ' * 10 + "Enter destination coordinates (latitude, longitude):".center(20))
    key_nearby_places = input('\n' + ' ' * 10 + "Enter key nearby places (hotel, restaurants, hospitals): ".center(20))
    category_id = int(input('\n' + ' ' * 10 + "Enter category ID: ".center(20)))
    # separate latitude and longitude
    location = location.split(',')
    latitude = location[0].strip()
    longitude = location[1].strip()

    new_destination = Destination(name, background, operating_hours, exciting_facts, latitude, longitude, 0, key_nearby_places, category_id)
    new_destination.update_destination_info()


def highly_recommended():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"HIGHLY RECOMMENDED PLACES".center(120) + Style.RESET_ALL)
    
    # Execute the SQL query
    query = "SELECT * FROM Destination WHERE rating = (SELECT MAX(rating) FROM Destination)"
    cursor.execute(query)
    
    # Fetch all the rows
    result = cursor.fetchall()
    
    # Print the result
    for row in result:
        print('\n' + f"{'=' * 100}".center(120))
        print(Fore.BLUE + f"Destination {row[0]}. {row[1]}\n".center(120) + Style.RESET_ALL)
        print(f"Category: {row[9]}".center(120))
        print(f"Operating Hours: {row[3]}".center(120))
        print(f"Location (lat, long): ({row[5]}, {row[6]})".center(120))
        print(f"Rating: {row[7]}/5".center(120))
        print(f"Exciting Facts:\n".center(120))
        print(f"-> {row[4]}".center(120))
        print(f"Key Nearby Places\n".center(120))
        print(f"-> {row[8]}".center(120))
        print(f"Description\n".center(120))
        description_lines = textwrap.wrap(row[2], width=100)
        for line in description_lines:
            print(line.center(120))
            print(f"{'=' * 100}".center(120))
