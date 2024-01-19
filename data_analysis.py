import sqlite3

def search_country_data():
    """Search Country inflation rate with three options: Country Code, Name, IMF Code"""
    conn = sqlite3.connect('global_inflation.db')
    cur = conn.cursor()

    while True:
        print("Search Country Data:")
        print("1. Search by Country Code")
        print("2. Search by Country Name")
        print("3. Search by IMF Code")
        print("q. Quit")

        option = input("Choose an option: ").lower()

        if option == 'q':
            print("Exiting search.")
            break

        if option in ['1', '2', '3']:
            identifier = ""
            type_inflation = ""
            year_input = ""

            if option == '1':
                identifier = input("Enter Country Code (3 Alphabetical Letters): ").upper()
            elif option == '2':
                identifier = input("Enter Country Name: ")
            elif option == '3':
                identifier = input("Enter IMF Code: ")

            type_inflation = input("Choose Inflation Type:\n1. Energy Consumer Price Inflation\n2. Food Consumer Price Inflation\n3. Headline Consumer Price Inflation\n4. Producer Price Inflation ")

            if type_inflation not in ['1', '2', '3', '4']:
                print("Invalid option")
                continue

            year_input = input("Enter the year: ")

            table_mapping = {
                '1': 'Energy_Consumer_Price_Inflation_Table',
                '2': 'Food_Consumer_Price_Inflation_Table',
                '3': 'Headline_Consumer_Price_Inflation_Table',
                '4': 'Producer_Price_Inflation_Table'
            }

            table_name = table_mapping[type_inflation]

            if option == '1':
                placeholders = ', '.join(['?' for _ in year_input.split()])
                query = f"SELECT \"{table_name}\".\"Country Code\", {', '.join([f'\"y{year}\"' for year in year_input.split()])} " \
                        f"FROM {table_name} " \
                        f"WHERE \"{table_name}\".\"Country Code\" = ? AND {placeholders}"
                cur.execute(query, (identifier,) + tuple(year_input.split()))

            elif option == '2':
                placeholders = ', '.join(['?' for _ in year_input.split()])
                query = f"SELECT \"{table_name}\".\"Country\", {', '.join([f'\"y{year}\"' for year in year_input.split()])} " \
                        f"FROM {table_name} " \
                        f"WHERE \"{table_name}\".\"Country\" = ? AND {placeholders}"
                cur.execute(query, (identifier,) + tuple(year_input.split()))

            elif option == '3':
                placeholders = ', '.join(['?' for _ in year_input.split()])
                query = f"SELECT \"{table_name}\".\"IMF Country Code\", {', '.join([f'\"y{year}\"' for year in year_input.split()])} " \
                        f"FROM {table_name} " \
                        f"WHERE \"{table_name}\".\"IMF Country Code\" = ? AND {placeholders}"
                cur.execute(query, (identifier,) + tuple(year_input.split()))

            data = cur.fetchall()
            if data:
                print("Search Results:")
                for row in data:
                    print(row)
            else:
                print("No data found.")

        else:
            print("Invalid option. Try Again.")
            continue

        search_again = input("Do you want to search for another country? (y/n): ").lower()
        if search_again != 'y':
            print("Exiting search.")
            break

    conn.close()

