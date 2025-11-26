import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os
from utils import logout, login, register, is_authenticated, getUserByName
import datetime


st.set_page_config(page_title="Invoices")
st.sidebar.header("Invoices")

st.markdown("# Invoices")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Manage your invoices")

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

def getInvoices(user_id : int):
    try:
        response = requests.get(f"{BASE_URL}/invoices/{user_id}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Response from server is not valid JSON.")
            st.write("Response text:", response.text[:500])  # Preview response
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch invoices: {e}")
        return []


def addInvoice(invoiceData):
    try:
        response = requests.post(f"{BASE_URL}/invoices/", json=invoiceData)
        response.raise_for_status()
        try:
            st.success(f"Invoice '{invoiceData['invoice_number']}' added successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add invoice: {e}")
        return None


def updateInvoice(invoice_number, invoiceData):
    try:
        response = requests.put(f"{BASE_URL}/invoices/{invoice_number}", json=invoiceData)
        response.raise_for_status()
        try:
            st.success(f"Invoice '{invoiceData['invoice_number']}' updated successfully!")
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Server response is not valid JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update invoice: {e}")
        return None


def deleteInvoice(invoice_number):
    try:
        response = requests.delete(f"{BASE_URL}/invoices/{invoice_number}")
        response.raise_for_status()
        try:
            st.success("Invoice deleted successfully!")
            return response.json()  # optional, if backend returns JSON
        except requests.exceptions.JSONDecodeError:
            st.warning("Invoice deleted, but server response is not JSON.")
            st.write("Response text:", response.text[:500])
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete invoice: {e}")
        return None


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
    def get_invoices_by_number(number, invoices):
        return next((i for i in invoices if i['invoice_number'] == number), None)
    def get_client_by_name(name, clients):  #get every client
        return next((c for c in clients if c['name'] == name), None)

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        logout()

    user = getUserByName(st.session_state["username"])[0]
    userId = user["id"]
    # Display invoices
    invoices = getInvoices(userId)
    if invoices:  # show clients
        st.subheader("Project List")
        df = pd.DataFrame(invoices, columns=["invoice_number", "client_id", "amount", "date", "status"])
        st.dataframe(df)
    else:
        st.write("No clients found.")

    # --- Add New Project ---

    clients = getClients(userId)
    chooseClient = [c["name"] for c in clients]
    chooseStatus = ["PAID", "UNPAID"]

    st.subheader("Add New Invoice")
    newAmount = st.number_input("Amount")
    newSelectedClient = st.selectbox(f"Select Client", options=chooseClient)
    newDate = st.date_input("Date")
    newSelectedStatus = st.selectbox(f"Select Status", options=chooseStatus)
    newInvoiceNumber = st.number_input("Invoice Number", min_value=1, step=1)
    if newSelectedClient and newSelectedStatus:
        client = get_client_by_name(newSelectedClient, clients)
        if st.button("Add Invoice"):
            if newInvoiceNumber:
                invoiceData = {
                    "client_id": client["id"],
                    "amount": newAmount,
                    "date": newDate.isoformat(),
                    "invoice_number": newInvoiceNumber,
                    "status" : newSelectedStatus
                }
                addInvoice(invoiceData)
                st.rerun()
            else:
                st.error("Everything has to be filled.")

    # --- Update or Delete Project ---
    action = st.radio("Select Action", ["Update Invoice", "Delete Invoice"])

    numbers = [i['invoice_number'] for i in invoices]
    selectedNumber = st.selectbox(f"Select Invoice to {action.split()[0]}", options=numbers)

    if selectedNumber:
        invoice = get_invoices_by_number(selectedNumber, invoices)
        date_value = datetime.date.fromisoformat(invoice["date"])

        if action == "Update Invoice":
            updated_amount = st.text_input("Amount", value=invoice['amount'])
            updated_date = st.date_input("Date", value=date_value)
            updated_invoiceNumber = st.number_input("Invoice Number", min_value=1, step=1, value=invoice['invoice_number'])
            updated_clientId = st.number_input("Client ID", value=invoice["client_id"])
            updated_status = st.text_input("Status", value=invoice["status"])

            if st.button("Update Invoice"):
                updateInvoice(invoice['id'], {
                    "client_id": updated_clientId,
                    "amount": updated_amount,
                    "date": updated_date.isoformat(),
                    "invoice_number": updated_invoiceNumber,
                    "status" : updated_status
                })
                st.rerun()

        elif action == "Delete Invoice":
            if st.button("Delete Invoice"):
                deleteInvoice(invoice['id'])
                st.rerun()