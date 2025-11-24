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
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        response.raise_for_status()  # raises error for non-200 status codes
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch projects: {e}")
        return []


def addProject(projectData):
    try:
        response = requests.post(f"{BASE_URL}/projects/", json=projectData)
        response.raise_for_status()
        try:
            st.success(f"Project '{projectData['title']}' added successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add project: {e}")
        return None


def updateProject(user_id, projectData):
    try:
        response = requests.put(f"{BASE_URL}/projects/{user_id}", json=projectData)
        response.raise_for_status()
        try:
            st.success(f"Project '{projectData['title']}' updated successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update project: {e}")
        return None


def deleteProject(user_id):
    try:
        response = requests.delete(f"{BASE_URL}/projects/{user_id}")
        response.raise_for_status()
        try:
            st.success("Project deleted successfully!")
            return response.json()  # optional, in case backend returns JSON
        except requests.exceptions.JSONDecodeError:
            st.warning("Project deleted, but server response is not JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete project: {e}")
        return None


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
newUserId = st.number_input("User ID", min_value=1, step=1)

if st.button("Add Project"):
    if newTitle.strip():
        projectData = {
            "title" : newTitle,
            "description" : newDescription,
            "client_id" : newClientID,
            "user_id" : newUserId
        }
        addProject(projectData)
    else:
        st.error("The title is empty or already existing!")

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