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
    response = requests.get(f"{BASE_URL}/invoices/")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to fetch invoices.")
        return []


def addInvoice(invoiceData):
    response = requests.post(f"{BASE_URL}/invoices/", json=invoiceData)
    if response.status_code == 200:
        st.success(f"Invoice '{invoiceData['invoice_number']}' added successfully!")
    else:
        st.error(f"Failed to add invoice: {response.json().get('detail', 'Unknown error')}")


def updateInvoice(invoice_number, invoiceData):
    response = requests.put(f"{BASE_URL}/invoices/{invoice_number}", json=invoiceData)
    if response.status_code == 200:
        st.success(f"Invoice '{invoiceData['invoice_number']}' updated successfully!")
    else:
        st.error(f"Failed to update invoice: {response.json().get('detail', 'Unknown error')}")


def deleteInvoice(invoice_number):
    response = requests.delete(f"{BASE_URL}/invoices/{invoice_number}")
    if response.status_code == 200:
        st.success("Invoice deleted successfully!")
    else:
        st.error(f"Failed to delete invoice: {response.json().get('detail', 'Unknown error')}")


# User Interface:

def get_invoices_by_number(number, invoices):
    return next((i for i in invoices if i['invoice_number'] == number), None)


# Display invoices
invoices = getInvoices()
st.dataframe(pd.DataFrame(invoices), use_container_width=True)

# --- Add New Project ---
st.subheader("Add New Invoice")
newAmount = st.number_input("Amount")
newDate = st.date_input("Date")
newInvoiceNumber = st.number_input("Invoice Number", min_value=1, step=1)

if st.button("Add Invoice"):
    if newInvoiceNumber.strip():
        addInvoice({
            "amount": newAmount,
            "date": newDate,
            "invoice_number": newInvoiceNumber
        })
    else:
        st.error("Nothing cannot be empty.")

# --- Update or Delete Project ---
action = st.radio("Select Action", ["Update Invoice", "Delete Invoice"])

numbers = [i['title'] for i in invoices]
selectedNumber = st.selectbox(f"Select Invoice to {action.split()[0]}", options=numbers)

if selectedNumber:
    invoice = get_invoices_by_number(selectedNumber, invoices)

    if action == "Update Invoice":
        updated_amount = st.text_input("Amount", value=invoice['amount'])
        updated_date = st.date_input("Description", value=invoice('date'))
        updated_invoiceNumber = st.number_input("Invoice Number", min_value=1, step=1, value=invoice['invoice_number'])

        if st.button("Update Invoice"):
            updateInvoice(invoice['id'], {
                "title": updated_amount,
                "client_id": updated_date,
                "description": updated_invoiceNumber
            })

    elif action == "Delete Invoice":
        if st.button("Delete Invoice"):
            deleteInvoice(invoice['invoice_number'])