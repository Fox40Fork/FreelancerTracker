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

@router.get('/{user_id}', response_model = List[Client])

def getUserClients(user_id : int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, name, email, phone, address FROM clients WHERE user_id=?", (user_id,))
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
        cursor.execute(
            "INSERT INTO clients (user_id, name, email, phone, address) VALUES (?, ?, ?, ?, ?)",
            (client.user_id, client.name, client.email, client.phone, client.address)
        )
        conn.commit()

        client_id = cursor.lastrowid
        cursor.execute("SELECT * FROM clients WHERE id = ?", (client_id,))
        row = cursor.fetchone()

        return Client(
            id=row[0],
            user_id=row[1],
            name=row[2],
            email=row[3],
            phone=row[4],
            address=row[5]
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{e}"
        )
    finally:
        conn.close()

@router.put("/{client_id}", response_model=Client)
def updateClient(client_id: int, client: ClientCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE clients SET user_id = ?, name = ?, email = ?, phone = ?, address = ? "
        "WHERE id = ?",
        (client.user_id, client.name, client.email, client.phone, client.address, client_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    conn.commit()
    conn.close()
    return Client(id=client_id, **client.model_dump())

@router.delete("/{client_id}", response_model=dict)
def deleteClient(client_id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Client not found")
    conn.commit()
    conn.close()
    return {"detail": "Client deleted"}