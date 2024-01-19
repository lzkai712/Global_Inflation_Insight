import sqlite3
import csv

# List of CSV file names
csv_files = [
    'Energy_Consumer_Price_Inflation.csv',
    'Food_Consumer_Price_Inflation.csv',
    'Headline_Consumer_Price_Inflation.csv',
    'Producer_Price_Inflation.csv'
]

# Function to create tables
def create_tables(cursor, table_name):
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if not cursor.fetchone():
        cursor.execute(f'''
            CREATE TABLE {table_name} (
                "Country Code" TEXT,
                "IMF Country Code" TEXT,
                "Country" TEXT,
                "Indicator Type" TEXT,
                "Series Name" TEXT,
                {", ".join([f'"y{year}" INTEGER' for year in range(1970, 2023)])}
            );
        ''')

conn = sqlite3.connect('global_inflation.db')
cursor = conn.cursor()

# Create tables for each CSV file
for csv_file in csv_files:
    table_name = csv_file.replace('.csv', '_table')
    create_tables(cursor, table_name)

    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) 
        for row in csv_reader:
            cursor.execute(f'INSERT INTO {table_name} VALUES ({", ".join(["?" for _ in range(len(row))])})', row)

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT NOT NULL,
        LastName TEXT NOT NULL,
        DateOfBirth DATE,
        Location TEXT,
        Username TEXT UNIQUE NOT NULL,
        Password TEXT NOT NULL
    )
''')

conn.commit()
conn.close()