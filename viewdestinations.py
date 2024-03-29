import mysql.connector

def explore_destinations():
    #connecting my database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='destinations_db',
        auth_plugin='mysql_native_password'
    )
    cursor = connection.cursor()

    cursor.execute('SELECT COUNT(*) FROM Destination')
    num_destinations = cursor.fetchone()[0]

    if num_destinations == 0:
        print("There are no destinations available. Please consider adding some.")
    else:
        #execute the select query 
        cursor.execute("SELECT * FROM Destination")

        #fetch all rows
        destinations = cursor.fetchall()
        #printing details for the available destinations
        for destination in destinations:
            print('Destination Id:', destination[0])
            print('Name:', destination[1])
            print('Description:', destination[2])
            print('Operating Hours:', destination[3])
            print('Exciting Facts:', destination[4])
            print('Location (lat, lon): (', destination[5], ',', destination[6], ')')
            print('Rating:', destination[7])
            print('Key Nearby Places:', destination[8])
            print('Category Id:', destination[9])
            print('------------------------------')

    #close the cursor and the connection
    cursor.close()
    connection.close()
