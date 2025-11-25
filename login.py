import streamlit as st
import requests
from dotenv import load_dotenv
import os
from database import getDBConnection

conn = getDBConnection()
cursor = conn.cursor()

load_dotenv()
BASE_URL = os.getenv("BASE_URL")

def getUsers():
    try:
        response = requests.get(f"{BASE_URL}/users/")
        response.raise_for_status()  # Raises an exception for non-200 responses
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            st.error("Response from server is not valid JSON.")
            st.write("Response text:", response.text[:500])  # Preview the response
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch users: {e}")
        return []

st.subheader("Log In")

usernameInput = st.text_input("Username")
passwordInput = st.text_input("Password")

if st.button("Log In"):
    users = getUsers()
    if any(u["username"] == usernameInput and u["password"] == passwordInput for u in users):
        st.write(f"Welcome, {usernameInput}!")
    else:
        st.error("Invalid login")
