from database import connect

def search_country_data():
    """Implement search functionality with three options: Country Code, Name, IMF Code"""
    while True:
        print("Search Country Data:")
        print("1. Search by Country Code")
        print("2. Search by Country Name")
        print("3. Search by IMF Code")
        print("q. Quit")

        option = input("Choose an option: ").lower()
        conn = connect()
        cur = conn.cursor()

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
            print("Invalid option. Exiting search.")
            conn.close()
            return

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


def identify_country_inflation():
    pass

def identify_global_highest_inflation():
    pass

def compare_countries():
    pass
def highest_lowest_inflation(country):
    pass

def global_highest_inflation(year):
    pass

def compare_countries(countries, year):
    pass

def manage_add_data():
    pass
def manage_update_data():
    pass
def manage_delete_data():
    pass
