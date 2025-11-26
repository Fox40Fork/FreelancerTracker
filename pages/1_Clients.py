import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from utils import logout, login, register, is_authenticated, getUserByName

st.set_page_config(page_title="Clients")
st.sidebar.header("Clients")

st.markdown("# Clients")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Manage your clients")

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

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


def addClient(clientData):
    try:
        response = requests.post(f"{BASE_URL}/clients/", json=clientData)
        response.raise_for_status()
        try:
            st.success(f"Client '{clientData['name']}' added successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add client: {e}")
        return None


def updateClient(user_id, clientData):
    try:
        response = requests.put(f"{BASE_URL}/clients/{user_id}", json=clientData)
        response.raise_for_status()
        try:
            st.success(f"Client '{clientData['name']}' updated successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update client: {e}")
        return None


def deleteClient(user_id):
    try:
        response = requests.delete(f"{BASE_URL}/clients/{user_id}")
        response.raise_for_status()
        try:
            st.success("Client deleted successfully!")
            return response.json()  # optional, if backend returns JSON
        except requests.exceptions.JSONDecodeError:
            st.warning("Client deleted, but server response is not JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete client: {e}")
        return None

# User Interface
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
    user = getUserByName(st.session_state["username"])[0]
    userId = user["id"]

    clients = getClients(userId)

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        logout()

    def get_client_by_name(name, clients):  #get every client
        return next((c for c in clients if c['name'] == name), None)


    if clients:  #show clients
        st.subheader("Client List")
        df = pd.DataFrame(clients, columns=["name", "email", "phone", "address"])
        st.dataframe(df)
    else:
        st.write("No clients found.")

    st.subheader("Add New Client") #as the subheader suggests, add new client

    name = st.text_input("Client Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone")
    address = st.text_input("Address")

    if st.button("Add Client"):
        if userId and name.strip():
            clientData = {  #data from the client just added
                "user_id" : userId,
                "name" : name,
                "email" : email,
                "phone" : phone,
                "address" : address
            }
            addClient(clientData) #send all the data to the database
            st.rerun()
        else:
            st.error("The User ID or Name are empty or already existing!")

    if clients:
        action = st.radio("Select Action", ["Update Client", "Delete Client"])

        names = [c['name'] for c in clients]
        selectedTitle = st.selectbox(f"Select Client to {action.split()[0]}", options=names)

        if selectedTitle:
            client = get_client_by_name(selectedTitle, clients)

            if action == "Update Client":
                updated_name = st.text_input("Name", value=client['name'])
                updated_email = st.text_input("Email", value=client['email'])
                updated_phone = st.text_input("Phone Number", value=client.get('phone'))
                updated_address = st.text_input("Address", value=client['address'])

                if st.button("Update Client"):
                    clientInformation = {
                        "user_id" : client["user_id"],
                        "name" : updated_name,
                        "email" : updated_email,
                        "phone" : updated_phone,
                        "address" : updated_address
                    }
                    updateClient(client["id"], clientInformation)
                    st.rerun()

            elif action == "Delete Client":
                if st.button("Delete Client"):
                    deleteClient(client['id'])
                    st.rerun()