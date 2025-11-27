import streamlit as st
import requests
import numpy as np
import plotly.express as px
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from collections import defaultdict, Counter
import os
from utils import logout, login, register, is_authenticated, getUserByName

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

st.set_page_config(
    page_title="Dashboard"
)


def getClients(user_id: int):
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


def getInvoices(user_id: int):
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

if not is_authenticated():
    st.header("Welcome to Freelancer Invoice Tracker")
    st.write("Please log in or register to access the dashboard.")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        login()

    with tab2:
        register()

    st.stop()
if is_authenticated():
    st.header("Dashboard")
    st.write(f"The dashboard for the Freelancer Invoice/Income Tracker app.")

    st.sidebar.warning("You can navigate through the pages here.")
    st.write(f"Welcome back, {st.session_state["username"]}!")

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        logout()

    user = getUserByName(st.session_state["username"])[0]
    userId = user["id"]

    invoices = getInvoices(userId)
    clients = getClients(userId)

    def get_invoices_by_number(number, invoices):
        return next((i for i in invoices if i['invoice_number'] == number), None)

    def get_client_by_title(title, clients):
        return next((c for c in clients if c['title'] == title), None)

    money = [inv['amount'] for inv in invoices]
    totalMoney = np.sum(money)

    # Average salary calculation

    averageSalary = np.average(money)

    # Monthly income calculation

    monthlyIncome = defaultdict(float)
    for invoice in invoices:
        dateObj = datetime.strptime(invoice['date'], '%Y-%m-%d')
        monthKey = dateObj.strftime('%Y-%m')
        monthlyIncome[monthKey] = monthlyIncome.get(monthKey, 0) + invoice['amount']
    monthlyIncome = dict(sorted(monthlyIncome.items()))  # Sort back into dict
    totalMonthly = np.sum(list(monthlyIncome.values()))

    #UI

    st.write("")
    st.write("")

    st.subheader("Let's look at your business' performance 💻")

    st.write("")

    if totalMoney <= 2500:
        st.write(f"Getting started! You currently made {totalMoney}! 💰")
    elif totalMoney <= 10000:
        st.write(f"Nice progress! You've earned {totalMoney}, keep building momentum! 💰")
    elif totalMoney <= 20000:
        st.write(f"Solid growth! Your income has reached {totalMoney}, things are moving forward! 💰")
    elif totalMoney <= 50000:
        st.write(f"Impressive! With {totalMoney} earned, you're establishing a strong foundation! 💰")
    elif totalMoney <= 100000:
        st.write(f"Fantastic achievement! You've crossed {totalMoney}, showing real consistency! 💰")
    elif totalMoney > 100000:
        st.write(f"Amazing milestone! Over {totalMoney} earned — you're in the big leagues now! 💰")

    if averageSalary <= 1000:
        st.write(f"Getting started! Your current salary is {averageSalary}! 💵")
    elif averageSalary <= 5000:
        st.write(f"Nice progress! You're earning {averageSalary}, keep going! 💵")
    elif averageSalary <= 10000:
        st.write(f"Solid growth! Your salary has reached {averageSalary}, things are moving forward! 💵")
    elif averageSalary <= 50000:
        st.write(f"Impressive! With {averageSalary} earning, your business has immense potential! 💵")
    elif averageSalary <= 100000:
        st.write(f"Fantastic achievement! You've crossed {averageSalary}, showing real consistency! 💵")
    elif averageSalary > 100000:
        st.write(f"Amazing job! Over {averageSalary} earning — millionaire territory reached! 💵")

    st.write("")

    st.write("Take a look at your earnings over the months:")
    df = pd.DataFrame(list(monthlyIncome.items()), columns=['Month', 'Income'])
    fig = px.line(df, x='Month', y='Income', title='Monthly Salary')
    st.plotly_chart(fig)

    st.write("")

    st.write("You can see your stats in detail by going to the Analytics page.")