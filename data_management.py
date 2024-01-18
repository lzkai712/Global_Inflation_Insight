from database import connect

def connect():
    """Connect to Databse- global_inflation.db"""
    return connect('global_inflation.db')

def manage_add_data():
    while True:
        print("\nAdd New Inflation Data:")
        print("1. Energy Consumer Price Inflation")
        print("2. Food Consumer Price Inflation")
        print("3. Headline Consumer Price Inflation")
        print("4. Producer Price Inflation")
        print("q. Quit")

        option = input("Choose an option: ").lower()
        if option == 'q':
            print("Exiting add data.")
            break

        conn = connect()
        cur = conn.cursor()

        # Mapping option to table names
        table_mapping = {
            '1': 'Energy_Consumer_Price_Inflation_Table',
            '2': 'Food_Consumer_Price_Inflation_Table',
            '3': 'Headline_Consumer_Price_Inflation_Table',
            '4': 'Producer_Price_Inflation_Table'
        }

        table_name = table_mapping.get(option)
        if table_name:
            identifier = input("Enter the country, country code, or IMF country code for which you want to add data: ")

            # Check if the specified country exists in the table
            cur.execute(f'SELECT * FROM {table_name} WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                        (identifier, identifier, identifier))
            existing_data = cur.fetchone()

            if existing_data:
                new_column_name = input("Enter the new column name (e.g., 'y2023'): ")
                new_value = input("Enter the value: ")

                # Alter the table to add the new column
                cur.execute(f'ALTER TABLE {table_name} ADD COLUMN "{new_column_name}" TEXT')

                # Insert the new data into the table for the specified country
                cur.execute(f'UPDATE {table_name} SET "{new_column_name}" = ? WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                            (new_value, identifier, identifier, identifier))

                print("New data added successfully!")
                conn.commit()
            else:
                print(f"The specified country '{identifier}' does not exist in the table. Please choose a valid country.")

        else:
            print("Invalid option. Please try again.")

        conn.close()


def manage_update_data():
    while True:
        print("\nUpdate Inflation Data:")
        print("1. Energy Consumer Price Inflation")
        print("2. Food Consumer Price Inflation")
        print("3. Headline Consumer Price Inflation")
        print("4. Producer Price Inflation")
        print("q. Quit")

        option = input("Choose an option: ").lower()
        if option == 'q':
            print("Exiting update data.")
            break

        conn = connect()
        cur = conn.cursor()

        # Mapping option to table names
        table_mapping = {
            '1': 'Energy_Consumer_Price_Inflation_Table',
            '2': 'Food_Consumer_Price_Inflation_Table',
            '3': 'Headline_Consumer_Price_Inflation_Table',
            '4': 'Producer_Price_Inflation_Table'
        }

        table_name = table_mapping.get(option)
        if table_name:
            identifier = input("Enter the country, country code, or IMF country code for which you want to update data: ")

            # Check if the specified country exists in the table
            cur.execute(f'SELECT * FROM {table_name} WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                        (identifier, identifier, identifier))
            existing_data = cur.fetchone()

            if existing_data:
                column_name = input("Enter the column name you want to update: ")
                new_value = input("Enter the new value: ")

                # Update the specified column for the specified country
                cur.execute(f'UPDATE {table_name} SET "{column_name}" = ? WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                            (new_value, identifier, identifier, identifier))

                print("Data updated successfully!")
                conn.commit()
            else:
                print(f"The specified country '{identifier}' does not exist in the table. Please choose a valid country.")

        else:
            print("Invalid option. Please try again.")

        conn.close()


def manage_delete_data():
    while True:
        print("\nDelete Inflation Data:")
        print("1. Energy Consumer Price Inflation")
        print("2. Food Consumer Price Inflation")
        print("3. Headline Consumer Price Inflation")
        print("4. Producer Price Inflation")
        print("q. Quit")

        option = input("Choose an option: ").lower()
        if option == 'q':
            print("Exiting delete data.")
            break

        conn = connect()
        cur = conn.cursor()

        # Mapping option to table names
        table_mapping = {
            '1': 'Energy_Consumer_Price_Inflation_Table',
            '2': 'Food_Consumer_Price_Inflation_Table',
            '3': 'Headline_Consumer_Price_Inflation_Table',
            '4': 'Producer_Price_Inflation_Table'
        }

        table_name = table_mapping.get(option)
        if table_name:
            identifier = input("Enter the country, country code, or IMF country code for which you want to delete data: ")

            # Check if the specified country exists in the table
            cur.execute(f'SELECT * FROM {table_name} WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                        (identifier, identifier, identifier))
            existing_data = cur.fetchone()

            if existing_data:
                delete_option = input("Choose an option for deletion:\n1. Delete entire row\n2. Delete entire column\n3. Delete single value\nWhat would you like to do: ")

                if delete_option == '1':
                    # Delete entire row for the specified country
                    cur.execute(f'DELETE FROM {table_name} WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                                (identifier, identifier, identifier))
                    print("Row deleted successfully!")
                elif delete_option == '2':
                    column_name = input("Enter the column name you want to delete: ")
                    # Delete entire column for the specified country
                    cur.execute(f'ALTER TABLE {table_name} DROP COLUMN "{column_name}"')
                    print("Column deleted successfully!")
                elif delete_option == '3':
                    column_name = input("Enter the column name for which you want to delete a single value: ")
                    identifier = input("Enter the country, country code, or IMF country code for which you want to delete a single value: ")
                    # Delete a specific value for the specified country and column/year
                    cur.execute(f'UPDATE {table_name} SET "{column_name}" = DEFAULT WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?',
                                (identifier, identifier, identifier))
                    print("Single value deleted successfully!")

                else:
                    print("Invalid option for deletion. Please try again.")
                
                conn.commit()
            else:
                print(f"The specified country '{identifier}' does not exist in the table. Please choose a valid country.")

        else:
            print("Invalid option. Please try again.")

        conn.close()

