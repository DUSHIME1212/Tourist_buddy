from category import Category, close_connection as close_category_conn
from destination import Destination, close_connection as close_destination_conn, cursor

def explore_destinations():
    # Select query for available destinations
    print("Exploring available destinations...")

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
