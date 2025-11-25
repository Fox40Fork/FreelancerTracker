#Sessions CRUD

from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.session import Session, SessionCreate
from database import getDBConnection

router = APIRouter()

@router.get('/', response_model = List[Session])

def getSessions():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, username FROM sessions")
    sessions = cursor.fetchall()
    return [{
        "id": session[0],
        "username": session[1],
    } for session in sessions]

@router.post("/", response_model = Session)
def createSession(session: SessionCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO sessions (username) VALUES (?)",
            (session.username,)
        )
        conn.commit()

        session_id = cursor.lastrowid
        cursor.execute("SELECT * FROM sessions WHERE id = ?", (session_id,))
        row = cursor.fetchone()

        return Session(
            id=row[0],
            username=row[1]
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Failed to add session: {e}"
        )
    finally:
        conn.close()

@router.put("/{id}", response_model=Session)
def updateSession(session_id: int, session: SessionCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE sessions SET username = ? "
        "WHERE id = ?",
        (session.username, session_id))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Session not found")
    conn.commit()
    conn.close()
    return Session(id=session_id, **session.model_dump())

@router.delete("/{id}", response_model=dict)
def deleteSession(session_id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Session not found")
    conn.commit()
    conn.close()
    return {"detail": "Session deleted"}
