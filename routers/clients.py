#Clients CRUD

import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.client import Client, ClientCreate
from database import getDBConnection

router = APIRouter()

@router.get('/', response_model = List[Client])

def getClients():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, name, email, phone, address FROM clients")
    clients = cursor.fetchall()
    return [{
        "id": client[0],
        "user_id": client[1],
        "name": client[2],
        "email": client[3],
        "phone": client[4],
        "address": client[5]
    } for client in clients]

@router.post("/", response_model = Client)
def createClient(client: ClientCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clients (name, email, phone, address)"
                    "VALUES (?, ?, ?, ?)",
                    (client.user_id, client.name, client.email, client.phone, client.address))
    except sqlite3.IntegrityError:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"The client '{client.name}' already exists."
        )
    finally:
        conn.commit()
        conn.close()

@router.put("/{user_id}", response_model=Client)
def updateClient(user_id: int, client: ClientCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clients SET user_id = ?, name = ?, email = ?, phone = ?, address = ?"
        "WHERE id = ?",
        (client.user_id, client.name, client.email, client.phone, client.address))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    conn.commit()
    conn.close()
    return Client(id=user_id, **client.dict())

@router.delete("/{user_id}", response_model=dict)
def deleteClient(user_id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    conn.commit()
    conn.close()
    return {"detail": "Client deleted"}