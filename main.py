from category import Category, close_connection as close_category_conn
from destination import Destination, close_connection as close_destination_conn, cursor
from viewdestinations import explore_destinations


def search_destination():
    # Select query for searching destination by name
    print("Searching destination...")

def filter_by_category():
    # Select query for filtering destination by category
    print("Filtering destination by category...")

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

    
def add_category():
    name = input("Enter category name: ")
    new_category = Category(name)
    new_category.save_to_db()

def get_categories():
    cursor.execute('SELECT COUNT(*) FROM Category')
    num_categories = cursor.fetchone()[0]

    if num_categories == 0:
        print("There are no categories available. Please consider adding some.")
    else:
        cursor.execute('SELECT * FROM Category')
        categories = cursor.fetchall()
        print("Available Categories:")
        for cat in categories:
            print(cat)

def get_recommended_places():
    # Select query for getting recommended places
    print("Getting recommended places...")

# Function to calculate destination time
def dest_time(start_time, add_hours, add_minutes, day_index):
    # Define constants
    days_in_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Parsing start time and converting hours to 24-hour format
    time, meridian = start_time.split()
    hours, minutes = map(int, time.split(':'))
    if meridian == 'PM' and hours != 12:
        hours += 12

    # Converting the duration into hours
    duration_minutes_hours = (add_minutes / 60) + add_hours
    total_time_24format_decimal = hours + duration_minutes_hours
    total_time_24format_int = int(total_time_24format_decimal)
    number_of_days = (total_time_24format_decimal - total_time_24format_int) > 0

    if number_of_days:
        total_time_24format_int += 1
        total_time_24format_decimal = total_time_24format_decimal - 1

    # Converting to 12-hour format and finding the meridian
    total_time_12format_hours = total_time_24format_int % 12
    if total_time_12format_hours == 0:
        total_time_12format_hours = 12
    meridian = 'AM' if total_time_12format_hours < 12 else 'PM'
    total_time_12format_minutes = int(total_time_24format_decimal * 60) % 60

    # Building the new time string
    total_hour_12format = '{:02d}'.format(total_time_12format_hours)
    totaltime_minutes = '{:02d}'.format(total_time_12format_minutes)
    dayoftheweek = days_in_week[day_index % 7]
    new_time = ' '.join([total_hour_12format, totaltime_minutes, meridian])

    if number_of_days and dayoftheweek is not None:
        new_time += f' (next day)'
    elif number_of_days:
        new_time += f' ({number_of_days} days later)'
    elif dayoftheweek is not None:
        new_time += f', {dayoftheweek}'

    return new_time

def arrival_time():
    start_time = input("Enter start time (HH:MM AM/PM): ")
    add_hours = int(input("Enter duration hours: "))
    add_minutes = int(input("Enter duration minutes: "))
    day_index = int(input("Enter the day index (1-7): "))

    dest_time(start_time, add_hours, add_minutes, day_index)

def calculate_distance():
    # Select query for calculating distance from current location
    print("Calculating distance from current location...")

def main_menu():
    while True:
        print("\n--- WELCOME TO TOURIST BUDDY ---")
        print("1. Explore Available Destinations")
        print("2. Search Destination Name")
        print("3. Filter Destination By Category")
        print("4. Add New Attractions")
        print("5. Add New Category")
        print("6. Get Available Categories")
        print("7. Get Recommended Places")
        print("8. Distance From Current Location")
        print("9. Find Arrival Time")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            explore_destinations()
        elif choice == '2':
            search_destination()
        elif choice == '3':
            filter_by_category()
        elif choice == '4':
            add_destination()
        elif choice == '5':
            add_category()
        elif choice == '6':
            get_categories()
        elif choice == '7':
            get_recommended_places()
        elif choice == '8':
            calculate_distance()
        elif choice == '9':
            arrival_time()
        elif choice == '10':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
    close_category_conn()
    close_destination_conn()
