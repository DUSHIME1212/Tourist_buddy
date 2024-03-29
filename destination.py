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

def search_by_category(category_id):
    cursor.execute('SELECT * FROM Destination WHERE category_id = %s', (category_id,))
    destinations = cursor.fetchall()
    if destinations:
        return destinations
    else:
        return "No Destination Found"
    

def search_by_query(query):
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
            return destinations
    else:
        return None
    
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

def convert_currency(amount, from_currency, to_currency, conversion_rates):
    if (from_currency, to_currency) in conversion_rates:
        rate = conversion_rates[(from_currency, to_currency)]
        converted_amount = amount * rate
        return converted_amount
    else:
        return None

