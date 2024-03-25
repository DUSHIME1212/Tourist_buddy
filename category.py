import mysql.connector

# Connect to MySQL database
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='destinations_db',
    auth_plugin='mysql_native_password'
)
class Category:
    def __init__(self, name):
        self.name = name

# Close the connection when done
def close_connection():
    conn.close()
