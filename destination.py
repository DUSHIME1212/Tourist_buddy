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
            print("Destination already exists in the database.")
        else:
            cursor.execute('''
            INSERT INTO Destination 
            (name, background, operating_hours, exciting_facts, latitude, longitude, rating, key_nearby_places, category_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (self.name, self.background, self.operating_hours, self.exciting_facts, self.latitude, self.longitude,
                self.rating, self.key_nearby_places, self.category_id))
            conn.commit()
            print("Destination added successfully.")
    
    def update_destination_info(self):
        cursor.execute('''
            UPDATE Destination 
            SET background = %s, operating_hours = %s, exciting_facts = %s, latitude = %s, longitude = %s, rating = %s, key_nearby_places = %s, category_id = %s
            WHERE name = %s
        ''', (self.background, self.operating_hours, self.exciting_facts, self.latitude, self.longitude, self.rating, self.key_nearby_places, self.category_id, self.name))
        conn.commit()
        print("Destination updated successfully.")

def rate_destination():
    name = input("Enter destination name: ")
    rating = float(input("Enter rating (0-5): "))
    if rating < 0 or rating > 5:
        print("Rating must be between 0 and 5.")
        return
    cursor.execute('SELECT id FROM Destination WHERE name = %s', (name,))
    existing_destination = cursor.fetchone()
    if not existing_destination:
        print("Destination does not exist in the database.")
    else:
        cursor.execute('''
        UPDATE Destination
        SET rating = %s
        WHERE name = %s
        ''', (rating, name))
        conn.commit()
        print("Destination rated successfully. Thank you for your feedback!")

def add_destination():
    name = input("Enter destination name: ")
    background = input("Enter description/background: ")
    operating_hours = input("Enter operating hours: ")
    exciting_facts = input("Enter exciting facts: ")
    location = input("Enter destination coordinates (latitude, longitude):")
    key_nearby_places = input("Enter key nearby places (hotel, restaurants, hospitals): ")
    category_id = int(input("Enter category ID: "))
    # separate latitude and longitude
    location = location.split(',')
    latitude = location[0].strip()
    longitude = location[1].strip()

    new_destination = Destination(name, background, operating_hours, exciting_facts, latitude, longitude, 0, key_nearby_places, category_id)
    new_destination.save_to_db()

def search_by_category():
    category_name = input("Enter category name to filter destinations: ")
    cursor.execute('''
    SELECT Destination.*
    FROM Destination JOIN Category
    ON Destination.category_id = Category.id
    WHERE Category.name = %s
    ''', (category_name,))
    results = cursor.fetchall()
    if results:
        print(f"Destinations in Category '{category_name}':")
        for dest in results:
            print(dest)
    else:
        print(f"No destinations found in Category '{category_name}'.")
    

def search_by_query():
    query  = input("Search anything relating to your destination: ")
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
        print(destinations)
    else:
        print("Result not found")
    
# Close the connection when done
def close_connection():
    conn.close()

# Destination information dictionary
destinations = {}

def update_destination():
    name = input("Enter destination name: ")
    background = input("Enter description/background: ")
    operating_hours = input("Enter operating hours: ")
    exciting_facts = input("Enter exciting facts: ")
    location = input("Enter destination coordinates (latitude, longitude):")
    key_nearby_places = input("Enter key nearby places (hotel, restaurants, hospitals): ")
    category_id = int(input("Enter category ID: "))
    # separate latitude and longitude
    location = location.split(',')
    latitude = location[0].strip()
    longitude = location[1].strip()

    new_destination = Destination(name, background, operating_hours, exciting_facts, latitude, longitude, 0, key_nearby_places, category_id)
    new_destination.update_destination_info()


def highly_recommended():
    # Execute the SQL query
    query = "SELECT * FROM Destination WHERE rating = (SELECT MAX(rating) FROM Destination)"
    cursor.execute(query)
    
    # Fetch all the rows
    result = cursor.fetchall()
    
    # Print the result
    for row in result:
        print(row)

        
