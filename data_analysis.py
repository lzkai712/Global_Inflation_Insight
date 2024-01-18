import sqlite3
from database import connect

def connect():
    """Connect to Databse- global_inflation.db"""
    return connect('global_inflation.db')

def search_country_data():
    """Search Country inflation rate with three options: Country Code, Name, IMF Code"""
    while True:
        print("Search Country Data:")
        print("1. Search by Country Code")
        print("2. Search by Country Name")
        print("3. Search by IMF Code")
        print("q. Quit")

        option = input("Choose an option: ").lower()
        conn = connect()
        cur = conn.cursor()
        while True:
            if option == '1':
                while True:
                    country_code = input("Enter Country Code (3 Alphabetical Letters): ").upper()
                    if len(country_code) == 3 and country_code.isalpha():
                        break
                    else:
                        print("Invalid country code. Please try again")
                year_input = input("Enter the year or range of years (comma-separated): ")
                query = f"SELECT * FROM Energy_Consumer_Price_Inflation_Table AS E " \
                        f"JOIN Food_Consumer_Price_Inflation_Table AS F ON E.Country_Code = F.Country_Code " \
                        f"JOIN Headline_Consumer_Price_Inflation_Table AS H ON E.Country_Code = H.Country_Code " \
                        f"JOIN Producer_Price_Inflation_Table AS P ON E.Country_Code = P.Country_Code " \
                        f"WHERE E.Country_Code = ? AND ({','.join(year_input.split())})"
                cur.execute(query, (country_code,))
            elif option == '2':
                country_name = input("Enter Country Name: ")
                year_input = input("Enter the year or range of years (comma-separated): ")
                query = f"SELECT * FROM Energy_Consumer_Price_Inflation_Table AS E " \
                        f"JOIN Food_Consumer_Price_Inflation_Table AS F ON E.Country_Name = F.Country_Name " \
                        f"JOIN Headline_Consumer_Price_Inflation_Table AS H ON E.Country_Name = H.Country_Name " \
                        f"JOIN Producer_Price_Inflation_Table AS P ON E.Country_Name = P.Country_Name " \
                        f"WHERE E.Country_Name = ? AND ({','.join(year_input.split())})"
                cur.execute(query, (country_name,))
            elif option == '3':
                imf_code = input("Enter IMF Code: ")
                year_input = input("Enter the year or range of years (comma-separated): ")
                query = f"SELECT * FROM Energy_Consumer_Price_Inflation_Table AS E " \
                        f"JOIN Food_Consumer_Price_Inflation_Table AS F ON E.IMF_Code = F.IMF_Code " \
                        f"JOIN Headline_Consumer_Price_Inflation_Table AS H ON E.IMF_Code = H.IMF_Code " \
                        f"JOIN Producer_Price_Inflation_Table AS P ON E.IMF_Code = P.IMF_Code " \
                        f"WHERE E.IMF_Code = ? AND ({','.join(year_input.split())})"
                cur.execute(query, (imf_code,))
            elif option == 'q':
                print("Exiting search.")
                conn.close()
                return
            else:
                print("Invalid option. Try Again.")
                conn.close()

            data = cur.fetchall()
            if data:
                print("Search Results:")
                for row in data:
                    print(row)
            else:
                print("No data found.")
            
            search_again = input("Do you want to search for another country? (y/n): ").lower()
            if search_again != 'y':
                print("Exiting search.")
                conn.close()
                return

            conn.close()


def country_highest_lowest_rate():
    """Find a country's highest and lowest year of inflation rate"""
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
            conn = connect()
            cur = conn.cursor()

            query_highest = f'''
                SELECT "Country", "Country Code", "IMF Country Code", MAX(rate) AS HighestRate
                FROM (
                    SELECT "Country", "Country Code", "IMF Country Code", {", ".join([f'"y{year}"' for year in range(1970, 2023)])} AS rate
                    FROM {table_name}
                    WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?
                ) AS country_data
            '''
            cur.execute(query_highest, (identifier, identifier, identifier))
            highest = cur.fetchone()

            query_lowest = f'''
                SELECT "Country", "Country Code", "IMF Country Code", MIN(rate) AS LowestRate
                FROM (
                    SELECT "Country", "Country Code", "IMF Country Code", {", ".join([f'"y{year}"' for year in range(1970, 2023)])} AS rate
                    FROM {table_name}
                    WHERE "Country" = ? OR "Country Code" = ? OR "IMF Country Code" = ?
                ) AS country_data
            '''
            cur.execute(query_lowest, (identifier, identifier, identifier))
            lowest = cur.fetchone()

            if highest and lowest:
                print(f"\nHighest and Lowest Inflation Rates for {identifier} in {table_name}:")

                print(f"\nHighest Inflation Rate ({highest['Country']}/{highest['Country Code']}/{highest['IMF Country Code']}): {highest['HighestRate']}")
                print(f"Lowest Inflation Rate ({lowest['Country']}/{lowest['Country Code']}/{lowest['IMF Country Code']}): {lowest['LowestRate']}")
            else:
                print(f"No data found for the specified country '{identifier}' in {table_name}. Please try again.")

            another_country = input("Do you want to see inflation rates for another country? (y/n): ").lower()
            if another_country != 'y':
                print("Exiting search for country's highest/lowest inflation rate.")
                break

            conn.close()
        else:
            print("Invalid option. Please try again.")


