import getpass
from database import connect

MANAGER_ACCOUNT = {
    "username": "zhongkai670@revature.net",
    "password": "123456789",
    "name" : "Manager"
}

def is_manager(username):
    return username == MANAGER_ACCOUNT["username"]

def register():
    """User registration process"""
    conn = connect()
    cur = conn.cursor()

    while True:
        f_name = input("Enter your first name: ").title()
        l_name = input("Enter your Last name: ").title()
        dob = input("Enter your birthday in mm/dd/yyyy: ")
        location = input("Enter city of your location(Optional): ")
        username = input("Enter your email to create account: ").lower()
        password = getpass.getpass("Enter your password: ")
        #Check if user already existed
        cur.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = cur.fetchone()

        if existing_user:
            print("Email already exists. Please double check and try again: ")
        else:
            cur.execute('''
                        INSERT INTO users (fistname, lastname, dateOfbirth, location, username, password) 
                        VALUES(?, ?, ?, ?, ?, ?) 
                        ''',(f_name, l_name, dob, location,username, password))
            conn.commit()

            print("Registration successful!")
            break
        conn.close()

def login():
    """Function for check logging in procedure"""
    conn = connect()
    cur = conn.cursor()

    while True:
        username = input("Enter your email: ").lower()
        password = getpass.getpass("Enter your password: ")

        if username == MANAGER_ACCOUNT["username"] and password == MANAGER_ACCOUNT("password"):
            conn.close()
            return MANAGER_ACCOUNT
        else:
            cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
            user = cur.fetchone()
            if user:
                print("Login successful!")
                conn.close()
                return user
            else:
                print("Invalid username or password. Please try again.")
        
        try_again = input("Do you want to try again? (y/n): ").lower()
        if try_again == 'n':
            break
    conn.close()