def country_highest_lowest_rate():
    """Find a country's highest and lowest year of inflation rate"""
    conn = sqlite3.connect('global_inflation.db')
    cur = conn.cursor()

    while True:
        print("\nSearch Country's Highest/Lowest Inflation Rate:")
        identifier = input("Enter the country, country code, or IMF country code for which you want to find the highest/lowest inflation rate: ")
        
        # Mapping option to table names
        table_mapping = {
            '1': 'Energy_Consumer_Price_Inflation_Table',
            '2': 'Food_Consumer_Price_Inflation_Table',
            '3': 'Headline_Consumer_Price_Inflation_Table',
            '4': 'Producer_Price_Inflation_Table'
        }

        option = input("Choose the inflation data type (1: Energy, 2: Food, 3: Headline, 4: Producer): ")
        table_name = table_mapping.get(option)

        if table_name:

            query_highest = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "Year", MAX(rate) AS HighestRate
                FROM (
                    SELECT "Country", "Country Code", "IMF Country Code", "Year",
                        {", ".join([f'"y{year}"' for year in range(1970, 2023)])} AS rate
                    FROM {table_name}
                    WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?
                ) AS country_data
                GROUP BY "Country", "Country Code", "IMF Country Code", "Year"
                ORDER BY HighestRate DESC
                LIMIT 1
            '''
            cur.execute(query_highest, (identifier, identifier, identifier))
            highest = cur.fetchone()

            query_lowest = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "Year", MIN(rate) AS LowestRate
                FROM (
                    SELECT "Country", "Country Code", "IMF Country Code", "Year",
                        MIN({", ".join([f'"y{year}"' for year in range(1970, 2023)])}) AS rate
                    FROM {table_name}
                    WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?
                    GROUP BY "Country", "Country Code", "IMF Country Code", "Year"
                ) AS country_data
                GROUP BY "Country", "Country Code", "IMF Country Code", "Year"
                ORDER BY LowestRate ASC
                LIMIT 1
            '''

            cur.execute(query_lowest, (identifier, identifier, identifier))
            lowest = cur.fetchone()

            print_highest_inflation_rate( highest )
            print_lowest_inflation_rate( lowest )

            another_country = input("Do you want to see inflation rates for another country? (y/n): ").lower()
            if another_country != 'y':
                print("Exiting search for country's highest/lowest inflation rate.")
                break

        else:
            print("Invalid option. Please try again.")
    
    conn.close()

def print_highest_inflation_rate(highest):
    if highest:
        print(f"\nHighest Inflation Rate for {highest[0]} is {highest[4]} from 1970 to 2022")
    else:
        print("No data found for the specified country. Please try again.")

def print_lowest_inflation_rate(lowest):
    if lowest:
        print(f"Lowest Inflation Rate for {lowest[0]} is {lowest[4]} from 1970 to 2022")
    else:
        print("No data found for the specified country. Please try again.")


def global_highest_lowest_inflation_rate():
    """Find the country with the highest and lowest inflation rates for the specified year"""
    conn = sqlite3.connect('global_inflation.db')
    cur = conn.cursor()
    while True:
        print("\nSearch Global Highest/Lowest Inflation Rate:")
        year = input("Enter the year for which you want to find the global highest/lowest inflation rate (e.g., 'y2023'): ")

        table_names = [
            'Energy_Consumer_Price_Inflation_Table',
            'Food_Consumer_Price_Inflation_Table',
            'Headline_Consumer_Price_Inflation_Table',
            'Producer_Price_Inflation_Table'
        ]

        highest_values = []
        lowest_values = []

        for table_name in table_names:
            
            highest_values_table = []
            lowest_values_table = []

            query = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "{year}" AS InflationRate
                FROM {table_name}
                ORDER BY "{year}" DESC
                LIMIT 1
            '''
            cur.execute(query)
            highest = cur.fetchone()
            if highest:
                highest_values_table.append((table_name, highest))

            query = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "{year}" AS InflationRate
                FROM {table_name}
                ORDER BY "{year}" ASC
                LIMIT 1
            '''
            cur.execute(query)
            lowest = cur.fetchone()
            if lowest:
                lowest_values_table.append((table_name, lowest))

            highest_values.extend(highest_values_table)
            lowest_values.extend(lowest_values_table)


        if highest_values and lowest_values:
            print(f"\nGlobal Highest and Lowest Inflation Rates for {year}:")

            print("\nHighest Inflation Rates:")
            for table_name, country in highest_values:
                print(f"{table_name}: {country[0]} ({country[1]} / {country[2]}): {country[3]}")

            print("\nLowest Inflation Rates:")
            for table_name, country in lowest_values:
                print(f"{table_name}: {country[0]} ({country[1]} / {country[2]}): {country[3]}")
        else:
            print(f"No data found for the specified year '{year}'. Please try again.")

        another_year = input("Do you want to see inflation rates for a different year? (y/n): ").lower()
        if another_year != 'y':
            print("Exiting search for global highest/lowest inflation rate.")
            return

        conn.close()

def compare_countries():
    """Compare inflation rates of multiple countries for a specific year and type."""
    pass
  



