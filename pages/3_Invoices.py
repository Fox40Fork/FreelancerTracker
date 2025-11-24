import streamlit as st
import requests
import pandas as pd
from dotenv import load_dotenv
import os

st.set_page_config(page_title="Invoices")
st.sidebar.header("Invoices")

st.markdown("# Invoices")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Manage your invoices")

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def getInvoices():
    try:
        response = requests.get(f"{BASE_URL}/invoices/")
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

def get_invoices_by_number(number, invoices):
    return next((i for i in invoices if i['invoice_number'] == number), None)


# Display invoices
invoices = getInvoices()
st.dataframe(pd.DataFrame(invoices), use_container_width=True)

# --- Add New Project ---
st.subheader("Add New Invoice")
newAmount = st.number_input("Amount")
newClientId = st.number_input("Client ID", min_value = 1, step = 1)
newDate = st.date_input("Date")
newInvoiceNumber = st.number_input("Invoice Number", min_value=1, step=1)

if st.button("Add Invoice"):
    if newInvoiceNumber:
        invoiceData = {
            "client_id": newClientId,
            "amount": newAmount,
            "date": newDate.isoformat(),
            "invoice_number": newInvoiceNumber
        }
        updateInvoice(newInvoiceNumber, invoiceData = invoiceData)
    else:
        st.error("Everything has to be filled.")

# --- Update or Delete Project ---
action = st.radio("Select Action", ["Update Invoice", "Delete Invoice"])

numbers = [i['title'] for i in invoices]
selectedNumber = st.selectbox(f"Select Invoice to {action.split()[0]}", options=numbers)

if selectedNumber:
    invoice = get_invoices_by_number(selectedNumber, invoices)

    if action == "Update Invoice":
        updated_amount = st.text_input("Amount", value=invoice['amount'])
        updated_date = st.date_input("Date", value=invoice('date'))
        updated_invoiceNumber = st.number_input("Invoice Number", min_value=1, step=1, value=invoice['invoice_number'])
        updated_clientId = st.date_input("Client ID", value=invoice('client_id'))

        if st.button("Update Invoice"):
            updateInvoice(invoice['id'], {
                "client_id": updated_clientId,
                "amount": updated_amount,
                "date": updated_date.isoformat(),
                "invoice_number": updated_invoiceNumber
            })

    elif action == "Delete Invoice":
        if st.button("Delete Invoice"):
            deleteInvoice(invoice['invoice_number'])