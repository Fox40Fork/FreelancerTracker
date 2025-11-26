import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv
import os
from utils import logout, login, register, is_authenticated

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

st.set_page_config(
    page_title="Dashboard"
)

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

    if st.sidebar.button("Logout", type="primary", use_container_width=True):
        logout()


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