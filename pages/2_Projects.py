import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os
from utils import logout, login, register, is_authenticated, getUserByName

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

def getClients(user_id : int):
    try:
        response = requests.get(f"{BASE_URL}/clients/{user_id}")
        response.raise_for_status()  # Raises an exception for non-200 responses
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Response from server is not valid JSON.")
            st.write("Response text:", response.text[:500])  # Preview the response
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch clients: {e}")
        return []


# User Interface:

if not is_authenticated():
    st.header("Welcome to Freelancer Invoice Tracker")
    st.write("Please log in or register to access the page.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        login()

    with tab2:
        register()

    st.stop()

if is_authenticated():
    def get_project_by_title(title, projects):
        return next((p for p in projects if p['title'] == title), None)
    def get_client_by_name(name, clients):  #get every client
        return next((c for c in clients if c['name'] == name), None)

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        logout()

    # Display projects
    projects = getProjects()
    if projects:  #show clients
        st.subheader("Project List")
        df = pd.DataFrame(projects, columns=["client_id", "title", "description"])
        st.dataframe(df)
    else:
        st.write("No clients found.")

    # --- Add New Project ---
    user = getUserByName(st.session_state["username"])[0]
    userId = user["id"]

    st.subheader("Add New Project")
    clients = getClients(userId)
    chooseClient = [c["name"] for c in clients]
    selectedClient = st.selectbox(f"Select Client", options=chooseClient)
    newTitle = st.text_input("Title")
    newDescription = st.text_area("Description")

    if selectedClient:
        client = get_client_by_name(selectedClient, clients)

        if st.button("Add Project"):
            if newTitle.strip():
                projectData = {
                    "title" : newTitle,
                    "description" : newDescription,
                    "client_id" : client["id"],
                    "user_id" : userId
                }
                addProject(projectData)
                st.rerun()
            else:
                st.error("The title is empty or already existing!")

    # --- Update or Delete Project ---
    action = st.radio("Select Action", ["Update Project", "Delete Project"])

    titles = [p['title'] for p in projects]
    selectedTitle = st.selectbox(f"Select Project to {action.split()[0]}", options=titles)

    if selectedTitle:
        project = get_project_by_title(selectedTitle, projects)

        if action == "Update Project":
            updated_selectedClient = st.selectbox(f"Client", options=chooseClient)
            updated_title = st.text_input("Title", value=project['title'])
            updated_description = st.text_area("Description", value=project.get('description', ''))

            if updated_selectedClient:
                client = get_client_by_name(selectedClient, clients)

                if st.button("Update Project"):
                    updateProject(project['id'], {
                        "user_id": project["user_id"],
                        "title": updated_title,
                        "client_id": client["id"],
                        "description": updated_description
                    })
                    st.rerun()

        elif action == "Delete Project":
            if st.button("Delete Project"):
                deleteProject(project['id'])
                st.rerun()