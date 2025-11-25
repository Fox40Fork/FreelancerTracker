#Baza podataka
#Treba dovršiti clients, projects TABLE-ove i inserte

import sqlite3

def getDBConnection():
    conn = sqlite3.connect("clients.db")
    conn.row_factory = sqlite3.Row
    return conn

def createDatabase():
    conn = getDBConnection()
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        address TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        client_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS invoices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        invoice_number INTEGER NOT NULL UNIQUE,
        client_id INTEGER NOT NULL,
        amount DECIMAL(10,2),
        date DATE,
        status VARCHAR(25),
        FOREIGN KEY (client_id) REFERENCES clients(id)
    )
    ''')

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT
            username TEXT NOT NULL,
            FOREIGN KEY (username) REFERENCES clients(id)
        )
        '''
    )

    return conn, cursor