#Baza podataka
#Treba dovršiti clients, projects TABLE-ove i inserte

import sqlite3

def getDBConnection():
    conn = sqlite3.connect("clients.db")
    conn.row_factory = sqlite3.Row

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
        user_id INTEGER NOT NULL,      --čijeg freelancera je ovaj klijent
        name TEXT NOT NULL,
        email TEXT,
        phone TEXT,     --opcionalna dodatna informacija
        address TEXT,
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,     --isto kao i prošla, čijeg freelancera je ovaj klijent
        client_id INTEGER NOT NULL,       --čijeg klijenta je ovaj projekt
        title TEXT NOT NULL,
        description TEXT
    )
    ''')

    return conn, cursor

def insertUsers(usersDict, cursor):    #ovo je valjda ovako
    for name, info in usersDict.items():
        cursor.execute('''
        INSERT INTO users (name, email, password)
        VALUES (?, ?, ?)
        ''', (
            name,
            info["email"],
            info["password"]
        ))

def insertClients(clientsDict, cursor):    #i ovo
    for (name, user_id), info in clientsDict.items():
        cursor.execute('''
        INSERT INTO clients (user_id, name, email, phone, address)
        VALUES (?, ?, ?, ?, ?)
        ''', (
            name,
            user_id,
            info["email"],
            info["phone"],
            info["address"],
        ))

def insertProjects(projectsDict, cursor):    #i ovo
    for (user_id, client_id), info in projectsDict.items():
        cursor.execute('''
        INSERT INTO clients (user_id, client_id, title, description)
        VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            client_id,
            info["title"],
            info["description"]
        ))