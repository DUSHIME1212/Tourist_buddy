from category import Category, close_connection as close_category_conn, add_category, get_categories
from destination import Destination, close_connection as close_destination_conn, cursor, add_destination, update_destination,search_by_category, search_by_query, currency_converter, convert_currency
from viewdestinations import explore_destinations

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

def currency_conversion():
    # Select query for currency conversion
    print("Converting currency...")

def main_menu():
    while True:
        print("\n--- WELCOME TO TOURIST BUDDY ---")
        print("1. Explore Available Destinations")
        print("2. Search Destination Name")
        print("3. Filter Destination By Category")
        print("4. Add New Attractions")
        print("5. Edit existing attraction")
        print("6. Add New Category")
        print("7. Get Available Categories")
        print("8. Get Recommended Places")
        print("9. Distance From Current Location")
        print("10. Currency Conversion")
        print("11. Find Arrival Time")
        print("12. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            explore_destinations()
        elif choice == '2':
            search_by_query()
        elif choice == '3':
            search_by_category()
        elif choice == '4':
            add_destination()
        elif choice == '5':
            update_destination()
        elif choice == '6':
            add_category()
        elif choice == '7':
            get_categories()
        elif choice == '8':
            get_recommended_places()
        elif choice == '9':
            calculate_distance()
        elif choice == '10':
            currency_conversion()
        elif choice == '11':
            arrival_time()
        elif choice == '12':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == '__main__':
    main_menu()
    close_category_conn()
    close_destination_conn()

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
