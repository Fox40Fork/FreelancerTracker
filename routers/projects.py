#Projects CRUD

import sqlite3
from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from models.project import Project, ProjectCreate
from database import getDBConnection

router = APIRouter()

@router.get('/', response_model = List[Project])

def getProjects():
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, client_id, title, description FROM projects")
    projects = cursor.fetchall()
    return [{
        "id": project[0],
        "user_id": project[1],
        "client_id": project[2],
        "title": project[3],
        "description": project[4]
    } for project in projects]

@router.post("/", response_model = Project)
def createProject(project: ProjectCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO projects (user_id, client_id, title, description) VALUES (?, ?, ?, ?)",
            (project.user_id, project.client_id, project.title, project.description)
        )
        conn.commit()

        project_id = cursor.lastrowid
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()

        return Project(
            id=row[0],
            user_id=row[1],
            client_id=row[2],
            title=row[3],
            description=row[4]
        )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Failed to add project: {e}"
        )
    finally:
        conn.close()

@router.put("/{user_id}", response_model=Project)
def updateProject(user_id: int, project: ProjectCreate):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE projects SET user_id = ?, client_id = ?, title = ?, description = ?"
        "WHERE id = ?",
        (project.user_id, project.client_id, project.title, project.description))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return Project(id=user_id, **project.dict())

@router.delete("/{user_id}", response_model=dict)
def deleteProject(user_id: int):
    conn = getDBConnection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (user_id,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Project not found")
    conn.commit()
    conn.close()
    return {"detail": "Project deleted"}