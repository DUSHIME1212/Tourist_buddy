import math
import os
from colorama import init, Fore, Style
from category import close_connection as close_category_conn, add_category, get_categories
from destination import close_connection as close_destination_conn, cursor, add_destination, update_destination,search_by_category, search_by_query, highly_recommended, rate_destination
from viewdestinations import explore_destinations

# Initialize colorama
init(autoreset=True)

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

    # Determine if the time exceeds 24 hours
    if total_time_24format_decimal >= 24:
        number_of_days = int(total_time_24format_decimal // 24)
        total_time_24format_decimal %= 24
    else:
        number_of_days = 0

    # Converting to 12-hour format and finding the meridian
    total_time_12format_hours = int(total_time_24format_decimal)
    total_time_12format_minutes = int((total_time_24format_decimal - total_time_12format_hours) * 60)
    if total_time_12format_hours == 0:
        total_time_12format_hours = 12
    meridian = 'AM' if total_time_12format_hours < 12 else 'PM'
    
    # Building the new time string
    total_hour_12format = '{:02d}'.format(total_time_12format_hours)
    totaltime_minutes = '{:02d}'.format(total_time_12format_minutes)
    dayoftheweek = days_in_week[(day_index - 1) % 7]
    new_time = ' '.join([total_hour_12format, totaltime_minutes, meridian])

    if number_of_days == 1 and dayoftheweek is not None:
        new_time += f' (next day)'
    elif number_of_days > 1:
        new_time += f' ({number_of_days} days later)'
    elif dayoftheweek is not None:
        new_time += f', {dayoftheweek}'

    return new_time

def arrival_time():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"ARRIVAL TIME".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    start_time = input('\n' + ' ' * 10 + "Enter start time (HH:MM AM/PM): ".center(20))
    add_hours = int(input('\n' + ' ' * 10 + "Enter duration hours: ").center(20))
    add_minutes = int(input('\n' + ' ' * 10 + "Enter duration minutes: ").center(20))
    day_index = int(input('\n' + ' ' * 10 + "Enter the day index (1-7): "))

    result = dest_time(start_time, add_hours, add_minutes, day_index)
    print('\n' + Fore.GREEN + f"Arrival Time: {result}".center(120) + Style.RESET_ALL)

def calculate_distance(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(float(lat1))
    lon1_rad = math.radians(float(lon1))
    lat2_rad = math.radians(float(lat2))
    lon2_rad = math.radians(float(lon2))

    # Haversine formula
    d_lat = lat2_rad - lat1_rad
    d_lon = lon2_rad - lon1_rad
    a = math.sin(d_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(d_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Radius of Earth in kilometers
    radius_earth_km = 6371.0

    # Calculate distance
    distance_km = radius_earth_km * c
    return distance_km

def distance_from_origin():

    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"DISTANCE FROM ORIGIN".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    destination_name = input('\n' + ' ' * 10 + "Enter your destination: ".center(20))
    user_lat = float(input('\n' + ' ' * 10 + "Enter your current latitude: ".center(20)))
    user_lon = float(input('\n' + ' ' * 10 + "Enter your current longitude: ".center(20)))

    cursor.execute('SELECT latitude, longitude FROM Destination WHERE name = %s', (destination_name,))
    destination_coords = cursor.fetchone()
    if destination_coords is None:
        print('\n' + Fore.LIGHTRED_EX + f"{'DESTINATION NOT FOUND'}".center(120) + Style.RESET_ALL)
        return
    else:
        dest_lat, dest_lon = destination_coords
        distance = calculate_distance(user_lat, user_lon, dest_lat, dest_lon)
        print('\n' + Fore.GREEN + f"Distance to destination: {distance} kilometers".center(120) + Style.RESET_ALL)

def currency_conversion():
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n' + ' ' * 10 + '=' * 100)
    print(Fore.BLUE + f"CURRENCY CONVERSION".center(120) + Style.RESET_ALL)
    print(' ' * 10 + '=' * 100)

    conversion_rates = {
        ('USD', 'EUR'): 0.94,
        ('EUR', 'USD'): 1.06,
        ('RWF', 'USD'): 0.00077,
        ('USD', 'RWF'): 1294,
        ('USD', 'KES'): 132,
        ('KES', 'USD'): 0.0076,
        ('USD', 'UGX'): 3833,
        ('UGX', 'USD'): 0.00026,
    }

    amount_to_convert = float(input('\n' + ' ' * 10 + "Enter the amount to convert: ".center(20)))
    from_currency = input('\n' + ' ' * 10 + "Enter the current currency (e.g., USD, EUR, RWF, KES, UGX): ".center(20)).upper()
    to_currency = input('\n' + ' ' * 10 + "Enter the desired currency (e.g., USD, EUR, RWF, KES, UGX): ".center(20)).upper()

    converted_amount = convert_currency(amount_to_convert, from_currency, to_currency, conversion_rates)
    if converted_amount is not None:
        print('\n' + Fore.GREEN + f"{amount_to_convert} {from_currency} is equal to {converted_amount} {to_currency}".center(120) + Style.RESET_ALL)
    else:
        print('\n' + Fore.LIGHTRED_EX + f"{'Conversion rate not available.'}".center(120) + Style.RESET_ALL)

def convert_currency(amount, from_currency, to_currency, conversion_rates):
    if (from_currency, to_currency) in conversion_rates:
        rate = conversion_rates[(from_currency, to_currency)]
        converted_amount = amount * rate
        return converted_amount
    else:
        return None

def main_menu():
    while True:
        print("\n" * 3)  # Add vertical spacing to center the menu vertically
        print(" " * 45 + Fore.BLUE + "=========================== WELCOME TO TOURIST BUDDY ===========================" + Style.RESET_ALL)
        print("\n" * 1)
        print(" " * 45 + "1. Explore Available Destinations")
        print(" " * 45 + "2. Search Destination by Name")
        print(" " * 45 + "3. Filter Destinations by Category")
        print(" " * 45 + "4. Rate a Destination")
        print(" " * 45 + "5. Get Recommended Places")
        print(" " * 45 + "6. Add New Category")
        print(" " * 45 + "7. Get Available Categories")
        print(" " * 45 + "8. Add New Attractions")
        print(" " * 45 + "9. Edit Existing Attraction")
        print(" " * 45 + "10. Distance from Current Location")
        print(" " * 45 + "11. Find Arrival Time")
        print(" " * 45 + "12. Currency Conversion")
        print(" " * 45 + "13. Exit")
        print("\n" * 1)
        
        choice = input(" " * 45 + "Enter your choice: ")

        if choice == '1':
            explore_destinations()
        elif choice == '2':
            search_by_query()
        elif choice == '3':
            search_by_category()
        elif choice == '4':
            rate_destination()
        elif choice == '5':
            highly_recommended()
        elif choice == '6':
            add_category()
        elif choice == '7':
            get_categories()
        elif choice == '8':
            add_destination()
        elif choice == '9':
            update_destination()
        elif choice == '10':
            distance_from_origin()
        elif choice == '11':
            arrival_time()
        elif choice == '12':
            currency_conversion()
        elif choice == '13':
            print('\n' + Fore.CYAN + f"{'THANK YOU FOR USING TOURISTY BUDDY. GOODBYE!'}".center(115) + Style.RESET_ALL)
            break
        else:
            print('\n' + Fore.LIGHTRED_EX + f"{'Unknown option. Please try again with a different option.'}".center(120) + Style.RESET_ALL)

if __name__ == '__main__':
    main_menu()
    close_category_conn()
    close_destination_conn()


