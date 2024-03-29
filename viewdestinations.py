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
    print('MSQL connection is closed')

#calling the explore function 
explore_destinations()
