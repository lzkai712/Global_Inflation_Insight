from data_analysis import *
from data_management import manage_add_data,manage_update_data,manage_delete_data

def is_valid_option(option):
    return option in ['1', '2', '3', '4']
def regular_user_interface():
    while True:
        print("\nRegular User Interface:")
        print("1. Search country's inflation data")
        print("2. Identify country's highest or lowest inflation rate")
        print("3. Identify globally the country with the highest inflation at a specific year")
        print("4. Compare inflation rates between different countries")
        print("5. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            search_country_data()
        elif choice == '2':
            country_highest_lowest_rate()
        elif choice == '3':
            global_highest_lowest_inflation_rate()
        elif choice == '4':
            compare_countries()
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please try again.")


def manager_interface():
    while True:
        print("\nManager Interface:")
        print("1. Add New Inflation Data")
        print("2. Update Inflation Data")
        print("3. Delete Inflation Data")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            manage_add_data()
        elif choice == '2':
            manage_update_data()
        elif choice == '3':
            manage_delete_data()
        elif choice == '4':
            print("Logged out.")
            break
        else:
            print("Invalid choice. Please try again.")