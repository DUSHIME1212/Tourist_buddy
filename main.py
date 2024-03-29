from category import Category, close_connection as close_category_conn, add_category, get_categories
from destination import Destination, close_connection as close_destination_conn, cursor, add_destination
from viewdestinations import explore_destinations
from main import destination



def search_destination():
    # Select query for searching destination by name
    print("Searching destination...")

def filter_by_category():
    # Select query for filtering destination by category
    print("Filtering destination by category...")


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
