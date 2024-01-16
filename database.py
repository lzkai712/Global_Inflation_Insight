import sqlite3
import csv

conn = sqlite3.connect('global_inflation.db')
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS global_inflation_data(
            CountryCode TEXT,
            IMFCountry Code TEXT,
            Country TEXT,
            Indicator Type TEXT,
            SeriesName TEXT,
            Year_1970 REAL,
            Year_1971 REAL,
            Year_1972 REAL,
            Year_1973 REAL,
            Year_1974 REAL,
            Year_1975 REAL,
            Year_1976 REAL,
            Year_1977 REAL,
            Year_1978 REAL,
            Year_1979 REAL,
            Year_1980 REAL,
            Year_1981 REAL,
            Year_1982 REAL,
            Year_1983 REAL,
            Year_1984 REAL,
            Year_1985 REAL,
            Year_1986 REAL,
            Year_1987 REAL,
            Year_1988 REAL,
            Year_1989 REAL,
            Year_1990 REAL,
            Year_1991 REAL,
            Year_1992 REAL,
            Year_1993 REAL,
            Year_1994 REAL,
            Year_1995 REAL,
            Year_1996 REAL,
            Year_1997 REAL,
            Year_1998 REAL,
            Year_1999 REAL,
            Year_2000 REAL,
            Year_2001 REAL,
            Year_2002 REAL,
            Year_2003 REAL,
            Year_2004 REAL,
            Year_2005 REAL,
            Year_2006 REAL,
            Year_2007 REAL,
            Year_2008 REAL,
            Year_2009 REAL,
            Year_2010 REAL,
            Year_2011 REAL,
            Year_2012 REAL,
            Year_2013 REAL,
            Year_2014 REAL,
            Year_2015 REAL,
            Year_2016 REAL,
            Year_2017 REAL,
            Year_2018 REAL,
            Year_2019 REAL,
            Year_2020 REAL,
            Year_2021 REAL,
            Year_2022 REAL,
            Note TEXT
            
)
            ''')

with open ('Global_Dataset_of_Inflation.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = {key: value if value != '' else None for key, value in row.items()}
        column_mapping = {
            '1970': 'Year_1970',
            '1971': 'Year_1971',
            '1972': 'Year_1972',
            '1973': 'Year_1973',
            '1974': 'Year_1974',
            '1975': 'Year_1975',
            '1976': 'Year_1976',
            '1977': 'Year_1977',
            '1978': 'Year_1978',
            '1979': 'Year_1979',
            '1980': 'Year_1980',
            '1981': 'Year_1981',
            '1982': 'Year_1982',
            '1983': 'Year_1983',
            '1984': 'Year_1984',
            '1985': 'Year_1985',
            '1986': 'Year_1986',
            '1987': 'Year_1987',
            '1988': 'Year_1988',
            '1989': 'Year_1989',
            '1990': 'Year_1990',
            '1991': 'Year_1991',
            '1992': 'Year_1992',
            '1993': 'Year_1993',
            '1994': 'Year_1994',
            '1995': 'Year_1995',
            '1996': 'Year_1996',
            '1997': 'Year_1997',
            '1998': 'Year_1998',
            '1999': 'Year_1999',
            '2000': 'Year_2000',
            '2001': 'Year_2001',
            '2002': 'Year_2002',
            '2003': 'Year_2003',
            '2004': 'Year_2004',
            '2005': 'Year_2005',
            '2006': 'Year_2006',
            '2007': 'Year_2007',
            '2008': 'Year_2008',
            '2009': 'Year_2009',
            '2010': 'Year_2010',
            '2011': 'Year_2011',
            '2012': 'Year_2012',
            '2013': 'Year_2013',
            '2014': 'Year_2014',
            '2015': 'Year_2015',
            '2016': 'Year_2016',
            '2017': 'Year_2017',
            '2018': 'Year_2018',
            '2019': 'Year_2019',
            '2020': 'Year_2020',
            '2021': 'Year_2021',
            '2022': 'Year_2022',
        }

        data = (
            row['Country Code'], row['IMF Country Code'], row['Country'],
            row['Indicator Type'], row['Series Name'], 
            row['1970'], row['1971'], row['1972'], row['1973'], row['1974'], 
            row['1975'], row['1976'], row['1977'], row['1978'], row['1979'], 
            row['1980'], row['1981'], row['1982'], row['1983'], row['1984'], 
            row['1985'], row['1986'], row['1987'], row['1988'], row['1989'], 
            row['1990'], row['1991'], row['1992'], row['1993'], row['1994'], 
            row['1995'], row['1996'], row['1997'], row['1998'], row['1999'], 
            row['2000'], row['2001'], row['2002'], row['2003'], row['2004'], 
            row['2005'], row['2006'], row['2007'], row['2008'], row['2009'], 
            row['2010'], row['2011'], row['2012'], row['2013'], row['2014'], 
            row['2015'], row['2016'], row['2017'], row['2018'], row['2019'], 
            row['2020'], row['2021'], row['2022'], row['Note']
        )
        insert_query = '''
            INSERT INTO global_inflation_data 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,  
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 
                    ?, ?)
        '''

        #Crete user table to store user information
        cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            dateofbirth TEXT NOT NULL,
            location TEXT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
            
        )
    ''')
        cur.execute(insert_query, data)
        conn.commit()
        conn.close()
