import math
from category import close_connection as close_category_conn, add_category, get_categories
from destination import close_connection as close_destination_conn, cursor, add_destination, update_destination,search_by_category, search_by_query, highly_recommended, rate_destination
from viewdestinations import explore_destinations

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
    start_time = input("Enter start time (HH:MM AM/PM): ")
    add_hours = int(input("Enter duration hours: "))
    add_minutes = int(input("Enter duration minutes: "))
    day_index = int(input("Enter the day index (1-7): "))

    result = dest_time(start_time, add_hours, add_minutes, day_index)
    print(f"Arrival time: {result}")

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
    destination_name = input("Enter your destination: ")
    user_lat = float(input("Enter your current latitude: "))
    user_lon = float(input("Enter your current longitude: "))

    cursor.execute('SELECT latitude, longitude FROM Destination WHERE name = %s', (destination_name,))
    destination_coords = cursor.fetchone()
    if destination_coords is None:
        print("Destination not found.")
        return
    else:
        dest_lat, dest_lon = destination_coords
        distance = calculate_distance(user_lat, user_lon, dest_lat, dest_lon)
        print(f"Distance to destination: {distance} kilometers")

def currency_conversion():
    conversion_rates = {
        ('USD', 'EUR'): 0.89,
        ('EUR', 'USD'): 1.12,
        ('RWF', 'USD'): 0.00099,
        ('USD', 'KES'): 111,
        ('USD', 'UGX'): 4071,
        ('KES', 'USD'): 0.009,
        ('UGX', 'USD'): 0.00025,
        ('USD', 'RWF'): 1015
    }

    amount_to_convert = float(input("Enter the amount to convert: "))
    from_currency = input("Enter the current currency (e.g., USD, EUR, RWF, KES, UGX): ").upper()
    to_currency = input("Enter the desired currency (e.g., USD, EUR, RWF, KES, UGX): ").upper()

    converted_amount = convert_currency(amount_to_convert, from_currency, to_currency, conversion_rates)
    if converted_amount is not None:
        print(f"{amount_to_convert} {from_currency} is equal to {converted_amount} {to_currency}")
    else:
        print("Conversion rate not available.")

def convert_currency(amount, from_currency, to_currency, conversion_rates):
    if (from_currency, to_currency) in conversion_rates:
        rate = conversion_rates[(from_currency, to_currency)]
        converted_amount = amount * rate
        return converted_amount
    else:
        return None

def main_menu():
    while True:
        print("\n--- WELCOME TO TOURIST BUDDY ---")
        print("1. Explore Available Destinations")
        print("2. Search Destination Name")
        print("3. Filter Destination By Category")
        print("4. Rate a Destination")
        print("5. Get Recommended Places")
        print("6. Add New Category")
        print("7. Get Available Categories")
        print("8. Add New Attractions")
        print("9. Edit existing attraction")
        print("10. Distance From Current Location")
        print("11. Find Arrival Time")
        print("12. Currency Conversion")
        print("13. Exit")

        choice = input("Enter your choice: ")

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
            print("Exiting program. Goodbye!")
            break
        else:
            print("Unknown option. Please try again with a different.")

if __name__ == '__main__':
    main_menu()
    close_category_conn()
    close_destination_conn()


