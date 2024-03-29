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
            print('Location:', destination[2])
            print('Description:', destination[3])
            print('------------------------------')

    #close the cursor and the connection
    cursor.close()
    connection.close()
