import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Projects")
st.sidebar.header("Projects")

st.markdown("# Projects")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Manage your projects")

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def getProjects():
    response = requests.get(f"{BASE_URL}/projects/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch projects.")
        return []


def addProject(projectData):
    response = requests.post(f"{BASE_URL}/projects/", json=projectData)
    if response.status_code == 200:
        st.success(f"Project '{projectData['title']}' added successfully!")
    else:
        st.error(f"Failed to add project: {response.json().get('detail', 'Unknown error')}")


def updateProject(user_id, projectData):
    response = requests.put(f"{BASE_URL}/projects/{user_id}", json=projectData)
    if response.status_code == 200:
        st.success(f"Project '{projectData['title']}' updated successfully!")
    else:
        st.error(f"Failed to update project: {response.json().get('detail', 'Unknown error')}")


def deleteProject(user_id):
    response = requests.delete(f"{BASE_URL}/projects/{user_id}")
    if response.status_code == 200:
        st.success("Project deleted successfully!")
    else:
        st.error(f"Failed to delete project: {response.json().get('detail', 'Unknown error')}")


# User Interface:

def get_project_by_title(title, projects):
    return next((p for p in projects if p['title'] == title), None)


# Display projects
projects = getProjects()
st.dataframe(pd.DataFrame(projects), use_container_width=True)

# --- Add New Project ---
st.subheader("Add New Project")
newTitle = st.text_input("Title")
newDescription = st.text_area("Description")
newClientID = st.number_input("Client ID", min_value=1, step=1)

if st.button("Add Project"):
    if newTitle.strip():
        addProject({
            "title": newTitle,
            "client_id": newClientID,
            "description": newDescription
        })
    else:
        st.error("Title cannot be empty.")

# --- Update or Delete Project ---
action = st.radio("Select Action", ["Update Project", "Delete Project"])

titles = [p['title'] for p in projects]
selectedTitle = st.selectbox(f"Select Project to {action.split()[0]}", options=titles)

if selectedTitle:
    project = get_project_by_title(selectedTitle, projects)

    if action == "Update Project":
        updated_title = st.text_input("Title", value=project['title'])
        updated_description = st.text_area("Description", value=project.get('description', ''))
        updated_client_id = st.number_input("Client ID", min_value=1, step=1, value=project['client_id'])

        if st.button("Update Project"):
            updateProject(project['id'], {
                "title": updated_title,
                "client_id": updated_client_id,
                "description": updated_description
            })

    elif action == "Delete Project":
        if st.button("Delete Project"):
            deleteProject(project['id'])