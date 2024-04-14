import sqlite3 as sql

connection = sql.connect('my_database.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Disease (
id INTEGER PRIMARY KEY,
name_dis TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Sings (
id INTEGER PRIMARY KEY,
name_sings TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Possible_values (
id INTEGER PRIMARY KEY,
id_sings INTEGER NOT NULL,
name_Possible_values TEXT NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Normal_values (
id INTEGER PRIMARY KEY,
id_sings INTEGER NOT NULL,
id_Possible_values INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS Picture (
id INTEGER PRIMARY KEY,
id_dis INTEGER NOT NULL,
id_sings INTEGER NOT NULL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS signs_of_disease (
id INTEGER PRIMARY KEY,
id_dis INTEGER NOT NULL,
id_sings INTEGER NOT NULL,
id_Possible_values INTEGER NOT NULL
)
''')


connection.commit()
connection.close()

