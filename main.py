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
    # Insert query for adding new destination
    print("Adding new destination...")

def add_category():
    # Insert query for adding new category
    print("Adding new category...")

def get_categories():
    # Select query for getting available categories
    print("Getting available categories...")

def get_recommended_places():
    # Select query for getting recommended places
    print("Getting recommended places...")

def calculate_distance():
    # Select query for calculating distance between destinations
    print("Calculating distance between destinations...")

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
        print("8. Calculate Destination Distance")
        print("9. Exit")

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
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
    close_category_conn()
    close_destination_conn()
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

# Example usage
start_time = '2:00 PM'
add_hours = 0
add_minutes = 45
day_index = 0

print(dest_time(start_time, add_hours, add_minutes, day_index))
