import os
import textwrap
from colorama import Fore, Style
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
    os.system('cls' if os.name == 'nt' else 'clear')


    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"ALL AVAILABLE DESTINATION".center(120) + Style.RESET_ALL)

    if num_destinations == 0:
        print('\n' + f"{'=' * 100}".center(120))
        print(f"There are no destinations available. Please consider adding some.".center(120))
        print(f"{'=' * 100}".center(120))

    else:
        #execute the select query 
        cursor.execute("SELECT * FROM Destination")

        #fetch all rows
        destinations = cursor.fetchall()
        #printing details for the available destinations
        
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
            
    #close the cursor and the connection
    cursor.close()
    connection.close()
