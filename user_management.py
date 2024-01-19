import getpass
import re
import sqlite3

MANAGER_ACCOUNT = {
    "username": "zhongkai670@revature.net",
    "password": "123456789",
    "name" : "Manager"
}

def is_manager(username):
    return username == MANAGER_ACCOUNT["username"]

def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email)

def register():
    """User registration process"""
    conn = sqlite3.connect('global_inflation.db')
    cur = conn.cursor()

    while True:
        f_name = input("Enter your first name: ").title()
        while not (f_name.isalpha()):
            print("Invalid first name. Please enter again name should only with alphabetical letters.")
            f_name = input("Enter your first name: ").title()

        l_name = input("Enter your Last name: ").title()
        while not (l_name.isalpha()):
            print("Invalid  last name. Please enter again name should only with alphabetical letters.")
            l_name = input("Enter your Last name: ").title()

        dob = input("Enter your birthday in mm/dd/yyyy: ")
        while not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
            print("Invalid date of birth format. Please enter in mm/dd/yyyy format.")
            dob = input("Enter your birthday in mm/dd/yyyy: ")

        location = input("Enter city of your location(Optional): ")
        username = input("Enter your email to create account: ").lower()
        while not is_valid_email(username):
            print("Invalid email format. Please enter a valid email address.")
            username = input("Enter your email to create account: ").lower()

        password = getpass.getpass("Enter your password: ")
        while len(password) < 9:
            print("Password must be at least 9 characters long.")
            password = getpass.getpass("Enter your password: ")

        # Check if the user already exists
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            print("Email already exists. Please double-check and try again.")
        else:
            cur.execute('''
                        INSERT INTO users (FirstName, LastName, DateOfBirth, Location, Username, Password) 
                        VALUES (?, ?, ?, ?, ?, ?) 
                        ''', (f_name, l_name, dob, location, username, password))
            conn.commit()

            print("Registration successful!")
            break

    conn.close()


def login():
    """Function for checkcing sign in procedure"""
    conn = sqlite3.connect('global_inflation.db')
    cur = conn.cursor()

    while True:
        username = input("Enter your email: ").lower()
        password = getpass.getpass("Enter your password: ")

        if username == MANAGER_ACCOUNT["username"] and password == MANAGER_ACCOUNT["password"]:
            conn.close()
            return MANAGER_ACCOUNT
        else:
            cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cur.fetchone()
            if user:
                user_dict = {
                    "FirstName": user[0],
                    "LastName": user[1],
                    "DateOfBirth": user[2],
                    "Location": user[3],
                    "Username": user[4],
                    "Password": user[5]
                }
                print("Login successful!")
                conn.close()
                return user_dict
            else:
                print("Invalid username or password. Please try again.")
        
        try_again = input("Do you want to try again? (y/n): ").lower()
        if try_again == 'n':
            break
    conn.close()

