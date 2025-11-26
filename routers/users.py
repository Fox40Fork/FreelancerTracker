#Invoices CRUD

import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.user import User, UserCreate
from database import getDBConnection

router = APIRouter()

@router.get('/', response_model = List[User])

def getUsers():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password FROM users")
    users = cursor.fetchall()
    return [{
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "password": user[3]
    } for user in users]

@router.get('/{username}', response_model = List[User])
def getUserByName(username: str):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username, email, password FROM users WHERE username=?", (username,) )
    users = cursor.fetchall()
    return [{
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "password": user[3]
    } for user in users]

@router.post("/", response_model = User)
def createUser(user: UserCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password)"
                "VALUES (?, ?, ?)",
                (user.username, user.email, user.password))
    conn.commit()
    user_id = cursor.lastrowid
    return User(id = user_id, username = user.username, email = user.email, password = user.password)


@router.put("/{id}", response_model=User)
def updateUser(id: int, user: UserCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET username = ?, email = ?, password = ?"
        "WHERE id = ?",
        (user.username, user.email, user.password, id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.commit()
    conn.close()
    return User(id=id, **user.dict())

@router.delete("/{id}", response_model=dict)
def deleteUser(id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
    conn.commit()
    conn.close()
    return {"detail": "User deleted"}