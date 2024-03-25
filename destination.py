import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='destinations_db',
    auth_plugin='mysql_native_password'
)

class Destination:
    def __init__(self, name, historical_background, operating_hours, exciting_facts, location, rating, key_nearby_places, category_id):
        self.name = name
        self.historical_background = historical_background
        self.operating_hours = operating_hours
        self.exciting_facts = exciting_facts
        self.location = location
        self.rating = rating
        self.key_nearby_places = key_nearby_places
        self.category_id = category_id

# Close the connection when done
def close_connection():
    conn.close()
