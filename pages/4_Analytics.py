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
# GET CLIENTS
# ----------
#

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def getClients():
    try:
        response = requests.get(f"{BASE_URL}/clients/")
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

#
# ----------
# GET INVOICES
# ----------
#

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
totalMonthly = np.sum(monthlyIncome)

#Total income by client calculation

clientIncome = defaultdict(float)
for invoice in invoices:
    clientIncome[invoice['client_id']] += invoice['amount'] #Fix: add client_id to the invoices database
clientIncome = dict(clientIncome) #Sort back into dict yet again lol
bestClient = np.max(clientIncome)

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

st.write(f"Earnings this month: {totalMonthly}")
st.write(f"Total earnings: {totalMoney}")

st.subheader("Total Earnings by Client")

df = pd.DataFrame(list(clientIncome.items()), columns=['Client', 'Income'])
fig = px.pie(df, title='Total Earnings by Client')
st.plotly_chart(fig)

st.write(f"Amount of clients: ")
st.write(f"Your best client: {bestClient}")

st.subheader("Invoice Status")

df = pd.DataFrame(list(statusCounts.items()), columns=['Status', 'Count'])
fig = px.bar(df, x='Status', y='Count', title='Paid vs Unpaid Invoices', color='Status')
st.plotly_chart(fig)