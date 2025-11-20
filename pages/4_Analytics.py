import streamlit as st
import requests
import numpy as np
import plotly.express as px
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict, Counter
import os

st.set_page_config(page_title="Analytics")
st.sidebar.header("Analytics")

st.markdown("# Analytics")
st.sidebar.warning("You can navigate through the pages here.")

st.write("Detailed statistics for your business")

#
# ----------
# GET CRUD FOR CLIENTS
# ----------
#

load_dotenv()
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

#
# ----------
# GET CRUD FOR INVOICES
# ----------
#

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


#
# ----------
# CALCULATIONS + NUMPY MANAGEMENT
# ----------
#

invoices = getInvoices()
clients = getClients()

def get_invoices_by_number(number, invoices):
    return next((i for i in invoices if i['invoice_number'] == number), None)
def get_client_by_title(title, clients):
    return next((c for c in clients if c['title'] == title), None)

money = [inv['amount'] for inv in invoices]
totalMoney = np.sum(money)

#Average salary calculation

averageSalary = np.average(money)

#Monthly income calculation

monthlyIncome = defaultdict(float)
for invoice in invoices:
    dateObj = datetime.strptime(invoice['date'], '%Y-%m-%d')
    monthKey = dateObj.strftime('%Y-%m')
    monthlyIncome[monthKey] = monthlyIncome.get(monthKey, 0) + invoice['amount']
monthlyIncome = dict(sorted(monthlyIncome.items())) #Sort back into dict

#Total income by client calculation

clientIncome = defaultdict(float)
for invoice in invoices:
    clientIncome[invoice['client']] += invoice['amount'] #Fix: add client to the invoices database
clientIncome = dict(clientIncome) #Sort back into dict yet again lol

#Paid/Unpaid invoices

statusCounts = Counter(invoice['status'] for invoice in invoices)

#
# ----------
# USER INTERFACE
# ----------
#

st.subheader("Monthly Earnings")

df = pd.DataFrame(list(monthlyIncome.items()), columns=['Month', 'Income'])
fig = px.line(df, x='Month', y='Income', title='Monthly Salary')
st.plotly_chart(fig)

st.write(f"Earnings this month: {monthlyIncome}")
st.write(f"Total earnings: {totalMoney}")

st.subheader("Total Earnings by Client")

df = pd.DataFrame(list(clientIncome.items()), columns=['Client', 'Income'])
fig = px.pie(df, title='Total Earnings by Client')
st.plotly_chart(fig)

st.subheader("Invoice Status")

df = pd.DataFrame(list(statusCounts.items()), columns=['Status', 'Count'])
fig = px.bar(df, x='Status', y='Count', title='Paid vs Unpaid Invoices', color='Status')
st.plotly_chart(fig)