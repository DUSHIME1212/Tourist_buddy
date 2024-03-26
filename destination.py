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