def global_highest_lowest_inflation_rate():
    """Find the country with the highest and lowest inflation rates for the specified year"""
    while True:
        print("\nSearch Global Highest/Lowest Inflation Rate:")
        year = input("Enter the year for which you want to find the global highest/lowest inflation rate (e.g., 'y2023'): ")
        conn = connect()
        cur = conn.cursor()

        table_names = [
            'Energy_Consumer_Price_Inflation_Table',
            'Food_Consumer_Price_Inflation_Table',
            'Headline_Consumer_Price_Inflation_Table',
            'Producer_Price_Inflation_Table'
        ]

        highest_values = []
        lowest_values = []

        for table_name in table_names:
            query = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "{year}" AS InflationRate
                FROM {table_name}
                ORDER BY "{year}" DESC
                LIMIT 1
            '''
            cur.execute(query)
            highest = cur.fetchone()

            query = f'''
                SELECT "Country", "Country Code", "IMF Country Code", "{year}" AS InflationRate
                FROM {table_name}
                ORDER BY "{year}" ASC
                LIMIT 1
            '''
            cur.execute(query)
            lowest = cur.fetchone()

            if highest:
                highest_values.append(highest)
            if lowest:
                lowest_values.append(lowest)

        if highest_values and lowest_values:
            print(f"\nGlobal Highest and Lowest Inflation Rates for {year}:")

            print("\nHighest Inflation Rate:")
            for country in highest_values:
                print(f"{country['Country']} ({country['Country Code']} / {country['IMF Country Code']}): {country['InflationRate']}")

            print("\nLowest Inflation Rate:")
            for country in lowest_values:
                print(f"{country['Country']} ({country['Country Code']} / {country['IMF Country Code']}): {country['InflationRate']}")
        else:
            print(f"No data found for the specified year '{year}'. Please try again.")

        another_year = input("Do you want to see inflation rates for a different year? (y/n): ").lower()
        if another_year != 'y':
            print("Exiting search for global highest/lowest inflation rate.")
            break

        conn.close()

from database import connect

def compare_countries(countries, inflation_type, year):
    """Compare inflation rates of multiple countries for a specific year."""
    while True:
        print("\nCompare Countries:")
        print("Enter 'q' to quit.")

        # Ask user for countries to compare
        countries_to_compare = input("Enter countries to compare (separated by commas): ").split(',')
        countries_to_compare = [country.strip().upper() for country in countries_to_compare]

        if 'q' in countries_to_compare:
            print("Exiting comparison.")
            return

        print("Choose Inflation Type:")
        print("1. Energy Consumer Price Inflation")
        print("2. Food Consumer Price Inflation")
        print("3. Headline Consumer Price Inflation")
        print("4. Producer Price Inflation")

        inflation_option = input("Enter the option (1-4): ")
        inflation_table_mapping = {
            '1': 'Energy_Consumer_Price_Inflation_Table',
            '2': 'Food_Consumer_Price_Inflation_Table',
            '3': 'Headline_Consumer_Price_Inflation_Table',
            '4': 'Producer_Price_Inflation_Table'
        }
        inflation_table = inflation_table_mapping.get(inflation_option)

        if not inflation_table:
            print("Invalid option. Please try again.")
            continue

        conn = connect()
        cur = conn.cursor()

        query = f'''
            SELECT "Country", "{year}" AS InflationRate
            FROM {inflation_table}
            WHERE "Country Code" IN ({', '.join(['?']*len(countries_to_compare))})
            ORDER BY InflationRate
        '''

        cur.execute(query, tuple(countries_to_compare))
        result = cur.fetchall()

        if result:
            print(f"\nComparison for {year} ({inflation_type}):")
            for row in result:
                print(f"{row[0]}: {row[1]}")
                
            another_comparison = input("\nDo you want to perform another comparison? (y/n): ").lower()
            if another_comparison != 'y':
                print("Exiting comparison.")
                conn.close()
                return
        else:
            print("No data found for the specified countries and inflation type. Please check your inputs.")

        conn.close()
