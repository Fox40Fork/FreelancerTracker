import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Clients")
st.sidebar.header("Clients")

st.markdown("# Clients")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Manage your clients")

BASE_URL = os.getenv("BASE_URL")

def getClients():
    response = requests.get(f"{BASE_URL}/clients/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch clients.")
        return []

def addClient(clientData):
    response = requests.post(f"{BASE_URL}/clients/", json=clientData)
    if response.status_code == 200:
        st.success(f"Client '{clientData['name']}' added successfully!")
    else:
        st.error(f"Failed to add client: {response.json().get('detail', 'Unknown error')}")

def updateClient(user_id, clientData):
    response = requests.put(f"{BASE_URL}/clients/{user_id}", json=clientData)
    if response.status_code == 200:
        st.success(f"Client '{clientData['name']}' updated successfully!")
    else:
        st.error(f"Failed to update client: {response.json().get('detail', 'Unknown error')}")

def deleteClient(user_id):
    response = requests.delete(f"{BASE_URL}/clients/{user_id}")
    if response.status_code == 200:
        st.success("Client deleted successfully!")
    else:
        st.error(f"Failed to delete client: {response.json().get('detail', 'Unknown error')}")

# User Interface
clients = getClients()

if clients:
    st.subheader("Client List")
    df = pd.DataFrame(clients)
    st.dataframe(df)
else:
    st.write("No clients found.")

st.subheader("Add New Client")
name = st.text_input("Client Name")
email = st.text_input("Email")
phone = st.text_input("Phone")
address = st.text_input("Address")

if st.button("Add Client"):
    clientData = {"name": name, "email": email, "phone": phone, "address": address}
    addClient(clientData)
    st.rerun()

st.subheader("Update Client")
if clients:
    client_ids = [client["id"] for client in clients]
    selected_id = st.selectbox("Select Client to Update", client_ids)
    newName = st.text_input("New Client Name")
    newEmail = st.text_input("New Email")
    newPhone = st.text_input("New Phone")
    newAddress = st.text_input("New Address")
    if st.form_submit_button("Update Client"):
        clientData = {"name": newName, "email": newEmail, "phone": newPhone, "address": newAddress}
        updateClient(selected_id, clientData)
        st.rerun()

st.subheader("Delete Client")
if clients:
    delete_id = st.selectbox("Select Client to Delete", client_ids, key="delete")
    if st.button("Delete Client"):
        deleteClient(delete_id)
        st.rerun()